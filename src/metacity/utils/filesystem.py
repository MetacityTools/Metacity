import os
import shutil
import orjson
import sys
import ntpath
import errno

# basics
def filename(file_path: str):
    return ntpath.basename(file_path)

def concat(*args):
    return os.path.join(*args)


def create_dir_if_not_exists(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)


def recreate_dir(dir: str):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    create_dir_if_not_exists(dir)


def file_exists(file: str):
    return os.path.exists(file)


def list_subdirectories(dir: str):
    return [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]


def list_files_recursive(dir: str):
    for root, dirs, files in os.walk(dir):
        for file in files:
            yield os.path.join(root, file)


def join_path(path: str, *args: str):
    return os.path.join(path, *args)


def rename(old: str, new: str):
    if file_exists(old) and not file_exists(new):
        os.rename(old, new)
        return True
    return False


def readable(file: str):
    f = open(file, "r")
    return f.readable()


def writable(file: str):
    f = open(file, "w")
    return f.writable()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def delete_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def write_json(filename, data):
    delete_file(filename)

    with open(filename, 'wb') as file:
        sdata = orjson.dumps(data)
        file.write(sdata)


def read_json(filename):
    with open(filename, 'r') as file:
        sdata = file.read()
    return orjson.loads(sdata)


def read_pbf(filename):
    with open(filename, 'rb') as file:
        return file.read()


def dir_from_path(path):
    return os.path.dirname(path)


def change_suffix(path, suffix):
    base = os.path.splitext(path)[0]
    return f"{base}.{suffix}"


def get_suffix(path):
    return os.path.splitext(path)[1][1:]


# https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123
'''
Windows-specific error code indicating an invalid pathname.

See Also:
    [Official listing of all such codes.](https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
        
'''

def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?

def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS *and*
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to *never* raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False
