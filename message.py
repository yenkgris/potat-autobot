import requests
import time
import traceback
import json

potatoReadyAt = 0
stealReadyAt = 0
cdrReadyAt = 0
statuscheck = True
currentPotatoData = False
switchedChannel = False
broadcasterId = 95676405
twitchHeaders = {
    "Authorization": "Bearer 81bnxff1j1omghah4u2dchrltatriu",
    "Client-ID": "im7plrnwhiw13n04bugjq6ndn9mn5e",
}
nextUpdateMessage = time.time() + 3600

with open('quiz.json') as file:
    qa_data = json.load(file)

potatHeaders = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NzI3OTY3NSIsImxvZ2luIjoiZXNzaXR5XyIsIm5hbWUiOiLjg5Xjgqfjg6Djgrfjg6Pjg7zjgq8iLCJzdHZfaWQiOiI2MjkwZjFmN2EwNTU5NTJmZGMzYmI5OWIiLCJpc19jaGFubmVsIjpmYWxzZSwiaWF0IjoxNzI0NTA1OTAxLCJleHAiOjE3NDAzMTcxMDF9.wVA_Ex8ajw9RAAYzA2mpeC5rIyE5tgmp-7gaa9wFCW4",
    "Content-Type": "application/json",
}

def getPotatoInfo():
    response = requests.get("https://api.potat.app/users/essity_")
    if response.status_code == 200:
        potatoData = response.json()['data'][0]['potatoes']
        if type(potatoData['cdr']['readyAt']) == None:
            potatoData['cdr']['readyAt'] = 1 
        potatoDataList =  [potatoData['potato']['ready'], potatoData['steal']['ready'], potatoData['cdr']['ready'], potatoData['count'], potatoData['rank'], potatoData['prestige'], potatoData['quiz']['ready'], potatoData['quiz']['completed'], potatoData['potato']['usage'], potatoData['trample']['ready']]
        dataList = []
        for data in potatoDataList:
            if data == None:
                dataList.append(1)
            else:
                dataList.append(int(data))
        return dataList
    else:
        print(response.text)

print("CertifiedForsenLevelMomentSignedByDonaldTrumpHimself")

def sendTwitchMessage(message):
    literalMessage = message
    try:
        message = message.replace("#", "%23")
        response = requests.post(f"https://api.twitch.tv/helix/chat/messages?broadcaster_id={broadcasterId}&sender_id=767279675&message={message}", headers=twitchHeaders)
        if response.status_code == 200:
            if response.json()['data'][0]['is_sent']:
                print(f"WOW!!! {literalMessage}!")
            else:
                print("Failed to send message ): ")
                print("data:")
                print(response.json())
        else:
            print(response.text)
    except TimeoutError:
        print(f"Maybe send message {literalMessage}, reason: TimeoutError")

sendTwitchMessage("CertifiedForsenLevelMomentSignedByDonaldTrumpHimself")  

potatoInfo = getPotatoInfo()
farmSize = potatoInfo[4]
lastPotatoes = potatoInfo[3]

farmSizes = {
    1: 1000,
    2: 5000,
    3: 10000,
    4: 25000,
    5: 50000,
    6: potatoInfo[5]*20000 + 100000
}
rankupCost = farmSizes[farmSize]

while True:
    try:
        currentTime = time.time()*1000 - 15

        if not currentPotatoData:
            potatoInfo = getPotatoInfo()

            potatoready = potatoInfo[0]

            stealready = potatoInfo[1]

            cdrready = potatoInfo[2]

            potatoAmount = potatoInfo[3]

            quizready = potatoInfo[6]

            quizcompleted = potatoInfo [7]

            potatousage = potatoInfo[8]

            trampleready = potatoInfo[9]

            currentPotatoData = True

        if potatoAmount > rankupCost and farmSize == 6:
            sendTwitchMessage("#prestige")
            farmSize = 1
            rankupCost = farmSizes[farmSize]
            currentPotatoData = False
        elif potatoAmount > rankupCost:
            sendTwitchMessage("#rankup")
            farmSize += 1
            rankupCost = farmSizes[farmSize]
            currentPotatoData = False

        if  potatoready == True:
            sendTwitchMessage("#p")
            time.sleep(1)
            sendTwitchMessage("#shop buy fertilizer")
            print(f"Farmer! {potatousage}")
            currentPotatoData = False
            statuscheck = True


        if trampleready == True:
            sendTwitchMessage("#burn")
            time.sleep(1)
            sendTwitchMessage("#shop buy guard")
            currentPotatoData = False
            statuscheck = True


        if  stealready == True: 
            sendTwitchMessage("#steal")
            time.sleep(1)
            currentPotatoData = False
            statuscheck = True

        if  cdrready == True:
            time.sleep(3)
            sendTwitchMessage("#c")
            time.sleep(1)
            sendTwitchMessage("#p")
            time.sleep(1)
            sendTwitchMessage("#steal")
            time.sleep(1)
            sendTwitchMessage("#shop buy cdr")
            currentPotatoData = False
            statuscheck = True

        if  quizready == True:
            sendTwitchMessage("#quiz")  
            time.sleep(1)
            print(f"Smart!!! {quizcompleted}")
            time.sleep(1)
            sendTwitchMessage("#shop buy quiz")
            currentPotatoData = False
            statuscheck = True
            
        if time.time() > nextUpdateMessage:
            nextUpdateMessage = time.time() + 3600
            currentPotatoes = potatoAmount
            potatoDifference = currentPotatoes - lastPotatoes
            if potatoDifference > 0:
                potatoDifference = f" %2B{str(potatoDifference)}" 
            message = f"{currentPotatoes} ({potatoDifference})"
            sendTwitchMessage(message)
            lastPotatoes = currentPotatoes
        
        if stealready == False and potatoready == False and cdrready == False and quizready == False and statuscheck == True:
            sendTwitchMessage("#status essity_")
            currentPotatoData = False
            statuscheck = False

        currentPotatoData = False    
        time.sleep(1)

    except Exception as e:
        traceback.print_exc()
        time.sleep(10)
