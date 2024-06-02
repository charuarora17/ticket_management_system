import requests

def send_message_to_google_chat(ticker_id):
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAA5TEogcY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=-DWAU3G0CD5SylaJ_g_aIU9PW-Z8I7hHfyJm1As7k2Y"
    message = f"Escalation alert for Ticket Number {ticker_id}"
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message. Status code: {response.status_code}")

# Example usage
ticker_id = "ABC123"
send_message_to_google_chat(ticker_id)
