import sys
sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("input.txt", "r", encoding="utf-8") as file:
    input_text = file.read()

user_prompt = input("What would you like me to do with this text? ")
prompt = f"{user_prompt}:\n\n{input_text}"

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500
    )
)

print(response.text)

if "pdf" in prompt.lower():
    from textwrap import wrap
    clean_text = response.text.replace("###", "").replace("**", "")
    
    pdf = canvas.Canvas("summarize.pdf", pagesize=A4)
    pdf.drawString(50, 800, "Summary:")

    lines = wrap(clean_text, width=90)
    y = 780
    for line in lines:
        pdf.drawString(50, y, line)
        y -= 20
    pdf.save()
    print("PDF file created: summarize.pdf")
elif "text file" in prompt.lower():
    with open("summarize.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Text file created: summarize.txt")
else:
    print("No format specified")