#!/usr/bin/env python3
import argparse

from cli.command_router import CommandRouter, COMMANDS

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('additional_args', nargs='*')

    args = parser.parse_args()
    router = CommandRouter()
    router.route_command(args.command, args.additional_args)

if __name__ == "__main__":
    main()
