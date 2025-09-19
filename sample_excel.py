import pandas as pd
import random

def create_sample_excel():
    """Create a sample Excel file with financial data for testing"""
    
    # Sample months
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Generate sample financial data
    data = []
    for month in months:
        # Generate random amounts between 1000 and 10000
        amount = round(random.uniform(1000, 10000), 2)
        data.append({
            'Month': month,
            'Amount': amount
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel file
    df.to_excel('sample_financial_data.xlsx', index=False)
    print("Sample Excel file 'sample_financial_data.xlsx' created successfully!")
    print("\nSample data preview:")
    print(df.head())

if __name__ == "__main__":
    create_sample_excel()