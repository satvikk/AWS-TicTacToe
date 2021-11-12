# AWS-TicTacToe

This repository contains the codebase for a RestAPI TicTacToe game made using the AWS services: API Gateway, Lambda, and DynamoDB. 

URL for the game: https://d7i48k9955.execute-api.us-east-1.amazonaws.com/ttt/
routes in the api:  
  
- createboard (creates a new game with *name* passed as a query parameter
- showgame (shows the state of the board through an HTML with *name* passed as a query parameter
- x (The X player makes their move. *name* and *pos* (position) passed as query paramters
- o (The O player makes their move. *name* and *pos* (position) passed as query paramters
