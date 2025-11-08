import requests
from google import genai
import schedule
import time
import datetime

#Add your API keys here
REDDIT_API_KEY = ""
GEMINI_API_KEY = ""
BOT_TOKEN = ""
GROUP_TOKEN = ""


AI_PROMPT = "Analysiere die folgenden Informationen aus den meistdiskutierten Reddit-Beiträgen des Monats über Bitcoin. \n \
	1.	Bewerte die allgemeine Stimmung der Community gegenüber Bitcoin (positiv, neutral oder negativ) und begründe deine Einschätzung anhand konkreter Aussagen oder Themen, die in den Beiträgen vorkommen. \n \
	2.	Fasse die zentralen Diskussionspunkte in klaren, nummerierten Stichpunkten zusammen (z. B. Markttrends, wirtschaftliche Einschätzungen, technische Entwicklungen, Sicherheitsbedenken). \n \
	3.	Ziehe ein Fazit, ob die aktuelle Stimmung eher für einen Kauf, Verkauf oder das Halten von Bitcoin spricht. Beziehe dich dabei ausschließlich auf die Reddit-Daten und erkläre deine Empfehlung in 2–3 Sätzen. \n \
 \n \
Formatiere die Antwort wie folgt: \n \
	•	Stimmung: [positiv | neutral | negativ] \n \
	•	Hauptpunkte: (nummerierte Liste) \n \
	•	Empfehlung: (max. 3 Sätze) \n \
\n \
Begrenze die gesamte Antwort auf maximal 500 Wörter."


def fetch_data(url):
    try:
        response = requests.get(url, headers={
            "access_token": REDDIT_API_KEY,
            "Authorization": "bearer ",
            "User-Agent": "ChangeMeClient/0.1 by YourUsername"
        })
        response.raise_for_status() 
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def extract_important_info(data):
    if not data or 'data' not in data:
        return "No data available"
    
    posts = data['data']['children']
    important_info = []
    
    for post in posts:
        post_data = post['data']
        info = {
            'Titel': post_data.get('title', 'N/A'),
            'Text': post_data.get('selftext', '') if post_data.get('selftext') else 'Kein Text'
        }
        if info['Text'] != 'Kein Text':
            important_info.append(info)
    
    return important_info

def ai_evaluation(important_info):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model= "gemini-2.5-flash", contents= AI_PROMPT + ":\n\n" + str(important_info))

    #filter response to return only the text content
    response_filtered = response.candidates[0].content.parts[0].text

    return response_filtered

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": GROUP_TOKEN,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Failed to send message!")
    else:
        print("Message sent successfully!")


def do_monthly_task():
    print("Executing task...")
    data = fetch_data("https://www.reddit.com/r/Bitcoin/top.json?limit=2500&t=month")
    important_info = extract_important_info(data)
    print(AI_PROMPT)
    ai_response = ai_evaluation(important_info)
    print(ai_response)
    send_telegram_message(ai_response)
    
if __name__ == "__main__":
    schedule.every().day.at("08:00").do(do_monthly_task)
    print("Scheduler started, waiting for next run...")

    while True:
        today = datetime.date.today()
        print("Checking day:", today.day)
        if today.day == 1:
            schedule.run_pending()
            print("checked at", datetime.datetime.now())
        time.sleep(60)  # Check once a minute
