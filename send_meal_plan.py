import json
import yagmail

# Gmail fiók beállításai
sender_email = "mealplanner06@gmail.com"
email_password = "ybie npwy slic pxpr"  # Normál Gmail jelszó vagy alkalmazás-specifikus jelszó

def read_json(file_path):
    """Beolvassa a JSON fájlt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def send_weekly_plan(yag, user):
    """Küldjön heti tervet a felhasználónak."""
    name = user['név']
    email = user['email']
    plan = user['terv']

    # HTML tartalom generálása
    email_body = f"""
    <html>
        <body>
            <h1>Kedves {name}!</h1>
            <h2>Heti Edzésterved</h2>
            <ul>
    """
    for day, workout in plan['edzésterv'].items():
        email_body += f"<li><strong>{day}</strong>: {workout}</li>"
    email_body += "</ul>"

    email_body += "<h2>Heti Étrendterved</h2><ul>"
    for day, meals in plan['étrendterv'].items():
        email_body += f"<li><strong>{day}</strong>:</li><ul>"
        for meal in meals:
            email_body += f"<li>{meal}</li>"
        email_body += "</ul>"
    email_body += "</ul>"

    email_body += "<p>Jó egészséget és sikeres hetet kívánunk!</p></body></html>"

    subject = f"Heti terved - {name}"

    try:
        yag.send(to=email, subject=subject, contents=email_body)
        print(f"Email elküldve: {email}")
    except Exception as e:
        print(f"Hiba történt az email küldésekor {email} részére: {e}")

def send_update_form_email(yag, user):
    """Küldjön emailt az adatok frissítésére vonatkozóan."""
    name = user['név']
    email = user['email']

    email_body = f"""
    <html>
        <body>
            <h1>Kedves {name}!</h1>
            <p>Kérjük, töltsd ki a frissített adataidat, ha bármilyen változás történt az edzési vagy étrendi terveidben.</p>
            <p>Az űrlapot itt éred el: <a href='https://example.com/update-form'>Adatfrissítő űrlap</a></p>
            <p>Köszönjük együttműködésed!</p>
        </body>
    </html>
    """

    subject = f"Adatfrissítés szükséges - {name}"

    try:
        yag.send(to=email, subject=subject, contents=email_body)
        print(f"Adatfrissítő email elküldve: {email}")
    except Exception as e:
        print(f"Hiba történt az adatfrissítő email küldésekor {email} részére: {e}")

def main():
    """Fő program."""
    json_file_path = "plan.json"  # A JSON fájl neve

    # JSON beolvasása
    try:
        data = read_json(json_file_path)
    except Exception as e:
        print(f"Hiba történt a JSON fájl beolvasásakor: {e}")
        return

    # Yagmail inicializálása
    try:
        yag = yagmail.SMTP(user=sender_email, password=email_password)
    except Exception as e:
        print(f"Hiba történt a Yagmail inicializálásakor: {e}")
        return

    # Email küldése minden felhasználónak
    for user in data:
        send_weekly_plan(yag, user)  # Heti terv email
        send_update_form_email(yag, user)  # Adatfrissítő email

if __name__ == "__main__":
    main()
