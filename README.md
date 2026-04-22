Healthy Harvest: IoT & ML Smart Farming System
Healthy Harvest is an integrated decision support system designed to optimize agricultural productivity. India is an agricultural nation where a massive portion of the population depends on farming, yet productivity can be hampered by unpredictable weather and lack of data driven insights. This smart farming system is automated to help farmers increase crop production by predicting which crops to grow based on real time soil and weather data. By bridging the gap between Internet of Things (IoT) hardware and Machine Learning (ML), Healthy Harvest aims to deliver actionable insights directly to farmers to maximize yield and profitability.

Key Features
Crop Recommendation Engine: Analyzes soil parameters (pH, moisture, temperature) and weather conditions to recommend the most suitable crop for a specific area, ensuring high yield.

Plant Disease Detection: Utilizes deep learning and image processing to classify images of leaves as normal or affected by bacteria, fungi, or viruses.

Intelligent Fertilizer Prediction: Recommends the optimal fertilizer and precise measurements based on the specific crop or the severity of a detected plant disease.

Market Analysis & Price Forecasting: Predicts crop market prices using historical Wholesale Price Index (WPI) and rainfall data to help farmers understand market trends and policies.

Real-Time IoT Monitoring: Continuously captures live data from the field using physical sensors for soil moisture, temperature, humidity, and pH levels.

Tech Stack
Backend: Python, Flask micro-framework

Machine Learning: TensorFlow, Keras. Utilizes algorithms such as Decision Trees, Naive Bayes, Support Vector Machines (SVM), and Deep Neural Networks (VGG).

Database: MySQL for storing user data, historical sensor logs, and past predictions.

Frontend: HTML5, CSS3, JavaScript for a dynamic and interactive user interface.

IoT Hardware: Arduino Uno, Raspberry Pi, DHT11 (Temperature/Humidity), Soil Moisture Sensors, and pH Sensors.

File Structure
├── app.py                     # Main Flask server entry point and ML routing
├── notebooks/                 # Jupyter Notebooks (.ipynb) for EDA and model training
├── templates/                 # Frontend HTML views (Dashboard, prediction forms, etc.)
├── static/                    # UI Assets (CSS, JS, Images)
├── models/                    # Trained weights (NN_MPH.hp5, Neural_Networks_MPH.hp5, VGG_plant.hp5)
├── datasets/                  # Training data (Crop_recommendation.csv, FertilizerPrediction.csv, etc.)
├── temperature_sensors/       # Hardware interfacing code for IoT sensors
├── weather.py                 # Backend script for fetching real-time environmental API data
├── final_db.sql               # Complete MySQL database schema and exports
└── Healthy Harvest_Black Book.pdf # Full technical and mathematical documentation

Setup & Installation

1. Clone the repository:
   git clone https://github.com/shubh182001/Healthy-Harvest-IoT-ML.git
   cd Healthy-Harvest-IoT-ML

2. Install dependencies:
   Ensure you have Python and pip installed, then run:
   pip install -r requirements.txt

3. Database Configuration:
   i) Install MySQL.
   ii) Import the provided final_db.sql file to set up the required schema and tables.
   iii) Update the database connection credentials in app.py or your configuration file.

4. Run the Application:
   python app.py
The application will be hosted locally. Open your browser and navigate to http://127.0.0.1:5000/.

Deep Technical Documentation
For a comprehensive dive into the theoretical framework, mathematical models, hardware circuit designs, and testing methodologies (including Black Box and White Box testing), please refer to the Healthy Harvest_Black Book.pdf included in this repository.
