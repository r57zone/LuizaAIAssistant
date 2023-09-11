[![EN](https://user-images.githubusercontent.com/9499881/33184537-7be87e86-d096-11e7-89bb-f3286f752bc6.png)](https://github.com/r57zone/LuizaGPTAssistant/) 
[![RU](https://user-images.githubusercontent.com/9499881/27683795-5b0fbac6-5cd8-11e7-929c-057833e01fb1.png)](https://github.com/r57zone/LuizaGPTAssistant/blob/master/README.RU.md)
&#8211; ← Choose language | Выберите язык

# Luiza GPT Assistant
A simple virtual assistant imitating your close friend, girlfriend or boyfriend, based on the [ChatGPT](https://openai.com/chatgpt) neural network and [Telegram](https://telegram.org/) messenger. You can make up the assistant with his history, tastes, add him necessary triggers. By default, it will wish you good morning, good night, write compliments and interesting facts, you can also dialog with it, ask questions, advice and learn something.

![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/7389f66e-1ae5-4d61-8552-fdb3ebfbf998)
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/5b54fc41-b902-4324-8aa5-2f3c97527177)

## Setup
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/483720af-4493-4d09-9e78-137bab2230a1)


1. Register at [OpenAI](https://chat.openai.com/chat) and [get key](https://platform.openai.com/account/api-keys). The service gives a free key for 3 months. 
2. [Create a bot](https://t.me/BotFather) in Telegram messenger, get a key, change your name and photo.
3. Install [Python](https://www.python.org/downloads/), then run Windows command prompt and enter the command `pip install openai` (library to work with ChatGPT).
4. Download the [assistant archive](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), unzip and change the history in the `PredictMessage.txt` file and the list of calls to you `MasterNames.txt`.
5. Open the `bot.py` file with notepad and enter your keys (`YOUR_OPENAI_KEY` and `YOUR_TELEGRAM_BOT_KEY`).
6. Run `bot.py` and write something to it in Telegram, then copy the first numeric code `masterChatId` and the second numeric code or nickname `masterUser`. You need to close `bot.py` and enter them in the code instead of the current ones.
7. If you want a hidden automatic startup at Windows startup, rename the `bot.py` file to `bot.pyw` and add a shortcut to the `%appdata%\Microsoft\Windows\Start Menu\Programs` folder.


## Features
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/044cc5fa-6dd5-464e-8f07-a13c52db2304)


The default triggers are: good morning wishes, good night. compliments, interesting facts. Change the time of triggering, according to your schedule. The minutes are randomized so that messages arrive at different times. Add your triggers or delete current triggers as needed by copying the trigger block or deleting it.


The messages sent by the triggers include animations of the character Lisa, aka actress Vanessa Angel, from the TV series Wonders of Science, given at random. You can change them in the `Triggers` folder, with the name of the corresponding trigger. You can see and delete animations by opening the `AnimDesigner.html` file and entering the contents of the files.


## Feedback
`r57zone[at]gmail.com`