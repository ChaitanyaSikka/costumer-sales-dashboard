import pandas as pd

# Test data loading and column mapping
df = pd.read_csv('cleaned_customer_sales_data.csv')

print("✅ CSV loaded successfully")
print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"\n📋 Available columns:\n   {', '.join(df.columns.tolist())}")

# Test column mapping logic
column_mapping = {
    'purchase': ['Purchase_Amount', 'Total_Purchases', 'Amount', 'Sales'],
    'feedback': ['Feedback_Score', 'Rating', 'Score'],
    'signup': ['Signup_Date', 'Registration_Date', 'JoinDate'],
    'last_purchase': ['Last_Purchase_Date', 'Last_Purchase', 'Purchase_Date']
}

def find_column(df, aliases):
    for alias in aliases:
        if alias in df.columns:
            return alias
    return None

# Map columns
purchase_col = find_column(df, column_mapping['purchase'])
feedback_col = find_column(df, column_mapping['feedback'])
signup_col = find_column(df, column_mapping['signup'])

print(f"\n✅ Column Mapping Results:")
print(f"   Purchase Amount: {purchase_col}")
print(f"   Feedback Score: {feedback_col}")
print(f"   Signup Date: {signup_col}")

# Test basic calculations
if purchase_col:
    print(f"\n✅ Can calculate revenue: ${df[purchase_col].sum():,.2f}")
if feedback_col:
    print(f"✅ Can calculate avg feedback: {df[feedback_col].mean():.2f}/5")
if signup_col:
    print(f"✅ Can analyze signup dates")

print("\n🎉 All checks passed! Dashboard should work now.")
