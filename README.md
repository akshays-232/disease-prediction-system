# 🩺 Disease Prediction System

A machine learning web application that provides **educational disease-risk predictions** for diabetes, heart disease, and kidney disease. Built with Python and Streamlit, the application accepts user-provided health measurements, generates model predictions, explains selected readings, and provides downloadable reports.

🔗 **[Live Demo](https://discover-disease-prediction-system.streamlit.app/)**

## ✨ Features

- 🩸 **Diabetes Prediction** — Estimates diabetes risk using patient information and blood-test measurements, including HbA1c and glucose.
- ❤️ **Heart Disease Prediction** — Uses cardiovascular health indicators to estimate patterns associated with heart disease.
- 🫘 **Kidney Disease Prediction** — Estimates kidney-disease risk using selected clinical measurements and medical-history indicators.
- 📊 **Health Reading Interpretation** — Provides explanatory notes for selected measurements.
- 📄 **Downloadable Reports** — Generates reports containing prediction results, input details, and relevant explanations.
- 🎨 **Interactive UI** — A dark-themed, multi-page interface built with Streamlit.

## 🛠️ Tech Stack

- **Language:** Python
- **Web Framework:** Streamlit
- **Data Processing:** Pandas
- **Machine Learning:** Scikit-learn, XGBoost
- **Model Persistence:** Joblib
- **Version Control:** Git and GitHub

## 🧠 Machine Learning

The application integrates three separately trained machine-learning pipelines:

| Module | Purpose |
|---|---|
| Diabetes | Diabetes-risk estimation |
| Heart Disease | Heart-disease pattern estimation |
| Kidney Disease | Kidney-disease risk estimation |

Each module loads its saved model and processes the inputs required by that model.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/akshays-232/disease-prediction-system.git
cd disease-prediction-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

## 📁 Project Structure

```text
disease-prediction-system/
├── app.py
├── requirements.txt
└── models/
    ├── diabetes_model_final.pkl
    ├── heart_disease_model.pkl
    └── kidney_model.pkl
```

## ⚠️ Disclaimer

This application is intended for **educational and demonstration purposes only**. Its predictions are machine-learning estimates, not medical diagnoses. Model performance and reliability depend on the training data and validation methods. Do not use these results as a substitute for professional medical advice, testing, or treatment.

## 👨‍💻 Author

**Akshay Singh**

- GitHub: [@akshays-232](https://github.com/akshays-232)
- Live Project: [Disease Prediction System](https://discover-disease-prediction-system.streamlit.app/)
