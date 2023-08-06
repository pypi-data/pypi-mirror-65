import io
import os.path
import subprocess

from pyside2uic import compileUi


def create_py_from_ui(ui_file):
    output = io.StringIO()
    head, tail = os.path.split(os.path.abspath(ui_file))
    cwd = os.getcwd()
    try:
        os.chdir(head)
        compileUi(tail, output)
    finally:
        os.chdir(cwd)
    return output.getvalue()


def compare_and_update(filename, new_contents):
    

    try:
        with open(filename, 'r') as f:
            old_lines = f.readlines()
        old_uncommented = [l for l in old_lines if not l.startswith("#")]
        
        new_lines = new_contents.splitlines(keepends=True)
        new_uncommented = [l for l in new_lines if not l.startswith("#")]
        
        no_change = (new_uncommented == old_uncommented)
    except FileNotFoundError:
        no_change = False

    if no_change:
        print("No Change: {}".format(os.path.basename(filename)))
        return
    else:
        with open(filename, 'w') as f:
            f.write(new_contents)
        print("Updated: {}".format(os.path.basename(filename)))


def update_ui(ui_file):
    # pull off the .ui
    root, _ext = os.path.splitext(ui_file)
    if _ext != ".ui":
        root = ui_file
    
    # add ui_ to the front and .py to the end
    head, tail = os.path.split(root)
    output_file = os.path.join(head, "ui_" + tail + ".py")

    new_contents = create_py_from_ui(ui_file)
    compare_and_update(output_file, new_contents)


def main():
    for root, dirs, files in os.walk("."):
        # skip hidden files and folders
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        # skip build directory
        if 'build' in dirs:
            dirs.remove('build')

        for file in files:
            if file.endswith(".ui"):
                update_ui(os.path.join(root, file))


if __name__ == "__main__":
    main()
