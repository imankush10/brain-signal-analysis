# Focus Finder

**Focus Finder** is a brain signal analysis project aimed at analyzing EEG data to generate visualizations and insights. This project includes a Flask backend and a React frontend.

## Project Setup

Follow the steps below to set up the project on your local machine.

### Backend Setup (Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/imankush10/brain-signal-analysis
   ```

2. Navigate to the project folder:
    ```bash
    cd brain-signal-analysis
    ```
3. Navigate to the server folder:
   ```bash
   cd server
   ```
4. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
6. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7.Run the Flask server:
```bash
python server.py
```

## Frontend Setup (React)

1. Open another terminal and navigate to the client folder:
   ```bash
   cd client
   ```
2. Install the required npm packages:
   ```bash
   npm i
   ```
3. Run the frontend server:
   ```bash
   npm run dev
   ```
## Dataset

1. Create a folder named data inside the server folder:
   ```bash
   mkdir server/data
   ```
2. Download the EEG dataset from https://www.kaggle.com/datasets/amananandrai/complete-eeg-dataset
3. Extract the downloaded dataset files into the data folder

## Usage
Once the setup is complete, you can access the project by:
1. Running the Flask server.
2. Running the React frontend.
3. Upload EEG data through the React interface to generate visualizations and insights.
