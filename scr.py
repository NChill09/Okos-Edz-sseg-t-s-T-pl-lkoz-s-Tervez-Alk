import os
import openai
import yagmail
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

try:
    with open("../OPENNAI_API_KEY", "r") as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    print("Hiba: Az OPENNAI_API_KEY fájl nem található!")
    exit(1)

sender_email = "mealplanner06@gmail.com"
email_password = "ybie npwy slic pxpr"  # Normál Gmail jelszó vagy alkalmazás-specifikus jelszó


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model= "gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Te egy dietetikus és egy személyi edző vagy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=5000
        )
        
        # A válasz a 'choices' listából kinyerhető:
        assistant_message = response.choices[0].message['content']
        return assistant_message.strip()
    except Exception as e:
        print("Hiba történt az API hívás során:", str(e))
        return None

def generate_plan(row):
    #output_file = "sample.json"
    prompt = "Kérlek, készíts egy heti edzés- és étrendtervet a következő adatok alapján: {0}  7 napra legyen edzésterv és étrend is. Csak az edzéstervet és étrendet kérem a válaszba más szöveget nem!".format(row)

    valasz = chat_with_gpt(prompt)

    if valasz:
        send_email(row[1], row[2], valasz)
    else:
        print("ChatGPT válasz:\n", valasz)

def get_form_answers():
    SERVICE_ACCOUNT_FILE = '../service_account.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Hitelesítés
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Google Sheets API kliens inicializálása
    service = build('sheets', 'v4', credentials=credentials)

    # A táblázat azonosítója (URL-ből másold ki)
    SPREADSHEET_ID = '1kAkZRI6Qzp3O-bYjFDwKCYgCgU6bBn8m3m6KHliw6UA'
    RANGE_NAME = 'Form_Responses1'  # Ez a Form válaszok alapértelmezett lapja

    # Adatok lekérése
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get('values', [])

    # Válaszok megjelenítése
    #if rows:
    #    for row in rows[1:]:
    #        generate_plan(row)
    #else:
    #    print("Nincsenek válaszok.")

    # Demo verzióhoz, csak az utolsó kitölt nézzük:
    generate_plan(rows[-1])


    

def send_email(name,receiver_email, plan):
    try:
        yag = yagmail.SMTP(user=sender_email, password=email_password)
    except Exception as e:
        print(f"Hiba történt a Yagmail inicializálásakor: {e}")

    receiver_email = "nemethcsicsi@gmail.com" 
    subject = "Heti edzés és étrend terv"
    message_body = f"Kedves {name}, a heti terved a következő:\n{plan}\n A sportolásra remek motivációkat kaphatsz itt: https://www.instagram.com/nchill_shots/?utm_source=hirlevel&utm_medium=email&utm_campaign=suliapp&utm_id=okos+egeszsegseg%C3%ADto&utm_term=suliapp&utm_content=suliapp"


    try:
        yag.send(to=receiver_email, subject=subject, contents=message_body)
        print(f"Email elküldve: {receiver_email}")
    except Exception as e:
        print(f"Hiba történt az email küldésekor {receiver_email} részére: {e}")

if __name__ == "__main__":
    get_form_answers()