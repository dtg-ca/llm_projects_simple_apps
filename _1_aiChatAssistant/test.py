import requests
import re

API_URL = "http://127.0.0.1:8000/chat"
prompt = "Hello, democracy or monarchy, which is better? Can you summarize it in 50 words?"

params = {"prompt": prompt}

response = requests.post(API_URL, params=params)

# Extract the response text
resp_json = response.json()
ai_response = resp_json.get("ai_response", "")

# Remove <think>...</think> part
final_answer = re.sub(r"<think>.*?</think>", "", ai_response, flags=re.DOTALL).strip()

print("Status code:", response.status_code)
# print("Response JSON:", resp_json)
# print("AI Response:", ai_response)
if not final_answer:
    print("No valid response received from the AI.")
print("Final Answer:", final_answer)