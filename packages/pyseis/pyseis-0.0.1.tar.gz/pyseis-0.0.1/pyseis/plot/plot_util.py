#!/usr/bin/env python
"""

Plot Utilities

"""


import os
from obspy import Trace
from ..utils.source import CMTSource

def plot_new_seismogram_sub(Trace: tr, outputdir, figure_format):

    station = tr.stats.station
    network = tr.stats.network
    channel = tr.stats.channel
    location = tr.stats.location
    outputfig = os.path.join(outputdir, "%s.%s.%s.%s.%s" % (
        network, station, location, channel, figure_format))

    # Times and offsets computed individually, since the grid search applies
    # a timeshift which changes the times of the traces.
    if cmtsource is None:
        offset = 0
    else:
        offset = obsd.stats.starttime - cmtsource.cmt_time
        offset_synt = synt.stats.starttime - cmtsource.cmt_time
        offset_new = new_synt.stats.starttime - cmtsource.cmt_time
    times = [offset + obsd.stats.delta * i for i in range(obsd.stats.npts)]
    times_synt = [offset_synt + synt.stats.delta * i
                  for i in range(synt.stats.npts)]
    times_new = [offset_new + new_synt.stats.delta * i
                 for i in range(new_synt.stats.npts)]
    fig = plt.figure(figsize=(15, 5))

    plt.rcParams.update({'font.size': 13,
                         'lines.linewidth': 1.5})

    # plot seismogram
    ax1 = plt.subplot(211)
    ax1.plot(times, obsd.data, color="black", linewidth=0.8, alpha=0.6,
             label="obsd")
    ax1.plot(times_synt, synt.data, color="red", linewidth=1,
             label="synt")
    ax1.plot(times_new, new_synt.data, color="blue", linewidth=1,
             label="new synt")
    ax1.set_xlim(times[0], times[-1])
    ax1.legend(loc='upper right', frameon=False, ncol=3, prop={'size': 11})

    # Setting top left corner text manually
    fontsize = 11
    ax1.text(0.005, 0.8,
             "Network: %2s    Station: %s\n"
             "Location: %2s  Channel: %3s" %
             (network, station, location, channel),
             fontsize=fontsize,
             transform=ax1.transAxes)

    for win in trwin.windows:
        left = win[0] + offset
        right = win[1] + offset
        re = Rectangle((left, plt.ylim()[0]), right - left,
                       plt.ylim()[1] - plt.ylim()[0], color="blue",
                       alpha=0.25)
        plt.gca().add_patch(re)

    # plot envelope
    ax2 = plt.subplot(212)
    ax2.plot(times, _envelope(obsd.data), color="black", linewidth=0.8,
             alpha=0.6, label="obsd")
    ax2.plot(times, _envelope(synt.data), color="red", linewidth=1,
             label="synt")
    ax2.plot(times, _envelope(new_synt.data), color="blue", linewidth=1,
             label="new synt")
    ax2.set_xlim(times[0], times[-1])

    ax2.set_xlabel("Time [s]", fontsize=13)

    for win in trwin.windows:
        left = win[0] + offset
        right = win[1] + offset
        re = Rectangle((left, plt.ylim()[0]), right - left,
                       plt.ylim()[1] - plt.ylim()[0], color="blue",
                       alpha=0.25)
        plt.gca().add_patch(re)

    logger.info("output figname: %s" % outputfig)
    ax2.legend(loc='upper right', frameon=False, ncol=3, prop={'size': 11})
    plt.savefig(outputfig)
    plt.close(fig)


def plot_new_seismogram_sub(Trace: tr, outputdir, figure_format):
    obsd = s

    station = obsd.stats.station
    network = obsd.stats.network
    channel = obsd.stats.channel
    location = obsd.stats.location
    outputfig = os.path.join(outputdir, "%s.%s.%s.%s.%s" % (
        network, station, location, channel, figure_format))

    # Times and offsets computed individually, since the grid search applies
    # a timeshift which changes the times of the traces.
    if cmtsource is None:
        offset = 0
    else:
        offset = obsd.stats.starttime - cmtsource.cmt_time
        offset_synt = synt.stats.starttime - cmtsource.cmt_time
        offset_new = new_synt.stats.starttime - cmtsource.cmt_time
    times = [offset + obsd.stats.delta * i for i in range(obsd.stats.npts)]
    times_synt = [offset_synt + synt.stats.delta * i
                  for i in range(synt.stats.npts)]
    times_new = [offset_new + new_synt.stats.delta * i
                 for i in range(new_synt.stats.npts)]
    fig = plt.figure(figsize=(15, 5))

    plt.rcParams.update({'font.size': 13,
                         'lines.linewidth': 1.5})

    # plot seismogram
    ax1 = plt.subplot(211)
    ax1.plot(times, obsd.data, color="black", linewidth=0.8, alpha=0.6,
             label="obsd")
    ax1.plot(times_synt, synt.data, color="red", linewidth=1,
             label="synt")
    ax1.plot(times_new, new_synt.data, color="blue", linewidth=1,
             label="new synt")
    ax1.set_xlim(times[0], times[-1])
    ax1.legend(loc='upper right', frameon=False, ncol=3, prop={'size': 11})

    # Setting top left corner text manually
    fontsize = 11
    ax1.text(0.005, 0.8,
             "Network: %2s    Station: %s\n"
             "Location: %2s  Channel: %3s" %
             (network, station, location, channel),
             fontsize=fontsize,
             transform=ax1.transAxes)

    # plot envelope
    ax2 = plt.subplot(212)
    ax2.plot(times, _envelope(obsd.data), color="black", linewidth=0.8,
             alpha=0.6, label="obsd")
    ax2.plot(times, _envelope(synt.data), color="red", linewidth=1,
             label="synt")
    ax2.plot(times, _envelope(new_synt.data), color="blue", linewidth=1,
             label="new synt")
    ax2.set_xlim(times[0], times[-1])

    ax2.set_xlabel("Time [s]", fontsize=13)

    for win in trwin.windows:
        left = win[0] + offset
        right = win[1] + offset
        re = Rectangle((left, plt.ylim()[0]), right - left,
                       plt.ylim()[1] - plt.ylim()[0], color="blue",
                       alpha=0.25)
        plt.gca().add_patch(re)

    logger.info("output figname: %s" % outputfig)
    ax2.legend(loc='upper right', frameon=False, ncol=3, prop={'size': 11})
    plt.savefig(outputfig)
    plt.close(fig)