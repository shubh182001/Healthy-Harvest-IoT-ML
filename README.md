# Healthy Harvest: IoT & ML Smart Farming System

Healthy Harvest is an integrated decision support system designed to optimize agricultural productivity. This smart farming system is automated to help farmers increase crop production by predicting which crops to grow based on real-time soil and weather data.

## Key Features

* **Crop Recommendation Engine:** Analyzes soil parameters and weather conditions to recommend the most suitable crop.
* **Plant Disease Detection:** Utilizes deep learning to classify images of leaves as normal or affected.
* **Intelligent Fertilizer Prediction:** Recommends optimal fertilizer types and measurements.
* **Market Analysis:** Predicts crop market prices using historical data.
* **Real-Time IoT Monitoring:** Captures live data from the field using physical sensors.

## Tech Stack

* **Backend:** Python, Flask
* **Machine Learning:** TensorFlow, Keras, Scikit-learn
* **Database:** MySQL
* **Frontend:** HTML5, CSS3, JavaScript
* **IoT Hardware:** Arduino Uno, Raspberry Pi, DHT11, Soil Moisture Sensors

## File Structure

```text
├── app.py                     # Main Flask server
├── notebooks/                 # Jupyter Notebooks for EDA
├── templates/                 # Frontend HTML views
├── static/                    # UI Assets (CSS, JS)
├── Healthy Harvest_Black Book.pdf # Full technical documentation
└── final_db.sql               # MySQL database schema
```
## **Setup & Installation**

1. **Clone the repository:**
   `git clone https://github.com/shubh182001/Healthy-Harvest-IoT-ML.git`

2. **Install dependencies:**
   `pip install -r requirements.txt`

3. **Run the Application:**
   `python app.py`

## **Documentation**

For a deep dive into the hardware and math, refer to the **[Healthy Harvest_Black Book.pdf](./Healthy%20Harvest_Black%20Book.pdf)**. This document covers the full technical framework developed at DJSCE.
