"""
A python utility for creating better modules/packages.
This module give the ability to quickly create and add files to different directories.
From creating directory & sub directory to managing the files that are put into those folders.
This is more of an automation tool for writing modules but can be used for other package related matters.

Example:
    >>> from cpackage import CPack, CAccess
    >>> CPack("mymodule", True, "code")
    >>> CAccess("mymodule/code", True, "example.py")
"""

__all__     = ["CPack", "Cdir", "CAccess", "CRemove", "CVolume"]
__author__  = "Cru1seControl <Cru1seControl.loot@gmail.com>"
__version__ = "v1.0.0"


try: #Ignore errors, just dont run this file!
    from cpackage.packaging import CPack
    from cpackage.packaging import Cdir
    from cpackage.packaging import CAccess
    from cpackage.packaging import CRemove
    from cpackage.packaging import CVolume

except ImportError as importerror:
    print(importerror)
