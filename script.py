import json
import os
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 2. AI se data mangna
prompt = "Ek latest trending laptop ka data do (JSON keys: title, price, oldPrice, image, amazonLink, discount)."
response = model.generate_content(prompt)
json_text = response.text.replace("```json", "").replace("```", "").strip()

try:
    new_laptop = json.loads(json_text)
except:
    print("AI response invalid tha, script stop ho rahi hai.")
    exit(1)

# 3. Laptops.json read aur update
json_file = 'laptops.json'
laptops = []

if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            if content.strip():
                laptops = json.loads(content)
        except:
            laptops = []

# Naya laptop insert karein aur limit rakhein (max 50)
laptops.insert(0, new_laptop)
if len(laptops) > 50:
    laptops = laptops[:50]

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=2, ensure_ascii=False)

# 4. Review folder aur files banana
if not os.path.exists('reviews'):
    os.makedirs('reviews')

for i, lap in enumerate(laptops):
    review_html = f"""
    <html>
    <head><title>{lap['title']}</title></head>
    <body>
        <h1>{lap['title']}</h1>
        <p>Price: {lap['price']} <strike>{lap['oldPrice']}</strike></p>
        <p>Discount: {lap['discount']}</p>
        <a href="{lap['amazonLink']}" target="_blank">Buy on Amazon</a><br>
        <a href="../review.html">Back to Home</a>
    </body></html>
    """
    with open(f'reviews/review_{i}.html', 'w', encoding='utf-8') as f:
        f.write(review_html)

# 5. Main review.html update karna
html_content = """
<!DOCTYPE html>
<html>
<head><style>.card{border:1px solid #ccc; padding:10px; margin:10px;}</style></head>
<body>
    <h1>Trending Laptops</h1>
"""

for i, lap in enumerate(laptops):
    html_content += f"""
    <div class="card">
        <h3>{lap['title']}</h3>
        <a href="reviews/review_{i}.html">Learn More</a> | 
        <a href="{lap['amazonLink']}" target="_blank">Buy Now</a>
    </div>
    """

html_content += "</body></html>"

with open('review.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Process success!")

