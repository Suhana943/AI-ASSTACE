import json
import os
import google.generativeai as genai
from datetime import datetime

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

HISTORY_FILE = "reviewed_laptops.txt"

# 2. History Load karna
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

reviewed_list = get_history()
exclude_string = ", ".join(reviewed_list) if reviewed_list else "None"

# 3. Prompt (Excluded list ke sath)
prompt = f"""
Write a professional review for a popular trending laptop.
IMPORTANT: Do NOT review any of these laptops: {exclude_string}.
Output ONLY JSON format, no extra text.
Structure:
{{
    "title": "...",
    "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=600",
    "amazon_link": "https://www.amazon.in/",
    "intro": "Write a 3-sentence intro.",
    "specs": {{"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "..."}},
    "pros": ["...", "..."],
    "cons": ["...", "..."],
    "verdict_intro": "...",
    "pro_tip": "...",
    "rating": "4.5/5"
}}
"""

try:
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(json_text)
    
    laptop_name = data['title']

    # 4. HTML Components
    specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
    pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
    cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])

    # 5. HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>{data['title']} - Professional Review</title>
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; }}
        .product-img {{ width: 100%; max-width: 400px; display: block; margin: 20px auto; border-radius: 10px; }}
        .buy-btn {{ display: block; width: 220px; margin: 20px auto; padding: 15px; background: #ff9f00; color: white; text-align: center; text-decoration: none; font-weight: bold; border-radius: 8px; }}
        .spec-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .spec-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .pros {{ background: #e8f5e9; padding: 20px; margin: 20px 0; }}
        .cons {{ background: #ffebee; padding: 20px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" class="product-img">
        <a href="{data['amazon_link']}" class="buy-btn" target="_blank">🛒 Buy Now on Amazon</a>
        <p>{data['intro']}</p>
        <h2>📋 Specifications</h2>
        <table class="spec-table">{specs_html}</table>
        <div class="pros"><h3>✅ Pros</h3><ul>{pros_html}</ul></div>
        <div class="cons"><h3>❌ Cons</h3><ul>{cons_html}</ul></div>
        <h3>⚖️ Verdict</h3>
        <p>{data['verdict_intro']}</p>
        <p><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</p>
        <p><strong>Rating: {data['rating']}</strong></p>
    </div>
</body>
</html>"""

    # 6. Save File
    if not os.path.exists('reviews'): os.makedirs('reviews')
    filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 7. Update History
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{laptop_name}\n")
    
    print(f"Success! Review saved: {filename}")
    print(f"Added {laptop_name} to history.")

except Exception as e:
    print(f"Error: {e}")
