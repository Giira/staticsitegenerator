import os
import shutil
from copydirectory import copy_files

def main():
    print("... Removing public directory ...")
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    
    print("... Copying static to new public directory ...")
    copy_files("./static", "./public")


main()
