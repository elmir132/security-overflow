# Security Overflow: OWASP Vulnerability Scanner

A Flask-based web application to detect OWASP Top 10 vulnerabilities (e.g., SQL injections, XSS, CSRF) in web applications using Wapiti, SQLMap, Nikto, and Gemini AI. This tool offers two scanning modes (Light and Deep) and provides recommendations for fixing detected vulnerabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
  - [Step 1: Install Essential Tools](#step-1-install-essential-tools)
  - [Step 2: Clone the Repository](#step-2-clone-the-repository)
  - [Step 3: Set Up the Python Environment](#step-3-set-up-the-python-environment)
  - [Step 4: Set Up the Gemini API Key](#step-4-set-up-the-gemini-api-key)
  - [Step 5: Run the Application](#step-5-run-the-application)
  - [Step 6: Start the Scanner](#step-6-start-the-scanner)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

**Security Overflow** is a web vulnerability scanner designed to identify OWASP Top 10 vulnerabilities in web applications. It uses:

- **Flask**: For the web framework and backend logic.
- **Wapiti**: For general vulnerability scanning.
- **SQLMap**: For detecting SQL injection vulnerabilities.
- **Nikto**: For additional web server scanning.
- **Gemini AI**: For generating recommendations to fix detected vulnerabilities.

The app was tested on [http://testphp.vulnweb.com/](http://testphp.vulnweb.com/), where it successfully identified critical vulnerabilities like SQL injections and missing security headers.

## Features

- **Two Scanning Modes**:
  - **Light Scan**: Quick scan using in-app analysis (regular expressions for SQL injections and XSS) and Wapiti.
  - **Deep Scan**: Thorough scan with SQLMap and Nikto for more detailed vulnerability detection.

- **Gemini AI Integration**: Provides actionable recommendations for fixing vulnerabilities.

- **User-Friendly Interface**: A simple web interface (`index.html`) for entering URLs and viewing scan results.

- **Progress Tracking**: Real-time scan progress updates via the `/scan-progress` endpoint.

## Project Structure

```
Security-Overflow/
│── app.py                 # Main Flask application script
│── templates/
│   └── index.html         # Frontend interface for the web app
│── static/
│   └── Logo.png           # Logo used in the frontend
│── requirements.txt       # List of Python dependencies
│── README.md              # This guide
│── LICENSE                # MIT License file
```

## Installation Guide

### Step 1: Install Essential Tools

#### 1.1 Install Git
Git is required to clone the repository.

- Download: [git-scm.com](https://git-scm.com)
- Install:
  - On Windows/macOS/Linux, follow the installer instructions.
- Verify Installation:
  ```bash
  git --version
  ```
  Expected output: git version 2.x.x

#### 1.2 Install Python 3.10+
Python is required to run the Flask app.

- Download: [python.org](https://python.org)
- Verify Installation:
  ```bash
  python3 --version
  ```
  Expected output: Python 3.10+

- Ensure pip is Installed:
  ```bash
  python3 -m pip --version
  ```
  If pip is missing, install it:
  ```bash
  python3 -m ensurepip --upgrade
  python3 -m pip install --upgrade pip
  ```

#### 1.3 Install Wapiti, SQLMap, and Nikto

Install Wapiti:
```bash
pip install wapiti3
```

Install SQLMap:
```bash
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap
```

Install Nikto:
- On Linux:
  ```bash
  sudo apt install nikto
  ```
- On macOS:
  ```bash
  brew install nikto
  ```

### Step 2: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/Security-Overflow.git
cd Security-Overflow
```

### Step 3: Set Up the Python Environment
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Gemini API Key
Get your API key from Google Gemini. 

```bash
https://aistudio.google.com/apikey
```
Create a `.env` file in the root of the project.

Add the following line with your actual API key:
```ini
GEMINI_API_KEY=your_api_key_here
```
<img width="934" alt="google_api" src="https://github.com/user-attachments/assets/e2d64c54-009f-4d72-a0f3-8ab8b3428801" />

### Step 5: Run the Application
Start the Flask app:
```bash
python app.py
```

### Step 6: Start the Scanner
- Open http://127.0.0.1:5000/ in your browser.
- Enter the target URL and choose a scan mode.
- Click Start Scan to analyze vulnerabilities.


## Troubleshooting

### 1. Flask App Startup Issues
- **Problem**: Flask app fails to start.
  **Solution**: Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### 2. API and Key Problems
- **Problem**: API key error.
  **Solution**: Verify `.env` file is correctly set up with your Gemini API key.

### 3. Tool Installation Issues
- **Problem**: SQLMap not found.
  **Solution**: Ensure sqlmap folder exists and is cloned properly.

### 4. Virtual Environment Issues
If the app isn't detecting dependencies, ensure the virtual environment is activated:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

If you mistakenly installed packages globally, delete the `venv` folder and recreate it using the setup steps in the Installation Guide:

```bash
# Remove existing virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### 5. Port 5000 Already in Use
If Flask fails to start due to port 5000 being occupied:

**For macOS/Linux**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process (replace <PID> with actual Process ID)
kill -9 <PID>
```

**For Windows**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual Process ID)
taskkill /F /PID <PID>
```

**Alternative**: Run Flask on a different port:
```bash
python app.py --port=5001
```

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
