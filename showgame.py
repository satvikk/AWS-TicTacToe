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
    game = table.query(
        KeyConditionExpression=Key('name').eq(boardname)
    )['Items']
    rows = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
    
    winner_statement = "No Winner yet"
    for i in game:
        if i['action_no']==0 and i['mark']!='?':
            winner_statement = "The winner is " + i['mark']
            pass
        pass
    
    for pos0 in [1,2,3]:
        for pos1 in [1,2,3]:
            n = pos0*10 + pos1
            for i in game:
                if i['pos'] == n:
                    rows[pos0-1][pos1-1] =  "<u>" + i['mark'] + "</u>"
    out_body = ["<html> <head> </head> <body> <h1> ", 
                "   |  ".join(rows[0]), "<br>",
                "   |  ".join(rows[1]), "<br>",
                "   |  ".join(rows[2]), "<br> <br> <br>",
                winner_statement,
                "</h1>  </body> </html>",
                ]
    return {
        "statusCode": 200,
        "body":  "".join(out_body),
        "headers": {
            'Content-Type': 'text/html',
        }
    }
    # return {
    #     "status": 0,
    #     "winner": "unknown",
    #     "row1": "".join(rows[0]),
    #     "row2": "".join(rows[1]),
    #     "row3": "".join(rows[2])
    # }
    
