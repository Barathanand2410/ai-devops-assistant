from openai import OpenAI

client = OpenAI()

def generate_devops_script(user_query: str):

    prompt = f"""
    You are a DevOps expert.

    Generate a production ready DevOps script for the following request:

    {user_query}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content