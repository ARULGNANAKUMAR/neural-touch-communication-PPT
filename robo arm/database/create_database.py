import pickle
import os
from datetime import datetime

DB_FILE = "robo_ai_db.bin"

# ---------------------------
# Initialize DB
# ---------------------------
def init_db():
    if not os.path.exists(DB_FILE):
        db = {
            "sample_data": [],
            "ui_logs": [],
            "model_memory": []
        }
        with open(DB_FILE, "wb") as f:
            pickle.dump(db, f)
        print("Database created ✅")
    else:
        print("Database already exists 👍")

# ---------------------------
# Load DB
# ---------------------------
def load_db():
    with open(DB_FILE, "rb") as f:
        return pickle.load(f)

# ---------------------------
# Save DB
# ---------------------------
def save_db(db):
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)

# ---------------------------
# Save Sensor Sample Data
# ---------------------------
def save_sample(data):
    db = load_db()
    data["timestamp"] = str(datetime.now())
    db["sample_data"].append(data)
    save_db(db)
    print("Sample saved 💾")

# ---------------------------
# Save UI Interaction Data
# ---------------------------
def save_ui_log(action):
    db = load_db()
    log = {
        "action": action,
        "time": str(datetime.now())
    }
    db["ui_logs"].append(log)
    save_db(db)
    print("UI log saved 🖥️")

# ---------------------------
# Save AI Learning Memory
# ---------------------------
def save_memory(memory):
    db = load_db()
    db["model_memory"].append(memory)
    save_db(db)
    print("AI memory stored 🧠")

# ---------------------------
# Read Stats
# ---------------------------
def show_stats():
    db = load_db()
    print("\n📊 DATABASE STATS")
    print("Samples:", len(db["sample_data"]))
    print("UI Logs:", len(db["ui_logs"]))
    print("Memories:", len(db["model_memory"]))


# ---------------------------
# MAIN DEMO
# ---------------------------
if __name__ == "__main__":
    init_db()

    # Example sensor data
    sample = {
        "temperature": 37.5,
        "pulse": 95,
        "stress": "MEDIUM",
        "servo1": 120,
        "servo2": 60,
        "servo3": 90,
        "servo4": 150
    }

    save_sample(sample)
    save_ui_log("Joystick moved LEFT")
    save_memory({"reward": 0.8, "state": "safe_mode"})

    show_stats()
