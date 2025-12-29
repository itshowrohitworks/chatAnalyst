# Run file as module: python -m src.pipeline.data_pipeline
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def droping_and_encoding_columns(df,threshold=0.1):
    cols_to_numeric = cols_to_numeric = [
        'avg_viewers', 
        'peak_viewers', 
        'chat_rate', 'like_count', 
        'duration_minutes', 
        'stream_donations'
    ]
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    y = df['stream_donations']

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

    # Manually dropping not needed columns:
    manual_drops = ['stream_id', 'stream_donations']

    # Dynamically dropping columns as per correlation:
    correlations = df_combined.corr()['stream_donations'].abs()

    features_to_keep = correlations[correlations >= threshold].index.tolist()

    final_features = [f for f in features_to_keep if f not in manual_drops]
    
    X = df_combined[final_features]

    print(f"Dynamic Selection: Kept {len(final_features)} features with correlation >= {threshold}")
    print(f"Features kept: {final_features}")

    return X, y, encoder