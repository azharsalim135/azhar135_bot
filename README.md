# azhat135_bot
telegram bot for coding project,

# Requirements

- Python 3

- pip

- postgreSQL

- telegram client


# Instructions

- setup ngrok and telegram bot API key and link them. Follow the below pattern.
  
    https://api.telegram.org/bot<BOT_TOKEN_ID>/setWebhook?url=<HOOK_URL>/azhar135_bot/update/

- setup postgreSQL and set username,database name,localhost port etc. 

- clone the repo to the drive.

- setup up virtual env for python

- run 'pip install -r requirements.txt

- add the nkgrok url to django ALLOWED_HOSTS 

- on tgbot/tgbot/settings.py dictionary TEMPLATE setup the username,database name, host and port adresses.

- run python migrate.py makemigratation

- run python migrate.py migrate

- run python migrate.py runserver


### SET THE BOT TOKEN AT tgbot/azhar135_bot/credentials.py

####  tgbot/tgbot/urls.py initialize db connection and check if the required tables are present in the db, if not it will proceed to create required tables.

####  azhar135_bot/tgbot/azhar135_bot/processors.py containes actual logic for the backend.

####  the bot resoponds with the buttons to select whenever user sent a text.

####  when user pressed a button call back listener will fetch the username and the button name,

####  for every call user makes to the bot, the bot will add the count to the database.



####  Screenshot 1

![alt text](https://github.com/azharsalim135/azhar135_bot/raw/main/screenshots/Screenshot%20chat.jpg)




####  Screenshot 2

![alt text](https://github.com/azharsalim135/azhar135_bot/raw/main/screenshots/Screenshot%202023-01-29%20171928.jpg)




####  Screenshot 3

![alt text](https://github.com/azharsalim135/azhar135_bot/raw/main/screenshots/Screenshot%202023-01-29%20172002.jpg)

