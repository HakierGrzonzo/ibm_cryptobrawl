import matplotlib.pyplot as plt

logs = [x.split("\t") for x in open("./logfile.tsv", "r+").readlines()]
plt.subplot(1, 2, 1)
plt.plot([float(x[1]) for x in logs], [float(x[2]) for x in logs], label="BTC Actual")
plt.plot([float(x[1]) for x in logs], [float(x[4]) for x in logs], label="BTC IBM")
plt.xlabel("Czas [s]")
plt.ylabel("Cena [$]")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot([float(x[1]) for x in logs], [float(x[3]) for x in logs], label="Ethereum Actual")
plt.plot([float(x[1]) for x in logs], [float(x[5]) for x in logs], label="Ethereum IBM")
plt.xlabel("Czas [s]")
plt.ylabel("Cena [$]")
plt.legend()
plt.show()

