#!/usr/bin/python3
import boto3


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='Teams',
        KeySchema=[
            {
                'AttributeName': 'table_number',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'team_hash',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'table_number',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'team_hash',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table


if __name__ == '__main__':
    team_table = create_table()
    print("Table status:", team_table.table_status)
    
    