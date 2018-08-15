
imageFolder=$1

for file in $imageFolder/*jpg ; do
 echo "process $file"
 name=$(basename "$file" ".jpg")
 echo ./bin/darknet detector test ./bin/voc.names ./bin/tiny-yolo-voc.cfg ./bin/tiny-yolo-voc.weights -thresh 0.24 $file $name
 ./bin/darknet detector test ./bin/voc.names ./bin/tiny-yolo-voc.cfg ./bin/tiny-yolo-voc.weights -thresh 0.24 $file $name

 done
