import os
import shutil
from copydirectory import copy_files, generate_page

def main():
    print("... Removing public directory ...")
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    
    print("... Copying static to new public directory ...")
    copy_files("./static", "./public")

    generate_page("content/index.md", "template.html", "public.index.html")

main()
