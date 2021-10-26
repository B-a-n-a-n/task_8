import numpy as np
import matplotlib.pyplot as plt
import time
import RPi.GPIO as GPIO

def decimal_binary(decimal):
	return [int(el) for el in bin(decimal)[2:].zfill(bits)]

def dac_bin(value):
	signal = decimal_binary(value)
	#GPIO.output(dac, signal)
	return signal


dac = [26,19,13,6,5,11,9,10]
leds = [21,20,16,12,7,8,25,24]
bits = len(dac)
levels= 2**bits
max_V = 3.3
troyka = 17
comparator = 4

GPIO.setmode(GPIO.BCM) #Зала
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def binary_acd(): #функция, находящая текущее значение напряжения на конденсаторе
    begin, end = 0, 256
    while begin < end:
        value = (begin + end)//2
        signal = dac_bin(value)
        GPIO.output(dac, signal)
        time.sleep(0.002)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            begin = value + 1
        else:
            end = value
    signal = dac_bin(value)
    GPIO.output(dac, signal)
    return value

def volume(value): # функция, отображающая на LEDS степень заряженности конденсатора по сравнению с максимальным
    c = int((9*value)/254)
    a = [0]*8
    for i in range(c-1):
        a[i] = 1
    GPIO.output(leds, a)
    #time.sleep(0.1)
GPIO.output(troyka, 1)

try:
	measured_data = [] # создание списка для записи напряжений
	times = [] #создание списка для записи времени
	times.append(time.time())
	k = True
	print("Конденсатор начал заряжаться")
	while k: #цикл для записи возрастающих напряжений
		value = binary_acd()
		GPIO.output(leds, decimal_binary(value))
		measured_data.append(value)
		if value > 230: 
			GPIO.output(troyka, 0)
			k = False
	k = True
	print("Конденсатор зарядился")
	while k: #цикл для записи убывающих напряжений
		value = binary_acd()
		GPIO.output(leds, decimal_binary(value))
		measured_data.append(value)
		if value < 50: 
				GPIO.output(troyka, 0)
				k = False  #1
	print("Конденсатор разрядился")
	print("Строим график")
	times.append(time.time())
	plt.plot(measured_data) #построение графика по снятым напряжениям
	plt.show()
	print("Заносим данные в файлы data.txt и settings.txt")
	measured_data_str = [str(item) for item in measured_data] #добавление снятых напряжений в файл data.txt
	with open("data.txt", "w") as outfile:
		outfile.write("\n".join(measured_data_str))
	settings = ["Период - " + str((times[1]-times[0])/(len(measured_data)-1)), "Коэффициент перевода - " + str(3.3/(255))]
	with open("settings.txt", "w") as outfile:
		outfile.write("\n".join(settings))
	

except KeyboardInterrupt:
	print("Прерывание с клавиатуры")
	pass
finally:
	GPIO.output(dac,GPIO.LOW)
	GPIO.cleanup()
	print("Конденсатор разрядился")