# pyls.py

import json
import os
import sys
from datetime import datetime


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def human_readable_size(size):
    for unit in ["B", "K", "M", "G", "T"]:
        if size < 1024:
            return f"{size}{unit}"
        size //= 1024


def format_time(epoch_time):
    return datetime.fromtimestamp(epoch_time).strftime("%b %d %H:%M")


def list_directory(
    directory,
    show_hidden=False,
    long_format=False,
    reverse=False,
    sort_by_time=False,
    human_readable=False,
    filter_by=None,
):
    items = directory.get("contents", [])

    if not show_hidden:
        items = [item for item in items if not item["name"].startswith(".")]

    if sort_by_time:
        items.sort(key=lambda x: x["time_modified"], reverse=reverse)
    else:
        items.sort(key=lambda x: x["name"], reverse=reverse)

    if filter_by:
        if filter_by == "file":
            items = [item for item in items if "contents" not in item]
        elif filter_by == "dir":
            items = [item for item in items if "contents" in item]
        else:
            print(
                f"error: '{filter_by}' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            )
            return

    for item in items:
        if long_format:
            if human_readable:
                size = human_readable_size(item["size"])
            else:
                size = item["size"]
            time_modified = format_time(item["time_modified"])
            print(f"{item['permissions']} {size:>6} {time_modified} {item['name']}")
        else:
            print(item["name"], end=" ")


def navigate_to_path(directory, path):
    if path in [".", "./"]:
        return directory
    parts = path.strip("/").split("/")
    current = directory
    for part in parts:
        for item in current.get("contents", []):
            if item["name"] == part:
                current = item
                break
        else:
            print(f"error: cannot access '{path}': No such file or directory")
            return None
    return current


def print_help():
    help_message = """
Usage: python -m pyls [OPTIONS] [PATH]

Options:
  -A             do not ignore entries starting with .
  -l             use a long listing format
  -r             reverse order while sorting
  -t             sort by modification time, newest first
  --filter=      filter output (dir or file)
  -h             show human readable sizes
  --help         display this help and exit
"""
    print(help_message)


def main():
    import argparse

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-A", action="store_true", help="do not ignore entries starting with ."
    )
    parser.add_argument("-l", action="store_true", help="use a long listing format")
    parser.add_argument("-r", action="store_true", help="reverse order while sorting")
    parser.add_argument(
        "-t", action="store_true", help="sort by modification time, newest first"
    )
    parser.add_argument("--filter", type=str, help="filter output (dir or file)")
    parser.add_argument("-h", action="store_true", help="show human readable sizes")
    parser.add_argument("--help", action="store_true", help="display help and exit")
    parser.add_argument("path", nargs="?", default=".", help="path to list")

    args = parser.parse_args()

    if args.help:
        print_help()
        return

    directory = load_json("structure.json")
    target_directory = navigate_to_path(directory, args.path)
    if target_directory:
        list_directory(
            target_directory,
            show_hidden=args.A,
            long_format=args.l,
            reverse=args.r,
            human_readable=args.h,
            sort_by_time=args.t,
            filter_by=args.filter,
        )


if __name__ == "__main__":
    main()
