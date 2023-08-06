from textwrap import dedent

def gitignore(name):
    return dedent(f"""\
    .vscode
    *.DS_Store
    *__pycache__
    *.env
    {name}_web/static/.webassets-cache
    {name}_web/static/gen
    """)