# team-assignment

## Setup

**You will need Python 3.7**

Python 3.7.9 on Cloud9
```
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar xvzf Python-3.7.9.tgz
cd Python-3.7.9
./configure
make
sudo make install
```

Python 3.7 on Mac
```
brew install python@3.7
```

## Install Serverless framework
```
$ npm install -g serverless
```

You will need two additional plugins
```
$ npm install -g serverless-wsgi serverless-python-requirements
```

## Activate python venv and requirements.txt
```
$ cd team-assignment
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Deploy application
```
sls deploy
```

## Upload data hashes
1. Download hash csv from event engine
2. Copy the file to this project root and rename to hash.csv
3. Run ```python3 load_hashes.py``` You should see output on the number of lines processed.

## Endpoint usage
Displays main page:
* ANY - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev

Admin panel
* GET - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/admin

## Local testing
```
sls invoke local -f app --path event.json
```

## Viewing Logs
```
sls logs -s dev -f app --tail
```
If you remove --tail and use --startTime 30m this can show the logs from 30 minutes ago. Accepts h for hour and d for days.
