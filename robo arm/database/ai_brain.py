import random
import pickle
import os
from datetime import datetime

DB_FILE = "robo_ai_db.bin"

# ================================
# DATABASE INIT
# ================================
def init_db():
    if not os.path.exists(DB_FILE):
        db = {
            "sample_data": [],
            "model_memory": []
        }
        with open(DB_FILE, "wb") as f:
            pickle.dump(db, f)

def load_db():
    with open(DB_FILE, "rb") as f:
        return pickle.load(f)

def save_db(db):
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)

init_db()

# ================================
# AI CLASS
# ================================
class FullRoboAI:
    def __init__(self):
        self.db = load_db()

    # ----------------------------
    # SAVE SENSOR DATA
    # ----------------------------
    def store_sensor(self, temp, pulse):
        entry = {
            "temperature": temp,
            "pulse": pulse,
            "time": str(datetime.now())
        }
        self.db["sample_data"].append(entry)
        save_db(self.db)

    # ----------------------------
    # STATE DETECTION
    # ----------------------------
    def get_state(self, temp, pulse):
        if temp > 39 or pulse > 115:
            return "DANGER"
        elif temp > 37 or pulse > 95:
            return "STRESS"
        return "NORMAL"

    # ----------------------------
    # FUTURE RISK PREDICTION
    # ----------------------------
    def predict_risk(self):
        data = self.db["sample_data"]
        if len(data) < 5:
            return 0

        last = data[-5:]
        avg_temp = sum(x["temperature"] for x in last) / 5
        avg_pulse = sum(x["pulse"] for x in last) / 5

        risk = 0
        if avg_temp > 38: risk += 50
        if avg_pulse > 100: risk += 50
        return risk

    # ----------------------------
    # ACTION DECISION
    # ----------------------------
    def choose_action(self, state, risk):
        if risk > 70:
            return "PREVENT_COOL"
        if state == "DANGER":
            return "COOL"
        if state == "STRESS":
            return "CALM_MODE"
        return "NORMAL_MODE"

    # ----------------------------
    # BASE REWARD
    # ----------------------------
    def base_reward(self, action):
        rewards = {
            "PREVENT_COOL": 1.2,
            "COOL": 1.0,
            "CALM_MODE": 0.6,
            "NORMAL_MODE": 0.3
        }
        return rewards.get(action, 0)

    # ----------------------------
    # USER FEEDBACK SYSTEM
    # ----------------------------
    def apply_feedback(self, action, feedback):
        score_map = {"GOOD": 1, "PARTIAL": 0.5, "BAD": -1}
        score = score_map.get(feedback.upper(), 0)

        entry = {
            "action": action,
            "feedback": feedback,
            "score": score,
            "time": str(datetime.now())
        }

        self.db["model_memory"].append(entry)
        save_db(self.db)
        return score

    # ----------------------------
    # REWARD ADJUST
    # ----------------------------
    def adjust_reward(self, base, feedback_score):
        return base + (feedback_score * 0.5)

    # ----------------------------
    # SELF LEARNING INSIGHTS
    # ----------------------------
    def self_insight(self):
        data = self.db["sample_data"]
        if len(data) < 10:
            return "Learning user patterns..."

        avg_temp = sum(x["temperature"] for x in data[-10:]) / 10
        avg_pulse = sum(x["pulse"] for x in data[-10:]) / 10

        if avg_temp > 38:
            return "Frequent overheating pattern detected."
        if avg_pulse > 100:
            return "User stress trend detected."
        return "User condition stable."

    # ----------------------------
    # CHAT OUTPUT
    # ----------------------------
    def chat_output(self, state, action, risk):
        if risk > 70:
            return "⚠ I predict a health risk soon. Activating preventive cooling."
        if state == "DANGER":
            return "🚨 High stress detected! Cooling immediately."
        if state == "STRESS":
            return "⚠ Mild stress detected. Switching to calm mode."
        return "✅ All vitals normal."

    # ----------------------------
    # MAIN AI THINK
    # ----------------------------
    def think(self, temp, pulse):
        self.store_sensor(temp, pulse)

        state = self.get_state(temp, pulse)
        risk = self.predict_risk()
        action = self.choose_action(state, risk)

        # Reinforcement Learning
        base = self.base_reward(action)

        # Simulated feedback (later UI la varum)
        feedback = random.choice(["GOOD", "PARTIAL", "BAD"])
        feedback_score = self.apply_feedback(action, feedback)

        final_reward = self.adjust_reward(base, feedback_score)

        insight = self.self_insight()
        chat = self.chat_output(state, action, risk)

        # Save decision memory
        decision = {
            "state": state,
            "risk": risk,
            "action": action,
            "reward": final_reward,
            "time": str(datetime.now())
        }
        self.db["model_memory"].append(decision)
        save_db(self.db)

        return {
            "state": state,
            "risk": risk,
            "action": action,
            "chat": chat,
            "feedback": feedback,
            "reward": final_reward,
            "insight": insight
        }

# ================================
# DEMO RUN
# ================================
if __name__ == "__main__":
    ai = FullRoboAI()

    # Simulated Sensors
    temperature = round(random.uniform(35, 42), 2)
    pulse = random.randint(70, 130)

    result = ai.think(temperature, pulse)

    print("\n🧠 FULL AI OUTPUT")
    print("Temp:", temperature)
    print("Pulse:", pulse)
    print("State:", result["state"])
    print("Risk:", result["risk"], "%")
    print("Action:", result["action"])
    print("AI Says:", result["chat"])
    print("Feedback:", result["feedback"])
    print("Reward:", result["reward"])
    print("Insight:", result["insight"])
