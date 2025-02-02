import json
import socket
from datetime import datetime, timedelta
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

def get_question_answa(question): #searches for the question and gets the answer from quiz.json
    print(f"Searching: {question}")
    answer = qa_data.get(question.lower())
    if answer:
        print(f"found!!!: {answer}")
    else:
        print("something went wrong...")
    return answer or "miyav"

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG :tmi.twitch.tv\n".encode('utf-8')) #Prevents twitch autodisconnecting if you dont pong back

    elif len(resp) > 0:
        parts = resp.split(':', 2)
        if len(parts) > 2:
            user_info = parts[1].split('!')
            username = user_info[0].strip()
            message = parts[2].strip()
            print(f"question from {username}: {message}")
            if "ACTION" in message: #this is to remove the characters that are added by using /me 
                oppenheimer = message.split("ACTION", 1)[0]
                message = message.split("ACTION", 1)[1]
                message = message.split(oppenheimer, 1)[0]


                if username.lower() == 'PotatBotat'.lower() and required_ending in message: #this is done so it only searches for the quiz answer if the sentence sent by the bot ends with the required ending
                        def sendmessagenow():
                            sock.send(f"PRIVMSG {channel} :{final_answer}\n".encode('utf-8'))
                        print(message)
                        message = message.replace(" @フェムシャーク ", "").lower() #removes the username to correctly read from quiz.json
                        print(f"final message{message}")

                        answer = get_question_answa(message)
                        final_answer = (f"#a {answer}")
                        timer = threading.Timer(8.0, sendmessagenow) #done because eventapi is sometimes slow and if you answer too fast it wont recognize it, you could lower this but 8 seconds is pretty alright
                        timer.start()
                        
