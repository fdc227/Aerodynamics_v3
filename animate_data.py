import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pickle


def animate_data(file_name, xlim, ylim):
    raw = open(file_name, 'rb')
    data = pickle.load(raw)
    x_num = len(data[0])
    x_axis = np.linspace(0, 10, x_num, endpoint=False)

    fig = plt.figure()
    ax = plt.axes(xlim=xlim, ylim=ylim)
    line, = ax.plot([], [], lw=2)

    def inite():
        line.set_data([], [])
        return line,

    def animate(i):
        x = x_axis
        y = data[i]
        line.set_data(x, y)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=inite, frames=499, interval=20, blit=True)

    now = dt.datetime.now()
    info = str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)


    anim.save(f'beam_bending_{info}.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

if __name__ == '__main__':
    file_name = 'final_output_v2.pkl'
    xlim = (0,10)
    ylim = (-4, 3)

    animate_data(file_name, xlim, ylim)