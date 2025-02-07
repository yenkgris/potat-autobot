import json
import socket
import threading

with open('quiz.json') as file: #loads quiz.json with the quizes and their respective answer
    qa_data = json.load(file)

server = 'irc.chat.twitch.tv'
port = 6667
nickname = '{YOURNICKNAME}'
token = 'oauth:{YOURTOKENHERE}'
channel = '#{YOURCHANNELHERE}'
required_ending = "(You have five minutes to answer correctly, time starts now!)"
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

def get_question_answer(question): #searches for the question and gets the answer from quiz.json
    print(f"Searching: {question}")
    answer = qa_data.get(question.lower())
    if answer:
        print(f"found!!!: {answer}")
    else:
        print("something went wrong...")
    return answer or "miyav"

def clear_message(message): #Removes  characters added by /me from the message 
    parts = message.split("ACTION ", 1)
    if len(parts) > 1:
        return parts[1].split(parts[0], 1)[0]
    return message

def send_message(): #sends the answer after getting it from quiz.json 
    sock.send(f"PRIVMSG {channel} :{final_answer}\n".encode('utf-8'))
    
try:
    while True:
     resp = sock.recv(2048).decode('utf-8')

     if resp.startswith('PING'):
        sock.send("PONG :tmi.twitch.tv\n".encode('utf-8')) #used to prevent disconnection
 
     elif len(resp) > 0:
        parts = resp.split(':', 2)
        if len(parts) > 2: #splits the message 
            
            user_info = parts[1].split('!')
            username = user_info[0].strip()
            message = parts[2].strip()

            print(f"Question from {username}: {message}")

            if "ACTION" in message:
                 message = clear_message(message)
                 if username.lower() == 'PotatBotat'.lower() and required_ending in message:
                     
                    message = message.replace(" @{YOURUSER} ", "").lower() #Added this because I have a japanese display name and it messed up the question recognition, this also works with normal usernames
                    answer = get_question_answer(message)
                     
                    final_answer = (f"#a {answer}")
                     
                    timer = threading.Timer(4.0, send_message) # Added a cooldown so there's enough time for PotatoBotat's cooldown to be up and read the answer
                     
                    timer.start()
except KeyboardInterrupt:
       print("script killed")
finally:
       sock.close()
       print("socket closed")                    
                        
