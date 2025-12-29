# Run script: python -m src.ml.train
from data.fetch_data import fetch_ml_data
from src.pipeline.data_pipeline import droping_and_encoding_columns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os
import joblib

def train_data(X,y,encoder):
    # Splitting the Model:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and Train the Model
    print("Training Random Forest on {len(X_train)} streams...")
    model = RandomForestRegressor(
        n_estimators=150,   # More trees for better averaging
        max_depth=4,        # Slightly shallower to prevent overfitting
        min_samples_leaf=5, # Ensure each 'leaf' has at least 5 streams
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate the Performance
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"--- Model Results ---")
    print(f"Mean Absolute Error: ${mae:.2f}")
    print(f"Accuracy (R2 Score): {r2:.4f}") 

    # Save everything to the 'models' folder
    os.makedirs('src/models', exist_ok=True)

    joblib.dump(model, 'src/models/streamer_model.pkl')
    joblib.dump(encoder, 'src/models/cat_encoder.pkl')
    joblib.dump(X.columns.tolist(), 'models/feature_names.pkl')

    print("Model, Encoder, and Feature list saved successfully!")

    # Returning model if needed:
    return model,mae

if __name__ == "__main__":
    # Fetch and Process
    df = fetch_ml_data()
    X, y, encoder = droping_and_encoding_columns(df,threshold=0.1)

    # Train and Save
    trained_model, final_error = train_data(X, y, encoder)

    # Now you can use 'trained_model' here if you want to test one manual prediction
    print(f"Training session finished with error: {final_error:.2f}")