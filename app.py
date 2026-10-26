import pandas as pd
import joblib
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

diabetes_model = joblib.load(MODEL_DIR / "diabetes_model_final.pkl")
heart_model = joblib.load(MODEL_DIR / "heart_disease_model.pkl")
kidney_model=joblib.load(MODEL_DIR/"kidney_model.pkl")

st.set_page_config(
    page_title="🩺 Disease Prediction System",
    layout="wide"
)


st.markdown("""
<style>
/* Sidebar background and spacing */
[data-testid="stSidebar"] {
    background-color: #151923;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Sidebar header */
.sidebar-header {
    padding: 10px 4px 18px 4px;
}

.sidebar-icon {
    background: #29344b;
    color: #a5b4fc;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 14px;
}

.sidebar-header h2 {
    font-size: 23px;
    margin: 0 0 5px 0;
    color: #f1f5f9;
}

.sidebar-header p {
    font-size: 13px;
    color: #9ca3af;
    margin: 0;
}

/* Navigation label */
.sidebar-label {
    color: #9ca3af;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 18px 0 10px 4px;
}

/* Navigation radio options */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #202633;
    border: 1px solid #303849;
    border-radius: 10px;
    padding: 12px 10px;
    margin-bottom: 9px;
    transition: background-color 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #2b3445;
}

/* Footer */
.sidebar-footer {
    margin-top: 30px;
    color: #9ca3af;
    font-size: 12px;
}

.sidebar-footer p {
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-icon">✚</div>
            <h2>Disease Prediction</h2>
            <p>Health Assessment Platform</p>
        </div>
        <hr>
        <p class="sidebar-label">NAVIGATION</p>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Choose Prediction System",
        [
            "🩸 Diabetes Prediction",
            "❤️ Heart Disease Prediction",
            "💊 Kidney Disease Prediction"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
        <div class="sidebar-footer">
            <hr>
            <p>For educational use only.</p>
            <p>Not a medical diagnosis.</p>
        </div>
    """, unsafe_allow_html=True)


if page == "🩸 Diabetes Prediction":
    st.title("🩸 Diabetes Prediction System")

    st.write(
        "Enter your details and blood test results "
        "to view the model's prediction and test interpretation."
    )

    st.info(
        "This application provides model estimates and "
        "educational information, not a medical diagnosis."
    )

    st.subheader("Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        age = st.number_input("Age", min_value=1, max_value=100, value=None)
        bmi = st.number_input("BMI", min_value=10.0, max_value=80.0, value=None)

    with col2:
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])
        heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
        smoking_history = st.selectbox(
            "Smoking History",
            ["never", "No Info", "current", "former"]
        )

    st.subheader("Blood Test Results")

    col3, col4 = st.columns(2)

    with col3:
        hba1c = st.number_input(
            "HbA1c (%)",
            min_value=3.0,
            max_value=15.0,
            value=None,
            step=0.1
        )

    with col4:
        glucose = st.number_input(
            "Random Blood Glucose (mg/dL)",
            min_value=40,
            max_value=500,
            value=None
        )

    predict_button = st.button("Predict and Interpret", type="primary")


    if predict_button:

        if (
        gender == "Select gender"
        or hypertension == "Select"
        or heart_disease == "Select"
        or smoking_history == "Select"
        or age is None
        or bmi is None
        or hba1c is None
        or glucose is None
    ):
            st.error("Please fill in all required fields.")
            st.stop()

        patient = pd.DataFrame({
            "gender": [gender],
            "age": [age],
            "hypertension": [1 if hypertension == "Yes" else 0],
            "heart_disease": [1 if heart_disease == "Yes" else 0],
            "smoking_history": [smoking_history],
            "bmi": [bmi],
            "HbA1c_level": [hba1c],
            "blood_glucose_level": [glucose]
        })

        probabilities = diabetes_model.predict_proba(patient)[0]
        diabetes_probability = probabilities[list(diabetes_model.classes_).index(1)]

        threshold = 0.40
        prediction = int(diabetes_probability >= threshold)


        st.subheader("Prediction Results")

        if prediction == 1:
            st.warning("**Model result: Diabetes predicted**")
        else:
            st.info("**Model result: Diabetes not predicted**")


        def interpret_hba1c(hba1c):
            if hba1c < 5.7:
                return "Normal Range"
            elif hba1c < 6.5:
                return "Pre-diabetic Range"
            else:
                return "Diabetic Range"


        def interpret_glucose(glucose):
            if glucose< 140:
                return "Normal"
            elif glucose < 200:
                return "Elevated"
            else:
                return "Significantly Elevated"


        def final_interpretation(hba1c,glucose):

            if hba1c == "Normal Range":
                if glucose == "Normal":
                    return {
                        "interpretation": "Both readings are within normal range.",
                        "next step": [
                            "Continue your usual healthy lifestyle."
                        ]
                    }
                
                elif glucose == "Elevated":
                    return {
                        "interpretation": "Your glucose is slightly elevated,but HbA1c is normal.",
                        "next step": [
                            "If the reading stays high, arrange follow-up testing."
                        ]
                    }

                else:
                    return {
                        "interpretation": "Your glucose is significantly high,despite a normal HbA1c.",
                        "next step": [
                            "Seek medical assesment,specially at 200 mg/dL or above.",
                            "Report unusual symptoms."
                        ]
                    }
            
            elif hba1c == "Pre-diabetic Range":
                if glucose == "Normal":
                    return{
                        "interpretation": "Your HbA1c is in pre-diabetic range but your glucose level is normal.",
                        "next step": [
                            "Maintain a healthy lifestyle.",
                            "Follow routine testing advice."
                        ]
                    }

                elif glucose == "Elevated":
                    return {
                        "interpretation": "Your HbA1c is in pre-diabetic range and glucose is elevated.",
                        "next step": [
                            "Get your blood sugar checked again."
                        ]
                    }

                else:
                    return {
                        "interpretation": "Your glucose is very high while HbA1c is in pre-diabetic range.",
                        "next step": [
                            "Seek prompt medical assessment, especially at 200 mg/dL or above. ",
                            "Report unusual symptoms.",
                            "Seek emergency care for severe symptoms such as vomiting, abdominal pain, or rapid/deep breathing."
                        ]
                    }

            else:

                if glucose == "Normal":
                    return {
                        "interpretation": "Your HbA1c is high, but your current glucose is lower.",
                        "next step": [
                            "Discuss your HbA1c result with a doctor."
                        ]
                    }

                elif glucose == "Elevated":
                    return {
                        "interpretation": "Your HbA1c is high, and your glucose is also elevated.",
                        "next step": [
                            "Arrange medical assessment.",
                            "Discuss any follow-up tests or care needed."
                        ]
                    }

                else:
                    return {
                        "interpretation": "Both your HbA1c and glucose are high.",
                        "next step": [
                            "Seek prompt medical assessment, especially at 200 mg/dL or above.",
                            "Report unusual symptoms.",
                            "Seek emergency care for severe symptoms such as vomiting, abdominal pain, or rapid/deep breathing."
                        ]
                    }

        hba1c_value = patient["HbA1c_level"].iloc[0]
        glucose_value = patient["blood_glucose_level"].iloc[0]

        hba1c_result = interpret_hba1c(hba1c_value)
        glucose_result = interpret_glucose(glucose_value)
        summary = final_interpretation(hba1c_result, glucose_result)


        st.subheader("Blood Test Interpretation")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("HbA1c", f"{hba1c_value:.1f}%")
            st.caption(f"Interpretation: {hba1c_result}")

        with col2:
            st.metric("Random Blood Glucose", f"{glucose_value} mg/dL")
            st.caption(f"Interpretation: {glucose_result}")

        if hba1c_result == "Normal Range" and glucose_result == "Normal":
            st.success(summary["interpretation"])
        else:
            st.warning(summary["interpretation"])


        st.subheader("Recommended Next Steps")
        next_steps = summary["next step"]

        if isinstance(next_steps, str):
            next_steps = [next_steps]

        for step in next_steps:
            st.markdown(f"- {step}")

        next_steps_text = "\n".join(f"- {step}" for step in next_steps)

        report = f"""
        DIABETES PREDICTION REPORT
        ==========================

        PATIENT INFORMATION
        Age: {age}
        Gender: {gender}
        BMI: {bmi}
        Hypertension: {hypertension}
        Heart Disease: {heart_disease}
        Smoking History: {smoking_history}

        BLOOD TEST RESULTS
        HbA1c: {hba1c_value}%
        Random Blood Glucose: {glucose_value} mg/dL

        MODEL RESULT
        {"Diabetes predicted" if prediction == 1 else "Diabetes not predicted"}

        BLOOD TEST INTERPRETATION
        {summary["interpretation"]}

        RECOMMENDED NEXT STEPS
        {next_steps_text}
            """

        st.download_button(
            label="Download Report",
            data=report,
            file_name="diabetes_prediction_report.txt",
            mime="text/plain"
        )

elif page == "❤️ Heart Disease Prediction":
    st.title("❤️ Heart Disease Prediction")
    st.write("Enter patient details to get the model's prediction.")

    st.info(
        "This tool provides educational model estimates, "
        "not a medical diagnosis."
    )

    st.subheader("Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=None)
        gender = st.selectbox("Gender", [ "M", "F"])
        chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "ASY", "TA"])
        resting_bp = st.number_input(
            "Resting Blood Pressure (mm Hg)",
            min_value=1, max_value=300, value=None
        )
        cholesterol = st.number_input(
            "Cholesterol (mg/dL)",
            min_value=0, max_value=700, value=None
        )
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL?", [0, 1])

    with col2:
        resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        max_hr = st.number_input(
            "Maximum Heart Rate", min_value=60, max_value=220, value=None
        )
        exercise_angina = st.selectbox("Exercise-Induced Angina", ["N", "Y"])
        oldpeak = st.number_input(
            "Oldpeak", min_value=-3.0, max_value=7.0, value=None, step=0.1
        )
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    
    if st.button("Predict Heart Disease", type="primary"):

        if any(v is None for v in [
            age, resting_bp, cholesterol, max_hr, oldpeak
        ]):
            st.error("Please fill in all fields before predicting.")
            st.stop()

        else:
            patient = pd.DataFrame([{
                "Age": age,
                "Gender": gender,
                "ChestPainType": chest_pain,
                "RestingBP": resting_bp,
                "Cholesterol": cholesterol,
                "FastingBS": fasting_bs,
                "RestingECG": resting_ecg,
                "MaxHR": max_hr,
                "ExerciseAngina": exercise_angina,
                "Oldpeak": oldpeak,
                "ST_Slope": st_slope
            }])

        prediction = heart_model.predict(patient)[0]
        probability = heart_model.predict_proba(patient)[0][1]

        st.subheader("Prediction Results")

        if prediction == 1:
            st.warning("The model predicts a pattern associated with heart disease.")
            st.write(
                "Please consult a healthcare professional for further evaluation."
            )
        else:
            st.success("The model does not predict a pattern associated with heart disease.")
            st.write(
                    "Continue maintaining a healthy lifestyle with regular physical activity, a balanced diet, "
                    "and routine health checkups."
            )
            

        st.divider()
        st.subheader("Heart Health Readings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Resting Blood Pressure**")
            st.metric("Reading", f"{resting_bp} mmHg")

            if resting_bp >= 140:
                st.warning("High resting blood pressure.")
            elif resting_bp >= 130:
                st.info("Above the ideal range; discuss it with a healthcare professional.")
            elif resting_bp < 90:
                st.info("Low blood pressure; interpretation depends on symptoms and context.")
            else:
                st.info("Within the usual adult range for this reading.")

            st.markdown("**Cholesterol**")
            st.metric("Reading", f"{cholesterol} mg/dL")

            if cholesterol >= 240:
                st.warning("High total cholesterol.")
            elif cholesterol >= 200:
                st.info("Borderline-high total cholesterol.")
            elif cholesterol > 0:
                st.info("Below 200 mg/dL, generally considered desirable for total cholesterol.")

        with col2:
            st.markdown("**Maximum Heart Rate During Exercise**")
            st.metric("Reading", f"{max_hr} bpm")
            st.info(
                "Interpretation depends on age, fitness, medication, "
                "and the exercise performed."
            )

            st.markdown("**Fasting Blood Sugar**")
            st.metric("Reading", "Above 120 mg/dL" if fasting_bs == 1 else "120 mg/dL or below")

            if fasting_bs == 1:
                st.warning(
                    "Elevated fasting blood sugar can be associated with increased "
                    "cardiovascular risk. Follow up with a healthcare professional."
                )
            else:
                st.info(
                    "This indicator is not elevated according to the model's threshold. "
                    "It does not rule out blood sugar problems."
                )

        
        report = f"""
    HEART DISEASE PREDICTION REPORT
    ================================

    PREDICTION RESULT
    -----------------
    {"Heart disease pattern detected" if prediction == 1 else "No heart disease pattern detected"}

    PATIENT INFORMATION
    -------------------
    Age: {age}
    Gender: {gender}

    INPUT READINGS
    --------------
    Chest Pain Type: {chest_pain}
    Resting Blood Pressure: {resting_bp} mmHg
    Cholesterol: {cholesterol} mg/dL
    Fasting Blood Sugar > 120 mg/dL: {"Yes" if fasting_bs == 1 else "No"}
    Resting ECG: {resting_ecg}
    Maximum Heart Rate During Exercise: {max_hr} bpm
    Exercise-Induced Angina: {exercise_angina}
    Oldpeak: {oldpeak}
    ST Slope: {st_slope}

    HEALTH READING NOTES
    --------------------
    Blood pressure: {"Above the ideal range; discuss with a healthcare professional." if resting_bp >= 130 
                     else "Below the 130 mmHg threshold used in this report."}
    Cholesterol: {"High total cholesterol." if cholesterol >= 240 else "Borderline high total cholesterol." 
                  if cholesterol >= 200 else "Desirable total cholesterol range."}
    Maximum heart rate: Interpretation depends on age, fitness, medication, and exercise performed.
    Fasting blood sugar: {"Above the model's 120 mg/dL threshold; follow up with a healthcare professional." 
                          if fasting_bs == 1 else "Not above the model's 120 mg/dL threshold."}

    IMPORTANT DISCLAIMER
    --------------------
    This report contains machine-learning estimates, not a medical diagnosis.
    A negative prediction does not rule out heart disease. Seek medical
    evaluation for concerning symptoms or health readings.

    """
        st.download_button(
        label="Download Report",
        data=report,
        file_name="heart_disease_report.txt",
        mime="text/plain"
    )


elif page == "💊 Kidney Disease Prediction":
    st.title("💊 Kidney Disease Prediction")
    st.caption(
        "Enter patient details and kidney function test results "
        "to view the model's prediction."
    )
    st.info(
        "This tool provides educational model estimates, not a medical diagnosis."
    )

    st.subheader("Patient Information")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=None)
        gender = st.selectbox("Gender", ["Male", "Female"])
        creatinine = st.number_input(
            "Serum Creatinine (mg/dL)",
            min_value=0.1, max_value=20.0, value=None, step=0.1
        )
        urine_albumin = st.number_input(
            "Urine Albumin-Creatinine Ratio (mg/g)",
            min_value=0.0, max_value=5000.0, value=None, step=1.0
        )
        

    with col2:
        potassium = st.number_input(
            "Potassium (mmol/L)",
            min_value=1.0, max_value=10.0, value=None, step=0.1
        )
        systolic_bp = st.number_input(
            "Systolic Blood Pressure (mmHg)",
            min_value=50, max_value=250, value=None
        )
        diabetes = st.selectbox("Diabetes", ["No", "Yes"])
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])

    predict_clicked = st.button("Predict Kidney Disease", use_container_width=True)
    if predict_clicked:
        if any(v is None for v in [
            age, creatinine, urine_albumin, potassium, systolic_bp
        ]):
            st.error("Please fill in all required fields.")
            st.stop()

        input_data = pd.DataFrame([{
            "Age_years": age,
            "Gender": gender,
            "SerumCreatinine_mg_dL": creatinine,
            "UrineAlbuminCreatinineRatio_mg_g": urine_albumin,
            "Potassium_mmol_L": potassium,
            "SystolicBP_mmHg": systolic_bp,
            "Diabetes": 1 if diabetes == "Yes" else 0,
            "Hypertension": 1 if hypertension == "Yes" else 0
        }])

        prediction = kidney_model.predict(input_data)[0]

        if prediction == 1:
            st.warning("The model detected a pattern associated with kidney disease.",
                icon="⚠️")
            st.write("Please consult a healthcare professional for further evaluation.")
        else:
            st.success("The model did not detect a pattern associated with kidney disease.",
                icon="✅")
            st.write("Continue looking after your health and attend routine checkups.")


        st.divider()
        st.subheader("Kidney Health Readings")

        # Serum Creatinine
        st.markdown("**Serum Creatinine**")
        st.metric("Reading", f"{creatinine:.1f} mg/dL")

        if (gender == "Male" and creatinine > 1.3) or (
            gender == "Female" and creatinine > 1.1
        ):
            st.warning(
                "This reading may be elevated. Higher creatinine can be associated "
                "with reduced kidney filtration. Discuss it with a healthcare professional."
            )
        else:
            st.info(
                "This reading is not above the approximate threshold used here. "
                "Creatinine ranges vary by laboratory and individual."
            )

        # Urine Albumin-Creatinine Ratio
        st.markdown("**Urine Albumin-Creatinine Ratio (UACR)**")
        st.metric("Reading", f"{urine_albumin:.1f} mg/g")

        if urine_albumin < 30:
            st.success("Below 30 mg/g is generally considered the normal-to-mildly increased range.")
        elif urine_albumin <= 300:
            st.warning(
                "30–300 mg/g is a moderately increased range. "
                "Discuss this result with a healthcare professional."
            )
        else:
            st.warning(
                "Above 300 mg/g is a severely increased range. "
                "Prompt medical follow-up is recommended."
            )

        # Potassium
        st.markdown("**Serum Potassium**")
        st.metric("Reading", f"{potassium:.1f} mmol/L")

        if potassium < 3.5:
            st.warning("This is below the common adult reference range; seek medical advice.")
        elif potassium > 5.0:
            st.warning("This is above the common adult reference range; seek medical advice.")
        else:
            st.info(
                "This falls within a common adult reference range of approximately "
                "3.5–5.0 mmol/L. Your laboratory's range may differ."
            )

        st.divider()
        st.subheader("Download Kidney Assessment Report")

        kidney_result = (
            "Pattern associated with kidney disease detected"
            if prediction == 1
            else "No kidney-disease-associated pattern detected"
        )

        kidney_report = f"""
    KIDNEY DISEASE PREDICTION REPORT
    ================================

    MODEL RESULT
    ------------
    {kidney_result}

    PATIENT INFORMATION
    -------------------
    Age: {age}
    Gender: {gender}
    Diabetes: {diabetes}
    Hypertension: {hypertension}

    KIDNEY HEALTH READINGS
    ----------------------
    Serum Creatinine: {creatinine:.1f} mg/dL
    Urine Albumin-Creatinine Ratio: {urine_albumin:.1f} mg/g
    Serum Potassium: {potassium:.1f} mmol/L
    Systolic Blood Pressure: {systolic_bp} mmHg

    IMPORTANT NOTE
    --------------
    This report contains an educational machine-learning estimate,
    not a medical diagnosis. The prediction cannot confirm or rule
    out kidney disease. Consult a healthcare professional for
    clinical interpretation of these readings.
    """

        st.download_button(
            label="Download Kidney Report",
            data=kidney_report,
            file_name="kidney_assessment_report.txt",
            mime="text/plain"
        )