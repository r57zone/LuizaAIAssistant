[![EN](https://user-images.githubusercontent.com/9499881/33184537-7be87e86-d096-11e7-89bb-f3286f752bc6.png)](https://github.com/r57zone/LuizaGPTAssistant/) 
[![RU](https://user-images.githubusercontent.com/9499881/27683795-5b0fbac6-5cd8-11e7-929c-057833e01fb1.png)](https://github.com/r57zone/LuizaGPTAssistant/blob/master/README.RU.md)

# Луиза GPT помощник
Простой виртуальный помощник, имитирующий вашего близкого друга, девушку или парня, работающий на базе нейросети [ChatGPT](https://openai.com/chatgpt) и мессенджера [Telegram](https://telegram.org/). Можно придумать помощнику его историю, вкусы, добавить ему необходимые триггеры. По умолчанию он будет желать вам доброго утра, спокойной ночи, писать комплименты и интересные факты, также с ним можно вести диалоги, спрашивать вопросы, советы и обучаться чем-либо.

![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/7389f66e-1ae5-4d61-8552-fdb3ebfbf998)
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/5b54fc41-b902-4324-8aa5-2f3c97527177)

## Настройка
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/483720af-4493-4d09-9e78-137bab2230a1)


1. Установите VPN или VPN расширение для браузера (можно FreeVPN или другое).
2. Зарегистрируйтесь на сайте [OpenAI](https://chat.openai.com/chat) и [получите ключ](https://platform.openai.com/account/api-keys). Сервис дает бесплатный ключ на 3 месяца. Для регистрации граждан России и Белоруссии понадобится виртуальный номер, его можно получить на сайте [5sim.biz](https://5sim.biz) (польский номер всего 12 рублей).
3. [Создайте бота](https://t.me/BotFather) в мессенджере Telegram, получите ключ, измените имя и фото.
4. Установите [Python](https://www.python.org/downloads/), после чего запустите командную строку Windows и введите команду `pip install openai` (библиотека для работы с ChatGPT).
5. Загрузите [архив с помощником](https://github.com/r57zone/LuizaGPTAssistant/archive/refs/heads/master.zip), распакуйте и измените историю в файле `PredictMessage.txt` и список обращений к вам `MasterNames.txt`.
6. Откройте файл `bot.py` блокнотом и введите ваши ключи (`YOUR_OPENAI_KEY` и `YOUR_TELEGRAM_BOT_KEY`).
7. Запустите `bot.py` и напишите что-нибудь ему в Telegram, после чего скопируйте первый числовой код `masterChatId` и второй числовой код или никнейм `masterUser`. Нужно закрыть `bot.py` и ввести их в коде, вместо текущих.
8. При необходимости скрытого автоматического запуска при старте Windows, переименуйте файл `bot.py` в `bot.pyw` и добавьте ярлык в папку автозагрузки `%appdata%\Microsoft\Windows\Start Menu\Programs`.

# Особенности
![](https://github.com/r57zone/LuizaGPTAssistant/assets/9499881/044cc5fa-6dd5-464e-8f07-a13c52db2304)


По умолчанию сделаны триггеры: пожелания доброго утра, спокойной ночи. комплименты, интересные факты. Измените время срабатывания, в соответствии с вашим графиком. Минуты рандомизируются, чтобы сообщения приходили в разное время. При необходимости добавьте свои триггеры или удалите текущие, скопировав блок триггера или удалив его.


Сообщения, посылаемые триггерами включают в себя анимации персонажа Лизы, она же актриса Ванесса Энджел, из сериала Чудеса Науки, выдаваемые случайным образом. Изменить их можно в папке `Triggers`, с названием соответствующего триггера. Увидеть и удалить анимации можно открыв файл `AnimDesigner.html` и введя содержимое файлов.


## Обратная связь
`r57zone[собака]gmail.com`