import random
import time
import pandas as pd

data_log = []

def generate_data():
    # Sensors
    temperature = round(random.uniform(28, 45), 2)  # DHT11
    pulse = random.randint(60, 140)  # Heart sensor
    
    # Joystick
    joystick_x = random.randint(0, 1023)
    joystick_y = random.randint(0, 1023)

    # Stress logic
    stress = "NORMAL"
    if pulse > 110 or temperature > 38:
        stress = "HIGH"
    elif pulse > 90:
        stress = "MEDIUM"

    # Servo motor angles
    servo1 = random.randint(0, 180)
    servo2 = random.randint(0, 180)
    servo3 = random.randint(0, 180)
    servo4 = random.randint(0, 180)

    # Alerts
    led_red = stress == "HIGH"
    led_yellow = stress == "MEDIUM"
    led_green = stress == "NORMAL"

    buzzer = stress == "HIGH"
    fan = temperature > 35
    vibration = stress == "HIGH"

    return {
        "temperature": temperature,
        "pulse": pulse,
        "joystick_x": joystick_x,
        "joystick_y": joystick_y,
        "stress": stress,
        "servo1": servo1,
        "servo2": servo2,
        "servo3": servo3,
        "servo4": servo4,
        "fan_on": fan,
        "buzzer_on": buzzer,
        "vibration_on": vibration,
        "led_red": led_red,
        "led_yellow": led_yellow,
        "led_green": led_green
    }

# Run simulation
for i in range(50):  # 50 samples
    data = generate_data()
    data_log.append(data)
    print(data)
    time.sleep(0.5)

# Save dataset
df = pd.DataFrame(data_log)
df.to_csv("esp32_simulated_data.csv", index=False)

print("\n✅ Dataset saved as esp32_simulated_data.csv")
