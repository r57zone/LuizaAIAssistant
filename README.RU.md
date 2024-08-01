[![EN](https://user-images.githubusercontent.com/9499881/33184537-7be87e86-d096-11e7-89bb-f3286f752bc6.png)](https://github.com/r57zone/LuizaGPTAssistant/) 
[![RU](https://user-images.githubusercontent.com/9499881/27683795-5b0fbac6-5cd8-11e7-929c-057833e01fb1.png)](https://github.com/r57zone/LuizaGPTAssistant/blob/master/README.RU.md)

# Луиза AI помощник
Простой виртуальный помощник, имитирующий вашего близкого друга, девушку или парня, работающий на базе нейросети [ChatGPT](https://openai.com/chatgpt) или [Llama](https://llama.meta.com/) и мессенджера [Telegram](https://telegram.org/). Можно придумать помощнику его историю, вкусы, добавить ему необходимые триггеры. По умолчанию он будет желать вам доброго утра, спокойной ночи, писать комплименты и интересные факты, также с ним можно вести диалоги, спрашивать вопросы, советы и обучаться чем-либо.

![](https://github.com/user-attachments/assets/8f29dfb7-4964-4d68-8889-79273d115cab)
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/5b54fc41-b902-4324-8aa5-2f3c97527177)

## Сообщения помощника (анимация):
![](https://github.com/user-attachments/assets/2f06cb62-b51a-40c9-94fb-aab48b92babe)

## Настройка
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/483720af-4493-4d09-9e78-137bab2230a1)

Виртуальный помошник поддерживает две нейросети: Llama (бесплатно, через сервис Groq) и ChatGPT (3 месяца использования бесплатно, потом платно). Выберите один из сервисов на своё усмотрение. Для России и Белоруссии Llama, через сервис Groq, будет оптимальным решением, однако необходимо использовать прокси соединение или VPN.

### Настройка помощника на основе нейросети Llama (Groq)
1. Установите VPN или VPN расширение для браузера (можно FreeVPN или другое).
2. Зарегистрируйтесь на сайте [Groq](https://console.groq.com/) и [получите ключ](https://console.groq.com/).
3. [Создайте бота](https://t.me/BotFather) в мессенджере Telegram, получите ключ, измените имя и фото.
4. Установите [Python](https://www.python.org/downloads/), после чего запустите командную строку Windows и введите команду `pip install openai` (библиотека для работы с ChatGPT) и `pip install requests[socks]` (библиотека для поддержки прокси).
5. Загрузите [архив с помощником](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), распакуйте и измените файлы на свое усмотрение: `AssistantDescriptionRu.txt` - описание помощника, `UserDescriptionRu.txt` - описание вас, `UserNamesRu.txt` - список обращений к вам. Отредактируйте триггеры помощника в файле `TriggersRu.xml`.
6. Введите ключи Telegram `TelegramToken` и Groq `GroqAPIKey`, в файл `Setup.ini`, также введите ваш никнейм `TelegramMasterUser`. 
7. Запустите `Luiza_AI_Assistant.py` и напишите что-нибудь ему в Telegram, после чего скопируйте первый числовой код и вставьте в `TelegramMasterChatID`, в файл `Setup.ini`. После чего можно изменить параметр `ShowMessages` на `0`, чтобы убрать вывод сообщений.
8. К сожалению, сервис блокирует запросы с российских и белоруских адресов, поэтому необходимо использовать socks5 прокси или VPN. Если у вас есть прокси, то введите её в параметр `Proxy`, в файл `Setup.ini`. Можно где-то развернуть ShadowSocks прокси.
9. При необходимости скрытого автоматического запуска при старте Windows, переименуйте файл `Luiza_AI_Assistant.py` в `Luiza_AI_Assistant.pyw` и добавьте ярлык в папку автозагрузки `%appdata%\Microsoft\Windows\Start Menu\Programs`.

### Настройка помощника на основе ChatGPT
1. Установите VPN или VPN расширение для браузера (можно FreeVPN или другое).
2. Зарегистрируйтесь на сайте [OpenAI](https://chat.openai.com/chat) и [получите ключ](https://platform.openai.com/account/api-keys). Сервис дает бесплатный ключ на 3 месяца. Для регистрации граждан России и Белоруссии понадобится виртуальный номер, его можно получить на сайте [5sim.biz](https://5sim.biz) (польский номер всего 12 рублей).
3. [Создайте бота](https://t.me/BotFather) в мессенджере Telegram, получите ключ, измените имя и фото.
4. Установите [Python](https://www.python.org/downloads/), после чего запустите командную строку Windows и введите команду `pip install openai` (библиотека для работы с ChatGPT) и `pip install requests[socks]` (библиотека для поддержки прокси).
5. Загрузите [архив с помощником](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), распакуйте и измените файлы на свое усмотрение: `AssistantDescriptionRu.txt` - описание помощника, `UserDescriptionRu.txt` - описание вас, `UserNamesRu.txt` - список обращений к вам. Отредактируйте триггеры помощника в файле `TriggersRu.xml`.
6. Введите ключи Telegram `TelegramToken` и OpenAI `OpenAPIKey`, в файл `Setup.ini`, также введите ваш никнейм `TelegramMasterUser`. 
7. Запустите `Luiza_AI_Assistant.py` и напишите что-нибудь ему в Telegram, после чего скопируйте первый числовой код и вставьте в `TelegramMasterChatID`, в файл `Setup.ini`. После чего можно изменить параметр `ShowMessages` на `0`, чтобы убрать вывод сообщений.
8. При необходимости скрытого автоматического запуска при старте Windows, переименуйте файл `Luiza_AI_Assistant.py` в `Luiza_AI_Assistant.pyw` и добавьте ярлык в папку автозагрузки `%appdata%\Microsoft\Windows\Start Menu\Programs`.

# Особенности
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/044cc5fa-6dd5-464e-8f07-a13c52db2304)


По умолчанию сделаны триггеры: пожелания доброго утра, спокойной ночи. комплименты, интересные факты. Измените время срабатывания, в соответствии с вашим графиком. Время может быть случайным, конкретным или приблизительным. При необходимости добавьте свои триггеры или удалите текущие, скопировав блок триггера или удалив его.


Сообщения, посылаемые триггерами включают в себя анимации персонажа Лизы, она же актриса Ванесса Энджел, из сериала Чудеса Науки, выдаваемые случайным образом. Изменить их можно в папке `Setup/Pics`, с названием соответствующего триггера. Увидеть и удалить анимации можно открыв файл `AnimDesigner.html` и введя содержимое файлов.

## Обратная связь
`r57zone[собака]gmail.com`