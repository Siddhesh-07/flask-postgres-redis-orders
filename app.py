from flask import Flask
import psycopg2
from redis import Redis

app = Flask(__name__)
redis_client = Redis(host='redis', port=6379)

conn = psycopg2.connect(
    host='postgres',
    database='ordersdb',
    user='postgres',
    password='postgres123'
)

