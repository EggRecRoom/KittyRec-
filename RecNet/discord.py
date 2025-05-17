import requests
import json

BOT_TOKEN = "OTcyMzQxNzYyMDkxNzk4NTI5.GdXVpA.ubiG-BXN8wVuJfbgZQMRqlniEV-Jwb7mlXVqQ4"
API_URL = "https://discord.com/api/v10/"
headers = {
    "authorization": "Bot " + BOT_TOKEN,
    "content-type": "application/json",
}

def sendEmbed(embed, channelID):
    url = f"{API_URL}channels/{channelID}/messages"
    payload = {
        "embeds": [embed]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    embed = {
      "title": "test",
      "color": 7209178
    }
    channelID = 1358573746528714852  # Replace with your channel ID
    sendEmbed(embed, channelID)