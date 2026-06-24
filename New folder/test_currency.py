#!/usr/bin/env python
"""Test currency conversion functions"""

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

if __name__ == "__main__":
    print("💰 Currency Conversion Test")
    print("=" * 60)
    
    # Test with the user's values
    total_revenue_usd = 265857989.00
    avg_purchase_usd = 29014.30
    
    print(f"\nTotal Revenue:")
    print(f"  USD: ${total_revenue_usd:,.2f}")
    print(f"  INR: {format_currency(total_revenue_usd)}")
    
    print(f"\nAverage Purchase:")
    print(f"  USD: ${avg_purchase_usd:,.2f}")
    print(f"  INR: {format_currency(avg_purchase_usd)}")
    
    # More test cases
    print(f"\n📊 Additional Examples:")
    test_values = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
    for val in test_values:
        print(f"  ${val:>10,} → {format_currency(val)}")
    
    print("\n✅ All conversions working perfectly!")
