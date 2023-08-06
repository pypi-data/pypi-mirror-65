import os
import subprocess


def add(args):
    '''Tags new Folders'''
    if args.directory == "":
        print("Nothing specified!\nPlease specify file")
        exit()

    else:
        directory = args.directory

        if not os.path.exists(directory):
            print(f"fatal: pathspec '{directory}' did not match any directories")
            exit()

        if not os.access(directory, os.W_OK):
            print(f"fatal: no writing permissions in '{directory}'")
            exit()

        vim_add(directory)
    
def vim_add(directory):
    subprocess.run(f"vim + ./{directory}/.joetag",shell=True)

