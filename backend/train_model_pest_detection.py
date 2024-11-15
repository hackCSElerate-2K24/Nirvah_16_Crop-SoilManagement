# Load dataset
import pandas as pd

# Assuming df is your DataFrame
df = pd.read_csv("C:\\Users\\pavan\\Desktop\\crop-soil-management\\backend\\Crop_recommendation.csv")


# Fill NaN values only in numeric columns with the mean of those columns
numeric_columns = df.select_dtypes(include=['number']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Display the first few rows to confirm the changes
print(df.head())
