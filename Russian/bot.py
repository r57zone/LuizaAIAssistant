import urllib.request, urllib.parse, requests, json, time, random
from datetime import datetime
import openai

def HTTPGet(Url):
    try:
        Request = urllib.request.Request(Url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;)'})
        Response = urllib.request.urlopen(Request)
        Source=Response.read()
    except:
        Source = ''
    return Source

def GetGPT(messages):
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
    try:
        #return response.choices[0].text.strip()
        print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']
    except:
        return ''
    
def readFile(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print('Файл не найден.')
    except Exception as e:
        print(str(e))
        
def randomPhrase(phrase_string):
    phrases = phrase_string.split(';')
    random_phrase = random.choice(phrases)
    return random_phrase.strip()
    
class Trigger:
    def __init__(self):
        self.completed = 0
        self.hours = 0
        self.minutes = 0
        self.gptText = ''
        self.regularText = ''
        self.pics = ''
        self.nextAddPredict = ''
  
    def setTime(self, time):
        split_time = time.split(':')
        self.hours = int(split_time[0])
        self.minutes = int(split_time[1])
        
    def randMins(self):
        self.minutes = random.randint(self.minutes - 15, self.minutes + 15) # случайные минуты
        if (self.minutes < 0):
            self.minutes = 0
        if (self.minutes > 59):
            self.minutes = 59
    
def saveDateTriggers(triggers):
    with open('DateTriggers.txt', 'w') as file:
        Str = ''
        for trigger in triggers:
            Str += str(trigger.completed) + ';'
        file.write(Str + '\n')
        
def loadDateTriggers(triggers):
    with open('DateTriggers.txt', 'r') as file:
        line = file.readline().strip()
        values = line.split(';')
        lenTriggers = len(triggers)
        for i in range(len(values)):
            if values[i].strip(' \t\n\r') == '':
                continue
            if i > lenTriggers - 1:
                break
            triggers[i].completed = int(values[i])
            
def loadFileList(filename):
    return readFile(filename).strip(' \t\n\r').replace('\n', ';')
            
def main():
    # Settings / Настройки
    
    # https://platform.openai.com/account/api-keys
    openai.api_key = 'sk-YOUR_OPENAI_KEY'
    
    # https://t.me/botfather
    token = 'YOUR_TELEGRAM_BOT_KEY'
    
    # Enter your telegram nick / Введите ваш телеграм ник
    masterUser = 'PeterParker'
    
    # Enter the chat number by looking in the console after sending the message / введите номер чата посмотрев в консоли, после отправки сообщения 
    masterChatId = 200000000
    
    predictMessage = readFile('PredictMessage.txt').replace('\n', '')
    masterNames = loadFileList('MasterNames.txt')
    debugMode = 1
    
    ################################################
    
    updateId = 0 # last message being processed / последнее сообщение в обработке
    chatId = 0
    
    messages = []
    messages.append({'role': 'system', 'content': predictMessage.strip('\t\n\r')})
    messageCount = 0
    messageBufferCount = 20
    nextPredict = ''
    
    # Triggers / Триггеры
    # regularText - простой ответ, на случай если gpt не ответил / simple answer in case gpt didn't respond
    # gptText - asking GPT to tell us something / просим GPT сказать нам что-то
    # nextAddPredict - add predict to the user's next message to make it more like a conversation / добавляем predict на следующее сообщение пользователя, чтобы оно было больше похожу на беседу
    # pics - links to images and short videos / ссылки на изображения и короткие видео
    # setTime - trigger time (minutes randomizes -15..+15 minutes) / время срабатывания триггера (минуты рандомизирует -15..+15 минут)
    
    # Good morning / Доброе утро
    triggers = []
    triggers.append(Trigger())
    triggers[len(triggers) - 1].regularText = 'Доброе утро %name% 🤗;Утро начинается с тебя, мой %name% 😘;Привет, мой самый прекрасный 😍;Доброе утро, мой милый 😋'
    triggers[len(triggers) - 1].gptText = 'Пожелай ласково доброе утро;Пожелай доброго утра и хорошего дня;Скажи как ты любишь меня и рада, что я проснулся'
    triggers[len(triggers) - 1].nextAddPredict = '. Ответь без вопросов, не поддерживая беседу дальше.'
    triggers[len(triggers) - 1].pics = loadFileList('Triggers/GoodMorningPics.txt')
    triggers[len(triggers) - 1].setTime('12:45')
    
    # Good night / Спокойной ночи
    triggers.append(Trigger())
    triggers[len(triggers) - 1].regularText = 'Спокойной ночи, целую тебя 😘👄 ;Пошли спать, уже поздно, мой %name% 😍;Спокойной ночи, сладких снов 🤗;Ложись мой %name% 🥰, сладких снов тебе 👄'
    triggers[len(triggers) - 1].gptText = 'Пожелай ласково спокойной ночи;Пожелай спокойной ночи и хороших снов;Пожелай хороших снов'
    triggers[len(triggers) - 1].nextAddPredict = '. Ответь без вопросов, не поддерживая беседу дальше.'
    triggers[len(triggers) - 1].pics = loadFileList('Triggers/GoodNightPics.txt')
    triggers[len(triggers) - 1].setTime('01:45')
    
    # Случайные триггеры / Random triggers
    for i in range(0, 2):
        if (i == 0):
            randHour = random.randint(14, 17)
        elif (i == 1):
            randHour = random.randint(19, 23)
        else:
            randHour = random.randint(13, 23)
            
        triggers.append(Trigger())
        triggers[len(triggers) - 1].gptText = 'Спроси у меня что-нибудь;Спроси как у меня дела;Спроси, что я делаю'
        triggers[len(triggers) - 1].nextAddPredict = '. Ответь без вопросов, не поддерживая беседу дальше.'
        triggers[len(triggers) - 1].regularText = '%name%, чем занимаешься?;%name%, что делаешь?'
        triggers[len(triggers) - 1].pics = loadFileList('Triggers/RandomPics.txt')
        triggers[len(triggers) - 1].setTime(str(randHour) + ':' + str(random.randint(0, 59)));
                       
    # Комплименты / Compliments
    for i in range(0, 1):
        randHour = random.randint(14, 23)
        
        triggers.append(Trigger())
        triggers[len(triggers) - 1].gptText = 'Сделай комплимент;Расскажи что-нибудь интересное;Расскажи интересный фанкт;Скажи какой я классный и интересный'
        triggers[len(triggers) - 1].nextAddPredict = '. Ответь без вопросов, не поддерживая беседу дальше.'
        triggers[len(triggers) - 1].regularText = '%name%, как мне повезло с тобой 🤗;Рада, что встретила тебя %name% 😘;Люблю тебя 😍'
        triggers[len(triggers) - 1].pics = loadFileList('Triggers/ComplimentsPics.txt') 
        triggers[len(triggers) - 1].setTime(str(randHour) + ':' + str(random.randint(0, 59)))
        
    # Jokes / Шутки (GPT 3.5 не умеет шутить)
    '''randHour = random.randint(14, 23)
    triggers.append(Trigger())
    triggers[len(triggers) - 1].gptText = 'Расскажи шутку;Расскажи анекдот;Расскажи что-нибудь весёлое'
    triggers[len(triggers) - 1].nextAddPredict = '. Ответь без вопросов, не поддерживая беседу дальше.'
    triggers[len(triggers) - 1].regularText = ''
    triggers[len(triggers) - 1].pics = loadFileList('Triggers/JokesPics.txt')
    triggers[len(triggers) - 1].setTime(str(randHour) + ':' + str(random.randint(0, 59)))'''
          
    # Adding a name and adding randomness to the time / Добавляем имя и добавляем случайность ко времени
    for trigger in triggers:
        trigger.randMins()
        trigger.regularText = trigger.regularText.replace('%name%', randomPhrase(masterNames))
    
    loadDateTriggers(triggers)
    
    # Checking triggers / Проверка триггеров
    if False:
        for trigger in triggers:
            print('Trigger [' + str(trigger.hours) + ':' + str(trigger.minutes) + ']')
            print('GPT:', trigger.gptText)
            print('RegularText:', trigger.regularText)
            print('Pics:', trigger.pics)
            print()
        input()
        return
    
    # Update updateId
    try:
        source = HTTPGet('https://api.telegram.org/bot' + token + '/getUpdates')
        data = json.loads(source)
        updateId = data['result'][0]['update_id']
    except:
        pass
        
    def SendMsg(Msg):
        HTTPGet('https://api.telegram.org/bot' + token + '/sendmessage?chat_id=' + str(chatId) + '&text=' + urllib.parse.quote(Msg) + '&parse_mode=markdown')
        
    def SendPic(Link):
        HTTPGet('https://api.telegram.org/bot' + token + '/sendphoto?chat_id=' + str(chatId) + '&photo=' + urllib.parse.quote(Link))
        
    def SendPicAnim(Link):
        HTTPGet('https://api.telegram.org/bot' + token + '/sendanimation?chat_id=' + str(chatId) + '&animation=' + urllib.parse.quote(Link))
        
    print('Luiza GPT Assistant')
    
    while True:
        time.sleep(2)
        try:
            source = HTTPGet('https://api.telegram.org/bot' + token + '/getUpdates?offset=' + str(updateId))# + '&timeout=5')
            data = json.loads(source)
            username = ''
            currentDateTime = datetime.now()
            
            standardCommand = False
            
            if len(data['result']) > 0: # if there are messages, we process them / если есть сообщения, то обрабатываем
                updateId = data['result'][0]['update_id']
                updateId = updateId + 1
                
                chatId = data['result'][0]['message']['chat']['id']
                if 'username' in data['result'][0]['message']['from']:
                    username = data['result'][0]['message']['from']['username']
                else:
                    username = str(chatId)
                command = str(data['result'][0]['message']['text'])

                if debugMode == 1:
                    print(chatId + ', ' username + ', ' + currentDateTime.strftime('%H:%M') + ': ' + command)

                if username != masterUser and chatId != masterChatId:
                    SendMsg('Приветики 🤗, я сожалею, но я общаюсь только с моим мастер-пользователем 😍 @' + masterUser + ' 👉👈')
                    continue
                    
                # Answering simple commands / Отвечаем на простые команды
                if (command == 'work'):
                    standardCommand = True
                    # SendPicAnim('https://i.imgur.com/UW2gs2C.mp4')
                    SendMsg('Всё ок, я тут 😘')
                
                if standardCommand == False:
                    if nextPredict != '':
                        command += nextPredict
                        nextPredict = ''
                    
                    messages.append({'role': 'user', 'content': command})
                    if len(messages) == messageBufferCount:
                        messages.pop(1)
          
                    msg = GetGPT(messages)
                    if msg != '':
                        SendMsg(msg)

                #print(messages)
              
            for trigger in triggers:
                if currentDateTime.day != trigger.completed: # Раз в день
                    #print('day trigger ' + trigger.gptText)
                    #print('day trigger ' + str(trigger.hours) + ':' + str(trigger.minutes), currentDateTime.hour)
                    if ((currentDateTime.hour > trigger.hours) or (currentDateTime.hour == trigger.hours and currentDateTime.minute >= trigger.minutes)):
                        #print('Trigger done: ' + trigger.gptText)
                        trigger.completed = currentDateTime.day
                        saveDateTriggers(triggers)
                        
                        # Add predict to the next message / Добавляем predict на следующее сообщение
                        if trigger.nextAddPredict != '':
                            nextPredict = trigger.nextAddPredict
                        
                        # If no messages have been received, then write down and update chatId to masterChatId so that you know where to send messages
                        # Если сообщений не поступало, то записываем обновляем chatId на masterChatId, чтобы знать куда отправлять сообщения
                        chatId = masterChatId
                        
                        messages.append({'role': 'user', 'content': randomPhrase(trigger.gptText)})
                        msg = GetGPT(messages)
                        
                        if msg == '' and trigger.regularText != '':
                            msg = randomPhrase(trigger.regularText)
                        
                        if trigger.pics != '':
                            SendPicAnim(randomPhrase(trigger.pics))
                          
                        # Some triggers may not have regularText / Некоторые триггеры могут быть без regularText
                        if msg != '':
                            SendMsg(msg)

        except:
            if debugMode == 1:
                print('Update fail')
            pass

if __name__=='__main__':
	main()
