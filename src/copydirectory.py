import os
import shutil
from markdownblocks import markdown_to_html_node, extract_title

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


def generate_page(from_path, template_path, dest_path):
    print(f"... Generating page from {from_path} to {dest_path} using {template_path} ...")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as g:
        template = g.read()
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', content)
    index = open(dest_path, "w")
    index.write(template)
    index.close()


def generate_page_recursive(content, template_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for file in os.listdir(content):
        from_dir = os.path.join(content, file)
        to_dir = os.path.join(dest_path, file)
        if to_dir.endswith(".md"):
            to_dir = to_dir.replace(".md", ".html")

        print(f"*** {from_dir} -> {to_dir} ***")

        if os.path.isfile(from_dir):
            generate_page(from_dir, template_path, to_dir)
        else:
            generate_page_recursive(from_dir, template_path, to_dir)
