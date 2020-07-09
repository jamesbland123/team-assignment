# app.py
import os
import boto3
from flask import Flask, jsonify, request
app = Flask(__name__)

TABLE = os.environ['DB_TABLE']
ENDPOINT = os.environ['ENDPOINT']
dynamodb = boto3.resource('dynamodb')
db_tbl = dynamodb.Table(TABLE)
team_size = 1

@app.route("/")
def main_page():
    page = '''
        <h2>Team Assignment Request</h2>
        <form action="{}" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>
        <input type="submit" value="Submit">
        </form>'''.format(ENDPOINT)
    return (page)    

@app.route("/teams")
def get_teams():
    response = db_tbl.scan()
    data = response['Items']

# Retrieve data records beyond 1MB dynamodb response
    while 'LastEvaluatedKey' in response:
        response = db_tbl.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return str(data)


@app.route("/member", methods=['POST'])
def add_member():
    name = request.form.get('name')
    if not name:
        return 'Please provide userId and name'
    
    response = db_tbl.scan()
    data = response['Items']
  
    # Retrieve data records beyond 1MB dynamodb response
    while 'LastEvaluatedKey' in response:
        response = db_tbl.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # reordering the response from dynamo to place table_number in numerical order
    # python sort doesn't work for this use case.
    
    # Initialize sorted_teams
    sorted_teams = [ x for x in range(len(data)) ]

    for i in data:
        table_number = i['table_number']
        idx_num = int(table_number) - 1
        sorted_teams[idx_num] = i

    for team in sorted_teams:
        if int(team['members_count']) < team_size: 
            team['members_count'] = int(team['members_count']) + 1
            team['members'].append(name)
            db_tbl.put_item(Item=team)
            
            return "Your team hash login is : <a href={0}>{0}</a> <br> <br> Please do not click the back button".format(team['team_hash_login'])
    
    full_message = '''
                   Sorry {}, but all teams are full. You are welcome to watch the event or follow
                   along in your own account. <br>Please let the event staff know that you were not 
                   assigned to a team.'''.format(name)
    return (full_message)          

if __name__ == "__main__":
    main_page()