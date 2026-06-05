import os
import google.generativeai as genai
from datetime import datetime

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Directory Path Set Karna
# Ye ensure karega ki file hamesha repository ke andar bane
repo_path = os.getcwd()
reviews_dir = os.path.join(repo_path, "reviews")

if not os.path.exists(reviews_dir):
    os.makedirs(reviews_dir)

# 3. Unique Filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = os.path.join(reviews_dir, f"laptop-{timestamp}.md")

# 4. Review Generation
prompt = "Ek latest trending laptop ka professional review likho jisme laptop ka naam, specs, pros, cons aur final verdict ho."

try:
    print(f"Generating review...")
    review = model.generate_content(prompt)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(review.text)
    
    print(f"File successfully created at: {filename}")
    
except Exception as e:
    print(f"Error occurred: {e}")
    
