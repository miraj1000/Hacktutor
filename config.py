# HackTutor configuration
# IMPORTANT: put a NEW Gemini API key here before running.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

ALLOWED_TARGETS = [
    "127.0.0.1", "localhost",
    "192.168.", "10.0.", "172.16.",
    "testphp.vulnweb.com", "dvwa", "hackazon",
]

ALLOWED_BINS = {
    "nmap", "gobuster", "nikto", "nuclei", "curl", "ffuf", "dirb",
    "whoami", "id", "uname", "ls", "cat", "pwd", "ping", "dig",
    "sqlmap", "whatweb", "wpscan", "hydra", "hashcat", "john",
}
