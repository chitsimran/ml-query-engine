from clients.groq_client import client

def ask_groq(prompt: str, model: str = "llama3-8b-8192") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {e}"
    
def ask_groq_to_parse_movie_review(review: str):
    prompt = f"""
You are a helpful movie expert. Analyze the following movie review and return ONLY two things in this exact format:
1. Genre (e.g., Action, Comedy, Drama)
2. Sentiment: positive or negative

Please respond ONLY with the following format, without any additional text:
<genre>,<positive/negative>

Review:
\"\"\"
{review}
\"\"\"
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.strip()}
        ]
    )
    return response.choices[0].message.content.strip()