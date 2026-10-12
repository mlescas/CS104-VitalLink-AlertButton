import time
import os
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

telegram_url = "https://api.telegram.org/bot" + bot_token + "/sendMessage"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            print("Someone pressed the alert button!")
            button_pressed = True

            response = requests.post(
                telegram_url,
                json={
                    "chat_id": chat_id,
                    "text": "Someone pressed the alert button, HEEEEELP!"
                },
                timeout=10
            )

            print("Telegram response:", response.status_code)

        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    GPIO.cleanup()
