

          import os
import google.generativeai as genai
from datetime import date

# API Key configure karein
genai.configure(api_key=os.environ["API_1"])

# Naya model jo aapke account mein chalega
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt
prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, specs, pros, cons aur final verdict ho."

try:
    review = model.generate_content(prompt)
    
    # Folder verify aur file saving
    if not os.path.exists('reviews'):
        os.makedirs('reviews')
        
    filename = f"reviews/laptop-{date.today()}.md"
    with open(filename, "w") as f:
        f.write(review.text)
    print(f"File created: {filename}")
    
except Exception as e:
    print(f"Error occurred: {e}")
    
