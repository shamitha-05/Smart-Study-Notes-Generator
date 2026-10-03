import os
import re
from flask import Flask, render_template, request
from huggingface_hub import InferenceClient

app = Flask(__name__)

MODEL = "facebook/bart-large-cnn"


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))
def generate_summary(text):
    token = os.getenv("HF_TOKEN")

    if not token:
        return None, "HF_TOKEN is not configured."

    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=token
        )

        result = client.summarization(
            text,
            model=MODEL
        )

        summary = result.summary_text

        if summary:
            return summary, None

        return None, "The AI model did not return a summary."

    except Exception as e:
        return None, f"AI connection error: {e}"


def make_key_points(summary):
    sentences = re.split(r"(?<=[.!?])\s+", summary.strip())
    points = [s.strip() for s in sentences if s.strip()]
    return points[:5]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if len(text.split()) < 20:
            error = "Please enter a paragraph with at least 20 words."

        else:
            summary, api_error = generate_summary(text)

            if api_error:
                error = api_error

            else:
                original_words = word_count(text)
                summary_words = word_count(summary)

                reduction = round(
                    ((original_words - summary_words) / original_words) * 100,
                    2
                )

                result = {
                    "original": text,
                    "summary": summary,
                    "key_points": make_key_points(summary),
                    "original_words": original_words,
                    "summary_words": summary_words,
                    "reduction": reduction
                }

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )