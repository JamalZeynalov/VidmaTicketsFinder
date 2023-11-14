import datetime
import logging
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.info("This is an informational message. Container is started!")

load_dotenv(".env")

TIMEOUT = int(os.environ.get("MINUTES_WAIT_BETWEEN_SEARCHES", 20))
NO_RESULTS_NOTIFICATION_HOUR = int(os.environ.get("NO_RESULTS_NOTIFICATION_HOUR", 17))

bot_token = "6883929632:AAGZlbgDpQZ5SF1jb6MKaECJwViF36PFKCo"  # VidmaTicketsBot
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

tickets_store_link = "http://ft.org.ua/ua/performance/konotopska-vidma"


def notify_via_telegram(message: str):
    # Construct the URL for sending a message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logging.info("Message sent successfully!")
        else:
            logging.error(
                f"Failed to send the message. Status code: {response.status_code}"
            )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def get_latest_event_date():
    r = requests.get(tickets_store_link)

    soup = BeautifulSoup(r.text, "html.parser")
    events = soup.find_all("div", {"class": "performanceevents_item_info_date"})

    dates_str = [re.match(r"(\D*)(.*)", ev.text).group(2) for ev in events]
    dates = [datetime.datetime.strptime(d, "%d/%m/%Y").date() for d in dates_str]

    logging.info(
        "Шукаю. Дати останніх трьох вистав:\n"
        + "\n".join([event.text for event in events[-3:]])
    )

    return dates[-1]


def search_for_vidma_tickets(search_day_date: datetime.date, initial_latest_date: datetime.date):
    while (latest_date := get_latest_event_date()) <= initial_latest_date:
        if (
            datetime.date.today() != search_day_date
            and datetime.datetime.now().hour == NO_RESULTS_NOTIFICATION_HOUR
        ):
            search_day_date = datetime.date.today()
            notify_via_telegram("Сьогодні нічого не знайшов. Почекаю до завтра.")

        logging.info(
            f"Нажаль, немає нових вистав після {initial_latest_date.strftime('%d/%m/%Y')}. "
            f"Я подивлюсь ще раз через {TIMEOUT} хвилин :("
        )
        time.sleep(TIMEOUT * 60)

    msg = (
        f"Перемога!!!\n"
        f"Є нова вистава 'Конотопська відьма': {latest_date.strftime('%d/%m/%Y')}\n\n"
        f"Купити квитки:\n{tickets_store_link}"
    )
    notify_via_telegram(msg)


def start_search():
    soup_ = BeautifulSoup(requests.get(tickets_store_link).text, "html.parser")
    latest = soup_.find_all("div", {"class": "performanceevents_item_info_date"})
    notify_via_telegram(
        f"Ну все, я налаштований серйозно. Шукаю квитки на виставу 'Конотопська відьма'.\n"
        f"Посилання на квитки:\n {tickets_store_link}\n"
        f"Дата останньої відомої вистави: {latest[-1].text}"
    )


# ======================================================================================================

start_search()
start_date = datetime.date.today()
latest_event = get_latest_event_date()
search_for_vidma_tickets(start_date, latest_event)
