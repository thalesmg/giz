from github import Github, Gist, InputFileContent
from github.GithubObject import NotSet
import os
from pathlib import PosixPath
import subprocess
from typing import List, Literal, Optional, Union


def auth(path: str) -> Github:
    p = subprocess.run(["pass", path], capture_output=True)
    token = p.stdout.decode("utf-8").rstrip()
    return Github(token)


def gist_ssh_url(gist: Gist) -> str:
    return f"git@gist.github.com:{gist.id}.git"


def clone_gist(gist: Gist, name: str):
    url = gist_ssh_url(gist)
    subprocess.run(["git", "clone", url, name])


def create_gist(
        gh: Github,
        name: str,
        filepaths: List[PosixPath],
        public: bool = False,
        description: Union[str, Literal[NotSet]] = NotSet
):
    files = {
        f.name: InputFileContent(f.read_text())
        for f in filepaths
    }
    u = gh.get_user()
    gist = u.create_gist(public, files, description)
    clone_gist(gist, name)
    dest = PosixPath(name)
    print("gist created and cloned")
    print(dest.absolute())
