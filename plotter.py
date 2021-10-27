import matplotlib.pyplot as plt


fig, axs = plt.subplots(3, 1, sharex=True)
fig.subplots_adjust(hspace=0)
fig.tight_layout()

while True:
    logs = [x.split("\t") for x in open("./logfile.tsv", "r+").readlines()]
    axs[0].clear()
    axs[0].scatter(
            [float(x[0]) for x in logs], 
            [float(x[3]) if float(x[-2]) else None for x in logs],
            label="Holds")
    axs[0].scatter(
            [float(x[0]) for x in logs], 
            [float(x[3]) if not float(x[-2]) and float(logs[max(i-1, 0)][-2]) else None for i, x in enumerate(logs)],
            label="Sales"
        )
    axs[0].plot([float(x[0]) for x in logs], [float(x[1]) for x in logs], label="BTC Actual")
    axs[0].plot([float(x[0]) for x in logs], [float(x[3]) for x in logs], label="BTC IBM")
    axs[0].grid()
    axs[0].legend()

    axs[1].clear()
    axs[1].scatter(
            [float(x[0]) for x in logs],
            [float(x[4]) if float(x[-1]) else None for x in logs], label="holds"
        )
    axs[1].scatter(
            [float(x[0]) for x in logs],
            [float(x[4]) if not float(x[-1]) and float(logs[max(i-1, 0)][-1]) else None for i, x in enumerate(logs)],
            label="Sales"
        )
    axs[1].plot([float(x[0]) for x in logs], [float(x[2]) for x in logs], label="ETC Actual")
    axs[1].plot([float(x[0]) for x in logs], [float(x[4]) for x in logs], label="ETC IBM")
    axs[1].grid()
    axs[1].legend()


    datax = []
    datay = []
    for x in logs:
        usd = float(x[-3])
        if usd > 0:
            datax.append(float(x[0]))
            datay.append(float(x[-3]) - float(logs[0][-3]))

    axs[2].clear()
    axs[2].plot(datax, datay, label="Profit")
    axs[2].legend()
    axs[2].grid()
    fig.show()
    plt.pause(10)

