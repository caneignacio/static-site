from splitters import markdown_to_blocks, markdown_to_html_node

import os
import sys
import shutil

def clean_directory(directory):
    #Remove all files from public directory
    paths = os.listdir(directory)
    for p in paths:
        p = f"{directory}{p}"
        if os.path.isfile(p):
            os.remove(p)
        else:
            p = p + "/"
            if os.listdir(p) != [] and os.listdir(p) != None:
                clean_directory(p)
            shutil.rmtree(p)

def copy_directory(directory):
    #Copy the files from static to public directory
    static_dir = "/home/ignaciocane/workspace/github.com/caneignacio/static-site/static/"
    docs_dir = "/home/ignaciocane/workspace/github.com/caneignacio/static-site/docs/"
    sub_list = os.listdir(directory)
    if sub_list == [] or sub_list == None:
        return
    for s in sub_list:
        s_dir = f"{directory}{s}"
        new_dir = s_dir.replace(static_dir, docs_dir)
        if os.path.isdir(s_dir):
            os.mkdir(f"{new_dir}/")
            copy_directory(f"{s_dir}/")
        elif os.path.isfile(s_dir):
            shutil.copy(s_dir, new_dir)
        else:
            return
    return


def extract_title(markdown):
    markdown_list = markdown_to_blocks(markdown)
    for m in markdown_list:
        if m[0] == "#" and m[1] != "#":
            return m[1:].strip()
    raise Exception


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    print(dir_list)
    for dir in dir_list:
        cont = dir_path_content + "/" + dir
        dest = dest_dir_path + "/" + dir
        if os.path.isfile(cont):
            generate_page(cont, template_path, dest, basepath)
        elif os.path.isdir(cont):
            generate_pages_recursive(cont, template_path, dest, basepath)
        else:
            return


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    create_file(template, dest_path.replace(".md", ".html"))


def create_file(f, p):
    p_list = p.split("/")[1:]
    sub_list = [p_list[0]]
    for i in range(1, len(p_list)):
        element = "/".join(p_list[0:i+1])
        sub_list.append(element)
    paths = sub_list[:-1]
    page_name = sub_list[-1]
    for pa in paths:
        if not(os.path.isdir(pa)):
            os.mkdir(pa)
    open(page_name, "w").write(f)
    

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    home_path = "/home/ignaciocane/workspace/github.com/caneignacio/static-site"
    clean_directory(home_path + "/docs/")
    copy_directory(home_path + "/static/")
    generate_pages_recursive(home_path + "/content", home_path + "/template.html", "/docs", basepath)

main()