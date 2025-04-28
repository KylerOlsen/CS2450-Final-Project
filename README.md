# CS 2450 Final Project
*Kyler Olsen* - *Spring 2025*

## Scripture Chase Game

- Repo: [git.purplecello.org/KylerOlsen/CS2450-Final-Project](https://git.purplecello.org/KylerOlsen/CS2450-Final-Project.git)
- Mirror: [github.com/KylerOlsen/CS2450-Final-Project](https://github.com/KylerOlsen/CS2450-Final-Project.git)

## Dependencies

Python 3.10 or greater is recommended.

In the root of the repo run this command to install the required python modules.

```$ pip install -r requirements.txt```

## Running

The following command to run the server.

```$ python3 main.py -s```

The following command to run the client.

```$ python3 main.py```

Here are the options for running.

```
$ python3 main.py -h
usage: main.py [-h] [-s] [-H HOST] [-p PORT] [-n PLAYERNAME] [-b]

Run the server or client.

options:
  -h, --help            show this help message and exit
  -s, --server          Run as server
  -H HOST, --host HOST  Host address (default: '')
  -p PORT, --port PORT  Port number (default: 7788)
  -n PLAYERNAME, --playername PLAYERNAME
                        Player name (for client)
  -b, --bible-only      Run in bible-only mode (for server)
```
