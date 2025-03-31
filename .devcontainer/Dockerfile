FROM python:3.10

ARG DEBIAN-FRONTEND=noninteractifve
ENV TZ=Asia/Tokyo
ENV SHELL=/bin/bash
ARG USERNAME=${USERNAME}
ARG USER_UID=${USER_UID}
ARG USER_GID=${USER_GID}
COPY ./requirements.txt /tmp/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    vim \
    git && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    pip install -U pip && \
    pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    echo 'alias python="python3"' >> /home/$USERNAME/.bashrc

USER $USERNAME
