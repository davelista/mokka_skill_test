# Flask Project Setup

This document provides step-by-step instructions to initialize and set up the Flask project.

---

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.13
- pip (Python package manager)
- virtualenv (optional but recommended)
- SQLite

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/davelista/mokka_skill_test.git
cd mokka_skill_test
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and configure necessary environment variables:
```ini
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=mokka.db
```
#### Notes
For simplicity, a .env file is already included in the project with the necessary configurations. 
If needed, you can update it with your specific settings.

### 5. Initialize the Database
Run the provided database initialization script:
```bash
chmod +x initialize_db.sh
./initialize_db.sh
```
This script will:
- Create the database
- Insert users
- Insert products
- Insert orders and order details

### 6. Run the Flask Application
```bash
flask run
```
By default, the application will be available at:
```
http://127.0.0.1:5000
```
