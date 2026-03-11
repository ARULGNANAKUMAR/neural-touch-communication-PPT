import pickle

with open("robo_ai_db.bin", "rb") as f:
    db = pickle.load(f)

print("\n📊 DATABASE CHECK")
print("Samples:", len(db["sample_data"]))
print("Memories:", len(db["model_memory"]))
