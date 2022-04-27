
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

measured_data = []

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12 ,7, 8, 25, 24]
troyka = 17
comp = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(leds,GPIO.OUT, initial = 0)
GPIO.setup(troyka, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(decimal):#Переделываем в бинарную систему
    return [int(elem) for elem in bin(decimal)[2:].zfill(8)]

def bin2dac(value):#иЗ бинарного в обычный
    b = decimal2binary(value)
    GPIO.output(dac,b)
    return b

def adc():#Треугольный сигнал
    i = 0
    num = [0,0,0,0,0,0,0,0]
    value = 0
    while (i != 7):
        num[i] = 1
        GPIO.output(dac,num)
        time.sleep(0.01)
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 0:
            num [i] = 0
        else:
            value += 2**(7-i)
        i += 1

    return value

try:
    start = time.time()

    decimal = 0
    GPIO.output(troyka, 1)

    while decimal <= 248:#Пока меньше 248
        decimal = adc()#Треугольный сигнал
        i = 0
        volume = int(8*decimal/250)
        bin = [0,0,0,0,0,0,0,0]
        for i in range (volume):
            bin[i] = 1
        GPIO.output(leds, bin)
        measured_data.append(decimal)
        print(decimal)
    
    print('Конденсатор заряжен. Выполняем разряд.')
    GPIO.output(troyka, 0)

    while decimal >= 14:#Пока сигнал уменьшается
        decimal = adc()
        i = 0
        volume = int(8*decimal/250)
        bin = [0,0,0,0,0,0,0,0]
        for i in range (volume):
            bin[i] = 1
        GPIO.output(leds, bin)
        measured_data.append(decimal)
        print(decimal)
    
    finish = time.time()

    experiment_time = finish - start

finally:#Отправляем на вывод нули
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)

plt.plot(measured_data)
plt.show()#Строим график по измерениям

print("Время эксперимента = {} c".format(experiment_time))
print("Период одного измерения = {} c".format(0.01))
print("Частота дескретизации = {} Гц".format(100))
print("Шаг квантования = {}".format(3.3/256))

measured_data_str = [str(item) for item in measured_data]

with open ("data.txt", "w") as data_outfile:#Выводим напряжение в столбик
        data_outfile.write("\n".join(measured_data_str))


with open("settings.txt", "w") as settings_outfile:#Выводим время. Период. Частота. Шаг квантования.
        settings_outfile.write(format(experiment_time))
        settings_outfile.write("\n{}".format(0.01))
        settings_outfile.write("\n{}".format(100))
        settings_outfile.write("\n{}".format(3.3/256))