from flask import Flask, render_template, request
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from contractions import fix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()

# Read CSV files
df1 = pd.read_csv('movie_data_train.csv')
df2 = pd.read_csv('movie_data_solution.csv')

# Concatenate DataFrames
df = pd.concat([df1, df2], axis=0)

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=10_000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Plot Summary'])

def recommend_and_print(plot):
    processed_plot = preprocess(plot)
    plot_vec = tfidf_vectorizer.transform([processed_plot])
    similarities = cosine_similarity(tfidf_matrix, plot_vec)
    indices = similarities.argsort(axis=0)[-10:][::-1]
    recommended_movies = []
    for idx in indices:
        original_idx = df.index[idx]  # Get the original index
        movie_title = df.loc[original_idx, 'Title']
        recommended_movies.append(movie_title)

    return recommended_movies

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = fix(text)
    text = lemmatizer.lemmatize(text)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    recommended_movies = []

    if request.method == "POST":
        plot = request.form.get("plot")
        recommended_movies = recommend_and_print(plot)
    
    return render_template("index.html", recommended_movies=recommended_movies)

if __name__ == "__main__":
    app.run(debug=True)
