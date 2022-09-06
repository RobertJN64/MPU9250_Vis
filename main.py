import matplotlib.pyplot as plt
import multiprocessing
from time import sleep
import serial

USE_SERIAL = False
port = 'COM5'

max_val = 100

def disp_func(end, killflag):
    print("Disp func running")
    start = (0, 0, 0)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    quiver = ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2])

    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])

    ax.plot([-max_val, max_val], [0,0], [0,0], color='black')
    ax.plot([0, 0], [-max_val, max_val], [0, 0], color='black')
    ax.plot([0, 0], [0, 0], [-max_val, max_val], color='black')

    plt.draw()
    while True:
        plt.draw()
        plt.pause(0.01)
        if not plt.fignum_exists(fig.number):
            break  # handle exit

        quiver.remove()
        quiver = ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2])

    killflag[0] = True
    print("Draw loop done")


def main():
    mpu = None
    manager = multiprocessing.Manager()
    end = manager.list([max_val/2, max_val/2, max_val/2])
    killflag = manager.list([False])

    p = multiprocessing.Process(target=disp_func, args=(end, killflag))
    p.start()
    sleep(1)

    if USE_SERIAL:
        mpu = serial.Serial(port, 115200)

    print("Ready: ")
    while not killflag[0]:
        if USE_SERIAL:
            line = mpu.readline().decode('utf-8').strip()
        else:
            line = input()

        if '$' in line:
            new = tuple(map(int, line.replace('$', '').split(' ')))
            end[0] = new[0]
            end[1] = new[1]
            end[2] = new[2]
        else:
            print(line) #for serial debug



if __name__ == '__main__':
    main()