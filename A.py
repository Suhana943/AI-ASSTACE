import requests
import json
import os

def update_laptops_data():
    # API key ko environment variable se lein (GitHub Secrets mein store karein)
    API_KEY = os.environ.get('d06627c0e0113a9096fed478a8757c3c') 
    
    if not API_KEY:
        print("Error: API_KEY set nahi hai!")
        return

    # Rainforest API ka endpoint aur parameters
    params = {
        'api_key': API_KEY,
        'type': 'search',
        'amazon_domain': 'amazon.in',
        'search_term': 'gaming laptop',
        'sort_by': 'featured'
    }

    try:
        response = requests.get('https://api.rainforestapi.com/request', params=params)
        data = response.json()

        if 'search_results' in data:
            formatted_data = []
            for item in data['search_results']:
                # Gaming laptops ka filter
                title = item.get('title', '')
                if "Gaming" in title or "RTX" in title:
                    formatted_data.append({
                        "title": title,
                        "price": item.get('price', {}).get('raw', 'N/A'),
                        "image": item.get('image', ''),
                        "amazonLink": item.get('link', ''),
                        "discount": "Deal Available" # API se discount field map karein
                    })

            # JSON file update karein
            with open('laptops.json', 'w') as f:
                json.dump(formatted_data, f, indent=4)
            print("Laptops.json successfully update ho gaya!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_laptops_data()
