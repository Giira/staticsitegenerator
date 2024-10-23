import os
import shutil

def copy_files(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    for file in os.listdir(source):
        from_dir = os.path.join(source, file)
        to_dir = os.path.join(destination, file)

        print(f"*** {from_dir} -> {to_dir} ***")

        if os.path.isfile(from_dir):
            shutil.copy(from_dir, to_dir)
        else:
            copy_files(from_dir, to_dir)

    
