
# Batch converts .hg repos to git with fast-export & attempts to push them to a server/group

# imports
import os
import subprocess
from pathlib import Path
import logging
import sys
from datetime import datetime

# paths
hg_base = str("/repositories")
git_base = str("/hg2git")
fast_exp = str("/home/fast-export/hg-fast-export.sh")
#authors_list = str("/home/fast-export/authors.map")

# remote push
gl_baseurl = str("https://YOUR_REMOTE.com/YOUR_GROUP/")
gl_email = str("")
gl_username = str("")
gl_password = str("")
attempt_push = True

# locals
git_repo_path = str("")
temppath = str("")
cmd = str("")
repo_count = 0

# configure logging
logging.basicConfig(format = '%(asctime)s %(levelname)-8s %(message)s',
                    level = logging.INFO,
                    datefmt ='%Y-%m-%d %H:%M:%S',
                    handlers = [
                        logging.FileHandler("log.txt"),
                        logging.StreamHandler(sys.stdout)
                    ])

# remeber start time
strt_time = datetime.now()

# iterate all .hg repos in hg_base
for hgpath in Path(hg_base).rglob('*.hg'):

    logging.info("################################################## CONVERTING REPO... ##################################################")

    logging.info("Found .hg repository at: " + str(hgpath))
    repo_count = repo_count + 1

    # create the directory within the git_base mount
    temppath = str(hgpath)
    temppath = str(temppath).replace('/repositories/', '')
    temppath = str(temppath).replace('/.hg', '')
    git_repo_path = str(git_base) + str("/") + str(temppath)
    if not os.path.exists(git_repo_path):
        logging.info("Creating new .git directory at: " + str(git_repo_path))
        logging.info(str(os.makedirs(git_repo_path)))
        logging.info("Done!")
    else:
        logging.info("Repo already exists at path: " + str(git_repo_path))
        continue    # skips repo here

    # cd to path
    logging.info("Migrating to path...")
    os.chdir(str(git_repo_path))
    cmd = str("cd ") + str("\"") + str(git_repo_path) + str("\"")
    cmd = str(cmd).replace("'", "")
    logging.info(str(os.system(cmd)))
    logging.info("Done!")

    # init git repo at new dir
    logging.info("Initialising git repo at new directory...")
    cmd = str(str("git init ") + str("\"") + str(git_repo_path) + str("\""))
    cmd = str(cmd).replace("'", "")
    logging.info("with command: " + str(cmd))
    logging.info(str(os.system(cmd)))
    logging.info("Done!")

    # execute fast-export
    hgpath_modded = str(hgpath).replace('/.hg', '')
    logging.info("Executing fast-export on .hg repo...")
    logging.info(str(subprocess.call([fast_exp, "-r", hgpath_modded, "-A", authors_list])))
    logging.info("Done!")

    # checkout the repo head
    logging.info("Checking out the HEAD branch...")
    logging.info(str(subprocess.call(["git", "checkout", "HEAD"])))
    logging.info("Done!")

    # push to the remote server
    if (attempt_push):

        # setup credentials
        logging.info("Configuring GitLab credentials...")
        subprocess.call(["git", "config", "--global", "user.email", str(gl_email)])
        subprocess.call(["git", "config", "--global", "user.name", str(gl_username)])
        subprocess.call(["git", "config", "--global", "user.password", str(gl_password)])
        logging.info("Done!")
        
        # generate the url and attempt push
        rename = str(hgpath).replace("/repositories/", "")
        rename = str(rename).replace(".hg", "")
        rename = str(rename).replace(" ", "_")
        rename = str(rename).replace("/", "-")
        rename = str(rename).replace("----", "-")
        rename = str(rename).replace("---", "-")
        rename = str(rename).replace("--", "-")
        rename = str(rename).replace("_-_", "-")
        rename = str(rename).replace("-_-", "-")
        rename = str(rename).replace("(", "")
        rename = str(rename).replace(")", "")
        rename = str(rename).lstrip(" !@%^&()-*")
        rename = str(rename).rstrip(" !@%^&()-*")
        rename = str(rename) + str(".git")
        rename = str(rename.lower())
        gl_remoteurl = str(gl_baseurl) + str(rename)
        logging.info("Pushing repo to the remote server at path: " + str(gl_remoteurl))

        # setup credentials
        logging.info("Configuring Git credentials...")
        subprocess.call(["git", "config", "--global", "user.email", str(gl_email)])
        subprocess.call(["git", "config", "--global", "user.name", str(gl_username)])
        subprocess.call(["git", "config", "--global", "user.password", str(gl_password)])
        logging.info("Done!")

        # push all
        logging.info("Pushing all to the remote server at path: " + str(gl_remoteurl))
        logging.info(str(subprocess.call(["git", "push", "--verbose", "--all"])))
        logging.info("Done!")

    else:
        logging.info("Push to server skipped.")

    logging.info("Repos processed so far: " + str(repo_count))
    logging.info(" ")

logging.info("Fin.")
logging.info("Conversion started at: " + str(strt_time))
logging.info("        & finished at: " + str(datetime.now()))
