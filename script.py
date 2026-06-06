import json
import os
import google.generativeai as genai
from datetime import datetime

# API Setup
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Strict Prompt
prompt = """
Ek latest trending laptop ka data do. Output ONLY in JSON format. No text, no intro, no markdown. 
Format: {"title": "String", "price": "String", "oldPrice": "String", "image": "String", "amazonLink": "String", "discount": "String"}
"""

try:
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    
    # Parse the data
    laptop = json.loads(json_text)
    
    # Prepare HTML content
    # Using a timestamp to ensure every review file has a unique name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reviews/review_{timestamp}.html"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{laptop['title']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            img {{ max-width: 300px; display: block; margin-bottom: 10px; }}
            .price {{ color: green; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>{laptop['title']}</h1>
        <img src="{laptop['image']}" alt="{laptop['title']}">
        <p><strong>Discount:</strong> {laptop['discount']}</p>
        <p class="price">Price: {laptop['price']} <strike>{laptop['oldPrice']}</strike></p>
        <a href="{laptop['amazonLink']}" target="_blank" style="padding: 10px; background: orange; color: white; text-decoration: none; border-radius: 5px;">View on Amazon</a>
    </body>
    </html>
    """

    # Save HTML file
    if not os.path.exists('reviews'): os.makedirs('reviews')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Success! Review saved at: {filename}")

except Exception as e:
    print(f"FATAL ERROR: {e}")
    
