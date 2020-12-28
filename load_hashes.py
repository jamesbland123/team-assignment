#!/usr/bin/python3 
import csv
import boto3

dynamodb = boto3.resource('dynamodb')

with open('hash.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for col in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(col)}')
            line_count += 1
        else:
            #print(f'\t{col}')
            table = dynamodb.Table('Teams-dev')
            table.put_item(Item={'row_number': int(col[3]), 'team_hash':col[4], 'team_hash_login':col[5], 'members_count': 0, 'members': [] })
            line_count += 1
    print(f'Processed {line_count} lines.')
    
# csv columns are game-id, team-id, name, table-number, team-hash, team-hash-login, aws-account-id, status
