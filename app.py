# app.py
import os
import boto3
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

TABLE = os.environ['DB_TABLE']
ENDPOINT = os.environ['ENDPOINT']
dynamodb = boto3.resource('dynamodb')
db_tbl = dynamodb.Table(TABLE)
team_size = 1

@app.route("/")
def main_page():
    return render_template('register.html', endpoint=ENDPOINT)    

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
            
            return render_template('hash.html', hash_code=team['team_hash_login'])
    
    return render_template('no_hashes.html', name=name)         

if __name__ == "__main__":
    main_page()