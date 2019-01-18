import csv
import datetime
import math
import os
import Tkinter
import tkFileDialog
import matplotlib.dates as daplt
import matplotlib.pyplot as plt
import numpy as np


from os import listdir
from os.path import isfile, join

# ---------------------- Write down the path of your Litchi Logs here -------------------------------
DefaultLogpath = 'C:\\Users\\aanderson29\\Documents\\Mission Planner\\logs\\Litchi'



def openlog():# open the CSV and convert it to a list
    f = open(join(DefaultLogpath, logfiles[filepos]), 'r')
    reader = csv.reader(f)
    flight = list(reader)
    f.close()
    return flight

def displaylog(flight):

    # convert lat/lon to meters
    x = np.array([float(b[1]) for b in flight[1:]])
    y = np.array([float(b[0]) for b in flight[1:]])
    a = np.array([float(b[2]) for b in flight[1:]])
    x = x - x[0]
    x = x * math.cos(y[0] * math.pi / 180)
    x = x / 360 * 40000000
    y = y - y[0]
    y = y / 360 * 40000000

    # convert text time to datetime format
    t = []
    for i in flight[1:]:
        str = i[12]
        str = str.replace('-', ' ')
        str = str.replace(':', ' ')
        str = str.replace('.', ' ')
        dtnums = [int(s) for s in str.split()]
        t.append(daplt.date2num(
            datetime.datetime(dtnums[0], dtnums[1], dtnums[2], dtnums[3], dtnums[4], dtnums[5], dtnums[6] * 1000)))
    np.array(t)

    # get takeoff, landing, and flight times
    hours1 = (t[0] - np.trunc(t[0])) * 24
    minutes1 = (hours1 - np.trunc(hours1)) * 60
    hours2 = (t[-1] - np.trunc(t[-1])) * 24
    minutes2 = (hours2 - np.trunc(hours2)) * 60
    flighttime = t[-1] - t[0]
    hoursf = (flighttime - np.trunc(flighttime)) * 24
    minutesf = (hoursf - np.trunc(hoursf)) * 60
    strlogtimes = "{}:{:0>2d}\t{}:{:0>2d}\t{}:{:0>2d}".format(int(hours1), int(minutes1), int(hours2), int(minutes2),
                                                              int(hoursf), int(minutesf))
    print strlogtimes

    strdistimes = "Takeoff: {}:{:0>2d}     Landing: {}:{:0>2d}     Flight Time: {}:{:0>2d}".format(int(hours1),
                                        int(minutes1), int(hours2), int(minutes2), int(hoursf), int(minutesf))



    # make plot interactive
    global cid
    if cid == 0:
        cid = plt.gcf().canvas.mpl_connect('key_press_event', on_key)
    # plot flight path
    ax = plt.gcf().add_subplot(1, 2, 1)
    plt.xlabel('Flight Path')
    ax.plot(x, y, 'b')

    bx = plt.gcf().add_subplot(1, 2, 2)
    plt.xlabel('Altitude')
    bx.plot_date(t, a, 'b')
    myFmt = daplt.DateFormatter('%H:%M:%S')
    bx.xaxis.set_major_formatter(myFmt)
    bx.xaxis.set_major_locator(plt.MultipleLocator(base=1.0 / 24 / 60))
    #bx.
    plt.xticks(rotation=20)
    titlestring = logfiles[filepos] + '\n' + strdistimes
    plt.gcf().suptitle(titlestring)
    plt.gcf().show()



def on_key(event):
    global filepos
    global logfiles

    if event.key == u'up' and filepos > 0:
        filepos -= 1
        plt.gcf().clf()
        flight = openlog()
        displaylog(flight)
    elif event.key == u'down' and filepos < len(logfiles)-1:
        filepos += 1
        plt.gcf().clf()
        flight = openlog()
        displaylog(flight)
    elif event.key == u'right':
        print '-------------------'
        plt.gcf().clf()
        flight = openlog()
        displaylog(flight)
    elif event.key == u'left':
        print '-------------------'
        plt.gcf().clf()
        flight = openlog()
        displaylog(flight)
    elif event.key == u'escape':
        print 'done'
        exit(0)
    elif event.key == 'q':
        print 'done'
        exit(0)
    return


#======================================== Main Program =============================
print 'Simpple Litchi Log Browser'
print '=========================='
print ''
print 'Use up/down arrows to navigate, left/right arrows to place output marker line'
print 'Press q or Esc to exit'
print 'You might have to click on the display window to activate interactivity'
print ''

try:
    os.chdir(DefaultLogpath)
except:
    DefaultLogpath = 'C:\\'
    os.chdir(DefaultLogpath)

root = Tkinter.Tk()
root.withdraw()
root.filename = tkFileDialog.askopenfilename(initialdir=DefaultLogpath, title="Open Litchi Log CSV", filetypes = (("csv files","*.csv"),("all files","*.*")))
if root.filename == '':
    exit(5)

fullfilename = root.filename.split('/')
filename = fullfilename[-1]  # just the filename
filepath = root.filename.replace(fullfilename[-1], '') # somewhat risky deletion of the filename from the path





cid = 0
fig = plt.figure(1)

# find all logs and list them, newest at the top
logfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
logfiles.sort(reverse=True)
logfiles = [f for f in logfiles if f.split(".")[-1] == 'csv']
filepos = logfiles.index(filename)

flight = openlog()
displaylog(flight)
plt.show()

print 'done'
