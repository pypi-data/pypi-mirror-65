#!/usr/bin/env python3

import os
import requests
import socket
from bs4 import BeautifulSoup
import argh
import subprocess
from clint.textui import progress
from colorama import Fore, Back, Style, init

init(autoreset=True)
serverDir = {}
url = "https://www.minecraft.net/en-us/download/server/"


def file_webscraper(url=url, search_file='server.jar'):
    """Searches a specified webpage searching for a hyperlink to a specified file
    
    Keyword Arguments:
        url {str} -- Url of the webpage to scrape (default: {https://www.minecraft.net/en-us/download/server/})
        search_file {str} -- The file to search for (default: {'server.jar'})
    
    Returns:
        [str] -- The url of the file we want to access
    """
    requester = requests.get(url)
    soupy = BeautifulSoup(requester.text, features="html.parser")
    for link in soupy.findAll('a'):
        if link.get("href") is not None:
            if search_file in link.get("href"):
                return link.get('href')

def identify_servers(path=os.getcwd()):
    # Identify any potential servers in current directory
    for subdir, _, filenames in walklevel(os.getcwd()):
        if "server.jar" in filenames:
            if os.path.basename(os.path.normpath(subdir)) in serverDir:
                serverDir[os.path.basename(os.path.normpath(subdir))].append(subdir)
            else:
                serverDir[os.path.basename(os.path.normpath(subdir))] = subdir

# os.walk, but allows for level distinction
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def fileNameFromURL(url):
    # Extracts the filename from a given url
    if url.find('/'):
        return url.rsplit('/', 1)[1]


def update(serverName):
    """Goes to the official Mojang website and downloads the server.jar file again. This works whether or not the
    executable is new """
    # identify where the server.jar file is located
    os.remove(f"{os.path.join(serverDir[serverName], 'server.jar')}")
    download_to_dir(file_webscraper(), serverDir[serverName])


def download_to_dir(url, outDir=os.getcwd()):
    """Downloads a file from a url and saves it in the specified output directory
    
    Arguments:
        url {str} -- The url of the file to be downloaded
    
    Keyword Arguments:
        outDir {str} -- Directory to save the file to (default: {os.getcwd()})
    """
    requestor = requests.get(url, stream=True)
    fileName = fileNameFromURL(url)
    directory = os.path.join(outDir, fileName)
    # Exception handling for the HTTPS request
    try:
        requestor.raise_for_status()
    except Exception as urlOof:
        print(Fore.RED + "Error in accessing URL: %s", urlOof)
        input("Press ENTER to continue...")

    print(Fore.YELLOW + Style.BRIGHT + "Downloading %s" % fileName)
    # Some exception handling for file writing stuff
    with open(directory, "wb") as file:
        total_length = int(requestor.headers.get('content-length'))
        for chunk in progress.bar(requestor.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                file.write(chunk)
                file.flush()


def eula_true(serverName):
    """Points to the eula.txt generated from the server executable, generates text to auto-accept the eula
    """
    eula_dir = os.path.join(serverDir[serverName], 'eula.txt')
    # with is like your try .. finally block in this case
    with open(eula_dir, 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # now change the 2nd line, note that you have to add a newline
    if data[-1] != 'eula=true':
        accept_eula = input("Would you like to accept the Mojang EULA? (Y/n)")
        if accept_eula.lower == "y" or accept_eula == "":
            data[-1] = 'eula=true'
        else:
            print("EULA not accepted. You can do this later within the 'eula.txt' file")

        # and write everything back
        with open(eula_dir, 'w') as file:
            file.writelines(data)


def setup():
    """Runs functions that generate the server files before running
    """
    serverName = input(Fore.YELLOW + Style.BRIGHT + "Input new server name: ")
    os.mkdir(os.path.join(os.getcwd(), serverName))
    download_to_dir(file_webscraper(), os.path.join(os.getcwd(), serverName))
    identify_servers()
    run(first_launch=True, serverName=serverName)
    eula_true(serverName)
    print(Fore.GREEN + Style.BRIGHT + '\nEULA Accepted and server is ready to go!!')


def run(max_ram: "Maximum amount of ram alloted" = "-Xmx1024M", min_ram: "Minimum amount of ram alloted" = "-Xms1024M",
        gui: "if True, will show the Mojang UI, else will remain CLI-based" = False,
        first_launch: "Backend, used to denote if this is part of the Setup" = False, serverName='Server'):
    """Executes the server binary with optional parameters
    """
    # If multiple folders exist, let user select
    #TODO

    gui = "nogui" if gui is False else ""
    if first_launch:
        subprocess.run(
            ["java", f"{max_ram}", f"{min_ram}", "-jar", f"{os.path.join((serverDir[serverName]), 'server.jar')}", f"{gui}"],
            cwd=serverDir[serverName], stdout=subprocess.DEVNULL)

        return

    # List all identified server folders and let user select them
    identify_servers()
    selectDir = ''
    if len(serverDir) > 1:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Choose server to run (enter number): ")
        for number, item in enumerate(serverDir):
            print(f"{number} - {item}  ", end=' ',)
        selectDir = list(serverDir)[int(input())]
        #TODO
    else:
        selectDir=list(serverDir)[0]
    # Networking IP information
    print(Fore.GREEN + Style.BRIGHT + f"\nStarting {selectDir}\n")
    print(Fore.YELLOW + Style.BRIGHT + 'Gathering Network Information...\n')
    hostname = socket.gethostname()
    IP_Ad = requests.get('http://ip.42.pl/raw').text
    print(
        Fore.CYAN + Style.BRIGHT + f"Hostname: {hostname}\nIP Address: {IP_Ad}\nPort:25565")

    print("Starting Server...")
    subprocess.run(["java", f"{max_ram}", f"{min_ram}", "-jar", f"{os.path.join(serverDir[selectDir], 'server.jar')}", f"{gui}"],
                   cwd=serverDir[selectDir])


# TODO
def GUI():
    """Executes the user interface for mserv, best for people who don't know how to use the command line
    """
    pass


def main():
    parser = argh.ArghParser()
    parser.add_commands([setup, run, update])
    parser.dispatch()
