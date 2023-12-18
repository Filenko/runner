# Используем Ubuntu 22.04 как базовый образ
FROM ubuntu:22.04

# Устанавливаем Python и pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Устанавливаем зависимости для Docker SDK for Python
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Добавляем GPG ключ Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Добавляем репозиторий Docker
RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

# Устанавливаем Docker
RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip3 install -r /requirements.txt

# Копируем модуль runner в контейнер
COPY runner /runner

# Открываем порт 50051
EXPOSE 50051

# Запускаем модуль runner
#CMD ["python3", "-m", "runner", "--port", "50051"]
