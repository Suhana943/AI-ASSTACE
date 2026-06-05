
import os
import google.generativeai as genai
from datetime import date

# API Key load karna
genai.configure(api_key=os.environ["API_1"])

# Naya model use karein jo aapke project mein work karega
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt
prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, specs, pros, cons aur final verdict ho."
review = model.generate_content(prompt)

# File saving
filename = f"reviews/laptop-{date.today()}.md"
with open(filename, "w") as f:
    f.write(review.text)
    
