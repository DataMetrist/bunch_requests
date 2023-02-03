from typing import List, Tuple
import asyncio
import random
import json
import time

import requests
from bs4 import BeautifulSoup, element


OFFCH = "https://www.offch.com/_next/data/dz4qH2OKIVkxcbRZJGNsQ/index.json"
headers = {"User-Agent": "Mozilla/5.0"}


def simple_request(offset: int = 0, limit: int = 100) -> dict:
    """
        docstring
    """
    query = {
        "offset": offset,
        "limit": limit,
    }
    with requests.Session() as session:
        session.headers.update(headers)
        with session.get(OFFCH, params=query) as response:
            response_data: dict = response.json()
            return response_data["pageProps"]["serverCouponList"]


def test_sync():
    """
        docstring
    """
    sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    retry = random.randint(10, 20)
    print(f"Retry {retry} Times!")

    for limit in sizes:
        t1 = time.time()
        for _ in range(retry):
            simple_request(limit=limit)
        t2 = time.time()
        take = round((t2 - t1) / retry, 3)
        print(f"{retry} Requests Takes {take} Seconds <=> SIZE [{limit}]")


def ddos_sync():
    """
        docstring
    """
    sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    length = len(sizes)

    while True:
        retry = random.randint(100, 200)
        print(f"Retry {retry} Times!")
        for _ in range(retry):
            t1 = time.time()
            for limit in sizes:
                simple_request(limit=limit)
            t2 = time.time()
            take = round((t2 - t1) / length, 3)
            print(f"{length} Requests Takes {take} Seconds!")


def function():
    """
        docstring
    """
    data = simple_request()
    copouns: int = data.get("count")
    # limit: int = int(data.get("limit"))

    sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    # length = len(sizes)

    # retry = random.randint(100, 200)
    # print(f"Retry {retry} Times!")
    Round = 1
    while True:
        for limit in sizes[-1::-1]:
            pages = copouns // limit
            pages += (1 if copouns % limit else 0)
            print(copouns, limit, pages)
            t1 = time.time()
            for page_number in range(pages):
                simple_request(limit=limit, offset=page_number * limit)
            t2 = time.time()
            take = round(t2 - t1, 3)
            print(f"{pages} Requests Takes {take} Seconds! ({limit})")
        else:
            Round += 1
            print(str(Round).zfill(4))
        # break
    return


def copouns_ids(limit: int = 1000):
    """
        docstring
    """
    data = simple_request()
    copouns: int = data.get("count")
    pages = copouns // limit
    pages += (1 if copouns % limit else 0)
    print(copouns, limit, pages)

    ids = []
    for page_number in range(pages):
        results = simple_request(limit=limit, offset=page_number * limit)
        for item in results["results"]:
            ids.append(item["id"])
    return ids


if __name__ == "__main__":
    ""
    # simple_request(test_digikala.format(product_id=9639430))
    # ddos_sync()
    function()
