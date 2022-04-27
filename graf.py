import numpy as np
import matplotlib.pyplot as plt

with open("settings.txt", "r") as settingsFile:
    settings =[float(i) for i in settingsFile.read().split("\n")]
    
data = np.loadtxt("data.txt", dtype = float)
data = data*3.3/255

print("Data: ")
print(data)
print("Settings: ")
print(settings)

indexOfmaxVolt = data.argmax()

x = np.linspace(0, settings[0], 1194)
print("Time: ")
print(x)
y = data

print("Время зарядки: ")
print(x[indexOfmaxVolt])
print("Время разрядки: ")
print(x[1193] - x[indexOfmaxVolt])

fig, ax = plt.subplots(figsize = (16, 10), dpi = 400)
ax.plot(x, y, label = "Напряжение", marker = ".", color = "green")
ax.set_title("Процесс заряда и разряда конденсатора в RC-цепочке")
ax.set_xlabel("t, с")
ax.set_ylabel("U, В")
ax.text(65,2.6,"Время зарядки = {:f} с".format(x[indexOfmaxVolt]))
ax.text(65,2.7,"Время разрядки = {:f} с".format(x[1193] - x[indexOfmaxVolt]))
ax.grid(linestyle = '--')
ax.legend()
fig.savefig("graphic.png")
