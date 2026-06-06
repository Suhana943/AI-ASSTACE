
import json
import os
import google.generativeai as genai
from datetime import datetime

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
# Fix: 'gemini-3.5-flash' invalid hai, isliye 'gemini-1.5-flash' use karein
model = genai.GenerativeModel('gemini-3.5-flash')

# 2. Prompt (Image aur Amazon Link ke saath)
prompt = """
Ek naye trending laptop ka professional review likho.
Output ONLY JSON format, koi extra text nahi.
Structure:
{
    "title": "String",
    "image_url": "URL of a product image",
    "amazon_link": "Amazon product link",
    "intro": "String (Short para)",
    "specs": {"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "...", "Weight": "..."},
    "pros": ["Point 1", "Point 2", "Point 3"],
    "cons": ["Point 1", "Point 2", "Point 3"],
    "verdict_intro": "String",
    "who_should_buy": "String",
    "pro_tip": "String",
    "rating": "4.5/5"
}
"""

try:
    # 3. Content generation
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(json_text)

    # 4. Dynamic HTML components
    specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
    pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
    cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])

    # 5. HTML Template (Image aur Buy Button ke saath)
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>{data['title']} - Review</title>
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

        <div class="verdict">
            <h3>⚖️ Final Verdict</h3>
            <p>{data['verdict_intro']}</p>
            <p><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</p>
            <p><strong>Rating: {data['rating']}</strong></p>
        </div>
    </div>
</body>
</html>"""

    # 6. File Save
    if not os.path.exists('reviews'): os.makedirs('reviews')
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"reviews/laptop-{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Success! File created: {filename}")

except Exception as e:
    print(f"Error: {e}")
