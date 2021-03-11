import argparse
import os
import pathlib
import sys
from github.GithubObject import NotSet

from . import core as giz

def create(args):
    if args.dest_dir:
        os.chdir(args.dest_dir)

    dest = pathlib.PosixPath(args.name)
    if dest.exists():
        print(f"destination {dest.absolute()} already exists. aborting.")
        exit(1)

    gh = giz.auth(args.pass_path)
    giz.create_gist(
        gh,
        args.name,
        args.files,
        args.public,
        args.description,
    )


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    create_parser = subparsers.add_parser("create",
                                          help="create a new gist and clone it locally")
    create_parser.add_argument("--name", "-n", required=True,
                               help="folder name to clone the gist under")
    create_parser.add_argument("--public", action="store_true",
                               default=False, required=False,
                               help="whether to create a public gist; default is False")
    create_parser.add_argument("--description", "-d",
                               required=False, default=NotSet,
                               help="optional description for the gist")
    create_parser.add_argument("--dest-dir", type=pathlib.PosixPath,
                               required=False, default=None,
                               help="destination directory to clone the gist into; defaults to current dir")
    create_parser.add_argument("--pass-path", type=str,
                               required=True,
                               help="password-store path where the github token is stored"
                               )
    create_parser.add_argument("files", nargs="+",
                               type=pathlib.PosixPath,
                               help="the files that will compose the gist"
                               )
    parsed = parser.parse_args(argv)

    if parsed.command == "create":
        create(parsed)


if __name__ == "__main__":
    main(sys.argv[1:])
