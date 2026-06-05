import os
import google.generativeai as genai
from datetime import datetime

# API configure karein
genai.configure(api_key=os.environ["API_1"])

# Naya model jo aapke account mein available hai
model = genai.GenerativeModel('gemini-3.5-flash')

# 1. Folder confirm karein
if not os.path.exists('reviews'):
    os.makedirs('reviews')

# 2. File ka naam (unique timestamp ke saath)
filename = f"reviews/laptop-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

# 3. Content generate karein
prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, specs, pros, cons aur final verdict ho."

try:
    print(f"Generating review using gemini-3.5-flash...")
    review = model.generate_content(prompt)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(review.text)
    
    print(f"File created: {filename}")
except Exception as e:
    print(f"Error occurred: {e}")
    
