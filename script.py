import json
import os
import google.generativeai as genai

# API Setup
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash-latest')

# Strict Prompt
prompt = """
Ek latest trending laptop ka data do. Output ONLY in JSON format. No text, no intro, no markdown. 
Format: {"title": "String", "price": "String", "oldPrice": "String", "image": "String", "amazonLink": "String", "discount": "String"}
"""

try:
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    
    # DEBUG LOG
    print(f"DEBUG AI RESPONSE: {json_text}")
    
    new_laptop = json.loads(json_text)
except Exception as e:
    print(f"FATAL ERROR: AI Response is invalid. {e}")
    exit(1) # Error ke saath band karo taaki action stop ho jaye

# JSON file handle karna
json_file = 'laptops.json'
laptops = []

if os.path.exists(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():
                laptops = json.loads(content)
    except:
        laptops = []

# Insert and Limit
laptops.insert(0, new_laptop)
if len(laptops) > 30: laptops = laptops[:30]

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=2, ensure_ascii=False)

# HTML Reviews generation (Same logic as before)
if not os.path.exists('reviews'): os.makedirs('reviews')
for i, lap in enumerate(laptops):
    with open(f'reviews/review_{i}.html', 'w', encoding='utf-8') as f:
        f.write(f"<html><body><h1>{lap['title']}</h1><a href='{lap['amazonLink']}'>Buy Now</a></body></html>")

print("Update Successful!")
