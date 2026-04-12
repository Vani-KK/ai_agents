import json
import os
from datetime import datetime

# This is where long term memories are saved
MEMORY_FILE = "memory.json"

def load_memories() -> dict:
    """
    Load long term memories from disk.
    Returns empty dict if no memories exist yet.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(key: str, value: str):
    """
    Save a specific fact to long term memory.
    Example: save_memory("user_name", "Vani")
    """
    memories = load_memories()
    memories[key] = {
        "value": value,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)
    print(f"Memory saved: {key} = {value}")

def get_memory(key: str) -> str:
    """
    Retrieve a specific memory by key.
    Returns None if not found.
    """
    memories = load_memories()
    if key in memories:
        return memories[key]["value"]
    return None

def get_all_memories() -> str:
    """
    Returns all memories as a formatted string.
    This gets injected into the agent's context.
    """
    memories = load_memories()
    
    if not memories:
        return "No long term memories stored yet."
    
    formatted = "Known facts about the user:\n"
    for key, data in memories.items():
        formatted += f"- {key}: {data['value']}\n"
    
    return formatted

def clear_memories():
    """Delete all long term memories."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print("All memories cleared.")

