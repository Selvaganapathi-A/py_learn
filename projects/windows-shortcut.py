import os
from win32com.client import Dispatch

from package.customPathlib import CustomWindowsPath as Path

def main():
    # * source file
    target:Path = Path("C:/Sa/Downloads").absolute()
    # * shortcut to the source file
    shortcut = Path("C:/Sa/Shortcut.lnk").absolute()
    #
    # target.hardlink_to(source)
    shell = Dispatch(
        'WScript.shell'
    )
    shortcut = shell.CreateShortCut(str(shortcut))
    shortcut.Targetpath = str(target)
    shortcut.save()
    pass


if __name__ == "__main__":
    main()
    pass
