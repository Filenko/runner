import psutil
import subprocess
import time

# Запуск длительной программы с помощью subprocess
process = subprocess.Popen(['python3', '-c', 'b=[]\nfor i in range(100000000000000):\n    b.append(i**2)'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Чтобы просмотреть информацию о памяти, создаём объект psutil.Process
ps_process = psutil.Process(process.pid)

# Цикл для регулярной проверки использования памяти
try:
    while True:
        mem_info = ps_process.memory_full_info()
        print(mem_info)
        time.sleep(0.5)  # Проверка каждые 0.5 секунды
except psutil.NoSuchProcess:
    print("Процесс завершился.")