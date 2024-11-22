import sqlite3
from bs4 import BeautifulSoup
import requests

entrypoint = "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus"
nodes = []


def download_page(page_url):
    print(f"Processing {page_url}")
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find(id="catalogtable")
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells[2].find("a"):
            continue
        print(f"processing {cells[2].find('a').text}")
        details_response = requests.get(cells[2].find("a")["href"])
        details_soup = BeautifulSoup(details_response.text, "html.parser")
        nodes.append(
            {
                "name": cells[2].find("a").text,
                "author": cells[1].find("a").text.replace("\xa0", " "),
                "links": "|".join([x["href"] for x in details_soup.find_all("a") if x["href"].endswith(".mp3")]),
            }
        )
        print(f"{len(nodes)=}")

    active_div = soup.find(id="roller_active")
    try:
        next_page_url = active_div.find_next_sibling().find("a")["href"]
    except Exception:
        print("Done")
    else:
        download_page(next_page_url)


if __name__ == "__main__":
    download_page(entrypoint)

    with sqlite3.connect("mds.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        name TEXT,
        author TEXT,
        links TEXT
    )
"""
        )

    for record in nodes:
        cursor.execute(
            """
        INSERT INTO books (name, author, links)
        VALUES (?, ?, ?)
    """,
            (record["name"], record["author"], record["links"]),
        )

    # Commit the transaction
    conn.commit()
