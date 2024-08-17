[![EN](https://user-images.githubusercontent.com/9499881/33184537-7be87e86-d096-11e7-89bb-f3286f752bc6.png)](https://github.com/r57zone/LuizaGPTAssistant/) 
[![RU](https://user-images.githubusercontent.com/9499881/27683795-5b0fbac6-5cd8-11e7-929c-057833e01fb1.png)](https://github.com/r57zone/LuizaGPTAssistant/blob/master/README.RU.md)
← Choose language | Выберите язык

# Luiza AI Assistant
A simple virtual assistant imitating your close friend, girlfriend or boyfriend, based on the [ChatGPT](https://openai.com/chatgpt) or [Llama](https://llama.meta.com/) neural network and [Telegram](https://telegram.org/) messenger. You can make up the assistant with his history, tastes, add him necessary triggers. By default, it will wish you good morning, good night, write compliments and interesting facts, you can also dialog with it, ask questions, advice and learn something.

![](https://github.com/user-attachments/assets/8f29dfb7-4964-4d68-8889-79273d115cab)
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/5b54fc41-b902-4324-8aa5-2f3c97527177)

## Assistant messages (animation):
![](https://github.com/user-attachments/assets/cdd4e6ac-b2f2-447c-b740-239955847248)

## Setup
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/483720af-4493-4d09-9e78-137bab2230a1)

Virtual Assistant supports two neural networks: Llama (free of charge, via Groq service) and ChatGPT (3 months of free use, then paid). Choose one of the services at your discretion. 

### Configuring Llama based assistant (Groq)
1. Register at [Groq](https://console.groq.com/) and [get key](https://console.groq.com/).
2. [Create a bot](https://t.me/BotFather) in Telegram messenger, get the key, change the name and photo.
3. Install [Python](https://www.python.org/downloads/), then run Windows Command Prompt and enter the command `pip install openai` (library to work with ChatGPT) and `pip install requests[socks]` (library to support proxies).
4. Download the [archive of assistant](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), unzip and modify the files to your liking: `AssistantDescriptionEn.txt` - description of the helper, `UserDescriptionEn.txt` - description of you, `UserNamesEn.txt` - list of requests to you. Edit the helper triggers in the `TriggersRu.xml` file.
5. Enter the Telegram keys `TelegramToken` and Groq keys `GroqAPIKey`, in the `Setup.ini` file, also enter your nickname `TelegramMasterUser`. 
6. Run `Luiza_AI_Assistant.py` and write something to him in Telegram, then copy the first numeric code and paste in `TelegramMasterChatID`, in the `Setup.ini` file. You can then change the `ShowMessages` parameter to `0` to remove the message output.
7. If you want a hidden auto-run at Windows startup, rename the `Luiza_AI_Assistant.py` file to `Luiza_AI_AI_Assistant.pyw` and add a shortcut to the `%appdata%\Microsoft\Windows\Start Menu\Programs` autoloader folder.

### Configuring ChatGPT based assistant
1. Register at [OpenAI](https://chat.openai.com/chat) and [get key](https://platform.openai.com/account/api-keys). The service gives a free key for 3 months. For registration citizens of Russia and Belarus will need a virtual number, you can get it at [5sim.biz](https://5sim.biz) (Polish number is only 12 rubles).
2. [Create a bot](https://t.me/BotFather) in Telegram messenger, get a key, change your name and photo.
3. Install [Python](https://www.python.org/downloads/), then run Windows Command Prompt and enter the command `pip install openai` (library to work with ChatGPT) and `pip install requests[socks]` (library to support proxies).
4. Download [archive of assistant](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), unpack and modify the files at your discretion: `AssistantDescriptionEn.txt` - description of the helper, `UserDescriptionEn.txt` - description of you, `UserNamesEn.txt` - list of references to you. Edit the helper triggers in the `TriggersRu.xml` file.
5. Enter the Telegram keys `TelegramToken` and OpenAI `OpenAPIKey`, in the `Setup.ini` file, also enter your nickname `TelegramMasterUser`. 
6. Run `Luiza_AI_AI_Assistant.py` and write something to him in Telegram, then copy the first numeric code and paste in `TelegramMasterChatID`, in the `Setup.ini` file. You can then change the `ShowMessages` parameter to `0` to remove the message output.
7. If you want hidden automatic startup at Windows startup, rename the `Luiza_AI_Assistant.py` file to `Luiza_AI_AI_Assistant.pyw` and add a shortcut to the `%appdata%\Microsoft\Windows\Start Menu\Programs` autoloader folder.

## Features
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/044cc5fa-6dd5-464e-8f07-a13c52db2304)


The default triggers are: good morning wishes, good night. compliments, interesting facts. Change the time of triggering, according to your schedule. Time can be random, specific, or approximate. Add your triggers or delete current triggers as needed by copying the trigger block or deleting it.


The messages sent by the triggers include animations of the character Lisa, aka actress Vanessa Angel, from the TV series Wonders of Science, given at random. You can change them in the `Setup/Pics` folder, with the name of the corresponding trigger. You can see and delete animations by opening the `AnimDesigner.html` file and entering the contents of the files.

## Media
[Коммерсантъ](https://www.kommersant.ru/doc/6891989).

Thanks for posting.

## Feedback
`r57zone[at]gmail.com`