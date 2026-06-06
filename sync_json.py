import json
import os

JSON_FILE = 'laptops.json'
REVIEWS_DIR = 'reviews'

def sync():
    # 1. Existing JSON load karo
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    # 2. Existing titles ki list banao
    existing_titles = [item['title'].lower() for item in data]

    # 3. Reviews folder check karo
    if not os.path.exists(REVIEWS_DIR):
        print("Reviews directory not found!")
        return

    files = [f for f in os.listdir(REVIEWS_DIR) if f.endswith('.html')]
    
    new_entries = 0
    for file in files:
        # File name ko title mein convert karo (e.g., Apple_MacBook.html -> Apple MacBook)
        title = file.replace('.html', '').replace('_', ' ')
        
        if title.lower() not in existing_titles:
            # Naya entry add karo
            new_item = {
                "title": title,
                "price": "Check on Amazon",
                "oldPrice": "N/A",
                "image": "https://via.placeholder.com/150", 
                "amazonLink": "https://www.amazon.in/",
                "discount": "0% OFF",
                "review_link": f"reviews/{file}"
            }
            data.append(new_item)
            existing_titles.append(title.lower())
            new_entries += 1
            print(f"Added: {title}")

    # 4. JSON Save karo
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"Sync complete. {new_entries} new laptops added.")

if __name__ == "__main__":
    sync()
  
