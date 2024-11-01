import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Spoonacular API configuration
API_KEY = 'YOUR-API-KEY'
URL = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}'

# Email configuration
EMAIL_ADDRESS = 'YOUR EMAIL'
EMAIL_PASSWORD = 'YOUR PASSWORD'
TO_EMAIL = 'DESTINATION EMAIL'

def fetch_random_recipe():
    response = requests.get(URL)
    if response.status_code == 200:
        recipe_data = response.json()
        return recipe_data['recipes'][0]
    else:
        print("Error fetching recipe:", response.status_code)
        return None


def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def daily_recipe():
    recipe = fetch_random_recipe()
    if recipe:
        title = recipe['title']
        ingredients = [ingredient['original'] for ingredient in recipe['extendedIngredients']]
        instructions = recipe['instructions']

        email_body = f"Recipe: {title}\n\nIngredients:\n" + "\n".join(ingredients) + \
                     f"\n\nInstructions:\n{instructions}"

        send_email(f"Your Daily Random Recipe: {title}", email_body)
        print("Email sent!")


# Schedule the daily recipe function
schedule.every().day.at("09:00").do(daily_recipe)  # Set the time you want the email to be sent

print("Scheduler started. Waiting for the scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
