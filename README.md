# Smart Study Notes Generator

A simple Generative AI mini project that:
- accepts a study paragraph,
- generates a short AI summary,
- displays key points,
- counts original and summary words,
- calculates text reduction percentage.

## Run locally

```bash
pip install -r requirements.txt
```

Create an environment variable named `HF_TOKEN` containing a Hugging Face access token.

Then:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Deployment

This project is ready for a Python web host such as Render. Add the `HF_TOKEN` secret in the host's environment variables.

## Formula

Reduction % = ((Original Words - Summary Words) / Original Words) × 100
