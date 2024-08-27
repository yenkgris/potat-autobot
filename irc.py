import json
import socket
from datetime import datetime, timedelta
import re
import threading

with open('quiz.json') as file: #loads quiz.json with the quizes and their respective answer
    qa_data = json.load(file)

server = 'irc.chat.twitch.tv'
port = 6667
nickname = '{YOURNICKNAME}'
token = 'oauth:{YOURTOKENHERE}'
channel = '#{CHANNEL}'
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
        sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))

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

                if username.lower() == 'PotatBotat'.lower() and "Potato:" in message: #this is used to tell at which time will the commands go off cooldowns by using the #status command: message.py
                    def read_message(message): # pattern only recognizes words such as "Quiz:" and not "Shop-Quiz:" 
                          pattern = r"\b(?<!Shop-)(\w+): (\d+h and \d+m|\d+m and \d+s|\d+s)"
                          matches = re.findall(pattern, message)
                          print(f"Matches found: {matches}")  
                          return matches
                    
                    def read_message2(message): # pattern only recognizes words such as "Shop-Quiz:" and not "Quiz:" separated due to value lmit
                          pattern2 = r"(\w+-\w+): (\d+h and \d+m|\d+m and \d+s|\d+s)"
                          matches2 = re.findall(pattern2, message)
                          print(f"Shop matches found: {matches2}")
                          return matches2       
                          
                    def check_cooldown(cooldowns): #calculates at what time of day will any command found by the first pattern be available
                          current_time = datetime.now()
                          availability_times = {}
     
                          for command, cooldown in cooldowns:
                            time_parts = list(map(int, re.findall(r'\d+', cooldown)))
                            if len(time_parts) == 3:
                             hours, minutes, seconds = time_parts
                            elif len(time_parts) == 2:
                              hours = 0
                              minutes, seconds = time_parts
                            else:
                             hours = 0
                             minutes = 0
                             seconds = time_parts[0]
                            cooldown_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                            availability_time = current_time + cooldown_time
                            availability_times[command] = availability_time.strftime("%H:%M:%S")
                          return availability_times
                    
                    def check_cooldown2(cooldowns2): #calculates at what time of day will any command found by the second pattern be available
                          current_time = datetime.now()
                          availability_times2 = {}
     
                          for command, cooldown2 in cooldowns2:
                            time_parts = list(map(int, re.findall(r'\d+', cooldown2)))
                            if len(time_parts) == 3:
                             hours, minutes, seconds = time_parts
                            elif len(time_parts) == 2:
                              hours = 0
                              minutes, seconds = time_parts
                            else:
                             hours = 0
                             minutes = 0
                             seconds = time_parts[0]
                            cooldown_time2 = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                            availability_time2 = current_time + cooldown_time2
                            availability_times2[command] = availability_time2.strftime("%H:%M:%S")
                          return availability_times2
                     
                    cooldowns = read_message(message)
                    cooldowns2 = read_message2(message)
                    availability_times = check_cooldown(cooldowns)
                    availability_times2 = check_cooldown2(cooldowns2)
                    for command, time in availability_times.items(): #displays on the terminal the final result using the first pattern
                      print(f"{command} will be available at {time}")

                    for command2, time in availability_times2.items(): #displays on the terminal the final result using the second pattern
                     print(f"{command2} will be available at {time}")   

                    if required_ending in message: #this is done so it only searches for the quiz answer if the sentence sent by the bot ends with the required ending
                        def delay_message(): #to add a delay between the quiz command being triggered and the answer sent using threading.Timer
                            sock.send(f"PRIVMSG {channel} :{final_answer}\n".encode('utf-8'))

                        print(message)
                        message = message.replace(" @{YOURUSER} ", "").lower() #removes the username to correctly read from quiz.json
                        print(f"final message{message}")

                        answer = get_question_answa(message)
                        final_answer = (f"#a {answer}")
                        timer = threading.Timer(2.0, delay_message)
                        timer.start()

                    
