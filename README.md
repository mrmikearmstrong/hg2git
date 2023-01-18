# hg2git Script :corn:
Gently wraps [fast-export by /frej](https://github.com/frej/fast-export) with a python script for a friendly hg to git experience.

Bulk convert a set of mercurial hg repositories to git with history and push them to some remote automatically if desired :rocket:

---

## Dependencies :cactus:
- A modern linux based operating system *tested & working in UbuntuServer 20.04 LTS*
- Python 3.6 for your distro
- This repo builds on: https://github.com/frej/fast-export so go get it

---

## How tho :information_desk_person:

1. Install Python & the following packages

Core python:
`sudo apt-get update`
`sudo apt-get python3`

Modules:
`sudo pip3 install logging`
`sudo pip3 install pathlib`

2. Install fast-export 
This script utilises the .sh fast-export script located in the repository
Pull it into a dir with permissions, you may need to chown the dir

3. Modify the script with your repo directory, user details and authors list accordingly

4. Convert! Call the script and *awaaaaaay we go*

### Disclaimer
Always backup first.
