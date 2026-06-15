import requests
import time

def ask_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    
    for attempt in range(5):  # Retry up to 5 times
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
        )
        
    print(response)

# Example usage
if __name__ == "__main__":
    prompt = "What is the capital of India?"
    reply = ask_gpt(prompt)
    print(reply)  # Should print "New Delhi" or similar response
