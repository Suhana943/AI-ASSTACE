import os
import google.generativeai as genai
from datetime import date

genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Current folder print karein
print("Current working directory:", os.getcwd())

prompt = "Ek latest trending laptop ka professional review likho."

try:
    review = model.generate_content(prompt)
    if not os.path.exists('reviews'):
        os.makedirs('reviews')
        print("Folder 'reviews' created.")
    
    filename = "reviews/laptop-review.md" # Name simple rakhte hain
    with open(filename, "w") as f:
        f.write(review.text)
    print(f"File created successfully at: {filename}")
except Exception as e:
    print(f"ERROR: {e}")
    
