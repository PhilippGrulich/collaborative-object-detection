
precisions=(0.1 0.01 0.001 0.0001 0.00001 0.000001)
image=((10 0))


for var in "${image[@]}"
    do
        for file in /home/philipp/usb/projects/yolo2_light_partitioned/data/frame_$var/*; do
            echo $file
        done
done








