# AI Hackathon – Revenue Leakage Audit Engine

A lightweight audit engine built using Python and Streamlit to detect revenue leakage, rule violations, and suspicious refund patterns in airline ticketing data.

---

## 📂 Project Structure

ai-audit-engine-demo/

│── streamlit_run_app.py      # Streamlit entry point  
│── .gitignore  
│── README.md  

├── rules/  
│   └── rules_engine.py       # Mandatory audit validations  

├── anomaly/  
│   └── anomaly_detector.py   # Anomaly detection logic  

├── reports/                  # (Future) CSV / Excel reports  

├── data/                     # Sample test data  

---

## 🚀 Tech Stack

- Python 3.10+  
- Streamlit
- Llama-3.2-1B-Instruct-Q4_0


---

## 🧪 Features Implemented

### ✅ Rules Engine (Revenue Validation)

- Fare must be greater than 0  
- Tax cannot be negative  
- Commission cannot exceed fare  

### ✅ Anomaly Detection

- Flags suspicious refunds (e.g., refund > 80% of fare)  

### ✅ API / Data Validation

- Strong request validation using Pydantic models  
- Structured JSON responses  

---
- Download Llama-3.2-1B-Instruct-Q4_0 from GPT-4-All and place in one folder and change the path in ai_engine.py
## ▶️ How to Run Locally

### 1️⃣ Install Streamlit

```bash
pip install streamlit
2️⃣ Run the App
streamlit run app.py
3️⃣ Open in Browser
The app will open automatically, or visit:

http://localhost:8501
