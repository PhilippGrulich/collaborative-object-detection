# NN Splitting - Edge

This is a modified version of the Yolo implementation from [AlexeyAB](https://github.com/AlexeyAB/yolo2_light).
Please check his repository for a setup guide and pre-requirements.

#### Execution:

The current implementation will compute the full NN for a given image and store the results from every layer.
```sh
./bin/darknet detector test ./bin/voc.names ./bin/tiny-yolo-voc.cfg ./bin/tiny-yolo-voc.weights -thresh 0.24 $file_path$ $file_name$ 
```

The output dir is currently hardcoded.

```processImages.sh``` is a script to execute this comand on all images in a given folder.



#### Compression

For layer compression you can use and modify the ```layercompress.sh``` and ```layerdecompress.sh``` scripts.
