import matplotlib.pyplot as plt
import multiprocessing
from time import sleep

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
    manager = multiprocessing.Manager()
    end = manager.list([1, 1, 5])
    killflag = manager.list([False])

    p = multiprocessing.Process(target=disp_func, args=(end, killflag))
    p.start()
    sleep(1)
    print("Ready: ")
    while not killflag[0]:
        new = tuple(map(int, input().replace('$', '').split(' ')))
        end[0] = new[0]
        end[1] = new[1]
        end[2] = new[2]


if __name__ == '__main__':
    main()

