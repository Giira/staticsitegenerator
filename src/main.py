import os
import shutil
from copydirectory import copy_files, generate_page_recursive

source = "./static"
content = "./content"
destination = "./public"
template = "./template.html"


def main():
    print("... Removing public directory ...")
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    
    print("... Copying static to new public directory ...")
    copy_files(source, destination)

    generate_page_recursive(content, template, destination)

main()
