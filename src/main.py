import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
from os import path, listdir, mkdir
from shutil import copy, rmtree
from markdown_blocks import generate_pages_recursive, generate_page

def copy_static_to_public(source, destination):
    #check that the path exists, and clear it
    if path.exists(destination):
        rmtree(destination)

    #create the destination directory
    mkdir(destination)
    
    #put all files and folders within the source into an array
    items = listdir(source)

    #iterate over files and folders in the source directory
    for item in items:
        source_path = path.join(source, item)
        dest_path = path.join(destination, item)

        #if the item is a file, copy it to the destination
        if path.isfile(source_path):
            copy(source_path, dest_path)
            print(f"Copying file: {source_path} to {dest_path}")
        else: #if the item is a directory
            #create subdirectory in the destination
            mkdir(dest_path)
            #recursively handle files in this directory
            copy_static_to_public(source_path, dest_path)


def main():
    copy_static_to_public("static", "docs")

    #set first argument to be the root path of the generated site, if provided
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = '/'

    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    main()