# NN Splitting - Cloud

This is a modified version of the Yolo implementation from [AlexeyAB](https://github.com/AlexeyAB/yolo2_light).
Please check his repository for a setup guide and pre-requirements.


## Execution:

```sh
./bin/darknet detector test ./bin/voc.names ./bin/tiny-yolo-voc.cfg ./bin/tiny-yolo-voc.weights -thresh 0.24  /home/philipp/usb/data/images/jpg_100/frame_50.jpg $partial_result$ $Layer_Nr$
```
