import requests
import json
import os

def update_laptops_data():
    API_KEY = os.environ.get('API_KEY') 
    
    # Debugging print
    if API_KEY:
        print("API KEY mil gayi! (Key length: " + str(len(API_KEY)) + ")")
    else:
        print("ERROR: API KEY nahi mili. Secret check karo.")
        return

    params = {
        'api_key': API_KEY,
        'type': 'search',
        'amazon_domain': 'amazon.in',
        'search_term': 'gaming laptop',
        'sort_by': 'featured'
    }

    try:
        print("Request bhej rahe hain...")
        response = requests.get('https://api.rainforestapi.com/request', params=params)
        print("Status Code: " + str(response.status_code))
        
        data = response.json()

        if 'search_results' in data:
            formatted_data = []
            for item in data['search_results']:
                title = item.get('title', '')
                if "Gaming" in title or "RTX" in title:
                    formatted_data.append({
                        "title": title,
                        "price": item.get('price', {}).get('raw', 'N/A'),
                        "image": item.get('image', ''),
                        "amazonLink": item.get('link', ''),
                        "discount": "Deal Available"
                    })

            with open('laptops.json', 'w') as f:
                json.dump(formatted_data, f, indent=4)
            print("SUCCESS: " + str(len(formatted_data)) + " laptops save ho gaye!")
        else:
            print("ERROR: API response mein search_results nahi mile.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_laptops_data()
    
