import pandas as pd

_df_cache = None

def load_data():
    global _df_cache

    if _df_cache is None:
        df = pd.read_csv('D:\\FIIPractic\\FP\\FP-training\\my_app\\data_service\\sentiment140.csv', header=None,
                         names=['sentiment', 'id', 'date', 'query', 'user', 'text'], encoding='ISO-8859-1')
        df['sentiment'] = df['sentiment'].map({4: "Positive", 0: "Negative"})
        df = df.rename(columns={'text': 'content'})
        df = df[df['content'].str.len() >= 10]
        _df_cache = df[['content', 'date', 'sentiment']].copy()

    batch_size = 15
    if _df_cache.empty:
        return []

    sample = _df_cache.sample(min(batch_size, len(_df_cache)))
    _df_cache = _df_cache.drop(sample.index)

    return sample.to_dict(orient='records')