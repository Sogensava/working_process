ARG UBUNTU_RELEASE_YEAR=20
ARG CUDA_MAJOR=12
ARG CUDA_MINOR=1

FROM nvidia/cuda:${CUDA_MAJOR}.${CUDA_MINOR}.0-devel-ubuntu${UBUNTU_RELEASE_YEAR}.04

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}compute,video,utility

RUN echo "Europe/Paris" > /etc/localtime ; echo "CUDA Version ${CUDA_MAJOR}.${CUDA_MINOR}.0" > /usr/local/cuda/version.txt


WORKDIR /workspace/

RUN echo 'Etc/UTC' > /etc/timezone && \
    # ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# GStreamer 
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    curl \
    wget \
    gcc \
    g++ \
    libx264-dev \
    libjpeg-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-libav \
    xdg-utils \
    gedit \
    && rm -rf /var/lib/apt/lists/*

#VOT
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/votchallenge/toolkit.git && \
    cd toolkit && \
    pip install -e .
    
#OpenCV
RUN pip3 install opencv-python

#Experimental Tracker
RUN git clone https://github.com/votchallenge/integration.git

#Copy 
COPY ./codes /workspace/codes
COPY ./main.py /workspace/main.py
COPY ./dockerfiles/mystack.yaml /workspace/toolkit/vot/stack/mystack.yaml
COPY ./dockerfiles/__init__.py /workspace/toolkit/vot/dataset/__init__.py

#Create VOT WORKSPACE
RUN vot initialize mystack --workspace vot_ws
#Copy Trackers.ini
COPY ./dockerfiles/trackers.ini /workspace/vot_ws/trackers.ini

# setup entrypoint
CMD ["bash"]

# ====================
# Custom Commands
# ====================

# Install common tools
#RUN apt-get update && apt-get install -y git gedit tmux \
#    && rm -rf /var/lib/apt/lists/*
