import socket
import sys
from config import *
import os
import pandas as pd

client_name = ''
player_score = ''
players = {}
print('Server : PID', os.getpid())
print('Welcome to TCP Game Server')

serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_soc.bind((SERVER_HOST, SERVER_PORT))
serv_soc.listen(5)

print('Server is waiting for a connection request ...')

try:
    while True:
        cli_soc, cli_addr = serv_soc.accept()
        print('Connected to:', cli_addr[0])
        client_name = ''

        while True:
            try:
                msg = cli_soc.recv(1024).decode('utf-8')
                if not msg:
                    print('Client disconnected.')
                    break

                if client_name == '':
                    client_name = msg
                    print(f"Player Name: {client_name}")
                    start_msg = "Start".encode('utf-8')
                    cli_soc.send(start_msg)
                    players[client_name] = {"IP address": cli_addr[0], "Score": 0}
                else:
                    player_score = msg
                    players[client_name]["Score"] = player_score
                    print(f"                    Player Score                    \nPlayer from {cli_addr[0]}   Name: {client_name}  Score: {player_score}")

            except ConnectionResetError:
                print('Connection was forcibly closed by the client.')
                break

        print('Closing connection with:', cli_addr[0])
        print(players)
        print("Player List:")

        #print the player
        for name, details in players.items():
            print(f"Name: {name}, IP address: {details['IP address']}, Score: {details['Score']}")

        # Directly create a DataFrame from the dictionary
        # the key inside the dict will be the row index , reset_index so that the key become a new column
        df = pd.DataFrame.from_dict(players, orient="index").reset_index()
        df.rename(columns={"index": "Name"}, inplace=True)
        df.to_csv('Player Record.csv', index=False)
        cli_soc.close()

except KeyboardInterrupt:
    print('Server shutting down...')
    serv_soc.close()
    sys.exit()

