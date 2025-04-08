from nodes import TextNode

import os
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
    public_dir = "/home/ignaciocane/workspace/github.com/caneignacio/static-site/public/"
    sub_list = os.listdir(directory)
    if sub_list == [] or sub_list == None:
        return
    for s in sub_list:
        s_dir = f"{directory}{s}"
        new_dir = s_dir.replace(static_dir, public_dir)
        if os.path.isdir(s_dir):
            os.mkdir(f"{new_dir}/")
            copy_directory(f"{s_dir}/")
        elif os.path.isfile(s_dir):
            shutil.copy(s_dir, new_dir)
        else:
            return
    return
    


def main():
    public_cache = "/home/ignaciocane/workspace/github.com/caneignacio/static-site/public/__pycache__/"
    if os.path.isdir(public_cache):
        shutil.rmtree("/home/ignaciocane/workspace/github.com/caneignacio/static-site/public/__pycache__/")
    clean_directory("/home/ignaciocane/workspace/github.com/caneignacio/static-site/public/")
    copy_directory("/home/ignaciocane/workspace/github.com/caneignacio/static-site/static/")

main()
