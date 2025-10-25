# Remote Control via Hand Gestures  

This project demonstrates remote control using hand movement recognition. A motion sensor (IMU) connected to a Raspberry Pi Pico collects gesture data, which is processed in real time by a machine learning model running on a PC. Each recognized gesture corresponds to a specific RGB LED color.

## Hardware Components  

-Raspberry Pi Pico WH  
-WaveShare 10 DOF IMU Sensor v2 (MPU9250)  
-RGB LED (common cathode)  
-Resistors: 3×220 Ω (for R, G, B)  
-Breadboard + jumper wires  
-MicroUSB cable (power + UART)  

## Connections:  
-IMU (I2C): SDA → GP0, SCL → GP1  
-RGB LED: R → GP15, G → GP14, B → GP13 (each via 220 Ω resistor), cathode → GND  

## Setup & Usage Steps  
 ### Hardware Setup  
 Connect IMU and LED to Pico as described.

### Hardware Testing  
python hw_testing/led_test.py  
python hw_testing/imu_reading_test.py


### Data Collection  
1. Flash imu_stream.py to Pico.
2. Run final_python_scripts/log_data.py on PC.
3. Record gestures and label them manually.

### Model Training  
1. Open jupyter_skripty.py in Jupyter Notebook.
2. Load CSVs, create windows, train a RandomForest model.
3. Save as model.pkl.

### Real-time Inference  
1. Flash main.py to Pico.
2. Run final_python_scripts/run_inference.py on PC.
3. Perform gestures → LED changes color in real time.

## Technologies  
-Hardware: Raspberry Pi Pico, MPU9250 IMU  
-Languages: Python (PC + MicroPython on Pico)  
-ML: scikit-learn (RandomForestClassifier)  
-Data Handling: CSV, Jupyter
