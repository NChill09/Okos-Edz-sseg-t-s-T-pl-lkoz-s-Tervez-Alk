import os
import openai

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
            max_tokens=1500
        )
        
        # A válasz a 'choices' listából kinyerhető:
        assistant_message = response.choices[0].message['content']
        return assistant_message.strip()
    except Exception as e:
        print("Hiba történt az API hívás során:", str(e))
        return None

if __name__ == "__main__":
    # Bemeneti prompt
    user_prompt = "Írj egy edzéstervet és étrendet egész jövőhétre kalóriállak. 30 éves vagyok, 80kg, 180 magas férfi. Hétfőn, Szerdán Pénteken érek rá. Vegetáriánus vagyok. Izomtömegnövelés a súlycélom. Maraton futás az edzéscélom. 2500 kaloriát eszem naponta!"
    valasz = chat_with_gpt(user_prompt)
    if valasz:
        print("ChatGPT válasz:\n", valasz)
