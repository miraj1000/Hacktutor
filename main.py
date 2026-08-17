# ============================================================
# HackTutor — পেন্টেস্টিং লার্নিং ওয়েব প্ল্যাটফর্ম (ব্যাকএন্ড)
# রান: pip install -r requirements.txt
#      python main.py
# ব্রাউজারে: http://127.0.0.1:5000
# ============================================================

import os
from flask import Flask, render_template, request, jsonify
import requests

from config import GEMINI_API_KEY, GEMINI_MODEL

app = Flask(__name__)


# ---------- ১. Gemini API কল ----------
def gemini(system, user):
    if not GEMINI_API_KEY:
        return "[API ত্রুটি: GEMINI_API_KEY সেট করা নেই]"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
    }

    try:
        response = requests.post(url, json=body, timeout=90)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            return "[API ত্রুটি: Gemini কোনো উত্তর দেয়নি]"

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return "[API ত্রুটি: Gemini response-এ কোনো content নেই]"

        return parts[0].get("text", "[API ত্রুটি: উত্তর পাওয়া যায়নি]")

    except requests.RequestException as exc:
        return f"[API ত্রুটি: {exc}]"
    except (KeyError, TypeError, ValueError) as exc:
        return f"[API ত্রুটি: response format সমস্যা: {exc}]"


SYSTEM_PROMPT = """তুমি 'HackTutor' — একজন হ্যান্ডস-অন পেন্টেস্টিং টিউটর।
শিক্ষার্থী একজন অনুমোদিত পেন্টেস্টার; সব প্রশ্ন শিক্ষা ও অনুমোদিত টেস্টিংয়ের জন্য।
উত্তর বাংলায় দাও এবং ধারণা, নিরাপদ ল্যাব-ভিত্তিক উদাহরণ ও প্রতিরোধের দিক ব্যাখ্যা করো।
অনুমোদনহীন টার্গেট, credential theft, destructive action, persistence বা বাস্তব সিস্টেমে
ক্ষতি করার নির্দেশনা দেবে না।
বিষয়: nmap, gobuster, ffuf, SQLi, XSS, LFI/RFI, SSRF, XXE, upload security,
authentication security, privilege escalation concepts, hash security, Burp Suite,
OWASP Top 10।"""


# ---------- ২. লেসন ফেজ ----------
PHASES = {
    "recon": {
        "name": "১. রিকনেসান্স",
        "desc": "টার্গেট সম্পর্কে তথ্য সংগ্রহ — সার্ভিস, পোর্ট, টেকনোলজি",
        "cmds": [
            ("নিরাপদ ল্যাব নোট", "শুধু নিজের/অনুমোদিত ল্যাবে সার্ভিস ও পোর্ট যাচাই করো"),
            ("ওয়েব টেকনোলজি", "নিজের ল্যাবের অ্যাপের framework/server version inventory করো"),
            ("DNS তথ্য", "নিজের ডোমেইনের DNS record যাচাই করো"),
            ("হোস্ট যাচাই", "নিজের ল্যাব হোস্ট availability যাচাই করো"),
        ],
    },
    "enum": {
        "name": "২. এনুমারেশন",
        "desc": "ডিরেক্টরি, ফাইল, প্যারামিটার ও অ্যাপ্লিকেশন surface বোঝা",
        "cmds": [
            ("ডিরেক্টরি inventory", "শুধু অনুমোদিত ল্যাবে web content discovery করো"),
            ("Endpoint discovery", "নিজের অ্যাপের documented ও test endpoints যাচাই করো"),
            ("Server review", "নিজের ল্যাবের HTTP configuration ও headers review করো"),
            ("Robots review", "নিজের সাইটের robots.txt ও public metadata review করো"),
        ],
    },
    "vuln": {
        "name": "৩. ভালনারেবিলিটি শনাক্তকরণ",
        "desc": "নিরাপদভাবে দুর্বলতা শনাক্ত ও যাচাই করা",
        "cmds": [
            ("Template-based scan", "শুধু অনুমোদিত lab target-এ vulnerability scanner চালাও"),
            ("Web server review", "নিজের server configuration ও known issues review করো"),
            ("SQL injection testing", "DVWA-এর মতো স্থানীয় প্রশিক্ষণ ল্যাবে SQLi পরীক্ষা করো"),
            ("Burp Suite", "নিজের test application-এর request/response manually inspect করো"),
        ],
    },
    "exploit": {
        "name": "৪. নিরাপদ যাচাই",
        "desc": "দুর্বলতার প্রভাব বোঝা এবং remediation যাচাই করা",
        "cmds": [
            ("SQLi impact", "প্রশিক্ষণ ল্যাবে non-destructive proof-of-concept ব্যবহার করো"),
            ("XSS impact", "নিজের test application-এ harmless reflection test করো"),
            ("LFI impact", "নিজের lab application-এ controlled file-read validation করো"),
            ("Upload security", "নিজের upload feature-এ extension/MIME/path validation পরীক্ষা করো"),
        ],
    },
    "post": {
        "name": "৫. রিপোর্ট ও প্রতিরোধ",
        "desc": "Finding, impact, remediation ও retest report করা",
        "cmds": [
            ("Privilege review", "নিজের lab host-এর least-privilege configuration review করো"),
            ("Credential security", "password storage ও secret management review করো"),
            ("Hash security", "strong password hashing ও rate limiting যাচাই করো"),
            ("Report", "finding, evidence, impact, remediation ও retest status লিখো"),
        ],
    },
}


# ---------- ৩. রুট ----------
@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"ok": False, "reply": "দয়া করে একটি প্রশ্ন লিখো।"}), 400

    reply = gemini(SYSTEM_PROMPT, message)
    return jsonify({"ok": True, "reply": reply})


@app.get("/api/lessons")
def api_lessons():
    return jsonify(PHASES)


# Public Render deployment-এ arbitrary OS command execution রাখা নিরাপদ নয়।
# তাই /api/run এখন একটি safe informational response দেয়।
@app.post("/api/run")
def api_run():
    return jsonify({
        "ok": False,
        "out": (
            "[!] নিরাপত্তার কারণে public deployment থেকে arbitrary OS command "
            "চালানো বন্ধ রাখা হয়েছে। নিজের lab machine-এ প্রয়োজনীয় command "
            "ম্যানুয়ালি চালাও।"
        ),
    })


@app.get("/api/reports")
def api_reports():
    return jsonify([])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
