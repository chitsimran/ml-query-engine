from clients.openai_client import client

def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    return response['choices'][0]['message']['content']