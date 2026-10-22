# Delivery Intelligence — Marketplace Delivery Analytics

A Streamlit dashboard for the Marketplace Delivery Performance Analysis assignment. It analyzes delivery records, evaluates SLA performance, compares couriers, and visualizes city-wise delivery outcomes.

**Live Demo:** https://marketplace-delivery-intelligence.streamlit.app/  
**GitHub Repository:** https://github.com/DattaramMuknak/marketplace-delivery-intelligence

## Features

- **Delivery SLA Analytics:** Classifies eligible orders as on-time or late.
- **Performance Overview:** Displays eligible orders, on-time orders, on-time rate, and late orders.
- **Courier Scorecard:** Compares courier performance using SLA on-time rates.
- **City Performance:** Visualizes delivery outcomes across cities.
- **Data Quality Checks:** Handles duplicate orders, test/internal records, and invalid delivery data.
- **CSV Upload:** Analyze delivery records from uploaded datasets.
- **Data Exploration:** View raw records, eligible orders, and courier summaries.
- **CSV Downloads:** Download analysis results and courier-level summaries.
- **User Authentication:** MySQL-backed registration and login with bcrypt password hashing.

## Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Data Processing:** Pandas
- **Visualizations:** Plotly
- **Database:** MySQL
- **Authentication:** bcrypt
- **Configuration:** Python dotenv and Streamlit Secrets

## Project Structure

```text
marketplace-delivery-intelligence/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── auth.py
│   └── analytics.py
└── data/
    └── task1_marketplace_delivery_sla_raw.csv
```

## Requirements

- Python 3.10 or later, compatible with the installed dependencies
- MySQL database
- Git

## Local Setup (Windows)

### 1. Clone the repository

```powershell
git clone https://github.com/DattaramMuknak/marketplace-delivery-intelligence.git
cd marketplace-delivery-intelligence
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Add your MySQL connection details to `.env`:

```dotenv
MYSQL_HOST=your-mysql-host
MYSQL_PORT=3306
MYSQL_USER=your-mysql-username
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=your-database-name
```

Keep your `.env` file private and do not commit it to GitHub.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

## MySQL Database

MySQL is used for user registration and authentication. The application creates the `app_users` table automatically when `init_db()` runs.

User information includes:

- User ID
- Full name
- Email address
- bcrypt password hash
- Account creation timestamp

Passwords are hashed before being stored in the database.

## Deployment on Streamlit Community Cloud

**Live application:** https://marketplace-delivery-intelligence.streamlit.app/

To deploy the application:

1. Push the project to GitHub without `.env` or other secret files.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account and select the repository.
4. Set `app.py` as the main file.
5. Open the app settings and configure your database credentials under **Secrets**.

Use TOML format for Streamlit Secrets:

```toml
[mysql]
host = "your-mysql-host"
port = 3306
database = "your-database-name"
username = "your-mysql-username"
password = "your-mysql-password"
```

Replace the placeholders with your actual database details. Ensure the authentication code reads the `[mysql]` configuration from Streamlit Secrets when deployed.

## Analytics Logic

- Filter delivery records according to the assignment's date and status requirements.
- Remove duplicate `order_id` records, keeping the latest `updated_at` record.
- Exclude test and internal orders.
- Validate delivery dates, transit duration, and promised delivery days.
- Normalize courier names for consistent reporting.
- Calculate actual transit days.
- Classify deliveries as on-time when `actual_transit_days <= promised_days`.
- Aggregate results for courier-level and city-level analysis.

## Author

**Dattaram Muknak**

- GitHub: https://github.com/DattaramMuknak
- Live Project: https://marketplace-delivery-intelligence.streamlit.app/

---

*Delivery Intelligence — Clear data. Meaningful insights. Better delivery decisions.*
