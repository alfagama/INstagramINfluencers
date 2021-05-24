import matplotlib.pyplot as plt

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%'.format(p=pct,v=val)
    return my_autopct

def plot_pie(values, info, labels):
    plt.figure(0)
    print(values)
    plt.pie(values, labels=labels, autopct=make_autopct(values), shadow=True)
    plt.show()

    if info:
        for i in info:
            val = []
            follow = i[2]
            val.append(follow)
            val.append(i[1]-follow)
            plt.pie(val, labels=['Follow', 'Don\'t follow'], autopct=make_autopct(val), shadow=True)
            plt.title(i[0])
            plt.show()