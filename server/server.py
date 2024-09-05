from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load and preprocess data from 'data' folder
def load_csv_data(directory_path):
    data_list = []
    file_names = os.listdir(directory_path)
    for file_name in file_names:
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            data = pd.read_csv(file_path, header=None)  # assuming no headers in CSV
            data_list.append(data)
    return data_list

# Feature Extraction
def extract_features(eeg_data):
    features = []

    # Convert DataFrame to NumPy array if not already
    eeg_data_np = eeg_data.to_numpy() if isinstance(eeg_data, pd.DataFrame) else eeg_data

    for channel in range(eeg_data_np.shape[1]):
        signal_data = eeg_data_np[:, channel]
        mean_val = np.mean(signal_data)
        std_val = np.std(signal_data)
        skewness = pd.Series(signal_data).skew()
        kurtosis = pd.Series(signal_data).kurt()

        # Frequency domain features (Welch's method for power spectral density)
        f, Pxx = signal.welch(signal_data, fs=256, nperseg=1024)
        power_delta = np.sum(Pxx[(f >= 0.5) & (f < 4)])  # delta band (0.5-4 Hz)
        power_theta = np.sum(Pxx[(f >= 4) & (f < 8)])    # theta band (4-8 Hz)
        power_alpha = np.sum(Pxx[(f >= 8) & (f < 12)])   # alpha band (8-12 Hz)
        power_beta = np.sum(Pxx[(f >= 12) & (f < 30)])   # beta band (12-30 Hz)

        features.extend([mean_val, std_val, skewness, kurtosis, power_delta, power_theta, power_alpha, power_beta])

    return np.array(features)

# Preprocess the data
def preprocess_data(data_list):
    feature_matrix = []
    for eeg_data in data_list:
        features = extract_features(eeg_data.to_numpy())
        feature_matrix.append(features)
    feature_matrix = np.array(feature_matrix)

    # Normalize features
    scaler = StandardScaler()
    feature_matrix_scaled = scaler.fit_transform(feature_matrix)
    return feature_matrix_scaled, scaler

# Clustering to create pseudo-attention scores
def create_attention_scores(X, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=30)
    attention_scores = kmeans.fit_predict(X)
    return attention_scores

# Train Random Forest Model
def train_random_forest(X_train, y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=32)
    rf_model.fit(X_train, y_train)
    return rf_model

# Predict on New User
def predict_new_user(model, new_user_data, scaler):
    new_user_data_scaled = scaler.transform(new_user_data)
    predicted_score = model.predict(new_user_data_scaled)
    return predicted_score

# Generate multiple visualizations
def generate_visualizations(eeg_data):
    visualizations = []
    eeg_data_np = eeg_data.to_numpy() if isinstance(eeg_data, pd.DataFrame) else eeg_data   

    signal_data = eeg_data_np[:, 1]

    # Line plot
    plt.figure()
    plt.plot(signal_data)
    plt.title('Cognitive Load Signal')
    plt.xlabel('Attention Score')
    plt.ylabel('Amplitude')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    visualizations.append(base64.b64encode(buf.read()).decode('utf-8'))
    plt.close()

    # Histogram
    plt.figure()
    plt.hist(signal_data, bins=50)
    plt.title(f'Channel Histogram')
    plt.xlabel('Amplitude')
    plt.ylabel('Frequency')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    visualizations.append(base64.b64encode(buf.read()).decode('utf-8'))
    plt.close()

    return visualizations

# Load and train the model on the initial 'data' folder data
data_directory = 'data'
data_list = load_csv_data(data_directory)
X, scaler = preprocess_data(data_list)
attention_scores = create_attention_scores(X)
X_train, X_test, y_train, y_test = train_test_split(X, attention_scores, test_size=0.2, random_state=42)
rf_model = train_random_forest(X_train, y_train)

# Route to predict attention score and return MSE for a new user-uploaded CSV
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.csv'):
        # Process uploaded file in-memory
        data = pd.read_csv(file, header=None)
        features = extract_features(data).reshape(1, -1)

        # Predict attention score based on the pre-trained model
        predicted_attention_score = predict_new_user(rf_model, features, scaler)

        # Calculate the Mean Squared Error (MSE) on the test set
        y_pred_test = rf_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred_test)

        return jsonify({
            "attention_score": predicted_attention_score.tolist(),
            "mean_squared_error": mse
        })

    return jsonify({"error": "File format not supported. Please upload a .csv file"}), 400

# Route to generate visualizations for the uploaded CSV file
@app.route('/generate_visualizations', methods=['POST'])
def generate_visualizations_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.csv'):
        # Process uploaded file in-memory
        data = pd.read_csv(file, header=None)
        visualizations = generate_visualizations(data)

        return jsonify({
            "visualizations": visualizations
        })

    return jsonify({"error": "File format not supported. Please upload a .csv file"}), 400

if __name__ == '__main__':
    app.run(debug=True)
