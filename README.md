# 🚀 Internal Reporting & Automation System

> Automate operational reporting & KPI dashboards with Python.  
> Save time, increase accuracy, and visualize insights instantly! 📊

---

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30-orange?logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green?logo=mongodb)

---


## 📌 Overview
The **Internal Reporting & Automation System** automates internal operational workflows:  
- Collect & clean raw data automatically  
- Process & store data into **MySQL** & **MongoDB**  
- Generate **interactive dashboards** via **Streamlit**  
- Reduce manual effort & improve accuracy 💯

---

## 🛠 Tech Stack
- **Python** – Core scripting & automation  
- **Pandas & NumPy** – Data manipulation & cleaning  
- **MySQL** – Structured operational database  
- **MongoDB** – Logs & semi-structured metrics  
- **Streamlit** – Dashboards & visualizations  
- **Logging & Error Handling** – Python `logging` & `try-except`

---

## 🚀 Features
- ✅ Automated data ingestion & cleaning  
- ✅ Modular backend functions for validation & processing  
- ✅ ETL pipelines storing data into **MySQL** & **MongoDB**  
- ✅ Interactive **Streamlit dashboards** for KPI visualization  
- ✅ Logging & error handling for smooth operation  
- ✅ Scalable automation of reporting tasks

---

## ⚙️ Setup & Installation

1. **Clone the repo:**
```bash
git clone https://github.com/Luckybisht2811/Internal_reporting_system.git
cd Internal_reporting_system

---


## 📁 Folder Structure

internal_reporting_system/
│
├── data/ # Raw & processed datasets
│ ├── raw_data.csv
│ └── processed_data.csv
│
├── backend/ # Core backend scripts
│ ├── data_extraction.py
│ ├── data_cleaning.py
│ └── data_pipeline.py
│
├── database/ # DB connection scripts
│ ├── mysql_connection.py
│ └── mongo_connection.py
│
├── dashboard/ # Streamlit dashboard
│ └── app.py
│
├── logs/ # Pipeline execution logs
│ └── pipeline.log
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

Create virtual environment:

python -m venv venv
# Activate
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
