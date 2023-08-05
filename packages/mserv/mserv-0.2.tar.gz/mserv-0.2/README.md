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


# Generated Help Page
```usage: mserv.py [-h] {setup,run,update,test} ...

positional arguments:
  {setup,run,update,test}
    setup               Runs functions that generate the server files before
                        running
    run                 Executes the server binary with optional parameters
                        Keyword Arguments: max_ram {str} -- Maximum amount of
                        ram alloted (default: {"-Xmx1024M"}) min_ram {str} --
                        Minimum amount of ram alloted (default: {"-Xms1024M"})
                        gui_flag {bool} -- if True, will show the UI, else
                        will remain CLI-based (default: {False})
    update              Goes to the official Mojang website and downloads the
                        server.jar file again. This works whether or not the
                        executable is new
    test

optional arguments:
  -h, --help            show this help message and exit
```

