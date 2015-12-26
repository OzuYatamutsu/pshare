# pshare
Need to share a file with someone real quick?

```
jinhai@dev.steakscorp.org:~$ pshare /path/to/file/file.7z
Your file is now accessible at these URLs:
http://localhost:45013/file.7z
http://dev.steakscorp.org:45013/file.7z
http://192.168.1.103:45013/file.7z
http://128.16.227.56:45013/file.7z
 * Running on http://0.0.0.0:45013/ (Press CTRL+C to quit)
128.16.227.23 - - [18/Dec/2015 14:34:06] "GET /file.7z HTTP/1.1" 200 -
Transfers complete! Shutting down server...

jinhai@dev.steakscorp.org:~$ 
```

_Pretty easy, right?_

## Waaaait, what just happened?
**pshare** starts up a simple Flask HTTP server on an arbitrary port. Upon a request from a client, it serves the file specified from its path, and then (by default) immediately shuts down upon transfer completion. _No more moving a file into a staging directory on your main web server!_

## Syntax
```
pshare <file_path> [max_transfers]
```

**`file_path`** The path to the file you want to share. The file must exist and be readable by the user running pshare.

**`max_transfers`** (optional) The maximum number of downloads of your file that you want to permit before you stop sharing it. The default is `1`. A value of `0` will permit an unlimited number of downloads.

## Installation
pshare requires `python` (2 or 3)`, as well as the Flask web framework and the socket library.

#### Python 2
```
sudo apt-get install -y python python-pip
sudo pip install flask socket
```

#### Python 3
```
sudo apt-get install -y python3 python3-pip
sudo pip3 install flask
```

pshare can then be run in the local directory by running `./pshare`.
To install pshare globally, move it into your bin path:
```
sudo mv pshare.py /usr/local/bin/
```

Then, simply run `pshare`, specifying the arguments detailed above.

## `ipgetter`

pshare makes use of the `ipgetter` library, maintained by phoemur@gmail.com.
