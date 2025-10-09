

CNN Train FlowChart


~/colcon_ws/src/smarc2/scripts$ ./unity_ros_bridge.sh 

# Train
python3 cnn_train_ROI_validate_normalized.py

# predict 
python3 cnn_predict_ROI_normalized.py

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








- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/uw_gps_link
  transform:
    translation:
      x: -0.4020000100135803
      y: -0.0
      z: 0.07800000160932541
    rotation:
      x: 0.0
      y: -0.0
      z: 0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/gps_link
  transform:
    translation:
      x: 0.527999997138977
      y: -0.0
      z: 0.07100000232458115
    rotation:
      x: 0.0
      y: -0.0
      z: 0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/sbg_link
  transform:
    translation:
      x: 0.459891140460968
      y: 5.076672096038237e-07
      z: 0.0020022206008434296
    rotation:
      x: -6.515676886920119e-12
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/imu_link
  transform:
    translation:
      x: 0.23994313180446625
      y: -1.2938259715156164e-05
      z: -0.03599848970770836
    rotation:
      x: -6.515676886920119e-12
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/sidescan_link
  transform:
    translation:
      x: -0.0430000014603138
      y: -0.0
      z: 0.0
    rotation:
      x: 0.0
      y: -0.0
      z: 0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/dvl_link
  transform:
    translation:
      x: 0.5729929804801941
      y: -2.2711403289576992e-05
      z: -0.06299982964992523
    rotation:
      x: -6.515676886920119e-12
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/pressure_link
  transform:
    translation:
      x: -0.503000020980835
      y: 0.02500000037252903
      z: 0.05700000002980232
    rotation:
      x: 0.0
      y: -0.0
      z: 0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/base_link
  child_frame_id: sam_auv_v1/thruster_yaw_link
  transform:
    translation:
      x: -0.6771003603935242
      y: 3.0437604436883703e-07
      z: 3.1348317861557007e-06
    rotation:
      x: -6.515676886920119e-12
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/thruster_yaw_link
  child_frame_id: sam_auv_v1/thruster_link
  transform:
    translation:
      x: 0.0
      y: -2.091837814077735e-11
      z: -5.960464477539063e-08
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/thruster_link
  child_frame_id: sam_auv_v1/back_prop_link
  transform:
    translation:
      x: -0.0770653486251831
      y: 3.493641997920349e-08
      z: 1.1771917343139648e-06
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/thruster_link
  child_frame_id: sam_auv_v1/front_prop_link
  transform:
    translation:
      x: -0.054348766803741455
      y: 2.463275450281799e-08
      z: 8.158385753631592e-07
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: map_gt
  child_frame_id: sam_auv_v1/odom
  transform:
    translation:
      x: 1327.0
      y: 1065.0
      z: 0.0
    rotation:
      x: 0.0
      y: 0.0
      z: 0.0
      w: 1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: sam_auv_v1/odom
  child_frame_id: sam_auv_v1/base_link
  transform:
    translation:
      x: 0.0
      y: -0.0029296875
      z: -0.09155570715665817
    rotation:
      x: -0.01137371826916933
      y: 0.011121723800897598
      z: -0.7070194482803345
      w: -0.7070151567459106
---
transforms:
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/camera_link
  transform:
    translation:
      x: 0.10000000149011612
      y: -0.10000000149011612
      z: -0.10000000149011612
    rotation:
      x: -0.0
      y: -0.7071068286895752
      z: -0.0
      w: -0.7071068286895752
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/camera_link
  child_frame_id: Quadrotor/camera
  transform:
    translation:
      x: -9.685389159130864e-06
      y: 0.002441554795950651
      z: -0.002441555727273226
    rotation:
      x: 4.0149917168719185e-08
      y: -2.0861622829215776e-07
      z: 4.0149917168719185e-08
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/camera_link_2
  transform:
    translation:
      x: 0.10000000149011612
      y: -0.10000000149011612
      z: -0.10000000149011612
    rotation:
      x: -0.0
      y: -0.9659258723258972
      z: -0.0
      w: 0.25881901383399963
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/camera_link_2
  child_frame_id: Quadrotor/camera_2
  transform:
    translation:
      x: 0.0021192918065935373
      y: 0.002441554795950651
      z: 0.001212389557622373
    rotation:
      x: -0.5000001192092896
      y: -4.095853611829625e-08
      z: -0.8660252690315247
      w: 3.771201662061685e-08
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/propeller1_link
  transform:
    translation:
      x: 0.3149005174636841
      y: 1.1205673217773438e-05
      z: -8.912114424219908e-08
    rotation:
      x: 0.4996607303619385
      y: 0.500339150428772
      z: 0.4996606111526489
      w: -0.5003390908241272
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/propeller2_link
  transform:
    translation:
      x: 1.1205673217773438e-05
      y: -0.31490054726600647
      z: 2.4025627709534092e-08
    rotation:
      x: 0.5002902746200562
      y: 0.4997096061706543
      z: 0.5002902150154114
      w: -0.4997096359729767
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/propeller3_link
  transform:
    translation:
      x: -0.3149005174636841
      y: -1.1205673217773438e-05
      z: 8.912114424219908e-08
    rotation:
      x: 0.4996721148490906
      y: 0.5003277063369751
      z: 0.4996720552444458
      w: -0.5003277659416199
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/propeller4_link
  transform:
    translation:
      x: -1.1205673217773438e-05
      y: 0.31490054726600647
      z: -2.4025627709534092e-08
    rotation:
      x: 0.5002931356430054
      y: 0.49970683455467224
      z: 0.500292956829071
      w: -0.49970677495002747
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/imu_link
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/imu_link
  child_frame_id: Quadrotor/IMU
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/depthsensor_link
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/rangereceiver_link
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/gps_link
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: 0.0
      y: -0.0
      z: 0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/gps_link
  child_frame_id: Quadrotor/GPS
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/hull
  transform:
    translation:
      x: 0.0
      y: -0.0
      z: 0.0
    rotation:
      x: 0.6532815098762512
      y: 0.27059808373451233
      z: 0.6532815098762512
      w: -0.27059808373451233
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/base_link
  child_frame_id: Quadrotor/winch_link
  transform:
    translation:
      x: -1.1886407413896904e-08
      y: -3.2048368403536642e-09
      z: -0.04199981689453125
    rotation:
      x: -0.0
      y: 0.0
      z: -0.0
      w: -1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: map_gt
  child_frame_id: Quadrotor/odom
  transform:
    translation:
      x: 1327.0
      y: 1065.0
      z: 7.0
    rotation:
      x: 0.0
      y: 0.0
      z: 0.0
      w: 1.0
- header:
    stamp:
      sec: 403
      nanosec: 342881207
    frame_id: Quadrotor/odom
  child_frame_id: Quadrotor/base_link
  transform:
    translation:
      x: 0.000244140625
      y: 0.00048828125
      z: -0.017129898071289062
    rotation:
      x: -7.848026939427655e-08
      y: 1.2377516611650208e-07
      z: -0.29716756939888
      w: -0.9548253417015076
---

