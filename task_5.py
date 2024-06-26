import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

df = pd.read_csv('/content/d1.csv', encoding='latin-1')

df['DateTime'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df['Season'] = df['DateTime'].dt.month.map({1: 'Winter', 2: 'Winter', 3: 'Spring', 
                                            4: 'Spring', 5: 'Spring', 6: 'Summer',
                                            7: 'Summer', 8: 'Summer', 9: 'Fall', 
                                            10: 'Fall', 11: 'Fall', 12: 'Winter'})

df['Weekend_encoded'] = df['Weekend?'].map({'Weekday': 0, 'Weekend': 1})

def analyze_patterns(df, column):
    plt.figure(figsize=(12, 6))
    df[column].value_counts().plot(kind='bar')
    plt.title(f'Distribution of Accidents by {column}')
    plt.xlabel(column)
    plt.ylabel('Number of Accidents')
    plt.tight_layout()
    plt.savefig(f'{column}_distribution.png')
    plt.close()

analyze_patterns(df, 'Hour')
analyze_patterns(df, 'Weekend?')
analyze_patterns(df, 'Season')
analyze_patterns(df, 'Collision Type')
analyze_patterns(df, 'Primary Factor')

df['Time_Category'] = pd.cut(df['Hour'], 
                             bins=[-1, 6, 12, 18, 24], 
                             labels=['Night', 'Morning', 'Afternoon', 'Evening'])
analyze_patterns(df, 'Time_Category')

correlation_columns = ['Hour', 'Weekend_encoded']
correlation = df[correlation_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation between Time Factors')
plt.savefig('time_factors_correlation.png')
plt.close()

df_clean = df.dropna(subset=['Latitude', 'Longitude'])

m = folium.Map(location=[df_clean['Latitude'].mean(), df_clean['Longitude'].mean()], zoom_start=4)
heat_data = [[row['Latitude'], row['Longitude']] for index, row in df_clean.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('accident_hotspots.html')

plt.figure(figsize=(12, 6))
df['Primary Factor'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Contributing Factors')
plt.xlabel('Primary Factor')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.savefig('top_contributing_factors.png')
plt.close()

print("Analysis complete. Check the generated images and HTML file for visualizations.")