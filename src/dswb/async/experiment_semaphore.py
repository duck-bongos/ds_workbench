import asyncio
import time
import json
from asyncio import Queue
from datetime import timedelta
from typing import Any, Dict, List, Tuple

import aiohttp
import numpy as np
from pydantic import BaseModel

MAX_TOKENS_PER_MINUTE = 100000
TOKENS_PER_REQUEST = 100
SEMAPHORE = asyncio.Semaphore(2050)
URL = "http://127.0.0.1:8000/items/"


# Shared resources
tokens_used = 0
last_reset_time = time.time()
ALOCK = asyncio.Lock()  # Lock for making tokens_used async-safe


async def fetch_data_with_burst_control(
    session: aiohttp.ClientSession,
    url: str,
    payload: Dict[str, Any],
    token_count,
    wq: Queue,
    eq: Queue,
    max_tokens_per_minute: int,
    lock: asyncio.Lock,
    semaphore: asyncio.Semaphore,
):
    global tokens_used
    global last_reset_time
    sleep_time = 0

    payload_size = len(json.dumps(payload))

    async with lock:
        # Reset tokens if a minute has passed
        current_time = time.time()
        if current_time - last_reset_time >= 60:
            tokens_used = 0
            last_reset_time = current_time

    async with lock:
        # Check if we need to wait to stay within the rate limit
        if tokens_used + token_count + payload_size > max_tokens_per_minute:
            sleep_time = 60 - (current_time - last_reset_time)

            last_reset_time = time.time()

        # Reset after sleep
        tokens_used = payload_size + token_count

    if sleep_time > 0:
        print(f"Rate limit reached. Sleeping for {sleep_time} seconds...")
        await asyncio.sleep(sleep_time)

    # Make the API request
    async with semaphore:
        async with session.post(url=url, json=payload) as response:
            print(await response.json())


async def async_main(
    content: List[Tuple[int, str]],
    q: Queue,
    e: Queue,
    max_tokens_per_minute: int = 1000000,
):

    semaphore = asyncio.Semaphore(2050)
    url = "http://127.0.0.1:8000/items/"
    alock = asyncio.Lock()  # Lock for making tokens_used async-safe

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _id, text in content:
            tokens_count = TOKENS_PER_REQUEST
            task = asyncio.create_task(
                fetch_data_with_burst_control(
                    session,
                    url=url,
                    payload={"text": text, "id": _id},
                    token_count=tokens_count,
                    wq=q,
                    eq=e,
                    lock=alock,
                    semaphore=semaphore,
                    max_tokens_per_minute=max_tokens_per_minute,
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks)


def rsize():
    return np.random.choice(np.arange(2, 8), p=[0.05, 0.3, 0.3, 0.2, 0.1, 0.05]) * 1000


def main():
    # Shared resources

    ALOCK = asyncio.Lock()  # Lock for making tokens_used async-safe

    work_queue = asyncio.Queue()
    err_queue = asyncio.Queue()
    integers = list(range(10000))

    content = [(_int, "X" * rsize()) for _int in integers]

    asyncio.run(async_main(content, q=work_queue, e=err_queue))


if __name__ in "__main__":
    performance = []
    with open("performance.txt", "w") as pfile:

        for _ in range(10):
            begin = time.time()
            main()
            end = time.time()
            runtime = end - begin
            pfile.write(f"Runtime: {str(timedelta(seconds=runtime))}\n")
            performance.append(runtime)

            print("Sleeping for 2")
            time.sleep(2)

        _avg = sum(performance) / len(performance)
        avg = str(timedelta(seconds=_avg))
        pfile.write(f"Average performance: {avg}\n")
