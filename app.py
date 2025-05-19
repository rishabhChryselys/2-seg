import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="SMA Gene Therapy Survey",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_welcome_screen():
    welcome_container = st.container()
    with welcome_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://cdn.capsulcn.com/Content/Images/uploaded/ZOLGENSMA_logo.png", width=200)
            st.title("Welcome to the Gene Therapy HCP Typing Tool")
            st.markdown("""
            ### Purpose of this Tool
            This survey helps categorize healthcare professionals (HCPs) based on their attitudes and practices regarding gene therapy prescribing for SMA patients.
            ### How to Use
            1. Complete the survey with information about the HCP  
            2. Submit the form to receive the HCP categorization  
            3. View detailed scores and recommendations based on the profile  
            ### HCP Categories
            - **Early Adopters**: Confident gene therapy prescribers  
            - **Wait n See Pragmatics**: Prefer more real-world evidence  
            ### Data Privacy
            All submitted information is confidential and used solely for HCP categorization.
            """)
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            if st.button("Continue to Survey", key="welcome_continue"):
                st.session_state.show_welcome = False
            st.markdown("</div>", unsafe_allow_html=True)

def main():
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
        show_welcome_screen()
        return

    # Sidebar
    with st.sidebar:
        st.image("https://cdn.capsulcn.com/Content/Images/uploaded/ZOLGENSMA_logo.png", width=150)
        st.markdown("### About This Survey")
        st.markdown("This tool collects data on SMA gene therapy prescribing practices to categorize HCPs.")
        st.markdown("### HCP Categories")
        st.markdown("**Early Adopters**: Confident in prescribing gene therapies.  \n**Wait n See Pragmatics**: Prefer more evidence before adoption.")
        st.markdown("---")
        st.markdown(f"Survey Date: {datetime.now().strftime('%B %d, %Y')}")

    st.title("Gene Therapy HCP Typing Tool")
    st.markdown("Please complete the following survey to determine the attitudinal segments for an HCP.")

    hcp_data = {
        "1336357615": {"first_name": "KERRI", "last_name": "LAROVERE", "account_site": "BOSTON CHILDRENS HOSPITAL"},
        "1396119806": {"first_name": "CORY", "last_name": "SIEBURG", "account_site": "UNIVERSITY OF WISCONSIN HEALTH UNIVERSITY HOSPITAL"},
        "1457541625": {"first_name": "JEFFREY", "last_name": "BOLTON", "account_site": "BOSTON CHILDRENS HOSPITAL"},
        "1720495757": {"first_name": "IRYNA", "last_name": "KALININA", "account_site": "THE CLEVELAND CLINIC FOUNDATION"},
        "1649552688": {"first_name": "CHANDRABHAGA", "last_name": "MISKIN", "account_site": "SAINT PETERS HEALTHCARE SYSTEM"}
    }

    col1, col2 = st.columns(2)
    with col1:
        npi_id = st.text_input("NPI ID *", placeholder="Enter NPI ID", max_chars=10)

    hcp_info = hcp_data.get(npi_id, {})
    with col2:
        HCP_account_site = st.text_input("HCP Account Site *", value=hcp_info.get("account_site", ""), placeholder="Enter account site")

    col_1, col_2 = st.columns(2)
    with col_1:
        reps_first_name = st.text_input("HCP First Name *", value=hcp_info.get("first_name", ""), placeholder="Enter first name")
    with col_2:
        reps_last_name = st.text_input("HCP Last Name", value=hcp_info.get("last_name", ""), placeholder="Enter last name")

    with st.form("survey_form"):
        input_data = {}

        # Q1
        st.subheader("Q1: Please select the level of satisfaction you have with Spinraza and Evrysdi for SMA patients > 2 years old")
        satisfaction_mapping = {"Satisfied": 1, "Neutral": 2, "Not Satisfied": 3}
        spinraza_satisfaction = st.radio("Spinraza", list(satisfaction_mapping.keys()), index=None, horizontal=True)
        evrysdi_satisfaction = st.radio("Evrysdi", list(satisfaction_mapping.keys()), index=None, horizontal=True)
        input_data['Q1_0'] = spinraza_satisfaction
        input_data['Q1_1'] = evrysdi_satisfaction

        st.markdown("---")

        # Q2
        st.subheader('Q2: Please state your agreement with "As a one-time treatment, I expect gene therapy to provide long-term benefits"')
        q2_answer = st.radio("Agreement Level", ["I Agree", "I Am Neutral", "I Disagree"], index=None)
        input_data['Q2'] = q2_answer

        st.markdown("---")

        # Q3
        st.subheader("Q3: For your SMA patients (> 2 years old), Please select the primary rationale considered for switching to gene therapies from existing therapies")
        q3_answer = st.radio("Primary Rationale", ["Mostly Efficacy", "Balance of Efficacy, Safety, Dosing", "Mostly Dosing"], index=None)
        input_data['Q3'] = q3_answer

        st.markdown("---")

        # Q4
        st.subheader("Q4: Please state whether you have expeirence with Zolgensma IV")
        q4_answer = st.radio("Zolgensma IV Experience", [
            "I have experience prescribing Zolgensma IV",
            "I have limited to no experience prescribing Zolgensma IV"
        ], index=None)
        input_data['Q4'] = q4_answer

        st.markdown("---")

        # Q5
        st.subheader("Q5: Please state if your institution is capable in administering Gene Therapy")
        q5_answer = st.radio("Institution Capability", [
            "Yes my institute is capable in administering Gene Therapy",
            "No my institute is not capable of administering Gene Therapy"
        ], index=None)
        input_data['Q5'] = q5_answer

        submit_col1, submit_col2 = st.columns([15, 5])
        with submit_col2:
            submit_button = st.form_submit_button("Submit Survey")

    if submit_button:
        if not all([npi_id, reps_first_name, spinraza_satisfaction, evrysdi_satisfaction, q2_answer, q3_answer, q4_answer, q5_answer]):
            st.error("Please answer all questions before submitting.")
        else:
            try:
                excel_df = pd.read_csv("data.csv")
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")
                return

            input_text_data = {
                'Q1_0': spinraza_satisfaction,
                'Q1_1': evrysdi_satisfaction,
                'Q2': q2_answer,
                'Q3': q3_answer,
                'Q4': q4_answer,
                'Q5': q5_answer
            }

            matching_df = excel_df.copy()
            for col, val in input_text_data.items():
                matching_df = matching_df[matching_df[col] == val]

            if matching_df.empty:
                st.error("No matching entry found in the Excel sheet for the given inputs.")
            else:
                row = matching_df.iloc[0]
                segment = row['Predicted Segment']
                prediction_score = row.get('Prediction Score', "N/A")

                st.success("Survey submitted successfully!")
                st.subheader("Survey Results")
                st.markdown(
                    f"<strong>Prediction:</strong> The HCP is categorized as a <span style='color: green; font-size: 30px;'>{segment}</span>",
                    unsafe_allow_html=True
                )
                st.metric(label="Prediction Score", value=prediction_score)

                st.subheader("What This Means")
                if segment == "Early Adopter":
                    st.info("This HCP is likely an early adopter of gene therapies and confident in prescribing them.")
                elif segment == "Wait-n-See Pragmatics":
                    st.info("This HCP prefers more real-world evidence and safety reassurance before adopting gene therapies.")
                else:
                    st.warning("This segment label is not recognized. Please check the Excel mapping.")

                with st.expander("View Response Summary"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Respondent Information**")
                        st.write(f"NPI ID: {npi_id}")
                        st.write(f"HCP First Name: {reps_first_name}")
                        st.write(f"HCP Last Name: {reps_last_name}")
                        st.write(f"HCP account Site: {HCP_account_site}")
                        st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
                    with col2:
                        st.write("**Responses**")
                        st.write("**Q1: Please select the level of satisfaction you have with Spinraza and Evrysdi for SMA patients > 2 years old**")
                        st.write(f"Spinraza: {spinraza_satisfaction}, Evrysdi: {evrysdi_satisfaction}")
                        st.write("**Q2: Please state your agreement with 'As a one-time treatment, I expect gene therapy to provide long-term benefits'**")
                        st.write(f"{q2_answer}")
                        st.write("**Q3: For your SMA patients (> 2 years old), Please select the primary rationale considered for switching to gene therapies from existing therapies**")
                        st.write(f"{q3_answer}")
                        st.write("**Q4: Please state whether you have experience with Zolgensma IV**")
                        st.write(f"{q4_answer}")
                        st.write("**Q5: Please state if your institution is capable in administering Gene Therapy**")
                        st.write(f"{q5_answer}")

if __name__ == "__main__":
    main()
