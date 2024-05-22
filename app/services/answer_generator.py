from openai import OpenAI

ANSWER_PROMPT = """
You are an expert in[ context-based question answering.
Answer the question based only on the following context:
{context}
Question: {question}]
"""

class AnswerGenerator:
    def __init__(self, temperature) -> None:
        self.temperature = temperature
        self.client = OpenAI()

    def answer(self, question, context):
        prompt = ANSWER_PROMPT.format(question=question, context=context)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                { "role": "system", "content": prompt}
            ],
            temperature=self.temperature
        )

        return response.choices[0].message.content