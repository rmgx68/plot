This project is Public Domain.

Author:  rmg68x

It is a simple class that allows the drawing of 2 data series sharing the same X-axis (eg timestamp), by using a DrawingArea from GUIZERO.
These data series are supposed to be have the same scale.

The need of this arises from the lack of integration of matplotlib with guizero.

It has 2 major ways of working:
a) Set the 2 data series at once. The drawing area will show the complete data series, and rescale its axii to show the complete data.
b) Insert data incrementally, 1 instant (X axis) at a time. Whenever the displayed data falls outside the extents of the drawing area, the axii scales are recalculated, and the full data set is displayed. 

There is an inspection function on this class, that shows the values of the data series in response to a click on the drawing area.

This class was initially on a public drive, but it is now on github, as only google was capable to find it :)
