import json
import os
import google.generativeai as genai

# API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_review_html(laptop):
    print(f"Generating review for: {laptop['title'][:30]}...")
    
    # Prompt mein laptop ki puri details daal rahe hain
    prompt = f"""
    Write a detailed, professional review for this laptop:
    Title: {laptop['title']}
    Price: {laptop['price']}
    Original Price: {laptop['oldPrice']}
    Discount: {laptop['discount']}
    
    Format the output as clean HTML (use <h1>, <h2>, <p>, <ul> for features, and a Verdict section). 
    Do not include markdown ticks like ```html. Just raw HTML content.
    """
    
    response = model.generate_content(prompt)
    return response.text

def run_processor():
    # 1. Check karo laptops.json hai ya nahi
    if not os.path.exists("laptops.json"):
        print("Error: laptops.json file nahi mili!")
        return

    with open("laptops.json", "r", encoding="utf-8") as f:
        laptops = json.load(f)

    # 2. Reviews folder banao agar nahi hai
    if not os.path.exists("reviews"):
        os.makedirs("reviews")

    # 3. Har laptop ke liye process karo
    for laptop in laptops:
        # Agar review_link pehle se bhara hai, toh skip karo
        if laptop.get("review_link"):
            continue

        try:
            # Review generate karo
            html_content = generate_review_html(laptop)
            
            # File ka naam banao
            safe_filename = laptop['title'].replace(" ", "_").replace("/", "-")[:30] + ".html"
            filepath = os.path.join("reviews", safe_filename)
            
            # HTML file save karo
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # JSON update karo
            laptop["review_link"] = filepath
            
        except Exception as e:
            print(f"Error generating review for {laptop['title']}: {e}")

    # 4. JSON file wapas save karo
    with open("laptops.json", "w", encoding="utf-8") as f:
        json.dump(laptops, f, indent=4)
    print("All reviews generated successfully!")

if __name__ == "__main__":
    run_processor()
      
