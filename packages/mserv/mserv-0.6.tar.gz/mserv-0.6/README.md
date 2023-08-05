# mserv
An attempt at a Minecraft Server manager.

## What can it do?
This is a wrapper around the official server.jar from Mojang
As of right now, it can...

- Download and generate files from the official server executable
- Run the server
- Displays network connection information (public ip, port number) so others can join your server
- Can update the server executable (This is still in testing)

## What can it NOT do?
This script/binary can not:
- Port forward for you (You have to do that yourself)
- Update itself (Yet!)
- Execute multiple servers at the same time (Probably wont implement...)

# Installation
Use Python's package manager pip
```
pip install mserv
```

# Generated Help Page
```
usage: mserv.py [-h] {setup,run,update,version} ...

positional arguments:
  {setup,run,update,version}
    setup               Runs functions that generate the server files before
                        running
    run                 Executes the server binary with optional parameters
    update              Goes to the official Mojang website and downloads the
                        server.jar file again. This works whether or not the
                        executable is new
    version             Displays the current version of the program

optional arguments:
  -h, --help            show this help message and exit
```

