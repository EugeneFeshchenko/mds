import sqlite3
from bs4 import BeautifulSoup
import requests


def download_page(page_url):
    print(f"processing {page_url}")
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find(id="catalogtable")

    conn = sqlite3.connect("mds.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM books")
    known_names = [row[0] for row in cursor.fetchall()]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells[2].find("a"):
            continue
        name = cells[2].find("a").text
        author = cells[1].find("a").text.replace("\xa0", " ")
        if not name in known_names:
            print(f"Adding {author} - {name}")

            details_response = requests.get(cells[2].find("a")["href"])
            details_soup = BeautifulSoup(details_response.text, "html.parser")
            links = "|".join([x["href"] for x in details_soup.find_all("a") if x["href"].endswith(".mp3")])
            cursor.execute(
                """
                    INSERT INTO books (name, author, links, status)
                    VALUES (?, ?, ?, ?)
                    """,
                (name, author, links, "pending"),
            )
            conn.commit()
    conn.close()

    active_div = soup.find(id="roller_active")
    try:
        next_page_url = active_div.find_next_sibling().find("a")["href"]
    except Exception:
        print("Done")
    else:
        download_page(next_page_url)


if __name__ == "__main__":
    entrypoint = "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus"
    download_page(entrypoint)
