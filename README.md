# 🎓 University Data Journalism

AI-powered interactive data analysis platform for Turkish university admissions data.

This project allows users to explore university admission data through an interactive dashboard and receive automated insights generated based on selected filters.

---

## 🚀 Features

- 📊 Interactive Streamlit dashboard
- 🎯 Department-based analysis (top scores, demand, competitiveness)
- 🏙 City-level insights
- 📈 Trend analysis over years
- ⚖️ University comparison tool
- 🤖 AI-generated commentary based on filters

---

## 📊 Dataset

This project uses the dataset from Kaggle:

👉 https://www.kaggle.com/datasets/ramazanizci/turkish-university-admissions

⚠️ Note: Dataset files are not included in this repository.

---

## 📂 Project Structure

university_data_journalism/

│

├── app/

│ └── streamlit_app.py # Main dashboard application

│

├── src/

│ ├── data_loader.py # Data loading functions

│ ├── data_preprocessing.py # Dataset preparation

│ ├── analysis.py # Analytical functions

│ ├── visualization.py # Plotly charts

│ └── ai_commentary.py # AI-based insights generation

│

├── data/

│├── raw/ # Raw dataset (not included)

│└── processed/ # Processed dataset (not included)

│

├── .gitignore

└── README.md

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/dilekcolak/university-data-journalism.git

cd university-data-journalism
```

### 2. Create virtual environment (recommended)

    python -m venv venv

    venv\Scripts\activate # Windows

### 3. Install dependencies

pip install -r requirements.txt

## 📥 Prepare Dataset

Download dataset from Kaggle

Place CSV files into:

    data/raw/

## 🔄 Data Processing

Run preprocessing script:

    python -m src.data_preprocessing

This will generate:

        data/processed/master_university_dataset.csv

        data/processed/analysis_dataset.csv

## ▶️ Run the Dashboard

    streamlit run app/streamlit_app.py

Then open in browser:
http://localhost:8501

## 🧠 AI Commentary

- The system generates automatic insights based on:

- Selected filters (year, city, score type)

- Trends in the data

- Top and bottom values

- Demand and competitiveness metrics

## 💡 Example Analyses

- Top departments by average score

- Most demanded departments

- Most competitive departments

- City-based preference analysis

- Yearly score trends

- Fastest rising departments

- University comparisons

## 🛠 Tech Stack

- Python

- Pandas

- Plotly

- Streamlit

## 👥 Contributors

- Dilek Miraç Çolak

- Zeyneb Çınar
