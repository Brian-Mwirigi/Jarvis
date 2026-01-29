"""
Development Journal for Jarvis - Track project progress day by day
"""
from langchain.tools import tool
import json
import os
from datetime import datetime
import logging

# Journal file location
JOURNAL_DIR = os.path.join(os.path.expanduser("~"), ".jarvis")
JOURNAL_FILE = os.path.join(JOURNAL_DIR, "development_journal.json")
os.makedirs(JOURNAL_DIR, exist_ok=True)

def load_journal():
    """Load the development journal"""
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading journal: {e}")
            return {}
    return {}

def save_journal(journal_data):
    """Save the development journal"""
    try:
        with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(journal_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error saving journal: {e}")
        return False


@tool
def log_project_day(day_number: int, accomplishments: str) -> str:
    """
    Log what was accomplished on a specific day of the AI learning project.
    Use this to record daily progress, features added, or milestones reached.
    
    Args:
        day_number: The day number (e.g., 21 for "Day 21")
        accomplishments: What was done on that day
    
    Examples:
        - "Today is day 21, we added vision capabilities"
        - "Day 15: Implemented speech recognition"
        - "Day 30: Added memory system"
    
    Returns:
        Confirmation message
    """
    try:
        journal = load_journal()
        
        day_key = f"day_{day_number}"
        journal[day_key] = {
            "day": day_number,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "accomplishments": accomplishments,
            "timestamp": datetime.now().isoformat()
        }
        
        if save_journal(journal):
            return f"Day {day_number} logged to neural archive."
        else:
            return "Memory write failed."
            
    except Exception as e:
        logging.error(f"Journal logging error: {e}")
        return f"Error logging day: {e}"


@tool
def get_project_day() -> str:
    """
    Get the current day number of the AI learning project.
    
    Returns:
        Current day number and summary
    """
    try:
        journal = load_journal()
        
        if not journal:
            return "No project days logged yet. Start by saying: 'Today is day 1 of learning AI'"
        
        # Find the highest day number
        day_numbers = [int(key.split('_')[1]) for key in journal.keys() if key.startswith('day_')]
        
        if not day_numbers:
            return "No project days found"
        
        current_day = max(day_numbers)
        
        return f"We are on day {current_day} of learning AI, sir."
        
    except Exception as e:
        logging.error(f"Error getting project day: {e}")
        return f"Error retrieving day: {e}"


@tool
def get_day_accomplishments(day_number: int) -> str:
    """
    Get what was accomplished on a specific day.
    
    Args:
        day_number: Which day to retrieve (e.g., 21)
    
    Returns:
        Accomplishments for that day
    """
    try:
        journal = load_journal()
        day_key = f"day_{day_number}"
        
        if day_key not in journal:
            return f"No entry found for Day {day_number}"
        
        day_info = journal[day_key]
        
        # Shorter response
        accomplishments = day_info['accomplishments']
        if len(accomplishments) > 100:
            accomplishments = accomplishments[:97] + "..."
        
        return f"Archive entry {day_number}: {accomplishments}"
        
    except Exception as e:
        logging.error(f"Error getting day accomplishments: {e}")
        return f"Error: {e}"


@tool
def get_today_summary() -> str:
    """
    Get what was accomplished today (most recent entry).
    Use this when user asks "what did we do today?"
    
    Returns:
        Today's accomplishments
    """
    try:
        journal = load_journal()
        
        if not journal:
            return "No entries logged yet"
        
        # Get most recent entry
        day_numbers = sorted([int(key.split('_')[1]) for key in journal.keys() if key.startswith('day_')], reverse=True)
        
        if not day_numbers:
            return "No entries found"
        
        latest_day = day_numbers[0]
        day_key = f"day_{latest_day}"
        day_info = journal[day_key]
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get full accomplishments
        accomplishments = day_info['accomplishments']
        
        if day_info['date'] == today:
            return f"Today we {accomplishments}"
        else:
            return f"On day {latest_day}, we {accomplishments}"
        
    except Exception as e:
        logging.error(f"Error getting today summary: {e}")
        return f"Error: {e}"


@tool
def get_project_summary() -> str:
    """
    Get a summary of the entire AI learning project.
    Shows all days and accomplishments.
    
    Returns:
        Full project timeline
    """
    try:
        journal = load_journal()
        
        if not journal:
            return "No project history yet"
        
        # Sort by day number
        day_numbers = sorted([int(key.split('_')[1]) for key in journal.keys() if key.startswith('day_')])
        
        summary = f"🚀 AI Learning Journey - {len(day_numbers)} days logged:\n\n"
        
        for day_num in day_numbers:
            day_key = f"day_{day_num}"
            day_info = journal[day_key]
            summary += f"Day {day_num}: {day_info['accomplishments']}\n"
        
        return summary
        
    except Exception as e:
        logging.error(f"Error getting project summary: {e}")
        return f"Error: {e}"


# Quick test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 Testing Journal System:")
    
    print("\n1. Logging Day 21...")
    result = log_project_day.invoke({
        "day_number": 21,
        "accomplishments": "Added vision capabilities with BLIP-2 camera and screen analysis"
    })
    print(f"   {result}")
    
    print("\n2. Getting current day...")
    result = get_project_day.invoke({})
    print(f"   {result}")
    
    print("\n3. Getting Day 21 accomplishments...")
    result = get_day_accomplishments.invoke({"day_number": 21})
    print(f"   {result}")
    
    print("\n4. Getting today's summary...")
    result = get_today_summary.invoke({})
    print(f"   {result}")
    
    print("\n✅ Journal system working!")

