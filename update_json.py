import json

# File load karein
with open('laptops.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Yahan apni specific URL likhein
my_review_link = "https://www.laptoptec.online/reviews/laptop-guide" 

# Har item mein link update karein
for item in data:
    item['review_link'] = my_review_link

# File wapas save karein
with open('laptops.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

print("Ho gaya! Sabhi 80 items mein link add ho gayi.")

