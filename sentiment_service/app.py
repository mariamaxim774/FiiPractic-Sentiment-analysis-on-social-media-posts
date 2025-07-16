from transformers import pipeline

model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
sentiment_pipeline = None

def initialize_model():
    global sentiment_pipeline
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
        print("Modelul de analiza a sentimentelor a fost incarcat cu succes.")
    except Exception as e:
        print(f"Eroare la incarcarea modelului: {e}")

def analyze_sentiment(text):
    global sentiment_pipeline
    if sentiment_pipeline is None:
        print("Modelul nu a fost initializat. Ruleaza initialize_model().")
        return "NEUTRAL"
    try:
        result = sentiment_pipeline(text)[0]
        return result['label']
    except Exception as e:
        print(f"Eroare la analiza sentimentelor: {e}")
        return "NEUTRAL"
