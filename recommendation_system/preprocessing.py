import emoji

def preprocess_data(review):
    text = emoji.demojize(review)
    return text

def save_preprocessed_data(df):
    df.to_csv('data/preprocessed/review_data.csv',index=False)