from dotenv import load_dotenv
from openai import OpenAI
import os, json
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)

class Coach:
    def __init__(self):
        self.client = OpenAI();
        self.username = "Pavle Milovanovic"
        reader = PdfReader("linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("summary.txt", "r", encoding="utf-8") as file:
            self.summary = file.read()

    def system_prompt(self):
        return f"""
You are an elite, practical career coach advising {self.username}.
Give brutally useful, actionable advice — career strategy, positioning, outreach, skill prioritization.

You may reference this context only when relevant — do NOT info-dump or quote excessively:
- LinkedIn extract: {self.linkedin[:2000]}
- Personal summary: {self.summary[:2000]}

Rules:
- Think like a high-level mentor with strong startup + AI industry knowledge.
- Your answers must be crisp, strategic, and solution-focused — never vague.
- Suggest next steps, not just thoughts.
- If clarity is needed, ask **one** short clarifying question — not more.

Start coaching now.
        """.strip()

    def chat(self, message, history):
        formatted_history = []
        for user_msg, assistant_msg in history:
            formatted_history.append({"role": "user", "content": user_msg})
            formatted_history.append({"role": "assistant", "content": assistant_msg})

        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + formatted_history
            + [{"role": "user", "content": message}]
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    coach = Coach()
    gr.ChatInterface(
        fn=coach.chat,
        title="Pavle’s AI Career Coach",
        description="Elite, actionable career mentorship — startup, AI, game dev, positioning, strategy."
    ).launch()