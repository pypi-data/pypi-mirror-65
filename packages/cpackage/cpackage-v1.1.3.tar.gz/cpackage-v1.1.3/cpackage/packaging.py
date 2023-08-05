from shutil import rmtree
import sys
import os

class _construct(object):
    # Create main module package directory
    def _pkgMain(pkg, cur=True):
        if cur:
            cpkg = os.getcwd() + "/" + pkg
        else:
            cpkg = sys.path[4] + "/" + pkg

        return cpkg

    # Create sub packages
    def _pkgSub(pkg, sub, cur=True):
        if cur:
            for sub_pkg in sub:
                spkg = os.getcwd() + "/" + pkg + "/" + sub_pkg
                yield spkg
        else:
            for sub_pkg in sub:
                spkg = sys.path[4] + "/" + pkg + "/" + sub_pkg
                yield spkg

    # Check if package name exists & raise FileExistsError
    def _exists(pkg, main=True):
        if main:
            if os.path.exists(pkg):
                raise FileExistsError("Main pkg {} already exists".format(pkg))
        else:
            if os.path.exists(pkg):
                raise FileExistsError("Sub package {} already exists".format(pkg))

# Create package name and subpackages
def CPack(pkg, cur_dir=True, *sub_packages):
    if cur_dir:
        main_current = _construct._pkgMain(pkg, True)

        _construct._exists(main_current, True)
        os.mkdir(main_current)

        for sub_current in _construct._pkgSub(pkg, sub_packages, True):
            _construct._exists(sub_current, False)
            os.mkdir(sub_current)

    else:
        main_site = _construct._pkgMain(pkg, False)

        _construct._exists(main_site, True)
        os.mkdir(main_site)

        for sub_site in _construct._pkgSub(pkg, sub_packages, False):
            _construct._exists(sub_site, False)
            os.mkdir(sub_site)

# Show all aviable packages in dictionary form e.g {"mymodule": ["sub1", "sub2"]}
def Cdir(pkg, cur_dir=True):
    items = []
    current = os.getcwd() + "/" + pkg
    site = sys.path[4] + "/" + pkg
    if cur_dir:
        for pkg_dir in os.listdir(current):
            items.append(pkg_dir)
            items.sort(reverse=True)
            items.reverse()
    else:
        for pkg_dir in os.listdir(site):
            items.append(pkg_dir)
            items.sort(reverse=True)
            items.reverse()

    return {pkg: items}

# Access sub directories in the specfied package
def CAccess(pkg, cur_dir=True, *fd):
    if cur_dir:
        for sub_pkg in _construct._pkgSub(pkg, fd, True):
            _construct._exists(sub_pkg, False)
            os.mknod(sub_pkg)

    else:
        for sub_pkg in _construct._pkgSub(pkg, fd, False):
            _construct._exists(sub_pkg, False)
            os.mknod(sub_pkg)


# Check the package or sub package volume
def CVolume(pkg):
    b = 0
    KB = 1.0
    MB = 1000.0
    GB = 1000000000.0

    for vol in os.listdir(pkg):

        if os.path.isdir(pkg + "/" + vol):

            for fname in os.listdir(pkg + "/" + vol):
                try:
                    with open(pkg + "/" + vol + "/" + fname, "rb") as rbfile_sub:
                        read_bytes = len(bytes(rbfile_sub.read()))
                        b += read_bytes
                        read_bytes = read_bytes * 0.001
                except IsADirectoryError:
                    pass

        else:
            with open(pkg + "/" + vol, "rb") as rbfile:
                read_bytes = len(bytes(rbfile.read()))
                b += read_bytes
                read_bytes = read_bytes * 0.001

            #b += read_bytes
            if read_bytes >= MB:
                return (read_bytes, "MB")

            elif read_bytes >= GB:
                return (read_bytes, "GB")

            elif read_bytes >= KB:
                return (read_bytes, "KB")

            else:
                return (b, "B")

# Remove the package tree 'good if you want everything gone'
def CRemove(pkg, cur_dir=True):
    if cur_dir:
        pl = os.getcwd() + "/" + pkg
    else:
        pl = sys.path[4] + "/" + pkg

    rmtree(pl)
