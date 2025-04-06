# ✈️ Flask Authentication System - Airline Auth

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-orange.svg)
![Flask](https://img.shields.io/badge/flask-latest-green.svg)

> Developed by Alejandro Areiza

## 📋 Description

This project implements a full-featured user authentication system built with Flask, specifically designed for an airline platform. It includes core functionalities such as user registration, login, password recovery, and flight reservation management. Additional features like email confirmation and secure password reset via email link are also integrated.

## 🚀 Key Features

### 🔐 Secure User Registration
- ✔️ Implemented in `routes.py` under the `/register/` route
- ✔️ Passwords are securely stored using bcrypt hashing

### 🔑 User Login with Credential Validation
- ✔️ Implemented in `routes.py` under the `/login/` route
- ✔️ Email and password are verified using bcrypt to compare the stored hash

### 🔁 Password Recovery System
- ✔️ Implemented in `routes.py` under `/reset_password` and `/reset_password/<token>`
- ✔️ A password reset link is sent via email using secure tokens

### 🧑‍💼 User Session Management with flask.session
- ✔️ Managed in `routes.py` using Flask-Login and the `@login_required` decorator
- ✔️ Sessions expire after 1 minute using `@routes.before_app_request` to manage timeouts

## 🎁 Bonus Features

### 📧 Account Activation via Email
- ✔️ Implemented in `routes.py` under `/register/` and `/confirm_account/<token>`
- ✔️ `utils.py` is used to generate and verify account activation tokens

### 🛠️ Password Recovery via Email Link or Code
- ✔️ Implemented in `routes.py` under `/reset_password`
- ✔️ Secure token handling is managed by `utils.py`

## ✅ Evaluation Criteria

### ✅ Fully Functional Code
- ✔️ All core features (registration, login, password recovery) are implemented and operational

### ✅ Best Practices Followed
- ✔️ Modular structure using Blueprints in `routes.py`
- ✔️ Flask-WTF is used for forms and validation
- ✔️ Passwords are hashed with bcrypt before storing

### ✅ Password Security
- ✔️ Passwords are stored as hashes using bcrypt
- ✔️ Enforced password policy: minimum of 8 characters

### ✅ Clean Project Structure
- ✔️ Well-organized into separate files for routes, models, forms, and utilities
- ✔️ Sensitive data like secret keys and email credentials are stored in a `.env` file

## 📦 Prerequisites

- Python 3.8 or higher
- A virtual environment (optional but recommended)
- SQLite (default database)

## ⚙️ Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/airline-auth.git
cd airline-auth
```

### 2. Set up the environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask
pip install -r requirements.txt
```

### 4. Create a .env file with the following configuration

```env
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 5. Initialize the database

```bash
flask db init
flask db migrate -m "Initialize database"
flask db upgrade
```

### 6. Run the application

```bash
python main.py
```

## 📄 License

MIT License

Copyright (c) 2025 Alejandro Areiza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
