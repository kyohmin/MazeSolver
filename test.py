from matplotlib import animation as ani
from matplotlib import pyplot as plt

class FuncAnimationDisposable(ani.FuncAnimation):
    def __init__(self, fig, func, **kwargs):
        super().__init__(fig, func, **kwargs)
        
    def _step(self, *args):
        still_going = ani.Animation._step(self, *args)
        if not still_going and self.repeat:
            super()._init_draw()
            self.frame_seq = self.new_frame_seq()
            self.event_source.interval = self._repeat_delay
            return True
        elif (not still_going) and (not self.repeat):
            plt.close()  # this code stopped the window
            return False
        else:
            self.event_source.interval = self._interval
            return still_going
        
    def _stop(self, *args):
        # On stop we disconnect all of our events.
        if self._blit:
            self._fig.canvas.mpl_disconnect(self._resize_id)
        self._fig.canvas.mpl_disconnect(self._close_id)

        

multiplier = 0
def get_data():         # some dummy data to animate
    x = range(-10, 11)
    global multiplier
    y = [multiplier * i for i in x]
    multiplier += 0.005
    return x, y

class Schrodinger_Solver(object):
    def __init__(self, xlim = (-10, 10), ylim = (-10, 10), num_frames = 200):

        self.num_frames = num_frames
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, xlim = xlim, ylim = ylim)
        self.p_line, = self.ax.plot([], [])

        self.ani = FuncAnimationDisposable(self.fig, self.animate_frame,
                                     init_func = self.init_func,
                                     interval = 1, frames = self.num_frames,
                                     repeat = False, blit = True)

        plt.show()

    def animate_frame(self, framenum):
        data = get_data()
        self.p_line.set_data(data[0], data[1])

        if framenum == self.num_frames - 1:
            raise StopIteration  # instead of plt.close()
            
        return self.p_line,

    def init_func(self):
        self.p_line.set_data([], [])
        return self.p_line,

Schrodinger_Solver()
# Schrodinger_Solver()

print(multiplier)