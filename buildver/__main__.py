import sys
from buildver import cli


__all__ = []


COMMANDS = {"help": cli.print_help,
            "check": cli.check_project,
            "set": cli.set_version,
            "build": cli.build_project}


def main():
    args = sys.argv[1:]
    # no args
    if not args:
        cli.print_help()
        return
    command = args[0].lower()
    arguments = args[1:]
    handler = COMMANDS.get(command)
    if handler:
        handler(*arguments)
    else:
        valid_commands = ", ".join(["'{}'".format(key) for key in COMMANDS.keys()])
        print("Valid commands are: {}.".format(valid_commands))


if __name__ == "__main__":
    main()
