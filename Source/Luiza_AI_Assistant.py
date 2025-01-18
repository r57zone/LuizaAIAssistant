import urllib.request, urllib.parse, requests, json, time, random
import xml.etree.ElementTree as ET
from datetime import datetime
import openai
import os, configparser
from pathlib import Path
import locale

# pip install openai
# pip install requests[socks] (for proxy / для прокси)

GroqAPIKey = '' 
Proxy = '';
UserHistory = ''
AIHistory = ''
TokensSize = 0

def HTTPGet(Url):
    try:
        Request = urllib.request.Request(Url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;)'})
        Response = urllib.request.urlopen(Request)
        Source=Response.read()
    except:
        Source = ''
    return Source
    
def GroqResponce(messages):
    if Proxy:
            proxies = {
                'http': Proxy,
                'https': Proxy
            }
    
    headers = {
        'Authorization': 'Bearer ' + GroqAPIKey,
        'Content-Type': 'application/json'
    }
    data = {
        "model": "llama-3.3-70b-versatile",  # Model name
        "messages": messages,
        "temperature": 0.5  # Desired temperature
    }

    try:
        if Proxy:
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
        #print('An error occurred:', e)
        return 'AI provider returned an error.'
        
def GPTResponce(messages):
    try:
        response = openai.ChatCompletion.create(model='gpt-4', messages=messages)
        #return response.choices[0].text.strip()
        #print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']
    except:
        return 'AI provider returned an error.'
        
def AIResponse(AIProvider, messages):
    if AIProvider == 0:
        return GPTResponce(messages)
    elif AIProvider == 1:
        return GroqResponce(messages)
        
def SaveHistory():
    #print('Save history')
    global UserHistory
    global AIHistory
    with open('Setup/UserHistory.txt', 'w', encoding='utf-8') as file:
        file.write(UserHistory)
    with open('Setup/AIHistory.txt', 'w', encoding='utf-8') as file:
        file.write(AIHistory)
        
def ImportanceCheck(AIProvider, prompt, messages, message, IsUser):
    global UserHistory, AIHistory, TokensSize
    
    ClearMessages = [
        {'role': 'user', 'content': prompt},
        {'role': 'user', 'content': json.dumps(message, ensure_ascii=False)}
    ]
    # ClearMessages = Messages + [{'role': 'user', 'content': Prompt}]
    
    response_content = AIResponse(AIProvider, ClearMessages)
    #print('Importance Request / Запрос важности:', message)
    #print(response_content)
    messages_len = sum(len(msg['content']) for msg in messages)
    #print(f"Message length / Длина сообщений: {messages_len}")
    
    current_date = datetime.now()
    
    try:
        if response_content and response_content.startswith('True: '):
            if IsUser:
                UserHistory += current_date.strftime('%d.%m.%Y') + ': ' + response_content[6:] + '\n'
                
                # Delete old lines if limit is exceeded / Удаляем старые строки, если превышен лимит
                while len(UserHistory) + messages_len >= TokensSize - 50:
                    if '\n' in UserHistory:
                        UserHistory = UserHistory.split('\n', 1)[1]
                    else:
                        UserHistory = ''
                        break
            else:  # Is AI
                AIHistory += current_date.strftime('%d.%m.%Y') + ': ' + response_content[6:] + '\n'
                
                # Delete old lines if limit is exceeded / Удаляем старые строки, если превышен лимит
                while len(AIHistory) + messages_len >= TokensSize - 50:
                    if '\n' in AIHistory:
                        AIHistory = AIHistory.split('\n', 1)[1]
                    else:
                        AIHistory = ''
                        break
            
            SaveHistory()
            
    except json.JSONDecodeError as e:
        print(f"Error JSONDecodeError: {e}")
    except Exception as e:
        print(f"Error: {e}")
        
def ResponseNeed(AIProvider, Messages, Prompt):
    ClearMessages = Messages + [{'role': 'user', 'content': Prompt}]
    ResponseContent = AIResponse(AIProvider, ClearMessages)
    try:
        if ResponseContent:
            if 'True' in ResponseContent:
                return True
            else:
                return False
        else:
            return True
    except:
        return True
    
def ReadFile(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        #print('File not found:', filename)
        return ''
    except Exception as e:
        #print(str(e))
        return ''
        
def LoadFileList(filename):
    return ReadFile(filename).strip(' \t\n\r').replace('\n', ';')
        
def RandomPhrase(phrase_string):
    phrases = phrase_string.split(';')
    random_phrase = random.choice(phrases)
    return random_phrase.strip()
    
class Trigger:
    def __init__(self):
        self.Name = ''
        self.Activate = True
        self.LastShownDay = 0
        self.Hours = 0
        self.Minutes = 0
        self.AnswerWithoutAI = ''
        self.AIRequest = ''
        self.AddPromptNextUserMsg = ''
        self.Pics = []
        
    def setTime(self, time):
        if time != 'X':
            split_time = time.split(':')
            if split_time[0] != 'X': 
                self.Hours = int(split_time[0])
            else:
                self.Hours = random.randint(0, 23)
                
            if split_time[1] != 'X': 
                self.Minutes = int(split_time[1])
            else:
               self.Minutes = random.randint(0, 59)
        else:
            self.Hours = random.randint(0, 23)
            self.Minutes = random.randint(0, 59)
            
    def randTime(self, values):
        if 'RANDOM-SMALL-MINUTES' in values:
            self.Minutes = max(0, min(59, self.Minutes + random.randint(-15, 15)))
        if 'RANDOM-MIDDLE-MINUTES' in values:
            self.Minutes = max(0, min(59, self.Minutes + random.randint(-30, 30)))
        if 'RANDOM-VERYSMALL-HOUR' in values:
            self.Hours = max(0, min(23, self.Hours + random.randint(-1, 1)))
        if 'RANDOM-SMALL-HOUR' in values:
            self.Hours = max(0, min(23, self.Hours + random.randint(-2, 2)))
        if 'RANDOM-MEDIUM-SMALL-HOUR' in values:
            self.Hours = max(0, min(23, self.Hours + random.randint(-3, 3)))
        if 'RANDOM-MEDIUM-HOUR' in values:
            self.Hours = max(0, min(23, self.Hours + random.randint(-6, 6)))
            
def LoadTriggers(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    triggers = []

    for trigger_elem in root.findall('Trigger'):
        # Number of duplicates / Количество повторений
        Count = int(trigger_elem.get('Count', '1'))  # Defaults to 1 if attribute is missing / По умолчанию 1, если атрибут отсутствует
        RandomActivate = int(trigger_elem.get('RandomActivate', '0'))  # Defaults to 0 if attribute is missing / По умолчанию 0, если атрибут отсутствует
        
        # Add the trigger the required number of times / Добавляем триггер нужное количество раз
        for _ in range(Count):

            trigger = Trigger()
            trigger.Name = trigger_elem.get('Name', '')
            
            if RandomActivate == 1: # Change only if enabled / Изменяем только если включено
                trigger.Activate = random.randint(0, 1) == 1
                
            trigger.AIRequest = trigger_elem.find('AIRequest').text
            
            # Promt / Промт
            AddPromptItem = trigger_elem.find('AddPrompt')
            if AddPromptItem is not None and AddPromptItem.text:
                trigger.AddPromptNextUserMsg = AddPromptItem.text
            
            # The answer without AI / Ответ без AI
            AnswerWithoutAI_elem = trigger_elem.find('AnswerWithoutAI')
            if AnswerWithoutAI_elem is not None and AnswerWithoutAI_elem.text:
                trigger.AnswerWithoutAI = AnswerWithoutAI_elem.text
            
            # Images / Изображения
            trigger.Pics = LoadFileList(trigger_elem.find('Pics').text)
            
            # Time
            time_elem = trigger_elem.find('Time')
            if time_elem is not None and time_elem.text:
                trigger.setTime(time_elem.text)
            else:
                trigger.setTime('X:X')
            
            # Attributes of randomness / Атрибуты случайности
            random_time_elem = trigger_elem.find('RandomTime')
            if random_time_elem is not None and random_time_elem.text:
                trigger.randTime(random_time_elem.text)
            triggers.append(trigger)
            
    return triggers
    
def SaveDateTriggers(triggers):
    with open('Setup/DateTriggers.txt', 'w') as file:
        Str = ''
        for trigger in triggers:
            Str += str(trigger.LastShownDay) + ';'
        file.write(Str + '\n')
        
def LoadDateTriggers(triggers):
    with open('Setup/DateTriggers.txt', 'r') as file:
        line = file.readline().strip()
        values = line.split(';')
        lenTriggers = len(triggers)
        for i in range(len(values)):
            if values[i].strip(' \t\n\r') == '':
                continue
            if i > lenTriggers - 1:
                break
            triggers[i].LastShownDay = int(values[i])
            
def LoadPromptsXML(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        prompts = {}
        for element in root:
            if element.text:
                prompts[element.tag] = element.text.strip().replace('\t', '')
            else:
                prompts[element.tag] = ''
        tree = None
        return prompts
    except Exception as e:
        #print(f"File not found: {filename}: {e}")
        return {}
           
def main():
    global UserHistory, AIHistory, TokensSize
    
    # Settings / Настройки
    UserLang = locale.getlocale()[0][:2]
    
    Config = configparser.ConfigParser()
    ConfigFile = Path('Setup/Setup.ini')
    Config.read(ConfigFile)
    # 0 - OpenAI, 1 - Groq (Llama 3)
    AIProvider = int(Config.get('Main', 'AIProvider'))
    
    TelegramToken = Config.get('Main', 'TelegramToken')
    MasterChatId = int(Config.get('Main', 'TelegramMasterChatId'))
    
    global GroqAPIKey, Proxy
    FirstRun = int(Config.get('Main', 'FirstRun')) == 1
    GroqAPIKey = Config.get('Main', 'GroqAPIKey')
    openai.api_key = Config.get('Main', 'OpenAPIKey')
    TokensSize = int(Config.get('Main', 'HistoryLimit'))
    Proxy = Config.get('Main', 'Proxy')
    SleepTimeOut = int(Config.get('Main', 'SleepTimeOut')) / 1000
    
    # Prompts / Подсказки
    if os.path.exists('Setup/Prompts' + UserLang + '.xml'):
        Prompts = LoadPromptsXML('Setup/Prompts' + UserLang + '.xml')
    else:
        Prompts = LoadPromptsXML('Setup/PromptsEn.xml')
    
    AssistantDescription = Prompts.get('AssistantDescription', '')
    UserDescription = Prompts.get('UserDescription', '')
    UserNames = Prompts.get('UserNames', '')
    
    HistoryUserPrompt = Prompts.get('HistoryUserPrompt', '')
    HistoryAIPrompt = Prompts.get('HistoryAIPrompt', '')
    
    ResponseNeedPromt = Prompts.get('ResponseNeedPromt', '')
     
    ShowMsgs = int(Config.get('Main', 'ShowMessages')) == 1
    DebugMode = int(Config.get('Main', 'DebugMode')) == 1
    SendImgs = int(Config.get('Main', 'SendImages')) == 1
    
    if False:
        print('AssistantDescription:', AssistantDescription)
        print('')
        print('UserDescription:', UserDescription)
        print('')
        print('UserNames:', UserNames)
        print('')
        print('HistoryUserPrompt:', HistoryUserPrompt)
        print('')
        print('HistoryAIPrompt:', HistoryAIPrompt)
        print('')
        exit()
    
    # Static answers / Статичные ответы
    
    AccessErrorAnswer = 'Hi 🤗, I''m sorry but I only communicate with my master user 😍 👉👈'
    WorkTestAnswer = 'Everything is ok, I''m here 😘'
    if UserLang == 'Ru':
        AccessErrorAnswer = 'Приветики 🤗, я сожалею, но я общаюсь только с моим мастер-пользователем 😍 👉👈'
        WorkTestAnswer = 'Всё ок, я тут 😘'
    
    ################################################
    
    UpdateId = 0 # last message being processed / последнее сообщение в обработке
    ChatId = 0
    
    messages = []
    messages.append({'role': 'assistant', 'content': AssistantDescription.strip('\t\n\r')})
    messages.append({'role': 'user', 'content': UserDescription.strip('\t\n\r')})
    
    # History / История
    UserHistory = ReadFile('Setup/UserHistory.txt')
    for line in UserHistory.strip().split('\n'):
        messages.append({'role': 'assistant', 'content': line.strip()})
    AIHistory = ReadFile('Setup/AIHistory.txt')
    for line in AIHistory.strip().split('\n'):
        messages.append({'role': 'user', 'content': line.strip()})

    AddPromptToNextUserMsg = ''
    
    # Triggers / Триггеры
    if os.path.exists('Setup/Triggers' + UserLang + '.xml'):
        triggers = LoadTriggers('Setup/Triggers' + UserLang + '.xml')
    else:
        triggers = LoadTriggers('Setup/TriggersEn.xml')
          
    # Adding a name and adding randomness to the time / Добавляем имя и добавляем случайность ко времени
    for trigger in triggers:
        trigger.AnswerWithoutAI = trigger.AnswerWithoutAI.replace('%name%', RandomPhrase(UserNames))
    
    LoadDateTriggers(triggers)
    
    # Checking triggers / Проверка триггеров
    if False:
        for trigger in triggers:
            print(trigger.Name, '(' + str(trigger.Activate) + ')', '-', str(trigger.Hours) + ':' + str(trigger.Minutes))
            print('Last Shown Day: ' + str(trigger.LastShownDay))
            print('AI request:', trigger.AIRequest.split(';')[0])
            print('Answer without AI:', trigger.AnswerWithoutAI.split(';')[0])
            print('Pics:', trigger.Pics.split(';')[0])
            print()
        exit()
    
    # Update UpdateId
    try:
        Source = HTTPGet('https://api.telegram.org/bot' + TelegramToken + '/getUpdates')
        Data = json.loads(Source)
        if Data['result']:
            UpdateId = Data['result'][0]['update_id']
    except:
        pass
        
    def SendMsg(Msg, Link):
        if Link == '':
            HTTPGet('https://api.telegram.org/bot' + TelegramToken + '/sendmessage?chat_id=' + str(ChatId) + '&text=' + urllib.parse.quote(Msg) + '&parse_mode=markdown')
        else:
            HTTPGet('https://api.telegram.org/bot' + TelegramToken + '/sendanimation?chat_id=' + str(ChatId) + '&animation=' + urllib.parse.quote(Link) + '&caption=' + urllib.parse.quote(Msg))
        # HTTPGet('https://api.telegram.org/bot' + TelegramToken + '/sendphoto?chat_id=' + str(ChatId) + '&photo=' + urllib.parse.quote(Link))

    print('Luiza AI Assistant')
    
    while True:
        time.sleep(SleepTimeOut)
        try:

            UserName = ''
            CurrentDateTime = datetime.now()
            ChatId = ''
            UserMessage = ''
            
            # If there are messages, we process and add them / Если есть сообщения, то обрабатываем и складываем
            MessagesCounter = 0
            while True:
                time.sleep(SleepTimeOut)
                
                Source = HTTPGet('https://api.telegram.org/bot' + TelegramToken + '/getUpdates?offset=' + str(UpdateId))# + '&timeout=5')
                Data = json.loads(Source)
                
                if not Data['result']:
                    break
                UpdateId = Data['result'][0]['update_id']
                UpdateId = UpdateId + 1
                
                ChatId = Data['result'][0]['message']['chat']['id']
                if FirstRun: # Сохраняем Chat ID первый раз / Saving Chat ID for the first time
                    Config.set('Main', 'FirstRun', '0')
                    Config.set('Main', 'TelegramMasterChatID', str(ChatId))
                    Config.write(ConfigFile.open('w'))
                    MasterChatId = ChatId
                    FirstRun = False
                    
                if 'username' in Data['result'][0]['message']['from']:
                    UserName = Data['result'][0]['message']['from']['username']
                else:
                    UserName = str(ChatId)
                    
                if ChatId != MasterChatId:
                    SendMsg(AccessErrorAnswer, '')
                else: 
                    ResponseUserMessage = Data['result'][0]['message']['text']
                    # Answering simple UserMessages / Отвечаем на простые команды
                    if ResponseUserMessage == 'work' or ResponseUserMessage == '/work': 
                        # SendMsg(WorkTestAnswer, 'https://i.imgur.com/UW2gs2C.mp4')
                        SendMsg(WorkTestAnswer, '')
                    else:
                        # We only add messages from the master user / Складываем только сообщения мастер-пользователя
                        if UserMessage and UserMessage[-1] not in '.?':
                            UserMessage += '. ' + ResponseUserMessage
                        else:
                            UserMessage += ResponseUserMessage
                        
                if ShowMsgs:
                    print(str(ChatId) + ', ' + UserName + ', ' + CurrentDateTime.strftime('%H:%M') + ': ' + UserMessage)
                    
                if UserMessage == 'work' or UserMessage == '/work': 
                    UserMessage = ''

                MessagesCounter += 1
                if len(Data['result']) == 0 or MessagesCounter > 3:
                    break
                    
            # If the user sent something . Если пользователь прислал что-то
            if UserMessage != '': 
                
                if AddPromptToNextUserMsg != '':
                    UserMessage += AddPromptToNextUserMsg
                    AddPromptToNextUserMsg = ''
                
                messages.append({'role': 'user', 'content': UserMessage})
                
                # Checking the importance of a user's message / Проверка важности сообщения пользователя
                ImportanceCheck(AIProvider, HistoryUserPrompt, messages, UserMessage, True)
                
                if sum(len(msg['content']) for msg in messages) > TokensSize - 50:
                    messages.pop(2)
                    messages.pop(3)
                    
                # Need an answer? / Нужно ли отвечать?
                NeedAnAnswer = ResponseNeed(AIProvider, messages, ResponseNeedPromt)
                if (ShowMsgs):
                    if NeedAnAnswer:
                        print('Answer required.')
                    else:
                        print('No answer required.')
                        
                # If an answer is needed / Если ответ нужен  
                if NeedAnAnswer:
          
                    # AI answer / Ответ AI
                    BotMessage = AIResponse(AIProvider, messages)
                    
                    if BotMessage != '':
                        SendMsg(BotMessage, '')
                        
                        # AI Response Importance Check / Проверка важности ответа AI
                        ImportanceCheck(AIProvider, HistoryAIPrompt, messages, BotMessage, False)
                        
                        messages.append({'role': 'assistant', 'content': BotMessage})
                    elif DebugMode:
                        print('Error receiving data from AI')

            #print(messages)
            
            for trigger in triggers:
                if CurrentDateTime.day != trigger.LastShownDay: # Once a day / Раз в день
                    #print('day trigger ' + trigger.AIRequest)
                    #print('day trigger ' + str(trigger.Hours) + ':' + str(trigger.Minutes), CurrentDateTime.hour)
                    if ((CurrentDateTime.hour > trigger.Hours) or (CurrentDateTime.hour == trigger.Hours and CurrentDateTime.minute >= trigger.Minutes)):
                        
                        if ShowMsgs:
                            print('Trigger done: ' + trigger.AIRequest)
                        trigger.LastShownDay = CurrentDateTime.day
                        SaveDateTriggers(triggers)
                        
                        # Add predict to the next message / Добавляем predict на следующее сообщение
                        if trigger.AddPromptNextUserMsg != '':
                            AddPromptToNextUserMsg = trigger.AddPromptNextUserMsg
                        
                        # If no messages have been received, then write down and update ChatId to MasterChatId so that you know where to send messages
                        # Если сообщений не поступало, то записываем обновляем ChatId на MasterChatId, чтобы знать куда отправлять сообщения
                        ChatId = MasterChatId
                        
                        messages.append({'role': 'user', 'content': RandomPhrase(trigger.AIRequest)})
                        
                        if DebugMode:
                            print(messages[1:])
                        BotMessage = AIResponse(AIProvider, messages)
                        
                        # Some triggers may not have AnswerWithoutAI / Некоторые триггеры могут быть без AnswerWithoutAI
                        if BotMessage == '' and trigger.AnswerWithoutAI != '': 
                            BotMessage = RandomPhrase(trigger.AnswerWithoutAI)
                        
                        if SendImgs and trigger.Pics != '':
                            SendMsg(BotMessage, RandomPhrase(trigger.Pics))
                        elif BotMessage != '':
                            SendMsg(BotMessage, '')
                        
                        messages.append({'role': 'assistant', 'content': BotMessage})
                        

        except:
            if DebugMode:
                print('Update fail')
            pass

if __name__=='__main__':
	main()
