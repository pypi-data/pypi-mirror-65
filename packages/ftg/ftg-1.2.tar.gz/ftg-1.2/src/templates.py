import os
from shutil import copytree, copy
from .utils.write_file import write_file
from os.path import dirname, abspath, isfile, join
from .files import (
    readme,
    gitignore,
    app,
    env,
    start,
    templates_layout
)

def gen_template(name):
    os.mkdir(name)
    web_path = join(name, f"{name}_web")
    api_path = join(name, f"{name}_api")
    root = dirname(abspath(__file__))
    static_path = join(root, "files", "static")
    static_files = [join(static_path, f) for f in os.listdir(static_path) if isfile(join(static_path, f))]
    for f in static_files:
        copy(f, name)
    copytree(join(static_path, "web"), web_path)
    copytree(join(static_path, "api"), api_path)
    copytree(join(static_path, "models"), join(name, "models"))
    write_file(join(name, ".gitignore"), gitignore(name))
    write_file(join(name, "README.md"), readme(name))
    write_file(join(name, "app.py"), app(name))
    write_file(join(name, ".env"), env(name))
    write_file(join(name, "start.py"), start(name))
    write_file(join(name, f"{name}_web", "templates", "_layout.html"), templates_layout(name))

