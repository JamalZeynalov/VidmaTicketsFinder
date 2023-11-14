# VidmaTicketsFinder

Find the newest events to buy tickets to 'The Witch of Konotop' by Ivan Franko Theatre
http://ft.org.ua/ua/performance/konotopska-vidma

# Description

Since it's almost impossible to quickly buy good tickets to this performance,
I've created this script to help me with that. Setup it and run in background to receive notifications in Telegram.
It will check the website every 20 minutes and notify you if there are any tickets available.
Also, if no tickets are found today, once a day it will notify you to confirm it's still working.

# Environment variables

Create .env file in the root of the project and add environment variables to it:

#### Required

```dotenv
# Put your Telegram chat id instead of 123456789
TELEGRAM_CHAT_ID=123456789
```

#### Optional (to change default behavior):

```dotenv
MINUTES_WAIT_BETWEEN_SEARCHES=15 # 20 by default
NO_RESULTS_NOTIFICATION_HOUR=16 # 17 by default
```

* `MINUTES_WAIT_BETWEEN_SEARCHES` - How often to check for tickets
* `NO_RESULTS_NOTIFICATION_HOUR` - At what hour to notify you if no tickets were found today

# Run in background Docker container (RECOMMENDED)

1. Install and run Docker
2. Start `@VidmaTicketsBot` to receive notifications [LINK](https://telegram.me/VidmaTicketsBot)
3. Start Telegram bot `@RawDataBot` to get your TELEGRAM_CHAT_ID. [LINK](https://telegram.me/rawdatabot)
4. Fill .env file with environment variables
5. Run `docker-compose up -d` <br>
   * (then you can check logs with `vidma-tickets-finder-vidma-tickets-1` or via desktop app Dashboard)
6. Wait for your tickets to be found and receive notifications in Telegram

# Run on your machine

1. Install Python 3.9+
2. Install requirements: `pip install -r requirements.txt`
3. Start `@VidmaTicketsBot` to receive notifications [LINK](https://telegram.me/VidmaTicketsBot)
4. Start Telegram bot `@RawDataBot` to get your TELEGRAM_CHAT_ID. [LINK](https://telegram.me/rawdatabot)
5. Fill .env file with environment variables
6. Run `python vidma.py`
7. Wait for your tickets to be found and receive notifications in Telegram


# Get TELEGRAM_CHAT_ID
Image below shows how to get your TELEGRAM_CHAT_ID using `@RawDataBot`:<br>
<img src="https://raw.githubusercontent.com/JamalZeynalov/vidma-tickets-finder/master/chat_id_screenshot.png" width=400 alt="chat_id">