from openai import OpenAI
from src.config.settings import settings

# 🔹 Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)


# ===============================
# 🚀 1. GENERATE PIPELINE
# ===============================
def generate_pipeline(query: str, tool: str):
    """
    Generate CI/CD pipeline based on selected tool
    """

    # 🔹 Decide platform
    if tool == "github":
        platform = "GitHub Actions YAML pipeline (.github/workflows/main.yml)"
    elif tool == "jenkins":
        platform = "Jenkinsfile pipeline script"
    elif tool == "gitlab":
        platform = "GitLab CI/CD YAML pipeline (.gitlab-ci.yml)"
    else:
        platform = "CI/CD pipeline"

    # 🔹 Prompt
    prompt = f"""
You are a DevOps expert.

Generate a {platform} for the following request:

{query}

IMPORTANT:
- Return only the pipeline script
- Do not add explanations
- Follow real-world best practices
"""

    # 🔹 OpenAI call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a DevOps expert"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ===============================
# 🧠 2. EXPLAIN PIPELINE
# ===============================
def explain_pipeline_service(script: str):
    """
    Explain CI/CD pipeline in simple terms
    """

    prompt = f"""
You are a DevOps expert.

Explain this CI/CD pipeline step-by-step in simple and beginner-friendly language:

{script}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You explain DevOps pipelines simply"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ===============================
# 🛠️ 3. FIX ERROR
# ===============================
def fix_error_service(error: str):
    """
    Fix CI/CD pipeline errors
    """

    prompt = f"""
You are a DevOps expert.

Fix the following CI/CD pipeline error and provide a clear solution:

{error}

Also include:
- What caused the error
- How to fix it
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You fix DevOps pipeline errors"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content