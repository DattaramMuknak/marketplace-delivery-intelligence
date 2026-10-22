# Delivery Intelligence — ML Analytics + RAG

A Streamlit dashboard for the Marketplace Delivery Performance Analysis assignment. It has two interview-friendly sections:
1. **ML & Analytics:** applies the assignment's SLA rule, shows courier summary and visualizations.
2. **RAG Assistant:** indexes uploaded CSV rows with Hugging Face Sentence Transformers and Pinecone, then answers questions with the xAI Grok API.

Authentication uses MySQL and bcrypt password hashing.

## 1. Requirements

- Python 3.10–3.12 recommended for compatibility with ML dependencies
- A MySQL database reachable from your machine and (for deployment) from Streamlit Cloud
- Pinecone API key
- xAI API key for Grok

## 2. Setup locally (Windows PowerShell)

```powershell
# Open this folder in VS Code
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Copy-Item .env.example .env
# Edit .env and add your real credentials
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. MySQL setup

Create a database using your MySQL client:
```sql
CREATE DATABASE delivery_intelligence;
```
Then set `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` in `.env`. The app creates the `app_users` table automatically. Passwords are hashed with bcrypt; plaintext passwords are never stored.

Do not use `localhost` for a deployed Streamlit app. Use a managed MySQL provider with network access configured for Streamlit Cloud. Restrict database privileges to this app's database and use TLS where supported.

## 4. Pinecone + Grok

- Create a Pinecone account and create an API key.
- Create an xAI API key for Grok.
- Add the keys to `.env`; never commit `.env` to GitHub.
- The app creates the Pinecone index if it doesn't exist. The default embedding model has 384 dimensions; keep the index dimension at 384.
- First use downloads the Sentence Transformer model and can take a little time.

## 5. Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository **without `.env`**.
2. Open Streamlit Community Cloud and deploy the repository with `app.py` as the entry point.
3. In app settings, add the environment values under **Secrets** using TOML syntax:
   ```toml
   MYSQL_HOST = "your-host"
   MYSQL_PORT = "3306"
   MYSQL_USER = "your-user"
   MYSQL_PASSWORD = "your-password"
   MYSQL_DATABASE = "delivery_intelligence"
   PINECONE_API_KEY = "your-pinecone-key"
   PINECONE_INDEX_NAME = "delivery-intelligence"
   PINECONE_CLOUD = "aws"
   PINECONE_REGION = "us-east-1"
   XAI_API_KEY = "your-xai-key"
   XAI_MODEL = "grok-3-mini"
   HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
   ```
4. Make sure your hosted MySQL firewall allows the deployment to connect. Do not expose database credentials in source code or screenshots.

The app reads environment variables. On Streamlit Cloud, `st.secrets` is not automatically exported to `os.environ`, so add this snippet near the top of `app.py` **before importing app modules** if using Streamlit Secrets:
```python
# Streamlit Cloud Secrets -> environment variables
for key, value in st.secrets.items():
    if isinstance(value, (str, int, float)):
        os.environ.setdefault(key, str(value))
```
Place it immediately after `load_dotenv()` and before `from src.auth...` imports, or alternatively modify the helper functions to read `st.secrets` directly. This matters for cloud deployment.

## 6. Assignment logic / assumptions

- Date scope: orders whose `delivered_at` is in May 2026.
- Test/internal orders are excluded.
- Duplicate `order_id` values are deduplicated by keeping the latest `updated_at` record.
- Only records with status `Delivered`, valid shipped/delivered dates, non-negative transit, and positive `promised_days` are eligible.
- Courier labels are normalized (`shipquick` → `ShipQuick`, `Fastbee` → `FastBee`, `Bluedart` → `Blue Dart`).
- On time if `actual_transit_days <= promised_days`.
- Cancelled, undelivered, out-of-month, test, and invalid-SLA records are excluded.

## 7. Explain it in an interview

**ML & Analytics:** “I clean inconsistent dates and courier labels, remove duplicate order IDs, filter delivered non-test orders delivered in May 2026, calculate transit days, classify on-time vs late using the SLA, then aggregate the courier-level rate. Plotly charts show courier comparison and city outcomes.”

**RAG:** “Each CSV row is converted into readable text, embedded using a Hugging Face Sentence Transformer, and stored in Pinecone. At question time, I embed the query, retrieve the most relevant rows, and pass only that context to Grok. The answer includes retrieved source snippets. Semantic retrieval is useful for questions, but exact numeric aggregation should use Pandas/SQL rather than assume top-k retrieval includes every row.”

**Authentication:** “Users register and log in with MySQL. Passwords are hashed with bcrypt. Pinecone namespaces are separated per user so one account's retrieval doesn't query another account's vectors.”

## Important limitations

- The supplied file has only 10 raw rows and duplicate/inconsistent records. It is not sufficient to train or validate a trustworthy predictive ML classifier. The dashboard therefore uses the exact transparent SLA rule from the assignment and explains that a predictive model needs more historical examples.
- For production, add rate limiting, email verification, account recovery, session expiry, database TLS, upload-size limits, and a proper secrets manager.
- This is a starter project. Test MySQL/Pinecone/xAI credentials and connectivity in your target environment before the interview/demo.
