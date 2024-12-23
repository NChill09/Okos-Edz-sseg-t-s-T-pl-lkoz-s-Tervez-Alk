import os
import openai
import json
from pathlib import Path

try:
    with open("../OPENNAI_API_KEY", "r") as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    print("Hiba: Az OPENNAI_API_KEY fájl nem található!")
    exit(1)

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model= "gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Te egy dietetikus és egy személyi edző vagy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        # A válasz a 'choices' listából kinyerhető:
        assistant_message = response.choices[0].message['content']
        return assistant_message.strip()
    except Exception as e:
        print("Hiba történt az API hívás során:", str(e))
        return None

if __name__ == "__main__":
    # Bemeneti prompt
    downloads_dir = Path.home() / "Downloads"
    file_path = downloads_dir / "data.json"
    
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    user_prompt = f"""
Kérlek, készíts egy heti edzés- és étrendtervet a következő adatok alapján JSON formában:

      név: {data['név']},
      email: {data['email']},
      kor: {data['kor']},
      súly: {data['súly']},
      magasság: {data['magasság']},
      nem: {data['nem']},
      kaloria_szukseglet: {data['kaloria_szukseglet']},
      edzés napok: {data['ráérés']},
      étkezési_szokások: {data['étkezési_szokások']},
      suly_cél: {data['suly_cél']},
      edzés_cél: {data['edzés_cél']}

A JSON formátum a következő legyen:

{{
  "edzésterv": {{
    "Hétfő": "Edzés leírása",
    "Kedd": "Pihenő",
    ...
    "Vasárnap": "Pihenő"
  }},
  "étrendterv": {{
    "Hétfő": ["Reggeli:", "Tízórai:" "Ebéd:", "Uzsonna:", "Vacsora:", "Snack:"],
    "Kedd": ["Reggeli:", "Tízórai:" "Ebéd:", "Uzsonna:", "Vacsora:", "Snack:"],
    ...
    "Vasárnap": ["Reggeli:", "Tízórai:" "Ebéd:", "Uzsonna:", "Vacsora:", "Snack:"],
  }}
}}

Adott napokon az étrendben és edzéstervben ne legyenek üresek a mezők!

Csak a json filet kérem válaszul
"""
    valasz = chat_with_gpt(user_prompt)
    
    print(user_prompt);
    
    if valasz:
        import json
        with open("sample.json", "w", encoding="utf-8") as f:
            json.dump(valasz, f, ensure_ascii=False, indent=4)
        print("A ChatGPT válasz JSON formában elmentve a sample.json fájlba.")
    else:
        print("ChatGPT válasz:\n", valasz)