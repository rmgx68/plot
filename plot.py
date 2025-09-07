"""
    Simple X-Y chart, with up to 3 Y values for each X. All Y values share
    the same scale
    Based on guizero's Drawing widget, this is a hack to have simple
    line charts, as mathplotlib and guizero do not integrate.

    Author: rmgx68
    Public Domain

    THIS CODE HAS ABSOLUTELY *NO GUARANTEE*.
    Do whaterver you want with it.
    Its only a pet-project I enjoyed doing to learn a bit about guizero and python.
    And yeah, I know it can be optimized, I just don't care.

    All constructor parameters are mandatory
    Plot( master, width, height, x_axis_label, y_axis_label, xmin, xmax, ymin,
          ymax, xscale, yscale, data_labels )
          master       : guizero master widget
          width        : total width in pixels of chart + margins
          height       : total height in pixels of chart + margins
          x_axis_label : label on X axis
          y_axis_label : label on Y axis
          xmin, xmax   : lower and upper limit of x axis
          ymin, ymax   : lower and upper limit of y axis
          xscale       : pre-scale of data, x axis
          yscale       : pre-scale of data, y axis
          data_labels  : list of labels for y data

    add_data(t)
        Add data points. Parameter is a tuple, where first value is X, all
        other are 1 to 3 Y values
        This is the recommended call for adding new points, as the drawing is
        incremental

    set_data(l)
        Set data points. Recommended for display static charts

    clear()
        Reset all data, clear chart

    redraw()
        Force redraw of complete chart

    configure()
        Redefine scales and grid to match configured data limits
"""

from guizero import Drawing


class Plot:
    def __init__(self, master, width, height, xlbl, ylbl, xmin, xmax, ymin,
                 ymax, xs, ys, ydatalbls):
        self.fig = Drawing(master, width, height)
        self.fig.when_clicked = self.clicked
        self.fig.when_mouse_dragged = self.clicked
        self.width = width
        self.height = height
        self.margin = 30
        self.xlabel = xlbl
        self.ylabel = ylbl
        self.ydatalabels = ydatalbls
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.oxmin = xmin
        self.oxmax = xmax
        self.oymin = ymin
        self.oymax = ymax
        self.xscale = xs
        self.yscale = ys
        self.colors = ["black", "green", "red", "blue"]
        self.inspect = []
        self.clear()
        self.fig.show()

    def xtransf(self, v):
        return int((self.width-2*self.margin)*(v-self.xmin)/(self.xmax-self.xmin)+self.margin)

    def ytransf(self, v):
        return int(self.height-(self.height-2*self.margin)*(v-self.ymin)/(self.ymax-self.ymin)-self.margin)

    def clear(self):
        self.fig.clear()
        self.data = []
        self.inspect = []
        self.last_data = None
        self.xmin = self.oxmin
        self.xmax = self.oxmax
        self.ymin = self.oymin
        self.ymax = self.oymax
        self.configure()

    def configure(self):
        # X axis
        self.fig.clear()
        self.fig.line(self.margin, self.height-self.margin,
                      self.width-self.margin, self.height-self.margin,
                      width=2)
        self.fig.text(3*self.width/4, self.height-20, self.xlabel)
        # Y axis
        self.fig.line(self.margin, self.margin,
                      self.margin, self.height-self.margin, width=2)
        self.fig.text(0, 0, self.ylabel)

        # vertical grid lines
        stepx = ( self.xmax - self.xmin ) / 10
        self.fig.text(self.xtransf(self.xmin)-3, self.height-self.margin+3,
                      "%.1f"%self.xmin, size=7,
                      color="blue", font="Courier")
        t = self.xmin+stepx
        while t < self.xmax+stepx:
            x = self.xtransf(t)
            self.fig.line(x, self.margin, x, self.height-self.margin, 
                          color="grey70")
            self.fig.text(x-3, self.height-self.margin+3, "%.1f"%t, size=7,
                          color="blue", font="Courier")
            t += stepx

        # horizontal grid lines
        stepy = ( self.ymax - self.ymin ) / 10
        self.fig.text(0, self.ytransf(self.ymin)-3, 
                      '{:>5}'.format("%.1f"%self.ymin), size=7, 
                      color="blue", font="Courier")
        t = self.ymin+stepy
        while t < self.ymax+stepy:
            y = self.ytransf(t)
            self.fig.line(self.margin, y, self.width-self.margin, y,
                          color="grey70")
            self.fig.text(0, y-3, '{:>5}'.format("%.1f"%t), size=7, 
                          color="blue", font="Courier")
            t += stepy

        # data labels
        i = 0
        while i < len(self.ydatalabels):
            self.fig.text(self.width-100, 4+i*8, self.ydatalabels[i],
                          size=7, color=self.colors[i+1], font="Courier")
            i += 1

    def add_data(self, t):
        self.data.append(t)
        need_config = False
        if t[0]*self.xscale > self.xmax:
            self.xmax += self.xmax-self.xmin
            need_config = True
        elif t[0]*self.xscale < self.xmin:
            self.xmin -= self.xmax-self.xmin
            need_config = True
        for i in range(1, len(t)):
            if t[i]*self.yscale > self.ymax:
                self.ymax += self.ymax-self.ymin
                need_config = True
            elif t[i]*self.yscale < self.ymin:
                self.ymin -= self.ymax-self.ymin
                need_config = True
        if need_config: 
            self.configure()
            self.redraw()
            return
        if self.last_data != None:
            for i in range(1, len(t)):
                self.fig.line(self.xtransf(self.last_data[0]*self.xscale),
                              self.ytransf(self.last_data[i]*self.yscale),
                              self.xtransf(t[0]*self.xscale), 
                              self.ytransf(t[i]*self.yscale), 
                              color=self.colors[i])
        self.last_data = t

    def set_data(self, data):
        self.xmin = self.oxmin
        self.xmax = self.oxmax
        self.ymin = self.oymin
        self.ymax = self.oymax
        self.data = data
        for k in range(len(data)):
            if data[k][0]*self.xscale > self.xmax:
                self.xmax += self.xmax - self.xmin
            elif data[k][0]*self.xscale < self.xmin:
                self.xmin -= self.xmax - self.xmin
            for i in range(1, len(data[k])):
                if data[k][i]*self.yscale > self.ymax:
                    self.ymax += self.ymax-self.ymin
                elif data[k][i]*self.yscale < self.ymin:
                    self.ymin -= self.ymax-self.ymin
        self.last_data = data[len(data)-1]
        self.configure()
        self.redraw()

    def redraw(self):
        if not self.data: return
        for i in range(1, len(self.data[0])):
            for t in range(1, len(self.data)):
                self.fig.line(self.xtransf(self.data[t-1][0]*self.xscale),
                              self.ytransf(self.data[t-1][i]*self.yscale),
                              self.xtransf(self.data[t][0]*self.xscale), 
                              self.ytransf(self.data[t][i]*self.yscale),
                              color=self.colors[i])

    def clicked(self, evdata):
        # compute x value
        x = (evdata.x - self.margin) * (self.xmax - self.xmin) / (self.width - 2*self.margin)
        if x < self.xmin: x = self.xmin
        if x > self.xmax: x = self.xmax
        for i in range(len(self.inspect)): 
            self.fig.delete(self.inspect[i])
        self.inspect = []

        # search nearest x on self.data
        for i in range(1, len(self.data)):
            if self.data[i][0]*self.xscale > x:
                self.inspect.append(self.fig.line(
                              self.xtransf(self.data[i-1][0]*self.xscale),
                              self.margin,
                              self.xtransf(self.data[i-1][0]*self.xscale), 
                              self.height-self.margin,
                              color="yellow"))
                self.inspect.append(self.fig.text(self.margin, self.height-16,
                        "%.1f"%(self.data[i-1][0]*self.xscale), 
                        size=8, color=self.colors[0], font="Courier"))
                j = 0
                while j < len(self.ydatalabels):
                    self.inspect.append(self.fig.text(self.margin+60+60*j, 
                            self.height-16, 
                            "%.1f"%(self.data[i-1][j+1]*self.yscale), 
                            size=8, color=self.colors[j+1], font="Courier"))
                    j += 1
                return

        # clicked on the right, out of data
        i = len(self.data)
        self.inspect.append(self.fig.line(
                      self.xtransf(self.data[i-1][0]*self.xscale),
                      self.margin,
                      self.xtransf(self.data[i-1][0]*self.xscale), 
                      self.height-self.margin,
                      color="yellow"))
        self.inspect.append(self.fig.text(self.margin, self.height-16,
                "%.1f"%(self.data[i-1][0]*self.xscale), 
                size=8, color=self.colors[0], font="Courier"))
        j = 0
        while j < len(self.ydatalabels):
            self.inspect.append(self.fig.text(self.margin+60+60*j, 
                    self.height-16, 
                    "%.1f"%(self.data[i-1][j+1]*self.yscale), 
                    size=8, color=self.colors[j+1], font="Courier"))
            j += 1
