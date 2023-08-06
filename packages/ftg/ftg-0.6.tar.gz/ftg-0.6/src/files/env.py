from textwrap import dedent

def env(name):
    return dedent(f"""\
    FLASK_ENV=development
    FLASK_APP=start
    DATABASE_URL=postgres://localhost:5432/{name}_dev
    """)