import os
import re
import json
import subprocess
import tempfile
import requests
import shutil
import logging
from flask import Flask, request, render_template, jsonify, send_from_directory
from urllib.parse import urlparse
import google.generativeai as genai

##########################
# CONFIGURATION
##########################
GEMINI_API_KEY = "AIzaSyDvMnMQhyUh33pGc8GsYmd_15dnmCvtfxM"

logging.basicConfig(level=logging.DEBUG)

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Global progress tracker
scan_progress = {"progress": 0, "message": "Initializing..."}

def reset_progress():
    global scan_progress
    scan_progress = {"progress": 0, "message": "Initializing..."}

def update_progress(progress, message):
    global scan_progress
    scan_progress["progress"] = progress
    scan_progress["message"] = message
    logging.debug(f"Progress updated: {progress}% - {message}")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'Logo.png', mimetype='image/png')

def analyze_page_content(content):
    vulnerabilities = []
    sql_injection_pattern = re.compile(
        r"(?:\b(?:union\s+all\s+select|select\s+.*\s+from|insert\s+into|delete\s+from|drop\s+table|alter\s+table)\b"
        r"|\bon\w+\s*=|\bwaitfor\s+delay|\bload_file\s*\()",
        re.IGNORECASE
    )
    if sql_injection_pattern.search(content):
        vulnerabilities.append("Possible SQL Injection")

    xss_pattern = re.compile(
        r"<script\b[^>]*>(?:[^<]|<[^/s>])*?</script\s*>",
        re.IGNORECASE
    )
    if xss_pattern.search(content):
        vulnerabilities.append("Possible Cross-Site Scripting (XSS)")

    if vulnerabilities:
        return {"severity": "High", "message": " / ".join(vulnerabilities)}
    else:
        return {"severity": "Low", "message": "No immediate vulnerabilities found."}

def run_wapiti(url):
    if not shutil.which("wapiti"):
        logging.info("Wapiti not installed, skipping.")
        return {"info": "Skipped: Wapiti not installed."}

    with tempfile.TemporaryDirectory() as tmp_dir:
        report_path = os.path.join(tmp_dir, "report.json")
        cmd = [
            "wapiti", "--url", url, "--scope", "page", "--format", "json",
            "--output", report_path, "--max-links-per-page", "5",
            "--max-files-per-dir", "3", "--timeout", "60",
            "-v", "1", "--flush-session"  # Clear cache for fresh scan
        ]
        try:
            logging.debug(f"Running Wapiti command: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=120)  # 2-minute total timeout
            logging.debug(f"Wapiti stdout: {stdout}")
            logging.debug(f"Wapiti stderr: {stderr}")
            if process.returncode != 0:
                logging.error(f"Wapiti failed with code {process.returncode}: {stderr}")
                return {"error": f"Wapiti failed with code {process.returncode}: {stderr}"}
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    return json.load(f)
            logging.info("Wapiti completed but no report generated.")
            return {"info": "Wapiti: No report generated."}
        except subprocess.TimeoutExpired as e:
            process.kill()
            stdout, stderr = e.stdout, e.stderr
            logging.error(f"Wapiti timed out after 120s - stdout: {stdout}")
            logging.error(f"Wapiti timed out after 120s - stderr: {stderr}")
            return {"error": f"Wapiti timed out after 120 seconds: {stderr}"}
        except Exception as e:
            logging.error(f"Wapiti failed: {e}")
            return {"error": f"Wapiti failed: {e}"}

def run_sqlmap(url):
    if not shutil.which("sqlmap"):
        return {"info": "Skipped: sqlmap not installed."}

    cmd = ["sqlmap", "-u", url, "--batch", "--crawl=1", "--level=2", "--risk=2", "--smart"]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return {"output": result.stdout[-1000:]}
    except Exception as e:
        return {"error": f"sqlmap failed: {e}"}

def run_nikto(url):
    if not shutil.which("nikto"):
        return {"info": "Skipped: Nikto not installed."}

    cmd = ["nikto", "-h", url, "-output", "/tmp/nikto_report.txt"]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return {"output": result.stdout[-1000:]}
    except Exception as e:
        return {"error": f"Nikto failed: {e}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan-progress", methods=["GET"])
def scan_progress_endpoint():
    global scan_progress
    return jsonify(scan_progress)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json() or {}
    url = data.get("url")
    scan_type = data.get("scan_type", "deep").lower()
    if not url:
        return jsonify({"error": "URL is required"}), 400

    reset_progress()

    update_progress(10, "Fetching webpage...")
    try:
        resp = requests.get(url, timeout=10)
        page_content = resp.text
    except Exception as e:
        return jsonify({"error": f"Failed to fetch {url}: {e}"}), 400

    update_progress(20, "Analyzing page content...")
    in_app_report = analyze_page_content(page_content)

    wapiti_results = {}
    sqlmap_results = {}
    nikto_results = {}

    if scan_type == "light":
        update_progress(35, "Running Wapiti scan...")
        wapiti_results = run_wapiti(url) or {}
        update_progress(50, "Scanners completed.")
        # For light scan, exclude SQLMap and Nikto from the final report
        final_report = {
            "in_app_analysis": in_app_report,
            "wapiti": wapiti_results,
            "scan_type": scan_type
        }
    else:
        update_progress(30, "Running Wapiti scan...")
        wapiti_results = run_wapiti(url) or {}
        update_progress(40, "Running SQLMap scan...")
        sqlmap_results = run_sqlmap(url) or {}
        update_progress(50, "Running Nikto scan...")
        nikto_results = run_nikto(url) or {}
        update_progress(60, "Scanners completed.")
        # For deep scan, include all scanner results
        final_report = {
            "in_app_analysis": in_app_report,
            "wapiti": wapiti_results,
            "sqlmap": sqlmap_results,
            "nikto": nikto_results,
            "scan_type": scan_type
        }

    update_progress(70, "Analyzing OWASP Top 10...")
    owasp_prompt = (
        "You are a cybersecurity analyst reviewing JSON-based security scan results from multiple tools. "
        "For a 'light' scan, only in-app analysis and Wapiti results are available (ignore SQLMap and Nikto). "
        "For a 'deep' scan, all tools (in-app analysis, Wapiti, SQLMap, Nikto) are available. "
        "Analyze the following results and map them to the OWASP Top 10 (2021) categories. "
        "For each category, provide a **status** and a **one-line summary**:\n\n"
        "- **Status Options**: 'Vulnerable' (for confirmed issues or significant potential risks explicitly tied to the category), "
        "'Not Vulnerable' (for no evidence of issues or only minor concerns not strongly linked to the category).\n"
        "- **Categories**:\n"
        "  - Broken Access Control\n"
        "  - Cryptographic Failures\n"
        "  - Injection\n"
        "  - Insecure Design\n"
        "  - Security Misconfiguration\n"
        "  - Vulnerable and Outdated Components\n"
        "  - Identification and Authentication Failures\n"
        "  - Software and Data Integrity Failures\n"
        "  - Security Logging and Monitoring Failures\n"
        "  - Server-Side Request Forgery\n\n"
        "Return the analysis as a structured list in this exact format:\n"
        "- **[Category]**: [Status] - [One-line summary]\n\n"
        "Ensure consistency: Mark as 'Vulnerable' if the issue is confirmed (e.g., 'SQL Injection detected') or if there's a significant potential risk "
        "explicitly mentioned in the results (e.g., 'Possible SQL Injection', 'Missing CSP', 'Weak Credentials'). Use 'Not Vulnerable' only when there's "
        "no clear evidence or the risk is negligible.\n\n"
        f"JSON: {json.dumps(final_report, indent=2)}"
    )

    update_progress(80, "Generating scan results...")
    gemini_prompt_frames = (
        "You are a cybersecurity analyst reviewing JSON-based security scan results. "
        "For a 'light' scan, only in-app analysis and Wapiti results are available (ignore SQLMap and Nikto). "
        "For a 'deep' scan, all tools (in-app analysis, Wapiti, SQLMap, Nikto) are available. "
        "Generate a **structured bullet-point list** summarizing each reported issue or check. "
        "Assign one of the following statuses consistently based on the scan data:\n\n"
        "🔴 **Vulnerable** → A confirmed security issue explicitly identified in the results.\n"
        "🟡 **Warning** → A potential risk or unconfirmed issue that should be reviewed further.\n"
        "🟢 **Safe** → The security check confirmed no vulnerabilities.\n"
        "⚪ **No Findings** → No relevant data or issues were detected from the scan.\n\n"
        "**Format Example:**\n"
        "- 🔴 **Vulnerable**: SQL Injection detected in login form (parameter 'username').\n"
        "- 🟢 **Safe**: Content Security Policy (CSP) is properly configured.\n"
        "- 🟡 **Warning**: HTTP headers missing 'X-Frame-Options'.\n"
        "- ⚪ **No Findings**: No weak credentials detected.\n\n"
        "Keep descriptions clear, brief, and consistent across scans. Avoid randomness in status assignment. "
        "For light scans, do not include any references to SQLMap or Nikto in the output.\n\n"
        f"JSON: {json.dumps(final_report, indent=2)}"
    )

    update_progress(90, "Summarizing findings...")
    gemini_prompt_summary = (
        "Provide a single short summary of these vulnerabilities in one block, based on the JSON scan results. "
        "For a 'light' scan, only in-app analysis and Wapiti results are available (ignore SQLMap and Nikto). "
        "For a 'deep' scan, all tools (in-app analysis, Wapiti, SQLMap, Nikto) are available.\n"
        f"JSON: {json.dumps(final_report, indent=2)}\n\n"
        "No bullet points, just a concise paragraph summarizing the overall risk."
    )

    update_progress(95, "Generating security suggestions...")
    gemini_prompt_suggestions = (
        "You are a cybersecurity expert reviewing JSON-based security scan results from multiple tools. "
        "For a 'light' scan, only in-app analysis and Wapiti results are available (ignore SQLMap and Nikto). "
        "For a 'deep' scan, all tools (in-app analysis, Wapiti, SQLMap, Nikto) are available. "
        "Based on the findings, provide a **structured bullet-point list** of 5-10 actionable security suggestions to improve the webpage's safety. "
        "Focus on practical, specific recommendations to mitigate identified risks. If no significant risks are found, provide general best practices.\n\n"
        "**Format:**\n"
        "- [Suggestion text]\n\n"
        "**Examples:**\n"
        "- Sanitize all user inputs to mitigate SQL Injection risks.\n"
        "- Implement Content Security Policy (CSP) headers to prevent XSS attacks.\n"
        "- Enforce HTTPS to secure data transmission.\n\n"
        "Ensure suggestions are clear, concise, and relevant to the scan results. Always return at least 5 suggestions, "
        "even if they are general improvements when specific issues are minimal.\n\n"
        f"JSON: {json.dumps(final_report, indent=2)}"
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        owasp_resp = model.generate_content(owasp_prompt)
        final_report["owasp_top_10"] = owasp_resp.text
        frames_resp = model.generate_content(gemini_prompt_frames)
        final_report["gemini_frames"] = frames_resp.text
        summary_resp = model.generate_content(gemini_prompt_summary)
        final_report["gemini_summary"] = summary_resp.text
        suggestions_resp = model.generate_content(gemini_prompt_suggestions)
        final_report["security_suggestions"] = suggestions_resp.text
        logging.debug(f"Security Suggestions Response: {suggestions_resp.text}")
        update_progress(100, "Scan completed!")
    except Exception as e:
        final_report["owasp_top_10"] = f"OWASP Top 10 analysis failed: {e}"
        final_report["gemini_frames"] = f"Gemini frames failed: {e}"
        final_report["gemini_summary"] = f"Gemini summary failed: {e}"
        final_report["security_suggestions"] = f"Security suggestions failed: {e}"
        logging.error(f"Gemini API error: {e}")
        update_progress(100, "Scan failed.")

    return jsonify(final_report)

if __name__ == "__main__":
    app.run(debug=True)