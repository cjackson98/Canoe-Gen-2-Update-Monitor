import time

import requests
from bs4 import BeautifulSoup
from plyer import notification


####################
REGULAR_DELAY = 300       # 5 minutes
TIMEOUT_DELAY = 600       # 10 minutes
####################


def get_article_dates():
    while True:
        try:
            result = requests.get("https://percent.studio/blogs/news", timeout=5)
            break
        except requests.exceptions.Timeout:
            print(f"Timed out. Waiting {TIMEOUT_DELAY} seconds ({TIMEOUT_DELAY/60} minutes).")


    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    time_tags = soup.find_all('time')

    dates = []
    for tag in time_tags:
        dates.append(tag.attrs['datetime'])

    return dates


def get_read_more_link():
    while True:
        try:
            result = requests.get("https://percent.studio/blogs/news", timeout=5)
            break
        except requests.exceptions.Timeout:
            print(f"Timed out. Waiting {TIMEOUT_DELAY} seconds ({TIMEOUT_DELAY/60} minutes).")

    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    a_tags = soup.find_all('a')

    read_more_tags = []
    for tag in a_tags:
        if "class" in tag.attrs.keys():
            if tag.attrs['class'] == ['blog-read-more']:
                read_more_tags.append(tag)

    recent_link = "https://percent.studio" + read_more_tags[0].attrs['href']
    return recent_link


if __name__ == "__main__":
    dates = get_article_dates()
    newest_date = dates[0]

    ctr = 1

    while True:
        print("="*75)
    
        num = str(ctr)
        
        print(f"Checking... ({ctr}):")

        dates = get_article_dates()

        if dates[0] != newest_date:
            print("\tUPDATED "*5)
            print(get_read_more_link())

            notification.notify(
                title='News updated',
                message=get_read_more_link(),
                app_icon=None,
                timeout=10,
            )

            time.sleep(10)

            break

        else:
            print(f"\tNo change. Checking again in {REGULAR_DELAY} seconds ({REGULAR_DELAY/60} minutes).")

        print("="*75)
        print()

        ctr += 1
        time.sleep(REGULAR_DELAY)
