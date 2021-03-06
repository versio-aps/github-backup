#!/usr/bin/env python
"""
Backup GitHub repositories

Usage:
  github-backup [-t github-access-token] [-a] -d DIR

Options:
  -d DIR     Backup directory
  -t TOKEN   Github Access Token, env: GITHUB_ACCESS_TOKEN
  -a         Backup all repos (not only own repos), default: false
"""

from __future__ import print_function

import os
import re
import sys
import json
import errno
import argparse
from urllib import parse
import requests
import subprocess

from docopt import docopt


def get_json(url, token):
    while True:
        response = requests.get(url, headers={
            "Authorization": "token {0}".format(token)
        })
        response.raise_for_status()
        yield response.json()

        if "next" not in response.links:
            break
        url = response.links["next"]["url"]


def check_name(name):
    if not re.match(r"^\w[-\.\w]*$", name):
        raise RuntimeError("invalid name '{0}'".format(name))
    return name


def mkdir(path):
    try:
        os.makedirs(path, 0o770)
    except OSError as ose:
        if ose.errno != errno.EEXIST:
            raise
        return False
    return True


def mirror(repo_name, repo_url, to_path, username, token):
    parsed = parse.urlparse(repo_url)
    modified = list(parsed)
    modified[1] = "{username}:{token}@{netloc}".format(
        username=username,
        token=token,
        netloc=parsed.netloc
    )
    repo_url = parse.urlunparse(modified)

    repo_path = os.path.join(to_path, repo_name)
    mkdir(repo_path)

    # git-init manual:
    # "Running git init in an existing repository is safe."
    subprocess.call(["git", "init", "--bare", "--quiet"], cwd=repo_path)

    # https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth:
    # "To avoid writing tokens to disk, don't clone."
    subprocess.call(["git", "fetch", "--force", "--prune", "--tags",
                     repo_url, "refs/heads/*:refs/heads/*"],
                    cwd=repo_path)


def main():
    args = docopt(__doc__, version='0.0.1')

    dir = args['-d']
    token = args['-t']
    all_repos = args['-a']

    if token is None:
        token = os.getenv("GITHUB_ACCESS_TOKEN")
        if token is None:
            print("GITHUB_ACCESS_TOKEN must be assigned")
            exit(-1)

    path = os.path.expanduser(dir)
    if mkdir(path):
        print("Created directory {0}".format(path), file=sys.stderr)

    user = next(get_json("https://api.github.com/user", token))
    for page in get_json("https://api.github.com/user/repos", token):
        for repo in page:
            name = check_name(repo["name"])
            owner = check_name(repo["owner"]["login"])
            clone_url = repo["clone_url"]

            if not all_repos and owner != user['login']:
                continue

            owner_path = os.path.join(path, owner)
            mkdir(owner_path)
            mirror(name, clone_url, owner_path, user["login"], token)


if __name__ == "__main__":
    main()
