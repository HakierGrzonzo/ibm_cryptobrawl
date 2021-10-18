import matplotlib.pyplot as plt

logs = [x.split("\t") for x in open("./logfile.tsv", "r+").readlines()]

plt.subplot(2, 1, 1)
plt.scatter(
        [float(x[0]) for x in logs], 
        [float(x[3]) if float(x[-2]) else None for x in logs],
        label="Holds")
plt.scatter(
        [float(x[0]) for x in logs], 
        [float(x[3]) if not float(x[-2]) and float(logs[max(i-1, 0)][-2]) else None for i, x in enumerate(logs)],
        label="Sales"
    )
plt.plot([float(x[0]) for x in logs], [float(x[1]) for x in logs], label="BTC Actual")
plt.plot([float(x[0]) for x in logs], [float(x[3]) for x in logs], label="BTC IBM")
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(
        [float(x[0]) for x in logs],
        [float(x[4]) if float(x[-1]) else None for x in logs], label="holds"
    )
plt.scatter(
        [float(x[0]) for x in logs],
        [float(x[4]) if not float(x[-1]) and float(logs[max(i-1, 0)][-1]) else None for i, x in enumerate(logs)],
        label="Sales"
    )
plt.plot([float(x[0]) for x in logs], [float(x[2]) for x in logs], label="ETC Actual")
plt.plot([float(x[0]) for x in logs], [float(x[4]) for x in logs], label="ETC IBM")
plt.legend()
plt.show()

