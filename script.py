import os
import google.generativeai as genai
from datetime import datetime

# API configure karein
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. Folder confirm karein
if not os.path.exists('reviews'):
    os.makedirs('reviews')

# 2. File ka naam aur path set karein (absolute path)
filename = f"reviews/laptop-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

# 3. Content generate karke save karein
prompt = "Ek latest trending laptop ka professional review likho."
review = model.generate_content(prompt)

with open(filename, "w", encoding="utf-8") as f:
    f.write(review.text)

print(f"File created: {filename}")
