import sqlite3
import sys

import geopandas as gpd
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from aiomultiprocess import Worker
from nltk.corpus import stopwords
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')


# Connect to SQLite database
def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn


# Load data into a Pandas DataFrame
def load_data(db_path):
    conn = connect_db(db_path)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


# Data Cleaning
def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna(subset=['title', 'salary_min', 'salary_max', 'location', 'country'])
    df['created'] = pd.to_datetime(df['created'])
    df['salary_min'] = df['salary_min'].astype(float)
    df['salary_max'] = df['salary_max'].astype(float)
    df['average_salary'] = (df['salary_min'] + df['salary_max']) / 2
    return df


# Print Job Statistics with Dynamic Console Updates
def job_statistics(df):
    sys.stdout.write("\r")
    sys.stdout.write("Job Statistics: ")
    sys.stdout.write(f"Total Jobs: {len(df)} | ")
    sys.stdout.write(f"Avg Salary: {df['average_salary'].mean():.2f} | ")
    sys.stdout.write(f"Top Company: {df['company'].value_counts().idxmax()} | ")
    sys.stdout.write(f"Top Country: {df['country'].value_counts().idxmax()}    ")
    sys.stdout.flush()


# Generate Word Cloud for Job Descriptions
def job_skills_wordcloud(df):
    text = " ".join(df['description'].dropna().values)
    stop_words = set(stopwords.words('english'))
    words = " ".join([word for word in text.split() if word.lower() not in stop_words])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Top Keywords in Job Descriptions')
    plt.show()


# Job Trends
def job_trends(df):
    df['created_date'] = df['created'].dt.date
    df.groupby('created_date').size().plot(figsize=(12, 5), title='Job Posting Trends', marker='o')
    plt.show()


# Top Job Locations
def job_locations(df):
    top_locations = df['location'].value_counts().head(10)
    sns.barplot(x=top_locations.values, y=top_locations.index)
    plt.title('Top 10 Job Locations')
    plt.show()

    top_countries = df['country'].value_counts().head(10)
    sns.barplot(x=top_countries.values, y=top_countries.index)
    plt.title('Top 10 Job Countries')
    plt.show()


# Salary Prediction Model
def predict_salary(df):
    df = df[['salary_min', 'salary_max', 'average_salary']].dropna()
    X = df[['salary_min', 'salary_max']]
    y = df['average_salary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))


# Job Market by Geography
def job_map(df):
    df = df.dropna(subset=['latitude', 'longitude', 'country'])
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    fig, ax = plt.subplots(figsize=(10, 5))
    world.plot(ax=ax, color='lightgray')
    geo_df.plot(ax=ax, markersize=10, alpha=0.5)
    plt.title("Job Postings by Location and Country")
    plt.show()

async def recalculate_stats():
    print("hello")
    df = load_data("adzuna.db")
    df = clean_data(df)
    job_statistics(df)
    # salary_analysis(df)
    job_trends(df)
    job_locations(df)
    job_skills_wordcloud(df)
    predict_salary(df)
    job_map(df)

async def recalculate_stats_async():
    print("hello")
    await Worker(target=recalculate_stats)
#
# @pipable_operator
# async def calculate_states(source: AsyncIterable[Any]) -> AsyncIterable[Any]:
#     return (source
#          | do_action_with_backpressure.pipe(recalculate_stats_async)
#      )

#
# # Main Execution Loop
# def main():
#     db_path = "adzuna.db"  # Update with your actual SQLite file path
#
#     while True:
#
#
#
# if __name__ == "__main__":
#     main()
