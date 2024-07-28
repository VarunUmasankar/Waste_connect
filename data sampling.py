import pandas as pd
import numpy as np

# Define the areas in Chennai
areas = ["Adyar", "Anna Nagar", "T. Nagar", "Kodambakkam", "Mylapore", "Royapettah", "Velachery", "Nungambakkam", 
         "Alwarpet", "Besant Nagar", "Saidapet", "Thiruvanmiyur", "Perambur", "Egmore", "Guindy",
         "Pallavaram", "Chromepet", "Tambaram", "Porur", "Madipakkam"]

# Generate dates from January 1, 2024, to July 21, 2024
dates = pd.date_range(start="2024-01-01", end="2024-07-21")

# Generate random dry waste data in tons
np.random.seed(0)  # For reproducibility
dry_waste_data = np.random.uniform(1, 5, size=(len(dates), len(areas)))

# Generate random wet waste data in tons
wet_waste_data = np.random.uniform(1, 5, size=(len(dates), len(areas)))

# Create DataFrames for dry and wet waste
dry_waste_df = pd.DataFrame(dry_waste_data, index=dates, columns=[f"{area} Dry Waste" for area in areas])
wet_waste_df = pd.DataFrame(wet_waste_data, index=dates, columns=[f"{area} Wet Waste" for area in areas])

# Combine the DataFrames
waste_data = pd.concat([dry_waste_df, wet_waste_df], axis=1)

# Save the DataFrame to CSV
csv_path = 'waste_data.csv'
waste_data.to_csv(csv_path)

# Save the DataFrame to XLSX
xlsx_path = 'waste_data.xlsx'
waste_data.to_excel(xlsx_path, engine='openpyxl')

