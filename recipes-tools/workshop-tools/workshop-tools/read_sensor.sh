#!/bin/bash - 
#===============================================================================
#
#          FILE: read_sensor.sh
# 
#         USAGE: ./read_sensor.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: IKS01A3 expansion board plugged and sensor drivers added 
#        AUTHOR: From https://wiki.st.com/stm32mpu/wiki/IKS01A3_MEMS_expansion_board
#  ORGANIZATION: STMicroelectronics 
#       CREATED: 05/13/2021 02:56:59 PM
#      REVISION:  ---
#===============================================================================


usage () {
    echo Usage: $0 \<sensor_type\>
    echo \<sensor_type\> should be one of: acc, mag or hum
    exit 1
} 

read_hum () {
iio_device_string=`grep hts221 /sys/bus/iio/devices/iio\:device*/uevent | grep OF_NAME | sed -e 's|\(.*\)/.*|\1|'`
if [ -z $iio_device_string ] ; then
	echo Sensor hts221 not found, Please check your kernel configuration and driver installation	
    	exit 1
fi
raw=`cat ${iio_device_string}/in_temp_raw`
offset=`cat ${iio_device_string}/in_temp_offset`
scale=`cat ${iio_device_string}/in_temp_scale`
printf "Value read: raw         %0f\n" $raw
printf "Value read: offset      %0f\n" $offset
printf "Value read: scale       %0f\n" $scale

temperature=`echo "scale=2;$raw*$scale + $offset*$scale" | bc`

echo "Temperature $temperature"
printf "Temperature %.01f\n" $temperature
}

read_acc () {
iio_device_string=`grep lis2dw12 /sys/bus/iio/devices/iio\:device*/uevent | grep OF_NAME | sed -e 's|\(.*\)/.*|\1|'`
if [ -z $iio_device_string ] ; then
	echo Sensor lis2dw12 not found, Please check your kernel configuration and driver installation	
    	exit 1
fi
xraw=`cat ${iio_device_string}/in_accel_x_raw`
xscale=`cat ${iio_device_string}/in_accel_x_scale`
yraw=`cat ${iio_device_string}/in_accel_y_raw`
yscale=`cat ${iio_device_string}/in_accel_y_scale`
zraw=`cat ${iio_device_string}/in_accel_z_raw`
zscale=`cat ${iio_device_string}/in_accel_z_scale`
printf "Value read: X (raw/scale)  %d / %.06f \n" $xraw $xscale
printf "Value read: Y (raw/scale)  %d / %.06f \n" $yraw $yscale
printf "Value read: Z (raw/scale)  %d / %.06f \n" $zraw $zscale

factor=`echo "scale=2;256.0 / 9.81" | bc`
xval=`echo "scale=2;$xraw*$xscale*$factor" | bc`
yval=`echo "scale=2;$yraw*$yscale*$factor" | bc`
zval=`echo "scale=2;$zraw*$zscale*$factor" | bc`

printf "Accelerometer value: [ %.02f, %.02f, %.02f ]\n" $xval $yval $zval
}

read_mag () {
iio_device_string=`grep lis2mdl /sys/bus/iio/devices/iio\:device*/uevent | grep OF_NAME | sed -e 's|\(.*\)/.*|\1|'`
if [ -z $iio_device_string ] ; then
	echo Sensor lis2mdl not found, Please check your kernel configuration and driver installation	
    	exit 1
fi
xraw=`cat ${iio_device_string}/in_magn_x_raw`
xscale=`cat ${iio_device_string}/in_magn_x_scale`
yraw=`cat ${iio_device_string}/in_magn_y_raw`
yscale=`cat ${iio_device_string}/in_magn_y_scale`
zraw=`cat ${iio_device_string}/in_magn_z_raw`
zscale=`cat ${iio_device_string}/in_magn_z_scale`
printf "Value read: X (raw*scale)  %d * %.06f \n" $xraw $xscale
printf "Value read: Y (raw*scale)  %d * %.06f \n" $yraw $yscale
printf "Value read: Z (raw&scale)  %d * %.06f \n" $zraw $zscale

factor=1000
xval=`echo "scale=2;$xraw*$xscale*$factor" | bc`
yval=`echo "scale=2;$yraw*$yscale*$factor" | bc`
zval=`echo "scale=2;$zraw*$zscale*$factor" | bc`

printf "Magnetometer value: [ %.02f, %.02f, %.02f ]\n" $xval $yval $zval
}

if [ $# -ne 1 ]; then
    usage
fi

sensor_type=$1

case $sensor_type in
acc)
read_acc
;;

mag)
read_mag
;;

hum)
read_hum
;;

*)
usage
;;

esac    # --- end of case ---
