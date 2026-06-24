# 🚀 Quick Start Guide

## ⚡ Get Running in 5 Minutes

### 1️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Dashboard
```bash
streamlit run app.py
```

### 3️⃣ Open Browser
Your dashboard will automatically open at `http://localhost:8501`

---

## 📊 Dashboard Features Overview

### Top Section
- **KPI Cards**: 6 key metrics for quick insights
- **Filters**: Country, Gender, City, Age Range, Signup Date

### Main Content
- **Distribution Charts**: Gender, Country, City distribution
- **Trend Analysis**: Age, Purchase Amount, Monthly Signups
- **Revenue Analysis**: By Country and Gender
- **Top 10 Customers**: Ranked by purchase amount
- **Feedback Scores**: Distribution visualization

### Bottom Section
- **Data Quality Report**: Missing values, duplicates, data types
- **Interactive Table**: Search and filter the data
- **Download Options**: Export as CSV or Excel

---

## 🔥 Key Features

✅ **No Coding Required** - Just upload your CSV  
✅ **Responsive Design** - Works on desktop, tablet, mobile  
✅ **Real-time Filters** - Instant data updates  
✅ **Professional Charts** - Interactive Plotly visualizations  
✅ **Data Export** - Download filtered results  
✅ **Error Handling** - Graceful handling of data issues  

---

## 💡 Tips

1. **Upload Custom Data**: Use the sidebar file uploader to load your own CSV
2. **Apply Filters**: Use sidebar filters to focus on specific segments
3. **Export Data**: Download filtered data as CSV or Excel
4. **View Details**: Hover over charts for detailed information
5. **Search Table**: Use the search feature in the data table

---

## 📋 Required CSV Columns

Your CSV should have these columns:
- `Country` - Customer's country
- `City` - Customer's city
- `Gender` - M or F
- `Age` - Age in years
- `Signup_Date` - YYYY-MM-DD format
- `Total_Purchases` - Purchase amount ($)
- `Feedback_Score` - Score 0-5

---

## 🌐 Deploy to Cloud (Streamlit Community Cloud)

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your GitHub repo and `app.py`
5. Click "Deploy"

See README.md for detailed deployment instructions!

---

## ❓ Common Issues

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| CSV not found | Place file in project folder or upload via sidebar |
| Charts not showing | Check that required columns exist in CSV |
| Slow performance | Apply filters to reduce data volume |

---

## 📧 Need Help?

- Read the full README.md for comprehensive documentation
- Check Streamlit docs: https://docs.streamlit.io
- See troubleshooting section in README.md

**Happy Analyzing! 📊**
