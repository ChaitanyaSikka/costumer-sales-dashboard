# 📊 Customer Sales Analytics Dashboard

A professional, interactive Streamlit dashboard for analyzing customer sales data with comprehensive visualizations, KPI cards, data quality reports, and interactive features.

## 🎯 Features

### 📈 Dashboard Components
- **KPI Cards**: Total Customers, Total Revenue, Average Purchase Amount, Average Feedback Score, Number of Cities, Number of Countries
- **Distribution Charts**: Gender distribution (pie chart), Country-wise and City-wise customer distribution
- **Trend Analysis**: Monthly signup trends, age distribution, purchase amount distribution
- **Revenue Analysis**: Revenue by country and gender
- **Top Performers**: Top 10 customers by purchase amount
- **Data Quality Report**: Missing values, duplicates, data types overview

### 🎛️ Interactive Features
- **Sidebar Filters**:
  - CSV file upload
  - Country filter (multi-select)
  - Gender filter (multi-select)
  - City filter (multi-select)
  - Age range slider
  - Signup date range picker
- **Data Table**: Searchable, filterable dataset display
- **Download Options**: Export filtered data as CSV or Excel
- **Responsive Layout**: Mobile-friendly, column-based design
- **Error Handling**: Graceful handling of missing values and errors

### 🎨 UI/UX
- Clean, modern interface with gradient styling
- Color-coded visualizations
- Interactive Plotly charts
- Expandable sections for detailed information
- Real-time filtering and updates

## 📋 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## 🚀 Local Installation & Running

### 1. Clone or Download the Project
```bash
git clone https://github.com/yourusername/customer-sales-dashboard.git
cd customer-sales-dashboard
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Data
- Place your `cleaned_customer_sales_data.csv` file in the project root directory
- Or use the file upload feature in the sidebar to load a custom CSV

### 5. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Data Requirements

The CSV file should contain the following columns:

| Column | Data Type | Description |
|--------|-----------|-------------|
| Customer_ID | String | Unique customer identifier |
| Country | String | Customer's country |
| City | String | Customer's city |
| Gender | String | Customer's gender (M/F) |
| Age | Integer | Customer's age |
| Signup_Date | DateTime | Date when customer signed up (YYYY-MM-DD) |
| Total_Purchases | Float | Total purchase amount in dollars |
| Feedback_Score | Float | Customer feedback score (0-5) |

**Note:** The dashboard will work with subsets of these columns, but all visualizations will display optimally with complete data.

## 🌐 Deployment on Streamlit Community Cloud

### Step 1: Prepare Your GitHub Repository

1. **Create a GitHub Account** (if you don't have one)
   - Go to https://github.com and sign up

2. **Create a New Repository**
   - Click on "New" button
   - Repository name: `customer-sales-dashboard`
   - Add description: "Customer Sales Analytics Dashboard"
   - Choose "Public" (required for free tier)
   - Click "Create repository"

3. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/customer-sales-dashboard.git
   cd customer-sales-dashboard
   ```

4. **Add Project Files**
   ```bash
   # Copy your files to the cloned repository
   # Files needed:
   # - app.py
   # - requirements.txt
   # - cleaned_customer_sales_data.csv
   ```

5. **Commit and Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Customer Sales Dashboard"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud

1. **Go to Streamlit Community Cloud**
   - Visit https://streamlit.io/cloud

2. **Sign in with GitHub**
   - Click "Sign in"
   - Authenticate with your GitHub account
   - Grant necessary permissions

3. **Create New App**
   - Click "New app"
   - Select your repository: `customer-sales-dashboard`
   - Select branch: `main`
   - Select main file path: `app.py`
   - Click "Deploy"

4. **Configure Secrets (if needed)**
   - In the app settings, click "Secrets" if you have sensitive information
   - Add any API keys or credentials in TOML format

5. **Access Your Dashboard**
   - Your app will be available at: `https://[your-username]-customer-sales-dashboard.streamlit.app`
   - Share this URL with others!

### Step 3: Automatic Updates

Any time you push changes to your GitHub repository, Streamlit Community Cloud will automatically redeploy your app with the latest version.

```bash
# Make changes locally
git add .
git commit -m "Update: Added new features"
git push origin main
# Dashboard automatically updates!
```

## 🔧 GitHub Deployment Guide (Step-by-Step)

### For Beginners:

1. **Install Git**
   - Download from https://git-scm.com
   - Follow installation wizard
   - Verify: `git --version`

2. **Create Repository Structure**
   ```
   customer-sales-dashboard/
   ├── app.py
   ├── requirements.txt
   ├── cleaned_customer_sales_data.csv
   └── README.md
   ```

3. **Initialize Git Repository**
   ```bash
   cd customer-sales-dashboard
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create GitHub Repository**
   - Log in to https://github.com
   - Click "+" icon → "New repository"
   - Name: `customer-sales-dashboard`
   - Click "Create repository"

5. **Connect Local to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/customer-sales-dashboard.git
   git branch -M main
   git push -u origin main
   ```

6. **Push Updates**
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

## 🎯 Using the Dashboard

### Navigation

1. **Sidebar Controls**
   - Upload a CSV file or use the default dataset
   - Use filters to narrow down your analysis
   - Click "🔄 Reset Filters" to clear all selections

2. **KPI Section**
   - View high-level business metrics at a glance
   - Delta values show comparison with full dataset

3. **Visualizations**
   - Hover over charts to see detailed information
   - Click legend items to show/hide data series
   - Use chart toolbar for zoom, pan, and download options

4. **Data Quality**
   - Check for missing values and data issues
   - Expand sections to see detailed breakdowns
   - Review data types and column information

5. **Data Table**
   - Search specific columns for values
   - Sort by clicking column headers
   - Download filtered results as CSV or Excel

## 🔍 Customization Guide

### Adding New Visualizations

```python
# Example: Add a new scatter plot
st.subheader("Scatter Plot: Age vs Purchase Amount")
if 'Age' in df_filtered.columns and 'Total_Purchases' in df_filtered.columns:
    fig = px.scatter(
        df_filtered,
        x='Age',
        y='Total_Purchases',
        color='Gender',
        size='Feedback_Score',
        title="Age vs Purchase Amount"
    )
    st.plotly_chart(fig, use_container_width=True)
```

### Changing Colors

```python
# Modify color scheme in visualizations
color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
```

### Adding New Filters

```python
# Add a new filter in the sidebar
filter_feedback = st.sidebar.slider(
    "Feedback Score Range",
    min_value=0.0,
    max_value=5.0,
    value=(0.0, 5.0)
)

# Apply the filter
df_filtered = df_filtered[
    (df_filtered['Feedback_Score'] >= filter_feedback[0]) & 
    (df_filtered['Feedback_Score'] <= filter_feedback[1])
]
```

## ⚙️ Configuration

### Environment Variables

You can set Streamlit configuration in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: cleaned_customer_sales_data.csv"
**Solution:**
- Place the CSV file in the project root directory, or
- Use the file uploader in the dashboard sidebar

### Issue: Slow Dashboard Performance
**Solution:**
- Reduce data size by applying filters
- Close other applications consuming resources
- Clear Streamlit cache: `streamlit cache clear`

### Issue: Charts Not Displaying
**Solution:**
- Ensure required columns exist in the data
- Check for special characters or encoding issues in CSV
- Verify data types are correct

## 📦 Project Structure

```
customer-sales-dashboard/
│
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── cleaned_customer_sales_data.csv     # Sample data (optional)
│
└── .streamlit/
    └── config.toml                     # Streamlit configuration (optional)
```

## 🚀 Performance Tips

1. **Use Filters**: Reduce data volume before visualizing
2. **Cache Data**: Add `@st.cache_data` decorator for large datasets
3. **Optimize Charts**: Limit chart data points when possible
4. **Upload Limits**: Keep CSV files under 200MB for optimal performance

## 📝 Best Practices

✅ Always validate input data before uploading
✅ Keep CSV files in UTF-8 encoding
✅ Use consistent date formats (YYYY-MM-DD)
✅ Remove special characters from column names
✅ Ensure numeric columns have valid numbers
✅ Test the dashboard locally before deploying

## 🔐 Security Considerations

- Never commit sensitive data (API keys, passwords) to GitHub
- Use Streamlit Secrets for sensitive configurations
- Keep dependencies updated for security patches
- Review data privacy regulations before sharing

## 📊 Data Analytics Tips

1. **Segment Customers**: Use filters to analyze customer segments
2. **Compare Metrics**: Use KPI deltas to track changes
3. **Identify Trends**: Monitor monthly signup trends
4. **Find Top Performers**: Check top customers by revenue
5. **Quality Check**: Review data quality report regularly

## 🤝 Contributing

If you want to improve this dashboard:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Streamlit documentation: https://docs.streamlit.io
- Open an issue on GitHub

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Express Guide](https://plotly.com/python/plotly-express/)
- [Pandas Tutorial](https://pandas.pydata.org/docs/)
- [GitHub Guides](https://guides.github.com)

## 📅 Changelog

### Version 1.0.0 (2024)
- Initial release
- 9 main visualizations
- 6 KPI cards
- Data quality report
- Interactive filters
- Download functionality
- Responsive layout

## ✨ Future Enhancements

- [ ] Database integration
- [ ] Real-time data updates
- [ ] Advanced analytics (prediction, clustering)
- [ ] Custom report generation
- [ ] Multi-language support
- [ ] Dark mode theme

---

**Built with ❤️ using Streamlit, Pandas, and Plotly Express**

Last Updated: 2024 | Version: 1.0.0
