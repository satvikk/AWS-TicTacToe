import json
import boto3
dynamodb = boto3.resource('dynamodb')
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    if "queryStringParameters" not in event.keys():
        return {
            "error": "Add name and position as query parameter",
            "status": -1
            }
        
    elif "name" not in event['queryStringParameters'].keys():
        return {
            "error": "Add name as query parameter",
            "status": -1
            }
    elif "pos" not in event['queryStringParameters'].keys():
        return {
            "error": "Add pos as query parameter",
            "status": -1
            }
    boardname = event['queryStringParameters']['name']
    pos = int(event['queryStringParameters']['pos'])
    table = dynamodb.Table('tictactoe_db')
    current_board = table.query(
        KeyConditionExpression=Key('name').eq(boardname)
    )
    current_board = current_board['Items']
    if len(current_board) == 0:
        return {
            "error": "game not found",
            "status": -2
        }
    action_nos = max([i['action_no'] for i in current_board])
    if action_nos in [1,3,5,7]:
        return {
            "error": "not x turn",
            "status": -3
        }
    if action_nos >= 9:
        return {
            "error": "game is over",
            "status": -3
        }
    if pos not in [11,12,13,21,22,23,31,32,33]:
        return {
            "error": "invalid pos",
            "status": -3
        }
    if pos in [i['pos'] for i in current_board]:
        return {
            "error": "pos already occupied",
            "status": -3
        }
    table.put_item(
        Item={
            'name': boardname,
            'action_no': action_nos+1,
            'pos': pos,
            'mark':'x'
            }
        )
    update_winner(boardname)
    return {
            "added_x": "success",
            "status": 0,
            'action_no': action_nos+1,
            'pos': pos,
            'name': boardname
            }
    
def update_winner(boardname):
    table = dynamodb.Table('tictactoe_db')
    win_seqs = [{11,12,13}, {21,22,23}, {31,32,33}, {11,21,31}, {12,22,32}, {13,23,33}, {11,22,33}, {13,22,31}]
    current_board = table.query(
        KeyConditionExpression=Key('name').eq(boardname)
    )
    current_board = current_board['Items']
    for i in current_board:
        if i['action_no']==0 and i['mark'] != '?':
            return -1
    
    xseq = {i['pos'] for i in current_board if i['mark']=='x'}
    oseq = {i['pos'] for i in current_board if i['mark']=='o'}
    for win_seq in win_seqs:
        if win_seq <= xseq:
            response = table.update_item(
                Key={
                    'name': boardname,
                    'action_no': 0
                    },
                UpdateExpression="set mark=:m",
                ExpressionAttributeValues={
                    ':m': 'x'
                },
                ReturnValues="UPDATED_NEW"
            )
            break
        if win_seq <= oseq:
            response = table.update_item(
                Key={
                    'name': boardname,
                    'action_no': 0
                    },
                UpdateExpression="set mark=:m",
                ExpressionAttributeValues={
                    ':m': 'o'
                },
                ReturnValues="UPDATED_NEW"
            )
            break
        pass
    return 0
