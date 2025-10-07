

CNN Train FlowChart






--------------------------------------  2025. 6. 7 
# Clean Files (Optional)
python3 cnn_remove_empty_data.py 

# Seperate (Train and Validate Data)   80% 20% validate 
python3 dataset_split.py

# Train
python3 cnn_train_ROI.py

# Predict 
python3 cnn_predict_ROI.py

# Control
ros2 launch auv_detector estimator_detector_auto_winch.launch 


--------------------------------------
# Clean Files
python3 cnn_remove_empty_data.py 

# Train
python3 cnn_train.py

# Predict 
python3 cnn_predict.py

