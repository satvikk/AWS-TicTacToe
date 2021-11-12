import json
import boto3
dynamodb = boto3.resource('dynamodb')
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    
    if "queryStringParameters" not in event.keys():
        return {
            "error": "Add name as query parameter",
            "status": -1
            }
        
    elif "name" not in event['queryStringParameters'].keys():
        return {
            "error": "Add name as query parameter",
            "status": -1
            }
    boardname = event['queryStringParameters']['name']
    table = dynamodb.Table('tictactoe_db')
    check_games = table.query(
        KeyConditionExpression=Key('name').eq(boardname)
    )
    if len(check_games['Items']) > 0:
        return {
            "error": "Game already exists",
            "status": -2
        }
    table.put_item(
    Item={
        'name': boardname,
        'action_no': 0,
        'pos': 0,
        'mark': '?'
        }
    )
    return {
        "created_board": boardname,
        "status": 0
        }

