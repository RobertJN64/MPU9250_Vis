import matplotlib.pyplot as plt
import multiprocessing
from time import sleep
import serial

USE_SERIAL = True
port = 'COM5'

max_val = 400
acc_mul = 200

def disp_func(mag_end, killflag):
    print("Disp func running")
    start = (0, 0, 0)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mag_q = ax.quiver(start[0], start[1], start[2], mag_end[0], mag_end[1], mag_end[2], color='blue')

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

        mag_q.remove()
        mag_q = ax.quiver(start[0], start[1], start[2], mag_end[0], mag_end[1], mag_end[2], color='blue')
        ax.scatter(mag_end[0], mag_end[1], mag_end[2], c='red')

    killflag[0] = True
    print("Draw loop done")


def main():
    mpu = None
    manager = multiprocessing.Manager()
    mag_end = manager.list([max_val/2, max_val/2, max_val/2])
    killflag = manager.list([False])

    p = multiprocessing.Process(target=disp_func, args=(mag_end, killflag))
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
            _, line = line.split(':')
            line = line.removeprefix(' ')
            new = tuple(map(float, line.split(' ')))
            mag_end[0] = new[0]
            mag_end[1] = new[1]
            mag_end[2] = new[2]

        else:
            print(line) #for serial debug



if __name__ == '__main__':
    main()