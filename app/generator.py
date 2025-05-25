# app/generator.py
from openai import OpenAI

def generate_answer(query, context_chunks):
    context_text = "\n\n".join(chunk.page_content for chunk in context_chunks)
    prompt = f"Answer the question based only on the context below.\n\nContext:\n{context_text}\n\nQuestion: {query}"

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
