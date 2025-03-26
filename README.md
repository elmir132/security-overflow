# Security Overflow: OWASP Vulnerability Scanner

A Flask-based web application to detect OWASP Top 10 vulnerabilities in web applications using Wapiti, SQLMap, Nikto, and Gemini AI. This tool provides two scanning modes (Light and Deep) and generates recommendations for fixing detected vulnerabilities.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Cloning the Repository](#cloning-the-repository)
- [Environment Content](#environment-content)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the Application](#running-the-application)
- [Starting the Scanner](#starting-the-scanner)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project, named **Security Overflow**, is a web vulnerability scanner designed to identify OWASP Top 10 vulnerabilities (e.g., SQL injections, XSS, CSRF) in web applications. It uses:
- **Flask**: For the web framework and backend logic.
- **Wapiti**: For general vulnerability scanning.
- **SQLMap**: For detecting SQL injection vulnerabilities.
- **Nikto**: For additional web server scanning.
- **Gemini AI**: For generating recommendations to fix detected vulnerabilities.

The app was tested on `http://testphp.vulnweb.com/`, where it successfully identified critical vulnerabilities like SQL injections and missing security headers.

## Features
- **Two Scanning Modes**:
  - **Light Scan**: Uses in-app analysis (regular expressions for SQL injections and XSS) and Wapiti for quick scans.
  - **Deep Scan**: Adds SQLMap and Nikto for more thorough vulnerability detection.
- **Gemini AI Integration**: Provides actionable recommendations for fixing vulnerabilities.
- **User-Friendly Interface**: A simple web interface (`index.html`) for entering URLs and viewing scan results.
- **Progress Tracking**: Real-time scan progress updates via the `/scan-progress` endpoint.

## Project Structure
- `templates/index.html`: Frontend interface for the web app.
- `static/Logo.png`: Logo used in the frontend.
- `app.py`: Main Flask application script.
- `requirements.txt`: List of Python dependencies required to run the app.
- `README.md`: This guidebook.
- `LICENSE`: MIT License file.

## Prerequisites
Before setting up the project, ensure you have the following tools installed:

### Essential Tools
1. **Git**: To clone the repository.
   - Download: [git-scm.com](https://git-scm.com/downloads)
   - Verify: `git --version`
2. **Python 3.10**: To run the Flask app.
   - Download: [python.org](https://www.python.org/downloads/)
   - Verify: `python3 --version` (should show 3.10 or higher).
3. **pip**: To install Python dependencies.
   - Included with Python, but ensure it’s up-to-date: `python -m pip install --upgrade pip`.
4. **Wapiti**: For vulnerability scanning (included in `requirements.txt`).
5. **SQLMap**: For SQL injection testing (required for Deep Scan).
   - Clone: `git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap`
   - Verify: `python sqlmap/sqlmap.py --version`
   - **Important**: Ensure the `sqlmap` directory is in your project folder or the `sqlmap` executable is in your system’s PATH.
6. **Nikto**: For web server scanning (required for Deep Scan).
   - Install on Linux (e.g., Ubuntu): `sudo apt install nikto`
   - Install on macOS (with Homebrew): `brew install nikto`
   - Alternatively, clone from GitHub: `git clone https://github.com/sullo/nikto.git` and follow the setup instructions in the Nikto documentation.
   - Verify: `nikto -Version`
   - **Important**: Ensure the `nikto` executable is in your system’s PATH.
7. **Gemini AI API Key**: For generating recommendations.
   - Sign up at [ai.google.dev](https://ai.google.dev/) to get an API key.

### Optional Tools
- **GitHub CLI**: For easier GitHub interactions.
  - Download: [cli.github.com](https://cli.github.com/)
- **VS Code**: For editing and debugging the code.
  - Download: [code.visualstudio.com](https://code.visualstudio.com/)
  - Recommended Extension: Python (for linting, debugging, and IntelliSense).

## Cloning the Repository
To download the project, clone the repository using Git:

```bash
git clone https://github.com/elmir132/security-overflow.git
