# app.py

import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

TABLE = os.environ['DB_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/teams")
def get_teams():
    response = client.scan(TableName=TABLE)
    data = response['Items']

# Retrieve data records beyond 1MB dynamodb response
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return jsonify(data)


@app.route("/member/<string:name>", methods=["POST"])
def add_member(name):
    response = client.scan(TableName=TABLE)
    data = response['Items']

    # Retrieve data records beyond 1MB dynamodb response
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    sorted_teams = sorted(data, key=lambda x: x['table_number'])

    available_teams = 0
    for team in sorted_teams:
    
        if team['members_count'] < team_size: 
            available_teams += 1
            team['members_count'] += 1
            team['members'].append('Jill')
            table.put_item(Item=team)
            

            return jsonify({
                'status': 'assigned',
                'team_hash_login': team['team_hash_login']
            })
            break
    
    if available_teams == 0:
        return jsonify({
            'status': 'No teams available'
        })