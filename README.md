# HackTutor - Render Ready

## Render settings

- Language: Python
- Branch: `main`
- Root Directory: leave **empty**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn main:app`
- Instance: Free is enough for testing

## Environment variable

In Render -> Environment add:

`GEMINI_API_KEY` = your Gemini API key

Do not put the real API key inside GitHub.

## GitHub structure

Upload the files/folders directly into the repository root:

```text
main.py
config.py
requirements.txt
README.md
templates/
  index.html
static/
  css/
    style.css
  js/
    app.js
```

This package is prepared as a web-learning deployment and does not expose arbitrary server command execution or reverse-shell/web-shell generation.
