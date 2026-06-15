import json
from datetime import datetime
 
def save_memory(command,reply):
    data={
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "reply": reply
    }
    try:
        with open("mem.json", "r") as file:
            memory = json.load(file)
    except FileNotFoundError:
        memory = []
    memory.append(data)
    with open("mem.json", "w") as file:
        json.dump(memory, file, indent=4)
    
def load_memory():
    try:
        with open("mem.json", "r") as file:
            memory = json.load(file)
            if memory:
                return memory[-1]

            return memory
    except :
        return None