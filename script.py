
import os
import google.generativeai as genai
from datetime import date

# API key configure karna
genai.configure(api_key=os.environ["API_1"])

# Model update kiya hai ('gemini-pro' ki jagah 'gemini-1.5-flash')
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt (Thoda aur specific banaya hai taaki achha result mile)
prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, main specifications, pros, cons aur ek final verdict zaroor ho."
review = model.generate_content(prompt)

# Review file save karna
# Dhyan rahe ki aapki repo mein 'reviews' naam ka folder hona chahiye
filename = f"reviews/laptop-{date.today()}.md"
with open(filename, "w") as f:
    f.write(review.text)
