# Collaborative Edge and Cloud Neural Networks for Real-Time Video Processing
**Abstract:**
The efficient processing of video streams is a key component in many emerging Internet of Things (IoT) and edge appli-
cations, such as Virtual and Augmented Reality (V/AR) and self-driving cars. These applications require real-time
high-throughput video processing. This can be attained via a collaborative processing model between the edge and the
cloud—called an Edge-Cloud model. To this end, many approaches were proposed to optimize the latency and bandwidth consumption of Edge-Cloud video processing, especially for Neural Networks (NN)-based methods. In this
demonstration. We investigate the efficiency of these NN techniques, how they can be combined, and whether combining them leads to better performance. Our demonstra tion invites participants to experiment with the various NN techniques, combine them, and observe how the underlying NN changes with different techniques and how these changes affect accuracy, latency and bandwidth consumption.

```
@article{grulich2018collaborative,
  title={Collaborative Edge and Cloud Neural Networks for Real-Time Video Processing},
  author={Grulich, Philipp M and Nawab, Faisal},
  journal={Proceedings of the VLDB Endowment},
  volume={11},
  number={12},
  year={2018}
}
```
## Demo Setup:

### Requirements:
This project requires at least GCC 7.X, OpenCV 3.X, Python 3.X and PyQt

## Components:
This project is seperated into multiple components, which have to be build individually. 

#### Ui:
The ui component represented basically our demo as described in the paper. It requires that all other components are built individually.
Execut the main.py to start the demo.

#### Difference Image:
In this component, we extract the difference between Frames and transfer only the part of the image which has changed in comparison to the last full transferred frame.
To implement this we rely on a Gaussian Mixture-based Background/Foreground Segmentation Algorithm implemented in OpenCV to detect the changes partly in the image [“An improved adaptive background mixture model for real-time tracking with shadow detection" by P. KadewTraKuPong and R. Bowden].
This component expected a difference image, which we use to crop out the differences.
[Details](https://github.com/PhilippGrulich/collaborative-object-detection/tree/master/differential_image)

#### NN Slitting:
In this component, we implement the "Neurosurgeon" approach on the Yolo implementation from https://github.com/AlexeyAB/yolo2_light. This is separated by an edge and a cloud component. 

- **Edge**:
On the edge, we compute the NN till the nth layer and then store the result to a file.
[Details](https://github.com/PhilippGrulich/Collaborative-Realtime-Object-Detection/tree/master/nn_splitting/edge)

- **Cloud**:
The cloud component read the file and completes the NN computation
[Details](https://github.com/PhilippGrulich/Collaborative-Realtime-Object-Detection/tree/master/nn_splitting/cloud)

- **Compression**:
Compression is implemented with the library [zfp](http://zfp.readthedocs.io). 
