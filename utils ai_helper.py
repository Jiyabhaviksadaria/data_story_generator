import os

def generate_ai_insights(df, api_key=None):
    """
    Generates AI-powered insights (Claude/OpenAI).
    Fallback to simple text if API key is missing.
    """
    
    if not api_key:
        return "AI mode is disabled. Add an API key to enable AI-powered insights."

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are an AI data scientist. Analyze this dataset and provide 5 deep insights.

        Columns: {df.columns.tolist()}
        Sample rows:
        {df.head(5).to_string()}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"AI insight generation failed: {e}"
