import json
import os
import urllib.parse
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
# 'gemini-1.5-flash' सबसे स्टेबल और फास्ट है
model = genai.GenerativeModel('gemini-3.5-flash')

HISTORY_FILE = "reviewed_laptops.txt"
JSON_FILE = "laptops.json"

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f.readlines()]
    return []

# 2. Prompt Preparation
reviewed_list = get_history()
exclude_string = ", ".join(reviewed_list) if reviewed_list else "None"

prompt = f"""
Write a professional, trending laptop review in HINDI.
IMPORTANT: Do NOT review these: {exclude_string}.

INSTRUCTIONS:
1. Output ONLY JSON.
2. Price: Use Indian Rupees (Format: ₹XX,XXX).
3. Image: Return this exact image URL to ensure it never breaks: "https://placehold.co/800x400/png?text=Laptop+Review"
4. Amazon Link: Return exactly this: "https://www.amazon.in/s?k=laptop"

Structure (JSON only):
{{
    "title": "...",
    "image_url": "https://placehold.co/800x400/png?text=Laptop+Review",
    "amazon_link": "https://www.amazon.in/s?k=laptop",
    "price": "₹...",
    "oldPrice": "₹...",
    "discount": "...",
    "intro": "5 sentences in Hindi.",
    "specs": {{"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "..."}},
    "pros": ["...", "..."],
    "cons": ["...", "..."],
    "verdict_intro": "...",
    "pro_tip": "...",
    "rating": "..."
}}
"""

try:
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(json_text)
    
    laptop_name = data['title']
    # Amazon search link generator
    encoded_name = urllib.parse.quote(laptop_name)
    amazon_link = f"https://www.amazon.in/s?k={encoded_name}"

    if laptop_name.lower() in reviewed_list:
        print(f"Skipping {laptop_name}, already reviewed.")
    else:
        # HTML Content
        specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
        pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
        cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])

        html_content = f"""
        <!DOCTYPE html><html lang="hi"><head><meta charset="UTF-8"><title>{data['title']}</title></head>
        <body><h1>{data['title']}</h1><img src="{data['image_url']}" width="800">
        <p>Price: {data['price']}</p><a href="{amazon_link}">Buy on Amazon</a>
        <h3>Specs</h3><table>{specs_html}</table></body></html>
        """
        
        # Save HTML
        if not os.path.exists('reviews'): os.makedirs('reviews')
        filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Update Files
        with open(HISTORY_FILE, "a", encoding='utf-8') as f:
            f.write(f"{laptop_name}\n")
        
        laptops = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                laptops = json.load(f)

        laptops.append({
            "title": laptop_name,
            "price": data.get('price', '₹0'),
            "oldPrice": data.get('oldPrice', 'N/A'),
            "discount": data.get('discount', '0% OFF'),
            "image": data.get('image_url', ''),
            "amazonLink": amazon_link,
            "review_link": filename
        })

        # ensure_ascii=False is MANDATORY for Hindi text
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(laptops, f, indent=4, ensure_ascii=False)
        
        print(f"Success! {laptop_name} added.")

except Exception as e:
    print(f"Error: {e}")
        
