import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FitCheck",
    page_icon="💪",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
import os

from pathlib import Path

MODEL_PATH = Path(__file__).parent / "bmi_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)



# ---------------- HELPER FUNCTIONS ----------------
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def diet_recommendation(category):
    plans = {
        "Underweight": "🍚 Increase calorie intake with carbs, healthy fats, nuts, milk, bananas.",
        "Normal": "🥗 Maintain a balanced diet with fruits, vegetables, whole grains & proteins.",
        "Overweight": "🥦 Focus on low-calorie foods, fiber-rich meals & portion control.",
        "Obese": "🚫 Reduce sugar & junk food. Prefer vegetables, lean protein & hydration."
    }
    return plans.get(category, "Stay healthy!")

def calorie_range(goal):
    if goal == "Weight Loss":
        return "🔻 1500 – 1800 kcal/day"
    elif goal == "Weight Gain":
        return "🔺 2200 – 2600 kcal/day"
    else:
        return "⚖️ 1800 – 2200 kcal/day"

# ---------------- TITLE ----------------
st.title("💪 FitCheck")
st.markdown("**Check your health. Fix your habits.**")
st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🧮 BMI Check", "🥗 Diet Plan", "ℹ️ About"])

# ---------------- TAB 1: BMI CHECK ----------------
with tab1:
    st.header("👤 Enter Your Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 100, 20)
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        height = st.number_input("Height (cm)", 100, 250, 170)
        weight = st.number_input("Weight (kg)", 30, 200, 70)

    goal = st.selectbox("🎯 Health Goal", ["Weight Loss", "Maintain Weight", "Weight Gain"])

    if st.button("🔍 Check My Health"):
        gender_val = 1 if gender == "Male" else 0

        input_df = pd.DataFrame(
            [[gender_val, height, weight]],
            columns=["Gender", "Height", "Weight"]
        )

        category = model.predict(input_df)[0]
        bmi = calculate_bmi(weight, height)

        st.subheader("📊 Results")
        st.success(f"**Your BMI:** {bmi}")
        st.info(f"**BMI Category:** {category}")

# ---------------- TAB 2: DIET PLAN ----------------
with tab2:
    st.header("🥗 Personalized Diet Insight")

    if 'category' in locals():
        st.write(diet_recommendation(category))
        st.subheader("🔥 Daily Calorie Suggestion")
        st.success(calorie_range(goal))
    else:
        st.warning("👉 First calculate your BMI in the BMI Check tab.")

# ---------------- TAB 3: ABOUT ----------------
with tab3:
    st.header("ℹ️ About FitCheck")
    st.write("""
    **FitCheck** is a smart HealthTech  project built using:
    
    • Python  
    • Machine Learning  
    • Streamlit  
    
    It helps users understand their BMI and receive diet suggestions  
    based on simple health inputs.
    """)

# ---------------- FOOTER ----------------
st.divider()
st.caption("Check your fit with Gauri")




