"""
Customer Sales Analytics Dashboard
====================================
A comprehensive Streamlit dashboard for analyzing customer sales data.
Built with Streamlit, Pandas, and Plotly Express.

Author: Data Analytics Team
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Customer Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com',
        'About': "Customer Sales Analytics Dashboard v1.0"
    }
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .kpi-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .section-header {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 20px 0 10px 0;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - FILE UPLOAD & FILTERS
# ============================================================================
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")

# File Upload Section
st.sidebar.subheader("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=['csv'],
    help="Upload a cleaned CSV file with customer sales data"
)

# Load sample data if no file is uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    # Try to load default file from workspace
    try:
        df = pd.read_csv("cleaned_customer_sales_data.csv")
        st.sidebar.info("📊 Using default dataset")
    except FileNotFoundError:
        st.error("❌ No CSV file found. Please upload a file using the sidebar uploader.")
        st.stop()

# ============================================================================
# CURRENCY & FORMATTING UTILITIES
# ============================================================================
# Exchange rate: 1 USD = 83 INR (as per 2026 rates)
USD_TO_INR = 83

def convert_to_inr(amount_usd):
    """Convert USD amount to INR"""
    return amount_usd * USD_TO_INR

def format_inr_short(amount_inr):
    """Format INR amount in short form (Cr/L)"""
    if amount_inr >= 10_000_000:  # >= 1 Crore
        return f"₹{amount_inr / 10_000_000:.2f} Cr"
    elif amount_inr >= 100_000:  # >= 1 Lakh
        return f"₹{amount_inr / 100_000:.2f} L"
    elif amount_inr >= 1_000:
        return f"₹{amount_inr / 1_000:.2f} K"
    else:
        return f"₹{amount_inr:,.0f}"

def format_currency(amount_usd):
    """Convert USD to INR and format in short form"""
    amount_inr = convert_to_inr(amount_usd)
    return format_inr_short(amount_inr)

# ============================================================================
# COLUMN NAME MAPPING (Handle different naming conventions)
# ============================================================================
# Define column aliases for flexibility
column_mapping = {
    'purchase': ['Purchase_Amount', 'Total_Purchases', 'Amount', 'Sales'],
    'feedback': ['Feedback_Score', 'Rating', 'Score'],
    'signup': ['Signup_Date', 'Registration_Date', 'JoinDate'],
    'last_purchase': ['Last_Purchase_Date', 'Last_Purchase', 'Purchase_Date']
}

# Function to find column by aliases
def find_column(df, aliases):
    """Find first matching column from list of aliases"""
    for alias in aliases:
        if alias in df.columns:
            return alias
    return None

# Map columns to standard names
purchase_col = find_column(df, column_mapping['purchase'])
feedback_col = find_column(df, column_mapping['feedback'])
signup_col = find_column(df, column_mapping['signup'])
last_purchase_col = find_column(df, column_mapping['last_purchase'])

# Ensure required columns exist
required_columns = ['Country', 'Gender', 'City', 'Age']
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.warning(f"⚠️ Missing core columns: {', '.join(missing_cols)}")
    st.info(f"📊 Available columns: {', '.join(df.columns.tolist())}")
else:
    st.sidebar.success("✅ Core columns found")

# ============================================================================
# DATA PREPROCESSING
# ============================================================================
# Convert data types
if signup_col:
    df[signup_col] = pd.to_datetime(df[signup_col], errors='coerce')

# Create age range for filtering
if 'Age' in df.columns:
    df['Age_Range'] = pd.cut(df['Age'], 
                              bins=[0, 20, 30, 40, 50, 60, 100],
                              labels=['<20', '20-30', '30-40', '40-50', '50-60', '60+'])

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

# Multi-select filters
filter_country = st.sidebar.multiselect(
    "Country",
    options=sorted(df['Country'].unique()) if 'Country' in df.columns else [],
    default=sorted(df['Country'].unique()) if 'Country' in df.columns else [],
    help="Select one or more countries"
)

filter_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df['Gender'].unique()) if 'Gender' in df.columns else [],
    default=sorted(df['Gender'].unique()) if 'Gender' in df.columns else [],
    help="Select one or more genders"
)

filter_city = st.sidebar.multiselect(
    "City",
    options=sorted(df['City'].unique()) if 'City' in df.columns else [],
    help="Select one or more cities (leave empty for all)"
)

# Age range filter
age_range = st.sidebar.slider(
    "Age Range",
    min_value=int(df['Age'].min()) if 'Age' in df.columns else 0,
    max_value=int(df['Age'].max()) if 'Age' in df.columns else 100,
    value=(int(df['Age'].min()) if 'Age' in df.columns else 0, 
           int(df['Age'].max()) if 'Age' in df.columns else 100),
    help="Select age range"
)

# Signup date range filter
if signup_col and df[signup_col].notna().any():
    min_date = df[signup_col].min()
    max_date = df[signup_col].max()
    date_range = st.sidebar.date_input(
        "Signup Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Select date range"
    )
else:
    date_range = None

# ============================================================================
# APPLY FILTERS
# ============================================================================
df_filtered = df.copy()

# Apply country filter
if 'Country' in df_filtered.columns and filter_country:
    df_filtered = df_filtered[df_filtered['Country'].isin(filter_country)]

# Apply gender filter
if 'Gender' in df_filtered.columns and filter_gender:
    df_filtered = df_filtered[df_filtered['Gender'].isin(filter_gender)]

# Apply city filter
if 'City' in df_filtered.columns and filter_city:
    df_filtered = df_filtered[df_filtered['City'].isin(filter_city)]

# Apply age filter
if 'Age' in df_filtered.columns:
    df_filtered = df_filtered[(df_filtered['Age'] >= age_range[0]) & 
                              (df_filtered['Age'] <= age_range[1])]

# Apply date filter
if date_range and signup_col:
    df_filtered = df_filtered[(df_filtered[signup_col] >= pd.Timestamp(date_range[0])) & 
                              (df_filtered[signup_col] <= pd.Timestamp(date_range[1]))]

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
st.title("📊 Customer Sales Analytics Dashboard")
st.markdown("---")

# Display record count
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**Displaying:** {len(df_filtered):,} records | **Total:** {len(df):,} records")
with col2:
    if st.button("🔄 Reset Filters", help="Reset all filters to default"):
        st.rerun()

st.markdown("---")

# ============================================================================
# KPI CARDS
# ============================================================================
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', 
            unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

with kpi_col1:
    total_customers = len(df_filtered)
    st.metric(
        label="👥 Total Customers",
        value=f"{total_customers:,}",
        delta=f"{total_customers - len(df):+,}" if total_customers != len(df) else None
    )

with kpi_col2:
    if purchase_col:
        total_revenue = df_filtered[purchase_col].sum()
        total_revenue_full = df[purchase_col].sum()
        total_revenue_inr = convert_to_inr(total_revenue)
        delta_inr = convert_to_inr(total_revenue - total_revenue_full) if total_revenue != total_revenue_full else None
        st.metric(
            label="💰 Total Revenue",
            value=format_currency(total_revenue),
            delta=format_inr_short(delta_inr) if delta_inr else None
        )
    else:
        st.metric(label="💰 Total Revenue", value="N/A")

with kpi_col3:
    if purchase_col:
        avg_purchase = df_filtered[purchase_col].mean()
        st.metric(label="🛒 Avg Purchase", value=format_currency(avg_purchase))
    else:
        st.metric(label="🛒 Avg Purchase", value="N/A")

with kpi_col4:
    if feedback_col:
        avg_feedback = df_filtered[feedback_col].mean()
        st.metric(label="⭐ Avg Feedback", value=f"{avg_feedback:.2f}/5")
    else:
        st.metric(label="⭐ Avg Feedback", value="N/A")

with kpi_col5:
    num_cities = df_filtered['City'].nunique() if 'City' in df_filtered.columns else 0
    st.metric(
        label="🏙️ Cities",
        value=f"{num_cities:,}"
    )

with kpi_col6:
    num_countries = df_filtered['Country'].nunique() if 'Country' in df_filtered.columns else 0
    st.metric(
        label="🌍 Countries",
        value=f"{num_countries:,}"
    )

st.markdown("---")

# ============================================================================
# VISUALIZATIONS SECTION 1
# ============================================================================
st.markdown('<div class="section-header">📊 Distribution & Trends</div>', 
            unsafe_allow_html=True)

viz_col1, viz_col2 = st.columns(2)

# Gender Distribution - Pie Chart
with viz_col1:
    if 'Gender' in df_filtered.columns:
        gender_dist = df_filtered['Gender'].value_counts()
        fig_gender = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="👫 Gender Distribution",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_gender.update_layout(
            showlegend=True,
            height=400,
            hovermode='closest'
        )
        st.plotly_chart(fig_gender, use_container_width=True)

# Country-wise Customer Distribution - Bar Chart
with viz_col2:
    if 'Country' in df_filtered.columns:
        country_dist = df_filtered['Country'].value_counts().head(10)
        fig_country = px.bar(
            x=country_dist.values,
            y=country_dist.index,
            orientation='h',
            title="🌍 Top 10 Countries by Customer Count",
            labels={'x': 'Number of Customers', 'y': 'Country'},
            color_discrete_sequence=['#636EFA']
        )
        fig_country.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_country, use_container_width=True)

# City-wise Customer Count - Bar Chart
st.subheader("🏙️ Top 15 Cities by Customer Count")
if 'City' in df_filtered.columns:
    city_dist = df_filtered['City'].value_counts().head(15)
    fig_city = px.bar(
        x=city_dist.values,
        y=city_dist.index,
        orientation='h',
        labels={'x': 'Number of Customers', 'y': 'City'},
        color_discrete_sequence=['#EF553B']
    )
    fig_city.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_city, use_container_width=True)

st.markdown("---")

# ============================================================================
# VISUALIZATIONS SECTION 2
# ============================================================================
st.markdown('<div class="section-header">📈 Purchase & Age Analysis</div>', 
            unsafe_allow_html=True)

hist_col1, hist_col2 = st.columns(2)

# Age Distribution - Histogram
with hist_col1:
    if 'Age' in df_filtered.columns:
        fig_age = px.histogram(
            df_filtered,
            x='Age',
            nbins=20,
            title="📅 Age Distribution",
            labels={'Age': 'Age (years)', 'count': 'Number of Customers'},
            color_discrete_sequence=['#00CC96']
        )
        fig_age.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)

# Purchase Amount Distribution - Histogram
with hist_col2:
    if purchase_col:
        fig_purchase = px.histogram(
            df_filtered,
            x=purchase_col,
            nbins=25,
            title="💳 Purchase Amount Distribution (₹)",
            labels={purchase_col: 'Purchase Amount (₹)', 'count': 'Frequency'},
            color_discrete_sequence=['#AB63FA']
        )
        fig_purchase.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_purchase, use_container_width=True)
    else:
        st.info("⚠️ Purchase amount column not found")

# Top 10 Customers by Purchase Amount
st.subheader("🏆 Top 10 Customers by Purchase Amount (₹)")
if purchase_col:
    # Create a display column for customers
    cols_to_show = [col for col in ['Customer_ID', purchase_col, 'Gender', 'Country'] if col in df_filtered.columns]
    if not cols_to_show:
        cols_to_show = [purchase_col] if purchase_col in df_filtered.columns else []
    
    if cols_to_show:
        top_customers = df_filtered.nlargest(10, purchase_col)[cols_to_show].reset_index(drop=True)
        
        fig_top_cust = px.bar(
            x=list(range(1, len(top_customers)+1)),
            y=top_customers[purchase_col].values,
            labels={'x': 'Rank', 'y': 'Purchase Amount (₹)'},
            color=top_customers[purchase_col].values,
            color_continuous_scale='Viridis',
            title="🏆 Top 10 Customers by Purchase Amount"
        )
        fig_top_cust.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_top_cust, use_container_width=True)
        
        # Display table
        st.dataframe(top_customers, use_container_width=True)
else:
    st.info("⚠️ Purchase amount column not found")

st.markdown("---")

# ============================================================================
# VISUALIZATIONS SECTION 3
# ============================================================================
st.markdown('<div class="section-header">📊 Trends & Scores</div>', 
            unsafe_allow_html=True)

trend_col1, trend_col2 = st.columns(2)

# Monthly Signup Trend - Line Chart
with trend_col1:
    if signup_col and df_filtered[signup_col].notna().any():
        df_filtered['Signup_Month'] = df_filtered[signup_col].dt.to_period('M')
        monthly_signups = df_filtered.groupby('Signup_Month').size()
        
        fig_trend = px.line(
            x=monthly_signups.index.astype(str),
            y=monthly_signups.values,
            labels={'x': 'Month', 'y': 'Number of Signups'},
            title="📅 Monthly Signup Trend",
            markers=True,
            color_discrete_sequence=['#FF6B6B']
        )
        fig_trend.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("⚠️ Signup date column not found")

# Feedback Score Distribution - Histogram
with trend_col2:
    if feedback_col:
        fig_feedback = px.histogram(
            df_filtered,
            x=feedback_col,
            nbins=10,
            title="⭐ Feedback Score Distribution",
            labels={feedback_col: 'Feedback Score', 'count': 'Number of Customers'},
            color_discrete_sequence=['#1F77B4']
        )
        fig_feedback.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_feedback, use_container_width=True)
    else:
        st.info("⚠️ Feedback score column not found")

# Revenue Analysis
st.subheader("💰 Revenue Analysis")
rev_col1, rev_col2 = st.columns(2)

# Revenue by Country
with rev_col1:
    if 'Country' in df_filtered.columns and purchase_col:
        revenue_by_country = df_filtered.groupby('Country')[purchase_col].sum().nlargest(10)
        fig_rev_country = px.bar(
            x=revenue_by_country.values,
            y=revenue_by_country.index,
            orientation='h',
            title="💰 Top 10 Countries by Revenue (₹)",
            labels={'x': 'Revenue (₹)', 'y': 'Country'},
            color_discrete_sequence=['#2CA02C']
        )
        fig_rev_country.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_rev_country, use_container_width=True)
    else:
        st.info("⚠️ Country or purchase column not found")

# Revenue by Gender
with rev_col2:
    if 'Gender' in df_filtered.columns and purchase_col:
        revenue_by_gender = df_filtered.groupby('Gender')[purchase_col].sum()
        fig_rev_gender = px.pie(
            values=revenue_by_gender.values,
            names=revenue_by_gender.index,
            title="💰 Revenue Distribution by Gender (₹)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_rev_gender.update_layout(height=400)
        st.plotly_chart(fig_rev_gender, use_container_width=True)
    else:
        st.info("⚠️ Gender or purchase column not found")

st.markdown("---")

# ============================================================================
# DATA QUALITY SECTION
# ============================================================================
st.markdown('<div class="section-header">🔍 Data Quality Report</div>', 
            unsafe_allow_html=True)

quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

with quality_col1:
    st.metric("📊 Dataset Shape", f"{df_filtered.shape[0]} rows × {df_filtered.shape[1]} cols")

with quality_col2:
    missing_values = df_filtered.isnull().sum().sum()
    st.metric("⚠️ Missing Values", f"{missing_values:,}")

with quality_col3:
    duplicate_records = df_filtered.duplicated().sum()
    st.metric("🔄 Duplicate Records", f"{duplicate_records:,}")

with quality_col4:
    st.metric("📈 Columns", f"{df_filtered.shape[1]}")

# Detailed Missing Values Summary
with st.expander("📋 Detailed Missing Values Summary"):
    missing_df = pd.DataFrame({
        'Column': df_filtered.columns,
        'Missing_Count': df_filtered.isnull().sum().values,
        'Missing_Percentage': (df_filtered.isnull().sum().values / len(df_filtered) * 100).round(2)
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    if len(missing_df) > 0:
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("✅ No missing values found!")

# Data Types Overview
with st.expander("📝 Data Types Overview"):
    dtype_df = pd.DataFrame({
        'Column': df_filtered.columns,
        'Data_Type': df_filtered.dtypes.values,
        'Non-Null_Count': df_filtered.count().values
    })
    st.dataframe(dtype_df, use_container_width=True)

st.markdown("---")

# ============================================================================
# INTERACTIVE DATA TABLE & DOWNLOAD
# ============================================================================
st.markdown('<div class="section-header">📊 Interactive Data Table</div>', 
            unsafe_allow_html=True)

# Search functionality
search_column = st.selectbox(
    "Search in column:",
    options=['None'] + list(df_filtered.columns),
    help="Select a column to search in"
)

if search_column != 'None':
    search_value = st.text_input(
        f"Search value in {search_column}:",
        help="Enter text to search"
    )
    
    if search_value:
        df_search = df_filtered[df_filtered[search_column].astype(str).str.contains(
            search_value, 
            case=False, 
            na=False
        )]
    else:
        df_search = df_filtered
else:
    df_search = df_filtered

# Display filtered data table
st.dataframe(
    df_search,
    use_container_width=True,
    height=400,
    column_config={
        col: st.column_config.TextColumn(width="medium") 
        for col in df_search.columns
    }
)

# Download filtered dataset
st.subheader("💾 Download Data")
download_col1, download_col2, download_col3 = st.columns(3)

with download_col1:
    csv_buffer = io.StringIO()
    df_search.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="📥 Download as CSV",
        data=csv_data,
        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Download the filtered dataset as CSV"
    )

with download_col2:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df_search.to_excel(writer, sheet_name='Data', index=False)
    excel_data = excel_buffer.getvalue()
    
    st.download_button(
        label="📥 Download as Excel",
        data=excel_data,
        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Download the filtered dataset as Excel"
    )

with download_col3:
    st.metric("Records to Download", len(df_search))

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
    <div style="text-align: center; padding: 20px; color: #888;">
        <p>Customer Sales Analytics Dashboard v1.0</p>
        <p>Built with Streamlit, Pandas, and Plotly Express</p>
        <p>Last Updated: 2024 | Data Source: cleaned_customer_sales_data.csv</p>
    </div>
""", unsafe_allow_html=True)
