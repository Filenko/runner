#!/bin/bash

# Обновляем список пакетов
sudo apt-get update

# Устанавливаем необходимые пакеты для использования репозитория по HTTPS
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Добавляем официальный GPG ключ Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Добавляем репозиторий Docker в список источников APT
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Обновляем список пакетов после добавления репозитория Docker
sudo apt-get update

# Устанавливаем Docker CE
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Добавляем текущего пользователя в группу docker
sudo usermod -aG docker $USER
