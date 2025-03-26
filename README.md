# security-overflow
A great insight into the world of secure pages

# OWASP Vulnerability Scanner

A Flask-based web application to detect OWASP Top 10 vulnerabilities in web applications using Wapiti, SQLMap, and Gemini AI. This tool provides two scanning modes (Light and Deep) and generates recommendations for fixing detected vulnerabilities.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Cloning the Repository](#cloning-the-repository)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project is a web vulnerability scanner designed to identify OWASP Top 10 vulnerabilities (e.g., SQL injections, XSS, CSRF) in web applications. It uses:
- **Flask**: For the web framework and backend logic.
- **Wapiti**: For general vulnerability scanning.
- **SQLMap**: For detecting SQL injection vulnerabilities.
- **Gemini AI**: For generating recommendations to fix detected vulnerabilities.

The app was tested on `http://testphp.vulnweb.com/`, where it successfully identified critical vulnerabilities like SQL injections and missing security headers.

## Features
- **Two Scanning Modes**:
  - **Light Scan**: Uses in-app analysis (regular expressions) and Wapiti for quick scans.
  - **Deep Scan**: Adds SQLMap for more thorough vulnerability detection.
- **Gemini AI Integration**: Provides actionable recommendations for fixing vulnerabilities.
- **User-Friendly Interface**: A simple web interface (`index.html`) for entering URLs and viewing scan results.
- **Progress Tracking**: Real-time scan progress updates via the `/scan-progress` endpoint.

## Project Structure
- `templates/index.html`: Frontend interface for the web app.
- `static/Logo.png`: Logo used in the frontend.
- `app.py`: Main Flask application script.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This guidebook.

## Prerequisites
Before setting up the project, ensure you have the following tools installed:

### Essential Tools
1. **Git**: To clone the repository.
   - Download: [git-scm.com](https://git-scm.com/downloads)
2. **Python 3.10**: To run the Flask app.
   - Download: [python.org](https://www.python.org/downloads/)
   - Verify: `python3 --version` (should show 3.10 or higher).
3. **pip**: To install Python dependencies.
   - Included with Python, but ensure it’s up-to-date: `python -m pip install --upgrade pip`.
4. **Wapiti**: For vulnerability scanning.
   - Install: `pip install wapiti3`
5. **SQLMap**: For SQL injection testing.
   - Clone: `git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap`
   - Verify: `python sqlmap/sqlmap.py --version`
6. **Gemini AI API Key**: For generating recommendations.
   - Sign up at [ai.google.dev](https://ai.google.dev/) to get an API key.
   - Install the library: `pip install google-generativeai`

### Optional Tools
- **GitHub CLI**: For easier GitHub interactions.
  - Download: [cli.github.com](https://cli.github.com/)
- **VS Code**: For editing and debugging the code.
  - Download: [code.visualstudio.com](https://code.visualstudio.com/)
  - Recommended Extension: Python (for linting, debugging, and IntelliSense).

## Cloning the Repository
To download the project, clone the repository using Git:

```bash
git clone https://github.com/<your-username>/owasp-vulnerability-scanner.git
