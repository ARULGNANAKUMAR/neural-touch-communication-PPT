import random
import time
from database import init_db, insert_data

init_db()

while True:
    temperature = round(random.uniform(30, 42), 2)
    pulse = random.randint(70, 130)

    stress = "NORMAL"
    if pulse > 110 or temperature > 38:
        stress = "HIGH"
    elif pulse > 90:
        stress = "MEDIUM"

    data = {
        "temperature": temperature,
        "pulse": pulse,
        "stress": stress,
        "servo1": random.randint(0, 180),
        "servo2": random.randint(0, 180),
        "servo3": random.randint(0, 180),
        "servo4": random.randint(0, 180)
    }

    insert_data(data)
    print("Inserted:", data)
    time.sleep(1)
