# GitHub backup script

```
Backup GitHub repositories

Usage:
  github-backup [-t github-access-token] -d DIR

Options:
  -d DIR     Backup directory
  -t TOKEN   Github Access Token, env: GITHUB_ACCESS_TOKEN

```

This directory contains a script, ```backup.py```, for backing up GitHub repositories.

The script requires a GitHub token and a destination directory. It then uses the token to populate the destination directory with clones of all the repositories the token can access.

Repeated runs only update the already existing backups and add new repositories, if any.

## Installation

Install the required Python dependencies using ```pip```:

```
$ pip install -r requirements.txt
```

### Create a token

For authorization you need to create a new personal GitHub token. You can do this from the GitHub settings, under the **Personal Access Tokens** tab.

![Step 1](images/new-token-1.png)

When you click the **Generate new token** button you enter the token creation screen. Here you should give the token a descriptive name and choose its *scopes*, which basically determine what the token is allowed to do.

![Step 2](images/new-token-2.png)

To backup public and private repositories you need to select only the **repo** scope. If you have no need for private repositories just choose the **public_repo** scope.

![Step 3](images/new-token-3.png)

After clicking the **Generate token** button you're presented with the generated token. Remember to store it now, as GitHub won't show it to you anymore!

In the next example let's assume your token is ```6b86190dd45c57c1a1b039a5a54d892e019102f7``` as in the above image.

## Running

After preparing the token and the configuration file you now can run the script:

```
$ python backup.py -t <ACCESS_TOKEN> -d github 
```

## Running with Docker

Build image
```bash
docker build . -t github-backup 
```

Run docker images, mounting the local github dir into the container
```bash
docker run -v $PWD/github:/app/repos --rm -it -e GITHUB_ACCESS_TOKEN=ADD_TOKEN_HERE github-backup
```

## Configuring

