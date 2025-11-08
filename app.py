import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

API_BASE = os.environ.get("API_BASE", "https://career-kol5.onrender.com")

st.set_page_config(
    page_title="Career Outcomes Agent", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎓"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #d4edda;
        border-left-color: #28a745;
    }
    .info-card {
        background: #d1ecf1;
        border-left-color: #17a2b8;
    }
    .warning-card {
        background: #fff3cd;
        border-left-color: #ffc107;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 Career Outcomes Intelligence Platform</h1>
    <p style="margin: 0; font-size: 1.2em; opacity: 0.9;">AI-Powered Career Insights for Indian Educational Institutions</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1em; opacity: 0.8;">Real-time data analysis with 2025-2030 projections</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with agent information
with st.sidebar:
    st.markdown("## 🤖 How the Agent Works")
    st.markdown("""
    **Technology Stack:**
    - **Backend:** FastAPI (Python web framework)
    - **Frontend:** Streamlit (Python web app framework)
    - **Data Processing:** Pandas, NumPy
    - **Search:** Gemini-powered embeddings + BM25 fallback
    - **AI:** Google Gemini 2.5 Flash (with offline fallback)
    
    **Agent Capabilities:**
    - 🤖 Gemini-powered insights and analysis
    - 📊 Real-time data analysis
    - 🔍 Intelligent document retrieval
    - 📈 ROI calculations with AI recommendations
    - 🏛️ Institution comparisons
    - 📋 Support services indexing
    
    **Data Sources:**
    - Employment rates by institution
    - Salary data with percentiles
    - Support services information
    - Career outcome reports
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    1. **Dashboard:** Enter degree and year
    2. **Insights:** Ask questions about careers
    3. **Support:** View institution services
    4. **Compare:** Analyze two institutions
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Gemini Configuration")
    
    # Check Gemini status
    try:
        resp = requests.get(f"{API_BASE}/", timeout=2)
        if resp.ok:
            st.success("✅ Backend connected")
        else:
            st.error("❌ Backend not responding")
    except:
        st.error("❌ Backend not running")
    
    st.markdown("**AI Status:**")
    st.info("🤖 Google Gemini 2.5 Flash integration enabled with offline fallback")
    
    st.markdown("---")
    st.markdown("### 📊 Data Quality")
    st.info("Data is processed using Gemini-powered analysis with statistical fallback for reliability.")

# Tabs
tabs = st.tabs([
    "🎓 Career Outcomes Dashboard",
    "💼 Employment Rate Insights", 
    "🧭 Post-Graduation Support Tools",
    "📊 Compare Institutions"
])

with tabs[0]:
    st.subheader("📊 Real-time Career Outcomes Analysis")
    st.markdown("Enter your degree program and graduation year to get personalized career insights.")
    
    # Create a form container
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            degree = st.text_input(
                "🎓 Degree Program", 
                placeholder="e.g., Computer Science, Engineering, Data Science", 
                key="degree_dashboard",
                help="Enter the field of study you're interested in"
            )
        with col2:
            year = st.number_input(
                "📅 Graduation Year", 
                min_value=2020, max_value=2035, value=2025, step=1, 
                key="year_dashboard",
                help="Select your expected graduation year"
            )
    
    year_val = int(year) if year else None
    
    if st.button("🔍 Analyze Outcomes", type="primary"):
        with st.spinner("Fetching real-time data..."):
            resp = requests.post(f"{API_BASE}/analyze", json={"degree": degree, "year": year_val})
            if resp.ok:
                data = resp.json()
                
                # Display summary with enhanced metrics
                st.success(data.get("summary"))
                
                # Show data quality info
                if "data_quality" in data:
                    st.info(f"📈 {data['data_quality']}")
                
                # Display trend if available
                if "trend" in data:
                    trend_color = "🟢" if data["trend"] == "improving" else "🔴" if data["trend"] == "declining" else "🟡"
                    st.metric("Market Trend", f"{trend_color} {data['trend'].title()}")
                
                # Show top institutions
                top = data.get("top_institutions", [])
                if top:
                    df = pd.DataFrame(top)
                    st.subheader("🏆 Top Performing Institutions")
                    
                    # Create enhanced chart
                    fig = px.bar(df, x="institution", y="avg_employment_rate", 
                               title="Employment Rate by Institution",
                               color="avg_employment_rate",
                               color_continuous_scale="Viridis")
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display detailed table
                    st.dataframe(df, use_container_width=True)
                
                # Show median salary if available
                if "median_salary" in data:
                    st.metric("Median Starting Salary", f"₹{data['median_salary']:,}")
                    
            else:
                st.error("❌ Failed to fetch analysis. Please check if the backend is running.")

with tabs[1]:
    st.subheader("🤖 AI-Powered Insight Generator")
    st.markdown("Ask questions about career outcomes, salary trends, and employment data using natural language.")
    
    # Pre-defined question templates for Indian institutions
    sample_questions = [
        "What are the top 5 employment outcomes for Computer Science graduates from VIT University in 2025?",
        "Which Indian institutions have the highest starting salaries in 2028?",
        "How do employment rates vary between IITs and private universities for 2030 graduates?",
        "What support services are most effective for career success in Indian universities?",
        "What are the salary trends for Engineering graduates from SRM, Amrita, and KL University through 2030?",
        "How will AI and automation affect job prospects for Indian graduates by 2030?"
    ]
    
    # Display sample questions as clickable buttons
    st.markdown("**💡 Sample Questions (click to use):**")
    cols = st.columns(2)
    for i, sample_q in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(f"💡 {sample_q[:50]}...", key=f"sample_{i}", help=sample_q):
                st.session_state.selected_question = sample_q
    
    # Pre-fill with selected question if any
    default_question = st.session_state.get('selected_question', '')
    question = st.text_area(
        "💬 Your Question:", 
        value=default_question, 
        placeholder="e.g., What are the employment prospects for Data Science graduates?", 
        height=100,
        help="Ask any question about career outcomes, salaries, or institutional comparisons"
    )
    
    if st.button("🚀 Generate Insights", type="primary") and question:
        with st.spinner("Analyzing data and generating insights..."):
            resp = requests.get(f"{API_BASE}/insights", params={"q": question})
            if resp.ok:
                data = resp.json()
                
                # Display confidence, data freshness, and LLM status
                col1, col2, col3 = st.columns(3)
                with col1:
                    if "confidence" in data:
                        conf_color = "🟢" if data["confidence"] == "High" else "🟡"
                        st.metric("Confidence", f"{conf_color} {data['confidence']}")
                with col2:
                    if "data_freshness" in data:
                        st.metric("Data Source", f"📊 {data['data_freshness']}")
                with col3:
                    if "llm_enabled" in data:
                        ai_status = "🤖 Gemini" if data["llm_enabled"] else "📊 Statistical"
                        st.metric("Processing", ai_status)
                
                # Display insights
                st.subheader("💡 AI-Generated Insights")
                st.write(data.get("summary"))
                
                # Show sources
                sources = data.get("sources", [])
                if sources:
                    with st.expander("📚 Data Sources"):
                        for i, s in enumerate(sources, 1):
                            st.write(f"{i}. {s}")
                            
            else:
                st.error("❌ Failed to generate insights. Please check if the backend is running.")

with tabs[2]:
    st.subheader("🧭 Post-Graduation Support & ROI Analysis")
    st.markdown("Analyze support services and calculate return on investment for your educational choices.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏛️ Support Services Index")
        st.markdown("View comprehensive support services offered by different institutions.")
        if st.button("📊 Load Support Services Data", type="primary"):
            with st.spinner("Loading support services data..."):
                resp = requests.get(f"{API_BASE}/support-services")
                if resp.ok:
                    rows = resp.json().get("institutions", [])
                    if rows:
                        df = pd.DataFrame(rows)
                        
                        # Display metrics
                        st.metric("Total Institutions", len(df))
                        st.metric("Average Support Index", f"{df['support_index'].mean():.1f}")
                        
                        # Create enhanced visualization
                        fig = px.bar(df, x="institution", y="support_index", 
                                   title="Support Services Index by Institution",
                                   color="support_index",
                                   color_continuous_scale="Blues")
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display detailed table
                        st.subheader("📋 Detailed Support Services")
                        display_df = df[['institution', 'support_index', 'career_services_rating', 
                                       'alumni_network_strength', 'total_services']].copy()
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Show services breakdown
                        with st.expander("🔍 View All Services by Institution"):
                            for _, row in df.iterrows():
                                st.write(f"**{row['institution']}** ({row['total_services']} services)")
                                services_list = ", ".join(row['services'][:5])  # Show first 5
                                if len(row['services']) > 5:
                                    services_list += f" ... and {len(row['services']) - 5} more"
                                st.write(services_list)
                                st.write("---")
                    else:
                        st.warning("No support services data available.")
                else:
                    st.error("❌ Failed to fetch support services data.")
    
    with col2:
        st.markdown("### 💰 ROI Calculator")
        st.markdown("Calculate return on investment for your education choice.")
        
        with st.form("roi_form"):
            institution = st.text_input(
                "🏛️ Institution Name", 
                placeholder="e.g., VIT University, IIT Delhi, BITS Pilani", 
                key="roi_institution",
                help="Enter the name of the institution"
            )
            degree_roi = st.text_input(
                "🎓 Degree Program", 
                placeholder="e.g., Computer Science, Engineering, Data Science", 
                key="roi_degree",
                help="Enter your field of study"
            )
            tuition = st.number_input(
                "💰 Total Tuition (INR)", 
                min_value=0.0, value=800000.0, step=10000.0,
                help="Enter the total cost of your education"
            )
            years = st.number_input(
                "📅 Program Length (years)", 
                min_value=1, value=4, step=1,
                help="Duration of your program"
            )
            
            submitted = st.form_submit_button("🧮 Calculate ROI", type="primary")
        
        if submitted:
            with st.spinner("Calculating ROI..."):
                resp = requests.post(f"{API_BASE}/roi", json={
                    "institution": institution,
                    "degree": degree_roi,
                    "tuition_total": tuition,
                    "years": int(years)
                })
                if resp.ok:
                    data = resp.json()
                    
                    # Display key metrics
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Median Salary", f"₹{data.get('median_salary', 0):,}")
                        st.metric("Employment Rate", f"{data.get('employment_rate', 0):.1f}%")
                    with col_b:
                        st.metric("Years to Break Even", f"{data.get('estimated_years_to_break_even', 0):.1f}")
                        st.metric("Risk Level", data.get('risk_level', 'Unknown'))
                    
                    # ROI projections
                    if 'roi_5_year' in data:
                        st.subheader("📈 ROI Projections")
                        col_c, col_d = st.columns(2)
                        with col_c:
                            st.metric("5-Year ROI", f"{data['roi_5_year']:.1f}%")
                        with col_d:
                            st.metric("10-Year ROI", f"{data['roi_10_year']:.1f}%")
                    
                    # Salary range
                    if 'salary_range' in data:
                        st.info(f"💵 Salary Range: {data['salary_range']}")
                    
                    # Data quality info
                    if 'data_quality' in data:
                        st.caption(f"📊 {data['data_quality']}")
                        
                else:
                    st.error("❌ Failed to calculate ROI. Please check your inputs.")

with tabs[3]:
    st.subheader("⚖️ Institution Comparison Tool")
    st.markdown("Compare two institutions across multiple metrics to make informed decisions.")
    
    with st.form("comparison_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inst_a = st.text_input(
                "🏛️ Institution A", 
                placeholder="e.g., VIT University, IIT Delhi", 
                key="inst_a",
                help="First institution to compare"
            )
        
        with col2:
            inst_b = st.text_input(
                "🏛️ Institution B", 
                placeholder="e.g., SRM University, IIT Bombay", 
                key="inst_b",
                help="Second institution to compare"
            )
        
        with col3:
            cmp_year = st.number_input(
                "📅 Graduation Year", 
                min_value=2020, max_value=2035, value=2025, step=1, 
                key="year_compare",
                help="Year for comparison"
            )
        
        submitted = st.form_submit_button("🔄 Compare Institutions", type="primary")
    
    cmp_year_val = int(cmp_year) if cmp_year else None
    
    if submitted:
        if inst_a == inst_b:
            st.warning("⚠️ Please select two different institutions for comparison.")
        else:
            with st.spinner("Comparing institutions..."):
                resp = requests.post(f"{API_BASE}/compare", json={
                    "institution_a": inst_a,
                    "institution_b": inst_b,
                    "year": cmp_year_val
                })
                if resp.ok:
                    data = resp.json()
                    
                    # Display comparison summary
                    st.success(data.get("summary"))
                    
                    # Show data quality
                    if "data_quality" in data:
                        st.info(f"📊 {data['data_quality']}")
                    
                    # Display comparison results
                    rows = data.get("comparison", [])
                    if rows:
                        df = pd.DataFrame(rows)
                        
                        # Create comparison charts
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            fig_emp = px.bar(df, x="institution", y="avg_employment_rate", 
                                           title="Employment Rate Comparison",
                                           color="avg_employment_rate",
                                           color_continuous_scale="RdYlGn")
                            st.plotly_chart(fig_emp, use_container_width=True)
                        
                        with col_b:
                            fig_salary = px.bar(df, x="institution", y="avg_salary", 
                                              title="Average Salary Comparison",
                                              color="avg_salary",
                                              color_continuous_scale="Blues")
                            st.plotly_chart(fig_salary, use_container_width=True)
                        
                        # Display detailed comparison table
                        st.subheader("📊 Detailed Comparison")
                        comparison_df = df[['institution', 'avg_employment_rate', 'avg_salary', 
                                          'employment_std', 'salary_std']].copy()
                        comparison_df.columns = ['Institution', 'Employment Rate (%)', 'Avg Salary (₹)', 
                                              'Employment Std Dev', 'Salary Std Dev']
                        st.dataframe(comparison_df, use_container_width=True)
                        
                        # Calculate and display winner
                        if len(df) == 2:
                            inst_a_data = df[df['institution'] == inst_a].iloc[0]
                            inst_b_data = df[df['institution'] == inst_b].iloc[0]
                            
                            st.subheader("🏆 Comparison Results")
                            col_c, col_d = st.columns(2)
                            
                            with col_c:
                                if inst_a_data['avg_employment_rate'] > inst_b_data['avg_employment_rate']:
                                    st.success(f"🥇 {inst_a} wins in Employment Rate")
                                else:
                                    st.success(f"🥇 {inst_b} wins in Employment Rate")
                            
                            with col_d:
                                if inst_a_data['avg_salary'] > inst_b_data['avg_salary']:
                                    st.success(f"💰 {inst_a} wins in Average Salary")
                                else:
                                    st.success(f"💰 {inst_b} wins in Average Salary")
                    else:
                        st.warning("No comparison data available for the selected institutions and year.")
                        
                else:
                    st.error("❌ Failed to compare institutions. Please check if the backend is running.")