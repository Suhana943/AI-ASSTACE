import os
import google.generativeai as genai
from datetime import datetime # date ki jagah datetime use karenge

genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Unique filename ke liye timestamp
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
filename = f"reviews/laptop-{timestamp}.md"

prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, specs, pros, cons aur final verdict ho."

try:
    review = model.generate_content(prompt)
    if not os.path.exists('reviews'):
        os.makedirs('reviews')
    
    with open(filename, "w") as f:
        f.write(review.text)
    print(f"File created: {filename}")
except Exception as e:
    print(f"Error: {e}")
    
