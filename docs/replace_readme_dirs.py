import os
from pathlib import Path
from glob import glob

fpath_this = Path(__file__)


# README
def update_readme(fpath: str):
    fpath = os.path.abspath(fpath)
    content = ""
    with open(fpath) as f:
        content = f.read()
    with open(fpath, "w+") as f:
        content = content.replace("docs/img/", "../img/")

        f.write(content)


def add_toctree_to_autoapi_rsts():
    dirpath = f"{fpath_this.parent.name}/source/autoapi"
    for dir, subdir, files in os.walk(os.path.abspath(dirpath)):
        for x in files:

            if x == "index.rst":
                fpath = os.path.join(dir, x)

                with open(fpath) as f:
                    content = f.read()
                with open(fpath, "w+") as f:
                    content += "\n.. toctree::"
                    f.write(content)


if __name__ in "__main__":
    update_readme(fpath=f"./{fpath_this.parent.name}/source/README.rst")
    update_readme(fpath=f"./{fpath_this.parent.name}/source/viz.rst")

    add_toctree_to_autoapi_rsts()
