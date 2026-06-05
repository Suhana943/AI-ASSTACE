import os
import google.generativeai as genai
from datetime import datetime

# API configure karein
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 1. Folder confirm karein
if not os.path.exists('reviews'):
    os.makedirs('reviews')

# 2. File ka naam
filename = f"reviews/laptop-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

# 3. Naya Prompt (Image aur Amazon link ke saath)
prompt = """
Ek latest trending laptop ka professional review likho.
Review mein ye cheezein honi chahiye:
1. Laptop ka pura naam aur uske main specs.
2. Pros aur Cons.
3. Ek 'Image Link' section jahan laptop ki ek achi image ka URL ho.
4. Ek 'Amazon Link' section jahan us laptop ka dummy Amazon search link ho.
Final verdict ke sath likho.
"""

try:
    print(f"Generating review with image and links...")
    review = model.generate_content(prompt)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(review.text)
    
    print(f"File created with links: {filename}")
except Exception as e:
    print(f"Error occurred: {e}")
    
