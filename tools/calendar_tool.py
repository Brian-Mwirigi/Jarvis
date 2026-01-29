"""
Calendar Tool for Jarvis
Google Calendar integration
"""
from langchain.tools import tool
import os
import logging
from datetime import datetime, timedelta
import json


# Simple JSON-based calendar for offline use
# For Google Calendar, you'd use google-api-python-client
CALENDAR_FILE = os.path.join(os.path.expanduser("~"), ".jarvis", "calendar.json")
os.makedirs(os.path.dirname(CALENDAR_FILE), exist_ok=True)


def load_calendar():
    """Load calendar from file"""
    if os.path.exists(CALENDAR_FILE):
        try:
            with open(CALENDAR_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_calendar(calendar_data):
    """Save calendar to file"""
    try:
        with open(CALENDAR_FILE, 'w') as f:
            json.dump(calendar_data, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Calendar save error: {e}")
        return False


@tool
def add_calendar_event(title: str, date: str, time: str = "09:00", duration_minutes: int = 60) -> str:
    """
    Add an event to the calendar.
    
    Args:
        title: Event title/description
        date: Date in format YYYY-MM-DD or relative (today, tomorrow)
        time: Time in HH:MM format (default: 09:00)
        duration_minutes: Event duration in minutes (default: 60)
    
    Examples:
        - "Add meeting tomorrow at 3pm"
        - "Schedule doctor appointment on 2025-11-15 at 10:00"
        - "Add event 'Team standup' today at 09:30"
    
    Returns:
        Confirmation message
    """
    try:
        # Parse relative dates
        if date.lower() == "today":
            event_date = datetime.now().strftime("%Y-%m-%d")
        elif date.lower() == "tomorrow":
            event_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            event_date = date
        
        # Create event
        calendar = load_calendar()
        event_id = f"{event_date}_{time}_{title}"
        
        calendar[event_id] = {
            "title": title,
            "date": event_date,
            "time": time,
            "duration_minutes": duration_minutes,
            "created_at": datetime.now().isoformat()
        }
        
        if save_calendar(calendar):
            return f"✅ Added '{title}' to calendar on {event_date} at {time}"
        else:
            return "❌ Failed to add event to calendar"
            
    except Exception as e:
        logging.error(f"Calendar add error: {e}")
        return f"❌ Failed to add event: {str(e)}"


@tool
def check_schedule(date: str = "today") -> str:
    """
    Check calendar schedule for a specific date.
    
    Args:
        date: Date to check (today, tomorrow, or YYYY-MM-DD)
    
    Examples:
        - "What's on my calendar today?"
        - "Do I have any events tomorrow?"
        - "Check my schedule for Friday"
        - "What's my schedule on 2025-11-15?"
    
    Returns:
        List of events for that date
    """
    try:
        # Parse date
        if date.lower() == "today":
            check_date = datetime.now().strftime("%Y-%m-%d")
        elif date.lower() == "tomorrow":
            check_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            # Try to parse various formats
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                check_date = dt.strftime("%Y-%m-%d")
            except:
                check_date = date
        
        # Load calendar and filter events
        calendar = load_calendar()
        events = []
        
        for event_id, event in calendar.items():
            if event["date"] == check_date:
                events.append(f"• {event['time']} - {event['title']} ({event['duration_minutes']} min)")
        
        if events:
            day_name = datetime.strptime(check_date, "%Y-%m-%d").strftime("%A, %B %d, %Y")
            return f"📅 Schedule for {day_name}:\n" + "\n".join(sorted(events))
        else:
            return f"📅 No events scheduled for {check_date}"
            
    except Exception as e:
        logging.error(f"Calendar check error: {e}")
        return f"❌ Failed to check schedule: {str(e)}"


@tool
def list_upcoming_events(days: int = 7) -> str:
    """
    List all upcoming events in the next N days.
    
    Args:
        days: Number of days to look ahead (default: 7)
    
    Examples:
        - "What events do I have this week?"
        - "Show me upcoming events"
        - "What's coming up in my calendar?"
    
    Returns:
        List of upcoming events
    """
    try:
        calendar = load_calendar()
        today = datetime.now()
        future_date = today + timedelta(days=days)
        
        events = []
        for event_id, event in calendar.items():
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            if today <= event_date <= future_date:
                day_name = event_date.strftime("%A, %b %d")
                events.append((event_date, f"• {day_name} at {event['time']} - {event['title']}"))
        
        # Sort by date
        events.sort(key=lambda x: x[0])
        
        if events:
            return f"📅 Upcoming events (next {days} days):\n" + "\n".join([e[1] for e in events])
        else:
            return f"📅 No upcoming events in the next {days} days"
            
    except Exception as e:
        logging.error(f"Calendar list error: {e}")
        return f"❌ Failed to list events: {str(e)}"


@tool
def delete_calendar_event(title: str, date: str) -> str:
    """
    Delete an event from the calendar.
    
    Args:
        title: Event title to delete
        date: Date of the event (YYYY-MM-DD or relative)
    
    Examples:
        - "Cancel meeting tomorrow"
        - "Delete event 'Doctor appointment' on 2025-11-15"
    
    Returns:
        Confirmation message
    """
    try:
        # Parse date
        if date.lower() == "today":
            event_date = datetime.now().strftime("%Y-%m-%d")
        elif date.lower() == "tomorrow":
            event_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            event_date = date
        
        calendar = load_calendar()
        deleted = False
        
        # Find and delete matching events
        to_delete = []
        for event_id, event in calendar.items():
            if event["date"] == event_date and title.lower() in event["title"].lower():
                to_delete.append(event_id)
        
        for event_id in to_delete:
            del calendar[event_id]
            deleted = True
        
        if deleted:
            save_calendar(calendar)
            return f"✅ Deleted event(s) matching '{title}' on {event_date}"
        else:
            return f"❌ No events found matching '{title}' on {event_date}"
            
    except Exception as e:
        logging.error(f"Calendar delete error: {e}")
        return f"❌ Failed to delete event: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Testing calendar...")
    
    # Add event
    result = add_calendar_event.invoke({"title": "Team Meeting", "date": "today", "time": "14:00"})
    print(result)
    
    # Check schedule
    result = check_schedule.invoke({"date": "today"})
    print(result)
