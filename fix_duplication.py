
import os

file_path = r'c:\Users\Admin\Downloads\ai-news-site\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: The bad row (02.09)
bad_start_pattern = '<div class="week-row"><div class="time-label"><span class="time-date">02.09</span>'

# Pattern 2: The good row (02.06)
good_start_pattern = '<div class="week-row"><div class="time-label"><span class="time-date">02.06</span>'

# Find indices
start_idx = content.find(bad_start_pattern)
end_idx = content.find(good_start_pattern)

if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
    print(f"Found bad row at {start_idx} and good row at {end_idx}")
    # Remove the bad row
    new_content = content[:start_idx] + content[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed duplication.")
else:
    print("Could not find the expected patterns or order is wrong.")
    print(f"Start index: {start_idx}")
    print(f"End index: {end_idx}")

