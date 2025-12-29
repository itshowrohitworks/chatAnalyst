# Run file as module: python -m src.pipeline.data_pipeline
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from data.fetch_data import fetch_ml_data

df = fetch_ml_data()

def droping_and_encoding_columns(df):
    cols_to_numeric = [ 
        'avg_viewers', 'avg_peak_viewers', 'avg_chat_rate', 
        'avg_like_count', 'total_donations'
    ]
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    y = df['total_donations']

    # OneHot Encoding for categorical columns:
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    cat_col = ['niche', 'country']
    encoded_data = encoder.fit_transform(df[cat_col])
    
    encoded_df = pd.DataFrame(
        encoded_data,
        columns=encoder.get_feature_names_out(cat_col),
        index=df.index
    )
    
    # Combining numerical and encoded columns
    df_combined = pd.concat([df.drop(columns=cat_col), encoded_df], axis=1)

    # 5. Drop Unwanted Columns all at once
    COLS_TO_DROP = [
        'followers', 'total_minutes', 'avg_like_count', 
        'niche_Gaming', 'streamer_id', 'total_donations'
    ]
    
    X = df_combined.drop(columns=COLS_TO_DROP)
    
    return X, y, encoder

X,y,emd = droping_and_encoding_columns(df)
print(X.shape,y.shape)
print('\n')
print(emd.categories_)