# team-assignment

## Setup
Install serverless framework

You will need two additional plugins
```
$ npm install serverless-wsgi serverless-python-requirements
```

## Activate python venv and requirements.txt
```
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

## To clear all items from DynamoDB
```
curl -H "x-api-key: paste-api-key-from-sls-deploy" https://xxxxxx.execute-api.us-west-2.amazonaws.com/dev/delete_all
```
**Be sure to paste in your actual api key and url to the delete_all function**  You can also log into the console and select all items and delete as well.

## Endpoint usage
Displays main page:
* ANY - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev
* ANY - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/{proxy+}

Display Teams.  Look at members and count columns to determine how many hashes you have remaining
* GET - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/teams
  
Function endpoint to process adding a user to team.
* POST - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/member

Delete all records.  This is behind an api-key, see clear all above
* GET - https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/delete_all

## Local testing
```
sls invoke local -f app --path event.json
```

## Viewing Logs
```
sls logs -s dev -f app --tail
```
If you remove --tail and use --startTime 30m this can show the logs from 30 minutes ago. Accepts h for hour and d for days.
