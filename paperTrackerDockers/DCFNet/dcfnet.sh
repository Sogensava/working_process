docker build -t dcfnet .
xhost +local:docker
sudo docker run --name dcfnet_cont --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev -it dcfnet
