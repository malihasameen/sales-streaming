from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from enum import Enum, unique, IntEnum
from kafka import KafkaProducer
import datetime as dt
import json

PER_UNIT_PRICE = 300.0

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['172.18.0.4:9092'],
    value_serializer=serializer
)

class Customer(IntEnum, Enum):
    id1 = 1
    id2 = 2
    id3 = 3
    id4 = 4
    id5 = 5
    id6 = 6
    id7 = 7
    id8 = 8
    id9 = 9
    id10 = 10
    id11 = 11
    id12 = 12
    id13 = 13
    id14 = 14
    id15 = 15
    id16 = 16
    id17 = 17

class Source(str, Enum):
    Dine_In = "Dine In"
    Takeaway = "Takeaway"
    Home_Delivery = "Home Delivery"
    
class OrderItem(BaseModel):
    customer_id: Customer
    source: Source
    quantity: int

app = FastAPI()

@app.post("/orderitem", status_code=status.HTTP_201_CREATED)
async def create_order(item: OrderItem):
    item = json.loads(item.json())
    item['total'] = item['quantity'] * PER_UNIT_PRICE
    item['created_at'] = dt.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    
    producer.send("Order", value=item)

    return {"status": "success", "message":"Stock entry created"}
