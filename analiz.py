import numpy as np
import matplotlib.pyplot as plt
import time

print("Получаем данные из файлов data.txt и settings.txt")
#обрабатываем данные из двух файлов
with open("settings.txt", "r") as settings:
	sett = [float(el) for el in settings.read().split("\n")]
data = np.loadtxt("data.txt", dtype = int)

voltage = np.array(data)*sett[1]

time = np.linspace(0,sett[0]*(len(data)), len(data))
time_max = time[data.argmax()]

# построение графика
print("Строим график")
fig, ax = plt.subplots(figsize = (16,10), dpi = 400)
ax.plot(time, voltage, alpha=0.9, label="Voltage to time", lw=0.3, c='b', mew=0.4, ms=10, marker = ".", markevery = 100, mfc = 'b', mec = 'b')

#настройка осей
max_hight = voltage.max()+0.2
plt.axis([0,time[-1] + 0.1 ,0, max_hight])
ax.minorticks_on()
ax.grid(which='major', color = 'k', linewidth = 2, alpha = 0.3)
ax.grid(which='minor', color = 'k', linestyle = '--', alpha = 0.1)
#настройка подписей
font = 8
str1 = plt.text(time_max+10, max_hight - 0.2, 'Время зарядки: ' + str(time_max), fontsize=font)   # выравнивание по левому краю
str2 = plt.text(time_max+10, max_hight - (0.2 + font/100), 'Время разрядки: ' + str(time[-1] - time_max), fontsize=font)

plt.title('Зависимость напряжения от времени')
plt.xlabel('время, с')
plt.ylabel('Напряжение, В')
plt.legend()
#сохранение графика в формате svg
print("Сохраняем график")
fig.savefig("graph.svg")
#plt.show()
