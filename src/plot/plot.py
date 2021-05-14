import matplotlib.pyplot as plt

plt.ion()


class PricePlot:
    # Suppose we know the x range
    min_x = 0
    max_x = 10
    xdata = []
    ydata = []

    def __init__(self):
        # Set up plot
        self.figure, self.ax = plt.subplots()
        (self.lines,) = self.ax.plot([], [], "b-")
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        # Other stuff
        self.ax.grid()

    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        # Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def add_point(self, val):
        self.xdata.append(len(self.xdata))
        self.ydata.append(val)
        self.on_running(self.xdata, self.ydata)
        return self.xdata, self.ydata
