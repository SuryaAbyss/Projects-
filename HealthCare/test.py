import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Health Report Analysis Dashboard",
    page_icon="🏥",
    layout="wide"
)

# # Load sample data for demonstration
# def load_data():
#     df = pd.read_json("health_data.json", lines=True)

#     # Convert date columns
#     df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
#     df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
#     return df

df = pd.read_csv('healthcare_with_predictions_lim.csv')

# If Date columns are strings, convert them to datetime with correct format
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], format='%d-%m-%Y', dayfirst=True)
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], format='%d-%m-%Y', dayfirst=True)

# Create a sidebar for filters
with st.sidebar:
    st.title("Data Filters")
    
    # Date range filter
    min_date = df['Date of Admission'].min()
    max_date = df['Date of Admission'].max()
    date_range = st.date_input("Select Date Range", [min_date, max_date])
    
    # Other filters
    selected_gender = st.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())
    selected_hospital = st.multiselect("Select Hospital", df['Hospital'].unique(), default=df['Hospital'].unique())
    selected_condition = st.multiselect("Select Condition", df['Medical Condition'].unique(), default=df['Medical Condition'].unique())
    
    # Apply filters
    filtered_df = df[
        (df['Date of Admission'].dt.date >= date_range[0]) &
        (df['Date of Admission'].dt.date <= date_range[1]) &
        (df['Gender'].isin(selected_gender)) &
        (df['Hospital'].isin(selected_hospital)) &
        (df['Medical Condition'].isin(selected_condition))
    ]

# Title
st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style='color: #0066cc;'>📊</span> Health Report Analysis Dashboard <span style='color: #0066cc;'>📊</span>
    </h1>
    """,
    unsafe_allow_html=True
)

# Part 1: Summary Statistics (Top Overview Panel)
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>📊 Summary Statistics</h2>", unsafe_allow_html=True)

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Patients",
        value=filtered_df.shape[0],
        delta=f"{filtered_df.shape[0] - df.shape[0]} from last period",
        help="Total number of patients in the filtered dataset"
    )

with col2:
    most_common_condition = filtered_df['Medical Condition'].mode()[0]
    condition_count = filtered_df['Medical Condition'].value_counts().max()
    st.metric(
        label="Most Common Condition",
        value=most_common_condition,
        delta=f"{condition_count} cases",
        help="Most frequent medical condition among patients"
    )

with col3:
    most_visited_hospital = filtered_df['Hospital'].mode()[0]
    hospital_visits = filtered_df['Hospital'].value_counts().max()
    st.metric(
        label="Most Visited Hospital",
        value=most_visited_hospital,
        delta=f"{hospital_visits} visits",
        help="Hospital with the highest number of patient visits"
    )

with col4:
    total_expenditure = filtered_df['Billing Amount'].sum()
    st.metric(
        label="Total Healthcare Expenditure",
        value=f"${total_expenditure:,.2f}",
        delta=f"${total_expenditure - df['Billing Amount'].sum():,.2f} from last period",
        help="Total amount spent on healthcare for all patients in the dataset"
    )

with col5:
    avg_length_of_stay = filtered_df['Length of Stay'].mean()
    st.metric(
        label="Average Length of Stay",
        value=f"{avg_length_of_stay:.1f} days",
        delta=f"{avg_length_of_stay - df['Length of Stay'].mean():.1f} days from last period",
        help="Average number of days patients stayed in the hospital"
    )

# Top 3 Doctors by Patient Count
top_doctors = filtered_df['Doctor'].value_counts().head(3).reset_index()
top_doctors.columns = ['Doctor', 'Patient Count']

st.markdown("<h3>Top Doctors by Patient Count</h3>", unsafe_allow_html=True)
fig = px.bar(top_doctors, x='Patient Count', y='Doctor', orientation='h', 
             title="Top 3 Doctors by Patient Count",
             color='Doctor', 
             color_continuous_scale=px.colors.sequential.Blues)
st.plotly_chart(fig, use_container_width=True)

# Part 2: Insights via Interactive Charts (Analytics Panel)
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>📈 Data Insights</h2>", unsafe_allow_html=True)

# Two columns layout for charts
col1, col2 = st.columns(2)

with col1:
    # Patient Age Group Distribution
    st.markdown("<h3>Patient Age Group Distribution</h3>", unsafe_allow_html=True)
    age_group_counts = filtered_df['Age_Group'].value_counts().reset_index()
    age_group_counts.columns = ['Age Group', 'Count']
    
    fig = px.pie(age_group_counts, names='Age Group', values='Count', 
                 title="Age Group Distribution",
                 color_discrete_sequence=px.colors.sequential.Reds)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Blood Type Frequency
    st.markdown("<h3>Blood Type Frequency</h3>", unsafe_allow_html=True)
    blood_type_counts = filtered_df['Blood Type'].value_counts().reset_index()
    blood_type_counts.columns = ['Blood Type', 'Count']
    
    fig = px.bar(blood_type_counts, x='Blood Type', y='Count',
                 title="Blood Type Frequency",
                 color='Count', 
                 color_continuous_scale=px.colors.sequential.Greens)
    st.plotly_chart(fig, use_container_width=True)

# Two columns for next set of charts
col1, col2 = st.columns(2)

with col1:
    # Condition Frequency
    st.markdown("<h3>Condition Frequency</h3>", unsafe_allow_html=True)
    condition_counts = filtered_df['Medical Condition'].value_counts().reset_index()
    condition_counts.columns = ['Condition', 'Count']
    
    fig = px.bar(condition_counts, x='Condition', y='Count',
                 title="Medical Condition Frequency",
                 color='Count', 
                 color_continuous_scale=px.colors.sequential.Purples)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Average Billing by Age Group
    st.markdown("<h3>Average Billing by Age Group</h3>", unsafe_allow_html=True)
    avg_billing_age = filtered_df.groupby('Age_Group')['Billing Amount'].mean().reset_index()
    avg_billing_age.columns = ['Age Group', 'Average Billing']
    
    fig = px.line(avg_billing_age, x='Age Group', y='Average Billing',
                  title="Average Billing Amount by Age Group",
                  markers=True,
                  color_discrete_sequence=px.colors.qualitative.D3)
    st.plotly_chart(fig, use_container_width=True)

# Two columns for next set of charts
col1, col2 = st.columns(2)

with col1:
    # Condition Risk Level Distribution
    st.markdown("<h3>Condition Risk Level Distribution</h3>", unsafe_allow_html=True)
    risk_counts = filtered_df['Condition_Risk'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']
    
    fig = px.pie(risk_counts, names='Risk Level', values='Count',
                 title="Condition Risk Distribution",
                 color_discrete_sequence=px.colors.sequential.YlOrRd)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Admissions by Season
    st.markdown("<h3>Admissions by Season</h3>", unsafe_allow_html=True)
    season_counts = filtered_df['Season'].value_counts().reset_index()
    season_counts.columns = ['Season', 'Count']
    
    fig = px.bar(season_counts, x='Season', y='Count',
                 title="Admissions by Season",
                 color='Count', 
                 color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig, use_container_width=True)

# Prediction Probability Distribution
st.markdown("<h3>Prediction Probability Distribution</h3>", unsafe_allow_html=True)
prob_counts = filtered_df['Prediction_Probability'].value_counts(bins=5).reset_index()
prob_counts.columns = ['Probability Range', 'Count']
prob_counts['Probability Range'] = prob_counts['Probability Range'].apply(lambda x: f"{x.left:.1f}-{x.right:.1f}")

fig = px.histogram(prob_counts, x='Probability Range', y='Count',
                   title="Distribution of Prediction Probabilities",
                   color='Probability Range',
                   color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

# # Part 3: Patient Lookup & Detailed View (Search Panel)
# st.markdown("---")

# Search functionality with improved accuracy and styling
with st.container():
    st.markdown(
        """
        <style>
    .search-section {
        background-color: #000000;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .search-input {
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        width: 100%;
        margin-bottom: 15px;
        color: white; /* ✅ Text color so it's visible */
        background-color: #1a1a1a; /* Optional: darker input background for contrast */
    }

    .search-results-info {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
    }

    .patient-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .risk-alert {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 15px;
    }
</style>

        """,
        unsafe_allow_html=True
    )
    st.markdown("<h2>🔍 Patient Lookup</h2>", unsafe_allow_html=True)
    
    search_term = st.text_input(
        "Search by Patient Name, ID, Condition, Doctor, or Hospital:",
        "",
        help="Enter search term. You can search by partial names or terms.",
        key="patient_search"
    )
    
    if search_term:
        # Convert search term to lowercase for case-insensitive search
        search_term_lower = search_term.lower()
        
        # Search in multiple relevant fields
        search_results = filtered_df[
            filtered_df['Name'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['Medical Condition'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['Doctor'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['Hospital'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['Insurance Provider'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['Medication'].str.lower().str.contains(search_term_lower, na=False)
        ]
        
        if not search_results.empty:
            # Display number of results found
            st.markdown(f"<p class='search-results-info'>Found {len(search_results)} matching records</p>", 
                       unsafe_allow_html=True)
            
            # Allow selection from search results with more details
            selected_patient = st.selectbox(
                "Select Patient to View Details:",
                options=search_results['Name'].tolist(),
                format_func=lambda x: f"{x} - {search_results[search_results['Name'] == x]['Medical Condition'].iloc[0]} - {search_results[search_results['Name'] == x]['Hospital'].iloc[0]}"
            )
            
            if selected_patient:
                patient_data = search_results[search_results['Name'] == selected_patient].iloc[0]
                
                # Display detailed information in a card layout with improved styling
                # st.markdown('<div class="patient-card">', unsafe_allow_html=True)
                st.markdown(f"""
                    <h3>Patient Details: {patient_data['Name']}</h3>
                    <div style='display: flex; gap: 20px; margin-top: 15px;'>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                        <div style='background-color: rgb(34 81 54); padding: 2px; border-radius: 5px;'>
                            <h4>Personal Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Age**: {patient_data['Age']} ({patient_data['Age_Group']})")
                    st.markdown(f"- **Gender**: {patient_data['Gender']}")
                    st.markdown(f"- **Blood Type**: {patient_data['Blood Type']}")
                    
                    st.markdown("""
                        <h4>Hospital Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Hospital**: {patient_data['Hospital']}")
                    st.markdown(f"- **Doctor**: {patient_data['Doctor']}")
                    st.markdown(f"- **Room Number**: {patient_data['Room Number']}")
                    
                    st.markdown("""
                        <h4>Stay Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Admission Date**: {patient_data['Date of Admission'].strftime('%Y-%m-%d')}")
                    st.markdown(f"- **Discharge Date**: {patient_data['Discharge Date'].strftime('%Y-%m-%d')}")
                    st.markdown(f"- **Length of Stay**: {patient_data['Length of Stay']} days")
                    st.markdown(f"- **Season**: {patient_data['Season']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div style='background-color: rgb(34 81 54); padding: 2px; border-radius: 5px;'>
                            <h4>Medical Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Medical Condition**: {patient_data['Medical Condition']}")
                    st.markdown(f"- **Condition Risk**: {patient_data['Condition_Risk']} (1=Low, 5=High)")
                    st.markdown(f"- **Test Results**: {patient_data['Test Results']}")
                    
                    st.markdown("""
                        <h4>Treatment Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Medication**: {patient_data['Medication']}")
                    st.markdown(f"- **Test Prediction**: {patient_data['Test_Prediction']}")
                    st.markdown(f"- **Prediction Probability**: {patient_data['Prediction_Probability']:.2f}")
                    
                    st.markdown("""
                        <h4>Billing Information</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"- **Billing Amount**: ${patient_data['Billing Amount']:.2f}")
                    st.markdown(f"- **Insurance Provider**: {patient_data['Insurance Provider']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Risk indicator with improved visibility
                if patient_data['Condition_Risk'] >= 4:
                    st.markdown('<div class="risk-alert">', unsafe_allow_html=True)
                    st.markdown("<h4>⚠️ High Risk Alert ⚠️</h4>", unsafe_allow_html=True)
                    st.markdown(f"- **Condition**: {patient_data['Medical Condition']}")
                    st.markdown(f"- **Risk Level**: {patient_data['Condition_Risk']}/5")
                    st.markdown(f"- **Test Results**: {patient_data['Test Results']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Visualize bill distribution with improved styling
                st.markdown("<h4>Billing Comparison</h4>", unsafe_allow_html=True)
                bill_comparison = filtered_df[filtered_df['Medical Condition'] == patient_data['Medical Condition']]
                fig = px.box(bill_comparison, x='Medical Condition', y='Billing Amount',
                            title=f"Billing Amount Comparison for {patient_data['Medical Condition']}",
                            color_discrete_sequence=['#0066cc'])
                
                # Highlight the selected patient's billing amount
                fig.add_vline(x=patient_data['Billing Amount'], line=dict(color='red', dash='dash'))
                fig.add_annotation(x=patient_data['Medical Condition'], y=patient_data['Billing Amount'],
                                  text=f"Your bill: ${patient_data['Billing Amount']:.2f}",
                                  showarrow=False)
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No patients found matching the search criteria. Try a different search term.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Advanced Predictive Insights Section
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>🔮 Predictive Insights</h2>", unsafe_allow_html=True)

# Two columns for predictive insights
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>High-Risk Patients with Normal Test Results</h3>", unsafe_allow_html=True)
    high_risk_normal = filtered_df[
        (filtered_df['Condition_Risk'] >= 4) & 
        (filtered_df['Test Results'] == 'Normal')
    ]
    
    if not high_risk_normal.empty:
        st.dataframe(high_risk_normal[['Name', 'Medical Condition', 'Condition_Risk', 'Test Results']])
    else:
        st.info("No high-risk patients with normal test results found in this dataset.")

with col2:
    st.markdown("<h3>Predictions of Future Hospital Visits</h3>", unsafe_allow_html=True)
    future_visits = filtered_df[filtered_df['Test_Prediction'] == 'At Risk']
    
    if not future_visits.empty:
        future_visits = future_visits.sort_values('Prediction_Probability', ascending=False).head(5)
        st.dataframe(future_visits[['Name', 'Medical Condition', 'Test_Prediction', 'Prediction_Probability']])
    else:
        st.info("No patients at risk of future hospital visits found in this dataset.")

# Outlier detection: Unusually high billing
st.markdown("<h3>Outlier Detection: Unusually High Billing</h3>", unsafe_allow_html=True)
high_billing = filtered_df[filtered_df['Billing Amount'] > filtered_df['Billing Amount'].quantile(0.95)]
if not high_billing.empty:
    st.dataframe(high_billing[['Name', 'Medical Condition', 'Billing Amount', 'Insurance Provider']])
else:
    st.info("No unusually high billing amounts detected in this dataset.")

# Footer
st.markdown("---")
st.markdown(
    """
    <style>
        footer {
            text-align: center;
        }
    </style>
    <footer>
        <p>📊 Health Report Analysis Dashboard - Developed with Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
        }
        .stMetricValue {
            font-size: 24px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)