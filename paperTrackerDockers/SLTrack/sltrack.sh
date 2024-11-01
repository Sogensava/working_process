docker build -t sltrack .
sudo docker run --name sltrack_cont --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev -it sltrack
