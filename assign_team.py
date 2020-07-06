#!/usr/bin/python3
import boto3

team_size = 3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Teams')

response = table.scan()
data = response['Items']

# Retrieve data records beyond 1MB dynamodb response
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

# Sort the list so users can be assigned in order
sorted_teams = sorted(data, key=lambda x: x['table_number'])

available_teams = 0
for team in sorted_teams:
    
    if team['members_count'] < team_size: 
        available_teams += 1
        team['members_count'] += 1
        team['members'].append('Jill')
        table.put_item(Item=team)
        
        print('Congratulations here is your new hash: {}'.format(team['team_hash_login']))
        break
    
if available_teams == 0:
    print("Sorry, but all teams are currently full")

