docker build -t ostrack .
sudo docker run --name ostrack_cont --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev -it ostrack
