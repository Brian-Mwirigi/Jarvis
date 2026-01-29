"""
Initialize Day 21 of the AI learning project
Run this to set up the journal with today's accomplishments
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from tools.journal import log_project_day

# Day 21 accomplishments - Natural sentence format
accomplishments = "integrated vision systems, memory core, and neural logs"

print("Initializing Day 21...")
result = log_project_day.invoke({
    "day_number": 21,
    "accomplishments": accomplishments
})

print(f"✅ {result}")
print("\nNow you can ask Jarvis:")
print('  - "What day are we on?"')
print('  - "What did we do today?"')
print('  - "What did we add today?"')

