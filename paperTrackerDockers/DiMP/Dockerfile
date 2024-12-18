FROM mcr.microsoft.com/azureml/o16n-base/python-assets@sha256:20a8b655a3e5b9b0db8ddf70d03d048a7cf49e569c4f0382198b1ee77631a6ad AS inferencing-assets

FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
USER root:root

ENV com.nvidia.cuda.version $CUDA_VERSION
ENV com.nvidia.volumes.needed nvidia_driver
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
ENV NCCL_DEBUG=INFO
ENV HOROVOD_GPU_ALLREDUCE=NCCL

# Inference
COPY --from=inferencing-assets /artifacts /var/

# Install Common Dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    apt-get install -y --no-install-recommends \
    # SSH and RDMA
    libmlx4-1 \
    libmlx5-1 \
    librdmacm1 \
    libibverbs1 \
    libmthca1 \
    libdapl2 \
    dapl2-utils \
    openssh-client \
    openssh-server \
    sudo \
    iproute2 && \
    # Others
    apt-get install -y --no-install-recommends \
    --allow-change-held-packages \
    build-essential \
    bzip2 \
    libbz2-1.0\
    systemd \
    git \
    wget \
    vim \
    tmux \
    unzip \
    ca-certificates \
    libjpeg-dev \
    cpio \
    jq \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libturbojpeg \
    fuse && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*


# Set timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# create dir for sshd
RUN mkdir -p /var/run/sshd /root/.ssh

# Inference
# Copy logging utilities, nginx and rsyslog configuration files, IOT server binary, etc.
# COPY --from=inferencing-assets /artifacts /var/
# RUN /var/requirements/install_system_requirements.sh && \
#     cp /var/configuration/rsyslog.conf /etc/rsyslog.conf && \
#     cp /var/configuration/nginx.conf /etc/nginx/sites-available/app && \
#     ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app && \
#     rm -f /etc/nginx/sites-enabled/default
# ENV SVDIR=/var/runit
# ENV WORKER_TIMEOUT=300
# EXPOSE 5001 8883 8888

# Conda Environment
ENV MINICONDA_VERSION latest
ENV PATH /opt/miniconda/bin:$PATH
RUN wget -qO /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -bf -p /opt/miniconda && \
    conda clean -ay && \
    rm -rf /opt/miniconda/pkgs && \
    rm /tmp/miniconda.sh && \
    find / -type d -name __pycache__ | xargs rm -rf
# Open-MPI installation
ENV OPENMPI_VERSION 3.1.2
RUN mkdir /tmp/openmpi && \
    cd /tmp/openmpi && \
    wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-${OPENMPI_VERSION}.tar.gz && \
    tar zxf openmpi-${OPENMPI_VERSION}.tar.gz && \
    cd openmpi-${OPENMPI_VERSION} && \
    ./configure --enable-orterun-prefix-by-default && \
    make -j $(nproc) all && \
    make install && \
    ldconfig && \
    rm -rf /tmp/openmpi

RUN conda install -c r -y conda python=3.9 pip
RUN conda install -y numpy pyyaml ipython mkl scikit-learn matplotlib pandas setuptools Cython h5py graphviz libgcc mkl-include cmake cffi typing cython && \
    conda install -y -c mingfeima mkldnn && \
    conda install -c anaconda gxx_linux-64

RUN conda install -c anaconda gxx_linux-64
RUN conda clean -ya
#RUN pip install boto3 addict tqdm regex pyyaml opencv-python opencv-contrib-python azureml-defaults nltk spacy future tensorboard wandb filelock tokenizers sentencepiece
RUN pip install regex pyyaml opencv-contrib-python future

# Set CUDA_ROOT
RUN export CUDA_HOME="/usr/local/cuda"

# Install littleboy related packages

# Install pytorch
#RUN conda install pytorch torchvision torchaudio cudatoolkit=10.0 -c pytorch 
#RUN conda install pytorch==1.10.1 torchvision==0.11.2 cudatoolkit=10.0 torchaudio==0.10.1 -c pytorch
#RUN conda install torchvision==0.19.1

# -c conda-forge

# Install other packages
RUN pip install PyYAML && \
    pip install easydict && \
    pip install cython && \
    pip install opencv-python && \
    pip install pandas && \
    pip install tqdm && \
    pip install pycocotools && \
    # apt-get install libturbojpeg && \
    pip install jpeg4py && \
    pip install tb-nightly && \
    pip install tikzplotlib && \
    pip install thop && \
    pip install lmdb && \
    pip install scipy && \
    pip install visdom && \
    pip install wandb && \
    pip install tensorboardX && \
    pip install yacs && \
    pip install timm && \
    pip install class_registry && \
    pip install shapely && \
    pip install gdown && \
    pip install pytracking
# conda env installation

WORKDIR /home

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

RUN git clone https://github.com/votchallenge/integration.git


#Copy 
COPY codes /home/codes
COPY main.py /home/main.py
COPY dockerfiles/mystack.yaml /home/toolkit/vot/stack/mystack.yaml
COPY dockerfiles/__init__.py /home/toolkit/vot/dataset/__init__.py

#Create VOT WORKSPACE
RUN vot initialize mystack --workspace vot_ws

#Copy Trackers.ini
#COPY ../../../dockerfiles/trackers.ini /home/vot_ws/trackers.ini
# setup entrypoint
CMD ["bash"]

WORKDIR /home
RUN git clone https://github.com/Sogensava/pytracking.git
RUN cd ./pytracking
WORKDIR /home/pytracking

RUN cp /home/pytracking/trackers.ini /home/vot_ws/trackers.ini

WORKDIR /home/pytracking
RUN cd /home/pytracking

RUN conda install -y matplotlib
RUN conda install -y pandas
RUN conda install -y tqdm
RUN pip install opencv-python
RUN pip install tb-nightly
RUN pip install visdom
RUN pip install scikit-image
RUN pip install tikzplotlib
RUN pip install gdown
RUN conda install -y cython
RUN pip install pycocotools
RUN pip install lvis
#RUN pip install spatial-correlation-sampler
RUN pip install jpeg4py 
#RUN sudo apt-get install ninja-build
RUN mkdir pytracking/networks
RUN gdown https://drive.google.com/uc\?id\=1qgachgqks2UGjKx-GdO1qylBDdB1f9KN -O pytracking/networks/dimp50.pth

RUN cd /home/pytracking && git submodule init
RUN python -c "from pytracking.evaluation.environment import create_default_local_file; create_default_local_file()"
RUN python -c "from ltr.admin.environment import create_default_local_file; create_default_local_file()"
RUN git submodule update

RUN rm /home/pytracking/ltr/external/PreciseRoIPooling/pytorch/prroi_pool/src/prroi_pooling_gpu.c
RUN cp /home/pytracking/pytracking/external/prroi_pooling_gpu.c /home/pytracking/ltr/external/PreciseRoIPooling/pytorch/prroi_pool/src/
 
WORKDIR /home

RUN pip uninstall torch -y
RUN pip uninstall torchvision -y 

RUN conda install pytorch=2.4.1 torchvision=0.19.1 torchaudio=2.4.1 pytorch-cuda=12.1 cudatoolkit=10.0 -c pytorch -c nvidia

RUN cd /home
WORKDIR /home

RUN mkdir dataset