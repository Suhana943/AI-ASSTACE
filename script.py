import os
import google.generativeai as genai
from datetime import date

# Yahan humne os.environ["API_1"] use kiya hai
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-pro')

review = model.generate_content("Ek latest trending laptop ka professional review likho jisme specs, pros, aur cons ho.")

filename = f"reviews/laptop-{date.today()}.md"
with open(filename, "w") as f:
    f.write(review.text)
  
