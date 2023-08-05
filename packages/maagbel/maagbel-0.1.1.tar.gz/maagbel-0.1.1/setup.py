import os
import itertools
from subprocess import Popen, PIPE
from setuptools import setup, Extension, find_packages
from distutils.command.build import build as build_orig

# Misc executables
UNAME = "uname"


def get_long_description():
    """Load the contents of README.md to use as a long description
    
    Returns:
        The content of README.md as a string.
    """
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


# Error classes
class SetupError(RuntimeError):
    """Base error class for this setup file"""

    pass


class CommandNotFoundError(SetupError):
    """Raised when running a command cannot be found"""

    pass


class CannotRunCommandError(SetupError):
    """Raised when running a command returns with an error"""

    pass


class DependencyNotFoundError(SetupError):
    """Raised when a dependency cannot be found"""

    pass


# Helper functions
def call_prog(prog, args, encoding=None, strip=False):
    """Call an executable and return its standard output
    Args:
        prog: (str) - the executable's name
        args: (list of str) - arguments for the executable
        encoding: (str, optional, default: None) - chose an encoding to convert the
            output of called programs to Python strings, uses the system-default
            encoding by default
        strip: (bool, optional, default: False) - whether to strip newlines and spaces
            from the end of the returned string

    Returns:
        The standard output of the executable called with the given arguments.

    Raises:
        CommandNotFoundError if the executable cannot be found.
        CannotRunCommandError if the executable did not yield an exit code of zero.
    """
    try:
        process = Popen([prog] + args, stdout=PIPE)
    except FileNotFoundError:
        raise CommandNotFoundError("Command '{}' not found".format(prog))
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        raise CannotRunCommandError(
            "Error running '{} {}', error: {}".format(prog, " ".join(args), err)
        )
    else:
        if encoding is not None:
            output = output.decode(encoding=encoding)
        else:
            output = output.decode()
        if strip:
            output = output.rstrip()
        return output


def get_lib_dirs(kind):
    """Obtain library dirs depending on the architecture.

    Supports determining system library dirs (kind="system") and conda library dirs
    (kind="conda").

    This may not be necessary depending on the compiler used. If the program "uname" is
    not installed, the system's architecture cannot be determined and a standard set of
    directories is returned.

    Args:
        kind: (string) - the kind of library paths you want

    Returns:
        A list of strings containing the library paths of the specified type.
    """
    if kind == "system":
        dirs = ["/usr/lib/"]
        try:
            arch = call_prog(UNAME, ["-m"], strip=True)
        except CommandNotFoundError:
            arch = None
        if arch is not None:
            dirs.append("/usr/lib/{}-linux-gnu/".format(arch))
    elif kind == "conda":
        dirs = []
        prefix = get_conda_prefix()
        if prefix is not None:
            dirs.append(os.path.join(prefix, "lib"))
    else:
        raise ValueError("Unknown kind '{}'".format(kind))
    return dirs


def get_include_dirs(kind):
    """Obtain include dirs depending on the architecture.

    Supports determining system include dirs (kind="system") and conda include dirs
    (kind="conda").

    This may not be necessary depending on the compiler used. If the program "uname" is
    not installed, the system's architecture cannot be determined and a standard set of
    directories is returned.

    Args:
        kind: (string) - the kind of include paths you want

    Returns:
        A list of strings containing the include paths of the specified type.
    """
    if kind == "system":
        dirs = ["/usr/include/"]
        try:
            arch = call_prog(UNAME, ["-m"], strip=True)
        except CommandNotFoundError:
            arch = None
        if arch is not None:
            dirs.append("/usr/include/{}-linux-gnu/".format(arch))
    elif kind == "conda":
        dirs = []
        prefix = get_conda_prefix()
        if prefix is not None:
            dirs.append(os.path.join(prefix, "include"))
    else:
        raise ValueError("Unknown kind '{}'".format(kind))
    return dirs


def get_eigen_include_dir():
    """Try to find the eigen include directory.

    Search all directories in the system and conda include paths for a directory called
    "eigen3". Stop at the first one found and return its path.

    Returns:
        A path to the eigen3 include directory if found, None otherwise
    """
    # Allow explicitly setting the eigen include directory
    env_vars = [
        "MAINST_EIGEN3_DIR",
    ]
    for var in env_vars:
        eigen_dir = os.environ.get(var, None)
        if eigen_dir is not None:
            return eigen_dir

    # Unless otherwise specified, prefer the conda installation of eigen3. If not found,
    # search the system paths.
    kinds = ("conda", "system")
    env_vars = [
        "MAINST_EIGEN3_PREFER_SYSTEM",
    ]
    for var in env_vars:
        if os.environ.get(var, "0") == "1":
            kinds = ("system", "conda")
    for kind in kinds:
        for d in get_include_dirs(kind):
            content = os.listdir(d)
            for c in content:
                if c == "eigen3" and os.path.isdir(d):
                    return os.path.join(d, c)

    return None


def get_conda_prefix():
    """Determine whether a conda environment is active and return its path
    
    Returns:
        The path if a conda env is active and None otherwise.
    """
    path = os.environ.get("CONDA_PREFIX", None)
    return path


class build(build_orig):
    """A class that allows re-ordering the build process.

    Re-order the commands build_py and build_ext so that build_ext is run first. That
    way, swig-generated Python files will be available for the build_py step.

    Taken from https://stackoverflow.com/questions/50239473/building-a-module-with-setuptools-and-swig
    """

    def finalize_options(self):
        super().finalize_options()
        condition = lambda l: l[0] == "build_ext"
        t1, t2 = itertools.tee(self.sub_commands)
        rest, sub_build_ext = (
            itertools.filterfalse(condition, t1),
            filter(condition, t2),
        )
        self.sub_commands[:] = list(sub_build_ext) + list(rest)


def is_file_type(file, type):
    """Determine whether a file is of a certain type.

    Supported types are "source" and "header". Files ending in ".cpp" or ".c" are
    considered "source" files, whereas files ending in ".hpp" or ".h" are considered
    "header" files.

    Args:
        file: (string) - the name of a file to be checked
        type: (string) - one of the supported file types

    Raises:
        ValueError if the type of file is not known
    """
    if type == "source":
        matches = file.endswith(".cpp") or file.endswith(".c")
    elif type == "header":
        matches = file.endswith(".hpp") or file.endswith(".h")
    else:
        raise ValueError("Unsupported file type '{}'".format(type))
    return matches


def get_files_in_dir(dir):
    """Return a list of relative paths to all files in a directory recursively.

    Args:
        dir: (string) - path to a directory
    """
    result = []
    for root, __, files in os.walk(os.path.join(dir)):
        result += [os.path.join(root, f) for f in files]
    return result


def get_ext_modules(basename):
    """Get a list of external modules.

    This will install the OpenBabel C++ module with reduced functionality.

    Args:
        basename: (str) - the name of the main module, used to ensure that any
            extensions are sub-modules

    Returns:
        A list of extensions to be passed to the ext_modules argument of the setup
        function.
    """

    # Determine source files
    files = get_files_in_dir(os.path.join(os.path.curdir, "src"))
    sources = [f for f in files if is_file_type(f, "source")]
    sources.append("maagbel/cpp.i")

    # # Determine header files
    # files += get_files_in_dir(os.path.join(os.path.curdir, "include"))
    # headers = [f for f in files if is_file_type(f, "header")]

    libraries = ["pthread", "c", "m"]
    extra_compile_args = [
        "-std=c++14",
        "-v",
        "-pedantic",
        "-Wall",
        "-Wextra",
        "-fPIC",
        "-O3",
    ]
    swig_opts = ["-c++", "-Iinclude"]

    include_dirs = get_include_dirs("system") + get_include_dirs("conda")
    eigen_include = get_eigen_include_dir()
    if eigen_include is not None:
        include_dirs.append(eigen_include)
    include_dirs.append("include")

    library_dirs = get_lib_dirs("system") + get_lib_dirs("conda")

    # Create the main C++ extension with either min or max funtionality
    maagbel_cpp_ext = Extension(
        basename + "._cpp",
        sources=sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        language="c++",
        swig_opts=swig_opts,
        extra_compile_args=extra_compile_args,
    )
    ext_modules = [maagbel_cpp_ext]

    return ext_modules


def check_dependencies():
    """Check whether all required dependencies can be found. Raise an exception if one
    is missing.
    """

    # Check whether SWIG is installed and can be found
    try:
        call_prog("swig", ["-version"])
    except CommandNotFoundError:
        raise CommandNotFoundError(
            "Cannot find SWIG and execute, please install it on your system, "
            "run 'swig --version' to check whether swig works"
        )
    # Check whether Eigen3 is installed and can be found
    if get_eigen_include_dir() is None:
        raise DependencyNotFoundError(
            "Cannot find installation of Eigen3, please install it on your system"
        )


def main():
    # Package data
    PACKAGE_DATA = {
        "name": "maagbel",
        "version": "0.1.1",
        "description": "Reduced fork of OpenBabel for the ManipulateAggregates tools",
        "author": "Torsten Sachse",
        "mail": "torsten.sachse@gmail.com",
        "url": "https://github.com/razziel89/MaAg-bel",
        "long_description": get_long_description(),
        "long_description_content_type": "text/markdown",
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: C++",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3 :: Only",
        ],
    }

    check_dependencies()

    setup(
        ext_modules=get_ext_modules(PACKAGE_DATA["name"]),
        packages=find_packages(),
        cmdclass={"build": build},
        package_data={"": [PACKAGE_DATA["name"] + "/data"]},
        **PACKAGE_DATA,
    )


if __name__ == "__main__":
    main()
