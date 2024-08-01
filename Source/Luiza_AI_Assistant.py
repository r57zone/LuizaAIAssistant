import urllib.request, urllib.parse, requests, json, time, random
import xml.etree.ElementTree as ET
from datetime import datetime
import openai
import os, configparser
from pathlib import Path
import locale

# pip install openai
# pip install requests[socks] (for proxy / для прокси)

groq_api_key = '' 
proxy = '';

def HTTPGet(Url):
    try:
        Request = urllib.request.Request(Url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;)'})
        Response = urllib.request.urlopen(Request)
        Source=Response.read()
    except:
        Source = ''
    return Source
    
def GroqResponce(messages):
    if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
    
    headers = {
        'Authorization': 'Bearer ' + groq_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        "model": "llama-3.1-70b-versatile",  # Model name
        "messages": messages,
        "temperature": 0.5  # Desired temperature
    }

    try:
        if proxy:
            response = requests.post('https://api.groq.com/openai/v1/chat/completions', json=data, headers=headers, proxies=proxies)
        else:
            response = requests.post('https://api.groq.com/openai/v1/chat/completions', json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message_content = response_data['choices'][0]['message']['content']
                #print(message_content)
                return message_content
            else:
                #print('No choices in the response.')
                return ''
        else:
            #print('Failed to fetch data:', response.status_code)
            #print(response.text)
            return ''
    except Exception as e:
        print('An error occurred:', e)
        return ''
        
def GPTResponce(messages):
    try:
        response = openai.ChatCompletion.create(model='gpt-4', messages=messages)
        #return response.choices[0].text.strip()
        #print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']
    except:
        return ''
        
def AIResponce(messages, aiProvider):
    if aiProvider == 0:
        return GPTResponce(messages)
    elif aiProvider == 1:
        return GroqResponce(messages)
    
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
        self.name = ''
        self.completed = 0
        self.hours = 0
        self.minutes = 0
        self.answer_without_ai = ''
        self.ai_request = ''
        self.add_promt_next_user_msg = ''
        self.pics = []
        
    def setTime(self, time):
        if time != 'X':
            split_time = time.split(':')
            if split_time[0] != 'X': 
                self.hours = int(split_time[0])
            else:
                self.hours = random.randint(0, 23)
                
            if split_time[1] != 'X': 
                self.minutes = int(split_time[1])
            else:
               self.minutes = random.randint(0, 59)
        else:
            self.hours = random.randint(0, 23)
            self.minutes = random.randint(0, 59)
            
    def randTime(self, values):
        if 'RANDOM-SMALL-MINUTES' in values:
            self.minutes = max(0, min(59, self.minutes + random.randint(-15, 15)))
        if 'RANDOM-MIDDLE-MINUTES' in values:
            self.minutes = max(0, min(59, self.minutes + random.randint(-30, 30)))
        if 'RANDOM-VERYSMALL-HOUR' in values:
            self.hours = max(0, min(23, self.hours + random.randint(-1, 1)))
        if 'RANDOM-SMALL-HOUR' in values:
            self.hours = max(0, min(23, self.hours + random.randint(-2, 2)))
        if 'RANDOM-MEDIUM-SMALL-HOUR' in values:
            self.hours = max(0, min(23, self.hours + random.randint(-3, 3)))
        if 'RANDOM-MEDIUM-HOUR' in values:
            self.hours = max(0, min(23, self.hours + random.randint(-6, 6)))
            
def loadTriggers(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    triggers = []

    for trigger_elem in root.findall('trigger'):
        # Number of duplicates / Количество повторений
        count = int(trigger_elem.get('count', '1'))  # По умолчанию 1, если атрибут отсутствует

        # Add the trigger the required number of times / Добавляем триггер нужное количество раз
        for _ in range(count):
            trigger = Trigger()
            trigger.name = trigger_elem.get('name', '')
            trigger.ai_request = trigger_elem.find('ai_request').text
            
            # Promt / Промт
            add_promt_item = trigger_elem.find('add_promt')
            if add_promt_item is not None and add_promt_item.text:
                trigger.add_promt_next_user_msg = add_promt_item.text
            
            # The answer without AI / Ответ без AI
            answer_without_ai_elem = trigger_elem.find('answer_without_ai')
            if answer_without_ai_elem is not None and answer_without_ai_elem.text:
                trigger.answer_without_ai = answer_without_ai_elem.text
            
            # Images / Изображения
            trigger.pics = loadFileList(trigger_elem.find('pics').text)
            
            # Time
            time_elem = trigger_elem.find('time')
            if time_elem is not None and time_elem.text:
                trigger.setTime(time_elem.text)
            else:
                trigger.setTime('X:X')
            
            # Attributes of randomness / Атрибуты случайности
            random_time_elem = trigger_elem.find('random_time')
            if random_time_elem is not None and random_time_elem.text:
                trigger.randTime(random_time_elem.text)
            triggers.append(trigger)
            
    return triggers
    
def saveDateTriggers(triggers):
    with open('Setup/DateTriggers.txt', 'w') as file:
        Str = ''
        for trigger in triggers:
            Str += str(trigger.completed) + ';'
        file.write(Str + '\n')
        
def loadDateTriggers(triggers):
    with open('Setup/DateTriggers.txt', 'r') as file:
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
    userLang = locale.getlocale()[0][:2]
    
    config = configparser.ConfigParser()
    configFile = Path('Setup/Setup.ini')
    config.read(configFile)
    # 0 - OpenAI, 1 - Groq (Llama 3)
    aiProvider = int(config.get('Main', 'AIProvier'))
    
    telegramToken = config.get('Main', 'TelegramToken')
    masterUser = config.get('Main', 'TelegramMasterUser')
    masterChatId = int(config.get('Main', 'TelegramMasterChatID'))
    
    global groq_api_key, proxy
    groq_api_key = config.get('Main', 'GroqAPIKey')
    openai.api_key = config.get('Main', 'OpenAPIKey')
    proxy = config.get('Main', 'Proxy')
    SleepTimeOut = int(config.get('Main', 'SleepTimeOut'))
    
    if os.path.exists('Setup/AssistantDescription' + userLang + '.txt'):
        assistantDescription = readFile('Setup/AssistantDescription' + userLang + '.txt').replace('\n', '')
    else:
        assistantDescription = readFile('Setup/AssistantDescriptionEn.txt').replace('\n', '')
    
    if os.path.exists('Setup/UserDescription' + userLang + '.txt'):
        userDescription = readFile('Setup/UserDescription' + userLang + '.txt').replace('\n', '')
    else:
        userDescription = readFile('Setup/UserDescriptionEn.txt').replace('\n', '')
    
    if os.path.exists('Setup/UserNames' + userLang + '.txt'):
        userNames = loadFileList('Setup/UserNames' + userLang + '.txt')
    else:
        userNames = loadFileList('Setup/UserNamesEn.txt')
    
    showMsgs = int(config.get('Main', 'ShowMessages'))
    debugMode = int(config.get('Main', 'DebugMode'))
    sendImgs = int(config.get('Main', 'SendImages'))
    
    accessErrorMsg = 'Hi 🤗, I''m sorry but I only communicate with my master user 😍 @' + masterUser + ' 👉👈'
    workTestMsg = 'Everything is ok, I''m here 😘'
    if userLang == 'Ru':
        accessErrorMsg = 'Приветики 🤗, я сожалею, но я общаюсь только с моим мастер-пользователем 😍 @' + masterUser + ' 👉👈'
        workTestMsg = 'Всё ок, я тут 😘'
    
    ################################################
    
    updateId = 0 # last message being processed / последнее сообщение в обработке
    chatId = 0
    
    messages = []
    messages.append({'role': 'assistant', 'content': assistantDescription.strip('\t\n\r')})
    messages.append({'role': 'user', 'content': userDescription.strip('\t\n\r')})
    messageCount = 0
    messageBufferCount = 10
    addPromtToNextUserMsg = ''
    
    # Triggers / Триггеры
    if os.path.exists('Setup/Triggers' + userLang + '.xml'):
        triggers = loadTriggers('Setup/Triggers' + userLang + '.xml')
    else:
        triggers = loadTriggers('Setup/TriggersEn.xml')
          
    # Adding a name and adding randomness to the time / Добавляем имя и добавляем случайность ко времени
    for trigger in triggers:
        trigger.answer_without_ai = trigger.answer_without_ai.replace('%name%', randomPhrase(userNames))
    
    loadDateTriggers(triggers)
    
    # Checking triggers / Проверка триггеров
    if False:
        for trigger in triggers:
            print(trigger.name, '-', str(trigger.hours) + ':' + str(trigger.minutes))
            print('AI request:', trigger.ai_request.split(';')[0])
            print('Answer without AI:', trigger.answer_without_ai.split(';')[0])
            print('Pics:', trigger.pics.split(';')[0])
            print()
        input()
    
    # Update updateId
    try:
        source = HTTPGet('https://api.telegram.org/bot' + telegramToken + '/getUpdates')
        data = json.loads(source)
        updateId = data['result'][0]['update_id']
    except:
        pass
        
    def SendMsg(Msg):
        HTTPGet('https://api.telegram.org/bot' + telegramToken + '/sendmessage?chat_id=' + str(chatId) + '&text=' + urllib.parse.quote(Msg) + '&parse_mode=markdown')
        
    def SendPic(Link):
        HTTPGet('https://api.telegram.org/bot' + telegramToken + '/sendphoto?chat_id=' + str(chatId) + '&photo=' + urllib.parse.quote(Link))
        
    def SendPicAnim(Link):
        HTTPGet('https://api.telegram.org/bot' + telegramToken + '/sendanimation?chat_id=' + str(chatId) + '&animation=' + urllib.parse.quote(Link))
        
    print('Luiza AI Assistant')
    
    while True:
        time.sleep(SleepTimeOut)
        try:
            source = HTTPGet('https://api.telegram.org/bot' + telegramToken + '/getUpdates?offset=' + str(updateId))# + '&timeout=5')
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

                if showMsgs == 1:
                    print(str(chatId) + ', ', username + ', ' + currentDateTime.strftime('%H:%M') + ': ' + command)

                if username != masterUser and chatId != masterChatId:
                    SendMsg(accessErrorMsg)
                    continue
                    
                # Answering simple commands / Отвечаем на простые команды
                if (command == 'work'):
                    standardCommand = True
                    # SendPicAnim('https://i.imgur.com/UW2gs2C.mp4')
                    SendMsg(workTestMsg)
                
                if standardCommand == False:
                    if addPromtToNextUserMsg != '':
                        command += addPromtToNextUserMsg
                        addPromtToNextUserMsg = ''
                    
                    messages.append({'role': 'user', 'content': command})
                    if len(messages) == messageBufferCount:
                        messages.pop(2)
          
                    msg = AIResponce(messages, aiProvider)
                    if msg != '':
                        SendMsg(msg)
                    elif debugMode == 1:
                        print('Error receiving data from AI')

                #print(messages)
              
            for trigger in triggers:
                if currentDateTime.day != trigger.completed: # Раз в день
                    #print('day trigger ' + trigger.ai_request)
                    #print('day trigger ' + str(trigger.hours) + ':' + str(trigger.minutes), currentDateTime.hour)
                    if ((currentDateTime.hour > trigger.hours) or (currentDateTime.hour == trigger.hours and currentDateTime.minute >= trigger.minutes)):
                        
                        if showMsgs == 1:
                            print('Trigger done: ' + trigger.ai_request)
                        trigger.completed = currentDateTime.day
                        saveDateTriggers(triggers)
                        
                        # Add predict to the next message / Добавляем predict на следующее сообщение
                        if trigger.add_promt_next_user_msg != '':
                            addPromtToNextUserMsg = trigger.add_promt_next_user_msg
                        
                        # If no messages have been received, then write down and update chatId to masterChatId so that you know where to send messages
                        # Если сообщений не поступало, то записываем обновляем chatId на masterChatId, чтобы знать куда отправлять сообщения
                        chatId = masterChatId
                        
                        messages.append({'role': 'user', 'content': randomPhrase(trigger.ai_request)})
                        
                        if debugMode == 1:
                            print(messages[1:])
                        msg = AIResponce(messages, aiProvider)
                        
                        if msg == '' and trigger.answer_without_ai != '':
                            msg = randomPhrase(trigger.answer_without_ai)
                        
                        if sendImgs == 1 and trigger.pics != '':
                            SendPicAnim(randomPhrase(trigger.pics))
                          
                        # Some triggers may not have answer_without_ai / Некоторые триггеры могут быть без answer_without_ai
                        if msg != '':
                            SendMsg(msg)

        except:
            if debugMode == 1:
                print('Update fail')
            #pass

if __name__=='__main__':
	main()
