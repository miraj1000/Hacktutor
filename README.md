# 🛡 HackTutor — Render Ready

বাংলা ভাষার অনুমোদিত ল্যাব/CTF-ভিত্তিক পেন্টেস্টিং learning web app।

## 📁 Project structure

```text
hacktutor/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 💻 Local run

```bash
pip install -r requirements.txt
python main.py
```

তারপর:

```text
http://127.0.0.1:5000
```

## 🚀 Render settings

**Environment**
- `GEMINI_API_KEY` = তোমার নতুন Gemini API key
- চাইলে `GEMINI_MODEL` = `gemini-2.5-flash`

**Build Command**
```bash
pip install -r requirements.txt
```

**Start Command**
```bash
gunicorn main:app
```

**Root Directory**
খালি রাখো, যদি repository root-এই `main.py` থাকে।

## 🔐 Security

- API key source code-এ রাখা হয়নি।
- Public deployment থেকে arbitrary OS command execution রাখা হয়নি।
- শুধু নিজের বা অনুমোদিত lab/CTF environment-এ testing করো।
