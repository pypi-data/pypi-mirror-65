import argparse
from .templates import gen_template

def main():
    parser = argparse.ArgumentParser(prog='flask-template', description="A flask app template generator.")

    parser.add_argument("command", choices=["new"], help="Commands to run, allowed values are: new => For template generation")

    parser.add_argument("name", help="Name for the resource generation")

    args = parser.parse_args()

    if args.command == "new":
        gen_template(args.name)

if __name__ == "__main__":
    main()