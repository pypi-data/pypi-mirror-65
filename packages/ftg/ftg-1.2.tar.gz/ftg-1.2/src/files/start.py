from textwrap import dedent

def start(name):
    return dedent(f"""\
    from app import app
    import {name}_api
    import {name}_web

    if __name__ == '__main__':
        app.run()
    """)