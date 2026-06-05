import os
import json
import google.generativeai as genai
from datetime import datetime

# API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 1. AI Prompt (Aapke format ke hisaab se)
prompt = """
Ek latest trending laptop ka data do. Output sirf valid JSON format mein hona chahiye, koi extra text nahi.
JSON keys ye honi chahiye: "title", "price", "oldPrice", "image", "amazonLink", "discount".
Dhyan rakhein ki price aur oldPrice mein comma (,) ho aur discount mein '% OFF' likha ho.
"""

# 2. Response generate aur clean karna
response = model.generate_content(prompt)
json_text = response.text.replace("```json", "").replace("
```", "").strip()
new_laptop = json.loads(json_text)

# 3. laptops.json update karna
json_file = 'laptops.json'

if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            laptops = json.load(f)
        except:
            laptops = []
else:
    laptops = []

# Naya data list mein add karein
laptops.insert(0, new_laptop)

# File save karein
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=2, ensure_ascii=False)

print("laptops.json successfully updated!")

