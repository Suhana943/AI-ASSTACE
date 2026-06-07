import json
import os
import urllib.parse
import google.generativeai as genai

# 1. Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')
JSON_FILE = "laptops.json"

def process_one_laptop():
    # Prompt ko update kiya hai taaki wo Amazon image link bhi de
    prompt = """
    Give me one trending laptop detail in HINDI. 
    Output JSON ONLY.
    IMPORTANT: Provide a valid, high-quality image URL for this laptop (preferably from Amazon or a product site).
    Structure:
    {
        "title": "Full Laptop Name",
        "price": "XX,XXX",
        "oldPrice": "XX,XXX",
        "discount": "XX% OFF",
        "image": "URL_HERE",
        "specs": {"Processor": "...", "RAM": "...", "Storage": "..."}
    }
    """

    try:
        response = model.generate_content(prompt)
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(json_text)
        
        # Amazon Link Generator
        encoded_name = urllib.parse.quote(data['title'])
        amazon_link = f"https://www.amazon.in/s?k={encoded_name}"
        
        # Prepare New Entry
        new_entry = {
            "title": data['title'],
            "price": data['price'],
            "oldPrice": data['oldPrice'],
            "discount": data['discount'],
            "image": data.get('image', 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8'), # Agar Gemini link na de toh fallback
            "amazonLink": amazon_link,
            "review_link": f"reviews/{data['title'].replace(' ', '_')[:15]}.html"
        }
        
        # ... (Baaki JSON save karne ka logic wahi rahega)

        # Prepare New Entry
        new_entry = {
            "title": data['title'],
            "price": data['price'],
            "oldPrice": data['oldPrice'],
            "discount": data['discount'],
            "image": data['image'],
            "amazonLink": amazon_link,
            "review_link": f"reviews/{data['title'].replace(' ', '_')[:15]}.html"
        }

        # Save to JSON
        laptops = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                try:
                    laptops = json.load(f)
                except:
                    laptops = []
        
        laptops.append(new_entry)

        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(laptops, f, indent=4, ensure_ascii=False)
        
        print(f"Success! {data['title']} added.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_one_laptop()
    
