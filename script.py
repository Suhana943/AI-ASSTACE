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
if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        try: laptops = json.load(f)
        except: laptops = []
else:
    laptops = []

laptops.insert(0, new_laptop)

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=2, ensure_ascii=False)

# 3. Reviews folder banana aur har laptop ke liye HTML file generate karna
if not os.path.exists('reviews'):
    os.makedirs('reviews')

for i, lap in enumerate(laptops):
    review_html = f"""
    <html><body>
        <h1>Full Review: {lap['title']}</h1>
        <p>Price: {lap['price']} <strike>{lap['oldPrice']}</strike></p>
        <p>Discount: {lap['discount']}</p>
        <a href="{lap['amazonLink']}" target="_blank">Buy Now on Amazon</a>
        <br><br>
        <a href="../review.html">Go Back to Home</a>
    </body></html>
    """
    with open(f'reviews/review_{i}.html', 'w', encoding='utf-8') as f:
        f.write(review_html)

# 4. Main review.html update karna (Learn More link ke saath)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn { padding: 8px 15px; background: blue; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Latest Laptop Reviews</h1>
"""

for i, lap in enumerate(laptops):
    html_content += f"""
    <div class="card">
        <h2>{lap['title']}</h2>
        <a href="reviews/review_{i}.html" class="btn">Learn More</a>
        <a href="{lap['amazonLink']}" target="_blank">Buy Now</a>
    </div>
    """

html_content += "</body></html>"

with open('review.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("JSON, Review files aur Main Page update ho gaye!")
