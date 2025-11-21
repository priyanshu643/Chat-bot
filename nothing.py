import requests
import json
import sys

#API_KEY => here
API_KEY = ""


MODEL_VERSION = "gemini-2.0-flash"
ENDPOINT_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_VERSION}:generateContent?key={API_KEY}"


def uplink():
    # Standard "Nerd" loop with clean JARVIS output
    print(f"SYSTEM: CONNECTED TO {MODEL_VERSION.upper()}...")

    while True:
        try:
            # 1. Clean Input
            user_input = input("\nYOU: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input.strip():
                continue

            # 2. Raw Payload Construction
            payload = {
                "contents": [{
                    "parts": [{"text": user_input}]
                }]
            }

            # 3. Manual Packet Transmission
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                ENDPOINT_URL,
                headers=headers,
                data=json.dumps(payload)
            )

            # 4. Response Handling
            if response.status_code == 200:
                data = response.json()
                try:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    print(f"JARVIS: {answer}")
                except (KeyError, IndexError):
                    # Sometimes the model returns a safety warning instead of text
                    print(f"JARVIS: [Empty Response] - Likely Safety Filter Triggered. Raw: {data}")
            else:
                print(f"JARVIS: [Error {response.status_code}] {response.text}")

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"JARVIS: [Critical Failure] {e}")


def check_models():
    """
    Run this ONLY if you keep getting 404 errors.
    It lists all valid model names for your API key.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("AVAILABLE MODELS:")
        for m in resp.json().get('models', []):
            print(f"- {m['name'].replace('models/', '')}")
    else:
        print(f"Error checking models: {resp.text}")


if __name__ == "__main__":
    # If you keep getting 404s, uncomment the line below to see valid model names:
    # check_models()

    uplink()