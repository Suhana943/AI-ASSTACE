import json
import os
import google.generativeai as genai
from datetime import datetime

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
model = genai.generativeai.GenerativeModel('gemini-1.5-flash')

# 2. Prompt: AI ko strict JSON ke liye instruction
prompt = """
Ek naye trending laptop ka professional review likho.
Output ONLY JSON format, koi extra text nahi.
Structure (JSON format mein hi dena):
{
    "title": "String",
    "intro": "String (Short para)",
    "specs": {"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "...", "Weight": "...", "Ports": "...", "Connectivity": "...", "OS": "..."},
    "pros": ["Point 1", "Point 2", "Point 3", "Point 4"],
    "cons": ["Point 1", "Point 2", "Point 3", "Point 4"],
    "verdict_intro": "String",
    "target_audience": ["..."],
    "who_should_buy": "String",
    "pro_tip": "String",
    "rating": "4.5/5"
}
"""

try:
    # 3. Content generation
    response = model.generate_content(prompt)
    
    # Error Fix: String ko ek hi line mein rakha gaya hai
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    
    # JSON parsing
    data = json.loads(json_text)

    # 4. Dynamic HTML components
    specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
    pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
    cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])
    audience_html = "".join([f"<li><strong>{a}</strong></li>" for a in data['target_audience']])

    # 5. HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>{data['title']} - Professional Review</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: sans-serif; line-height: 1.8; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        header {{ text-align: center; margin-bottom: 40px; }}
        .spec-table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        .spec-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .pros {{ background: #e8f5e9; padding: 30px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #4caf50; }}
        .cons {{ background: #ffebee; padding: 30px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #f44336; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{data['title']}</h1>
            <p>Professional Review</p>
        </header>
        <div class="intro-section">{data['intro']}</div>

        <h2>📋 Specifications</h2>
        <table class="spec-table">{specs_html}</table>

        <div class="pros"><h3>✅ Pros</h3><ol>{pros_html}</ol></div>
        <div class="cons"><h3>❌ Cons</h3><ol>{cons_html}</ol></div>

        <div class="verdict">
            <h3>⚖️ Final Verdict</h3>
            <p>{data['verdict_intro']}</p>
            <ul>{audience_html}</ul>
            <div class="purchase-section">
                <h4>Kise kharidna chahiye?</h4>
                <p>{data['who_should_buy']}</p>
            </div>
            <div class="pro-tip"><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</div>
            <div class="rating"><strong>Rating: {data['rating']}</strong></div>
        </div>
    </div>
</body>
</html>"""

    # 6. File Save karna
    if not os.path.exists('reviews'): os.makedirs('reviews')
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"reviews/laptop-{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Success! File created: {filename}")

except Exception as e:
    print(f"Error: {e}")
        
