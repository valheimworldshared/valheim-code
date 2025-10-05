import os
from git import Repo
from datetime import datetime
import shutil
dougkey = "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"

username = os.getlogin()
local_filepath = r"C:\Users\\"+username+r"\AppData\LocalLow\IronGate\Valheim\worlds_local"
remote_url = f'https://{"DougCilli"}:{"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"}@github.com/DougCilli/Valheim_Shared_Worlds.git'
valheim_directory = "C:/Program Files (x86)/Steam/steamapps/common/Valheim"

def pull_from_remote(local_filepath, remote_url):
    repo = Repo(local_filepath)
    origin = repo.remotes.origin
    origin.pull()

def push_to_remote(local_filepath, remote_url):
    repo = Repo(local_filepath)

    repo.git.add(all=True)

    # Make this a timestamp and include username
    now = datetime.now()
    formatted_time_string = now.strftime("%A, %B %d, %Y %I:%M:%S %p")

    commit_message = "World updated on "+formatted_time_string+" by "+username
    repo.index.commit(commit_message)

    origin = repo.remote('origin')
    origin.push()

def run_valheim():
    os.chdir(valheim_directory)
    os.system("valheim.exe")

def clone_repo(local_filepath, remote_url):
    print("cloning repo")

    # Clone the repo into a temporary directory
    repo = Repo.clone_from(remote_url, local_filepath+"/temp")

    # Move all files and the .git from the temp directory into the worlds_local directory
    filenames = os.listdir(local_filepath+"/temp")
    for filename in filenames:
        print("Moving "+local_filepath+"/temp/"+filename+" to "+filename,local_filepath+filename)
        shutil.move(local_filepath+"/temp/"+filename,local_filepath+"/"+filename)
    
    os.removedirs(local_filepath+"/temp")

def launch_valheim_sharer(local_filepath = local_filepath, remote_url = remote_url,valheim_directory = valheim_directory):

    # Sign into the shared github account
    # sign_into_shared_github()

    # If a repo does not already exist locally, clone it down
    if ".git" not in os.listdir(local_filepath):
        clone_repo(local_filepath=local_filepath,remote_url=remote_url)

    # pull from repo
    print("Pulling from repo")
    pull_from_remote(local_filepath=local_filepath, remote_url=remote_url)

    # run valheim
    run_valheim()

    # push to repo
    print("Pushing to repo")
    push_to_remote(local_filepath=local_filepath, remote_url=remote_url)

launch_valheim_sharer()