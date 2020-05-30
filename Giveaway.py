""" 
TODO:
- Add multithreading
- Add GUI
- Standartize code (remove global variables and other bad practices)
""" 

import requests, json, time

limit = 100 #Number of messages to scan in the channel. MAX: 100
baseurl = ("https://discord.com/api/v6")

def token_input():
    global token
    token = input("Input authentification token here: ") #How to get authentification token: https://bit.ly/3chIsbQ
    token_check(token)

def token_check(token):
    user = requests.get(baseurl + '/users/@me', headers={"Authorization":token})
    if user.status_code == 200:
        user = json.loads(user.text)['username']
        print('----------------------')
        print('Logged in with user ' + user)
    elif user.status_code == 401:
        print('Wrong code.')
        print()
        token_input()
token_input()


start = time.time()
servers = json.loads(requests.get(baseurl + '/users/@me/guilds', headers={"Authorization":token}).text) #Getting list of joined servers

print('Number of servers: ' + str(len(servers)))
print('----------------------')
print()

for x in range(len(servers)):
    serverid = servers[x]['id']
    servername = servers[x]['name']
    channels = json.loads(requests.get(baseurl + '/guilds/' + serverid + '/channels', headers={"Authorization":token}).text) #Getting list of channels in server
    print('Starting with: ' + servername)
    for y in range(len(channels)):
        if channels[y]['type'] != 0: #Checking if it is a text-channel
            continue
        channelid = channels[y]['id']
        response = requests.get(baseurl + '/channels/' + channelid + '/messages?limit=' + str(limit), headers={"Authorization":token})
        messages = json.loads(response.text) #Getting messages in channel
        if response.status_code != 200: #Checking if we have access to channel
            continue
        for i in range(len(messages)):
            message = messages[i]
            try:
                content = message['content']
                bot = message['author']['bot']
                participated = message['reactions'][0]['me']
                msgid = message['id']
                for f in range(len(message['reactions'])):
                    reaction = message['reactions'][f]['emoji']['name'] #Get reactions
                    if participated == False and reaction == '🎉' or reaction == '🎁':
                        requests.put(baseurl  + "/channels/" + str(channelid) + "/messages/" + str(msgid) + "/reactions/" + str(reaction) + "/@me", headers={"Authorization":token})
            except KeyError:
                pass
    print('(' + str(x+1) + '/' + str(len(servers)) + ') ' + servername + ' complete.')
    print()
end = time.time()
seconds = int(end - start)
minutes = int(seconds / 60)
print('Finished task in ' + str(minutes) + ' minutes.')
