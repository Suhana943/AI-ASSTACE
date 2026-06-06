import requests
import json
import os

def update_laptops_data():
    # Nayi API Key ko fetch karein aur strip() lagayein taaki extra spaces hat jaye
    API_KEY = os.environ.get('API_KEY', '').strip() 
    
    if not API_KEY:
        print("Error: API_KEY set nahi hai!")
        return

    # Yahan 'url' wo Amazon search link hai jiska data aapko chahiye
    # Amazon search link ko proper URL encoding ke saath rakhein
    amazon_search_url = "https://www.amazon.in/s?k=gaming+laptop"
    
    # Payload settings
    payload = {
        'api_key': API_KEY,
        'url': amazon_search_url,
    }

    try:
        print("Scraper API se data mangwa rahe hain...")
        # API request
        response = requests.get('http://api.scraperapi.com/', params=payload)
        
        if response.status_code == 200:
            print("Success! Data mil gaya.")
            # Yahan ab aapko HTML parse karna hoga (BeautifulSoup use karein)
            # Ya agar API JSON deta hai, toh directly use karein
            # Example parsing (yahan aap apna custom logic daalein):
            print("Data process ho raha hai...")
            
            # Simulated data save (Yahan apni parsing logic daalein)
            # with open('laptops.json', 'w') as f:
            #     json.dump(data, f, indent=4)
        else:
            print(f"Error: API status code {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_laptops_data()
    
