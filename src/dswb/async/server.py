import random
import asyncio
import time
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from requests.exceptions import RequestException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.requests import Request


limiter = Limiter(key_func=get_remote_address, default_limits=["2100 per minute"])

# app.add_exception_handler(429, _rate_limit_exceeded_handler)

app = FastAPI()
app.state.limiter = limiter


class Item(BaseModel):
    text: str
    id: int


LOCK = asyncio.Lock()
DEQUE = deque()
BUCKET_CAPACITY = 100
LEAK_PER_SECOND = 60
REQUEST_PER_SECOND = 75


class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = []
        self.last_leak_timestamp = datetime.now()

    def allow_request(self, request):
        self.leak()
        if len(self.queue) < self.capacity:
            self.queue.append(request)
            return True
        return False

    def leak(self):
        now = datetime.now()
        elapsed = now - self.last_leak_timestamp
        leaks = elapsed * self.leak_rate
        for _ in range(int(leaks)):
            if self.queue:
                return self.queue.pop(0)
        self.last_leak_timestamp = now


async def process():
    if not len(DEQUE):
        return None
    with LOCK:
        return DEQUE.popleft()


async def request(item: Item):
    if len(DEQUE) >= BUCKET_CAPACITY:
        return False

    with LOCK:
        DEQUE.append(item)


# @limiter.limit("210/minute")
@app.post("/items/")
async def post_item(item: Item):
    # randomerr = random.randint(0, 2)
    rsleeptime = random.uniform(7.5, 12.99)
    result = f"[ {item.id} ] slept for {rsleeptime} seconds."
    await asyncio.sleep(rsleeptime)
    return result


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item: Item):
    return item
