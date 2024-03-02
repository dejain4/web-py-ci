import time
from datetime import datetime
from os import getenv

import redis
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
context = {"start_time": datetime.now()}

# Load environment variables from .env file
load_dotenv()

redis_host = getenv("REDIS_HOST", "redis")
redis_port = int(getenv("REDIS_PORT", 6379))


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/health")
def health():
    return "Ok", 200


@app.route("/redis-hits")
def redis_hits():
    if "redis" not in context:
        # Create a Redis connection
        context["redis"] = redis.Redis(
            host=redis_host, port=redis_port, socket_connect_timeout=5
        )
    cache = context["redis"]
    retries = 5
    while True:
        try:
            # Increment and return the number of hits in Redis cache
            return "Redis hits " + str(cache.incr("hits"))
        except redis.exceptions.ConnectionError:
            if retries == 0:
                return "No response from Redis"
            retries -= 1
            time.sleep(0.5)
