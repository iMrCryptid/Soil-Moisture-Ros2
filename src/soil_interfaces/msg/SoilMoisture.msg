# One reading from a capacitive soil moisture sensor on the science module
std_msgs/Header header      # timestamp and frame of the reading
string sensor_id            # which probe produced the reading
uint16 raw_adc              # raw analog value (higher = drier for capacitive sensors)
float32 moisture_percent    # calibrated volumetric estimate, 0 (air dry) to 100 (in water)
