import pandas as pd
from flask import send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def sentiment_diagram(posts):
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0}
    for post in posts:
        sentiment = post.get("sentiment")
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1

    df = pd.DataFrame(list(sentiment_counts.items()), columns=['Sentiment', 'Count'])
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Sentiment', y='Count', data=df, palette={'POSITIVE': 'green', 'NEGATIVE': 'red'})
    for index, row in df.iterrows():
        plt.text(row.name, row['Count'] - 1, int(row['Count']), ha='center', va='top', color='white', fontsize=12)
    plt.title('Distributia sentimentelor in postari')
    plt.ylabel('Numarul de postari')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

def length_diagram(data):
    df = pd.DataFrame(data)

    df['length'] = df['content'].str.len()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='sentiment', y='length', data=df, palette='Set2',flierprops=dict(marker='o', color='red', markersize=8))

    plt.title('Lungimea postarilor dupa sentiment', fontsize=16)
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Lungimea postarii (caractere)', fontsize=12)

    plt.xticks(rotation=45)

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')