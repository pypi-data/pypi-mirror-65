try:
    import argparse
    import os
    import sys
    from cpackage.packaging import Cdir, CRemove, CVolume

except ImportError as importerror:
    print(importerror)

parser = argparse.ArgumentParser()
parser.add_argument("-pkg", help="Package name to create")
parser.add_argument("-sub", help="Sub package names to create", nargs="+", type=str)
parser.add_argument("-listdir", help="List directory and sub packages")
parser.add_argument("-access", help="Create files within a package")
parser.add_argument("-remove", help="Remove entire package tree")
parser.add_argument("-volume", help="View the current package volume size")
parser.add_argument("-volumes", help="Add two or more volume sizes together", nargs="+", type=str)

parser.add_argument("--site", help="Use python site packages directory", action="store_true")
parser.add_argument("--current", help="Use current working directory", action="store_true")

args = parser.parse_args()

class _toolConstruct(object):
    def isCurrent():
        if args.current:
            return True
        elif args.site:
            return False

    # has potential future use
    def subTup():
        argsubLst = []
        if args.sub:
            for arg in args.sub:
                argsubLst.append(arg)
        return argsubLst

def tool():
    # get package argument and create directory
    if args.pkg:
        if _toolConstruct.isCurrent():
            directory = os.getcwd() + "/" + args.pkg
            os.mkdir(directory)
        else:
            directory = sys.path[4] + "/" + args.pkg
            os.mkdir(directory)

    # create package and sub packages
    if args.pkg and args.sub:
        if _toolConstruct.isCurrent():
            for sub_dir in args.sub:
                sub_directory = os.getcwd() + "/" + args.pkg + "/" + sub_dir
                os.mkdir(sub_directory)
        else:
            for sub_dir in args.sub:
                sub_directory = sys.path[4] + "/" + args.pkg + "/" + sub_dir
                os.mkdir(sub_directory)

    # list the packages in a dictionary
    if args.listdir:
        if _toolConstruct.isCurrent():
            print(Cdir(args.listdir, True))
        else:
            print(Cdir(args.listdir, False))

    # access a package and write a file
    if args.access:
        if _toolConstruct.isCurrent():
            #for main_dir in args.access:
            main_directory = os.getcwd() + "/" + args.access
            os.mknod(main_directory)

        else:
            sub_directory = sys.path[4] + "/" + args.access
            os.mknod(sub_directory)

    # remove an entire package tree
    if args.remove:
        if _toolConstruct.isCurrent():
            CRemove(args.remove, True)
        else:
            CRemove(args.remove, False)

    if args.volume:
        print(CVolume(args.volume))

    if args.volumes:
        size = 0
        for vols in args.volumes:
            size += CVolume(str(vols))[0]

        print(size)
tool()
