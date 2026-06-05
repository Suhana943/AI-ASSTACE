import json
import os
import google.generativeai as genai

# API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 1. AI se data mangna
prompt = "Ek latest trending laptop ka data do (JSON keys: title, price, oldPrice, image, amazonLink, discount)."
response = model.generate_content(prompt)
json_text = response.text.replace("```json", "").replace("```", "").strip()
new_laptop = json.loads(json_text)

# 2. JSON Update karna
json_file = 'laptops.json'
laptops = []
if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        try: laptops = json.load(f)
        except: laptops = []
laptops.insert(0, new_laptop)

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=2, ensure_ascii=False)

# 3. HTML Review file banana (Professional Design)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .price { color: green; font-weight: bold; }
        .discount { background: red; color: white; padding: 2px 5px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Latest Laptop Reviews</h1>
"""

for lap in laptops:
    html_content += f"""
    <div class="card">
        <h2>{lap['title']}</h2>
        <p>Price: <span class="price">{lap['price']}</span> <strike>{lap['oldPrice']}</strike></p>
        <p class="discount">{lap['discount']}</p>
        <a href="{lap['amazonLink']}" target="_blank">Check on Amazon</a>
    </div>
    """

html_content += "</body></html>"

with open('review.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("JSON aur HTML dono update ho gaye!")
