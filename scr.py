import os
import openai
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

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
            max_tokens=1000
        )
        
        # A válasz a 'choices' listából kinyerhető:
        assistant_message = response.choices[0].message['content']
        return assistant_message.strip()
    except Exception as e:
        print("Hiba történt az API hívás során:", str(e))
        return None

def generate_plan(row):
    #output_file = "sample.json"
    prompt = "Kérlek, készíts egy heti edzés- és étrendtervet a következő adatok alapján: {0} csak az edzéstervet és étrendet kérem a válaszba más szöveget nem".format(row)
    print(prompt)

    valasz = chat_with_gpt(prompt)

    if valasz:
        print(valasz)
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
    if rows:
        for row in rows[1:]:
            generate_plan(row)
    else:
        print("Nincsenek válaszok.")

if __name__ == "__main__":
    get_form_answers()
    