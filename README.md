File Merger
A Streamlit web application for merging CSV or Excel files based on user-selected columns. Supports exact and fuzzy matching on multiple columns, ideal for reconciling lists (e.g., inventory, customer data).
Features

Upload CSV or Excel files.
Join on multiple columns with exact or fuzzy matching.
Select columns to include in output.
Preview results, download merged file, and view match summary.
No persistent data storage for security.

Setup
Prerequisites

Python 3.12+
Docker (optional for containerized deployment)

Local Installation
git clone <repository-url>
cd file_merger_tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
streamlit run main.py

Docker Deployment
docker-compose up --build

Access at http://localhost:8501.
Documentation

docs/security_plan.md: Security measures.
docs/user_guide.md: User instructions.

Deployment
Host on an internal server or cloud (e.g., AWS, Azure) with SSO and HTTPS. See security_plan.md.
Contact
For support, contact [Your Name] at [Your Email].
# file-merger
