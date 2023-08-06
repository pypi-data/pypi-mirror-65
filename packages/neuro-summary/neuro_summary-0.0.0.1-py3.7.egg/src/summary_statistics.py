#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys, os, scipy.io, pickle, h5py, argparse
from p_util.old_util import getSignals
import constants
import p_util.preprocessing as pre
import p_util.spike_detection as sd
from statsmodels.tsa.stattools import acf
from neurodsp.spectral.power import compute_spectrum_welch as welch
from neurodsp.plts.spectral import plot_power_spectra as plot_psd
from neurodsp.plts.time_series import plot_time_series as plot_ts

def run_summary():
    '''
    Takes in a data set as a commandline argument, it expects a two-dimensional array of [channels x signals]
    '''
    parser = argparse.ArgumentParser(description='Create a plot of summary statistics.')
    parser.add_argument('file', metavar='F',
                                help='Navigate to, and name data set to run')
    args = parser.parse_args()
    myFile=args.file
    myDir=os.path.dirname(os.path.abspath(__file__))

    data = None
    fs=12500
    if os.path.isdir(myFile):
        try:
            fs, data = getSignals(myFile)
        except e:
            print('Please input a valid filetype. Inputs must be either .mat or a OE binary folder structure.')
            sys.exit()
    else:
        fileExtension=myFile.split()[1]
        mat=h5py.File(myFile, 'r')
        data=mat['MEA']
    mea=data

    #Sample Rate Of Down Sampled signal.
    ds_fs=1000

    #Re- reference the timeseries.
    re_ts=pre.reference_channels(mea)

    #Create a high passed, and low passed(downsampled) signal.
    lp_ds_ts, hp_ts = pre.filter_channels(re_ts, fs, mea_filter=ds_fs)


    #Make down sampled/low-pass filtered time array.
    lp_ds_t=np.arange(len(lp_ds_ts[0]))/ds_fs

    #Make high-pass filter time array.
    hp_t=np.arange(len(hp_ts[0]))/fs

    plt.tight_layout()
    fig = plt.figure(figsize=[12, 12])
    gs = gridspec.GridSpec(4, 2, figure=fig)
    labelSize=18
    titleSize=20

    #from constants import *
    spike_threshold=constants.spike_threshold #Scaler threshold for what is considered a spike based on standard deviation
    bin_length=int(fs/1000) #Convention to do one millisecond
    nperseg=int(ds_fs) #Segment length of psd welch function
    noverlap=int(nperseg/2) #Overlap of psd welch function
    spike_nperseg=int(fs) #Segment length of psd welch function
    spike_noverlap=int(spike_nperseg/2) #Overlap of psd welch function
    wave_size=constants.wave_size #Constrain wave plots
    acf_lags=constants.acf_lags #Used to constrain the population spiking vector autocorr lags

    '''
    Plot lowpassed filtered time series
    '''
    mpl.rcParams['lines.linewidth'] = .1
    ax = fig.add_subplot(gs[0, 1])
    plot_factor=int(len(lp_ds_ts)/9)
    for i, channel in enumerate(lp_ds_ts):
        if i % plot_factor:
            ax.plot(lp_ds_t, channel)
    ax.set_title('Lowpass Filtered Time Series', fontsize=titleSize)
    ax.set_ylabel('Voltage (uV)', fontsize=labelSize)
    ax.set_xlabel('Time (s)', fontsize=labelSize)
    mpl.rcParams['lines.linewidth'] = 1

    '''
    Get and plot power spectral distribution
    '''
    mpl.rcParams['lines.linewidth'] = .1
    ax = fig.add_subplot(gs[1, 0])
    power_list=[]
    freq_list=[]

    for channel in lp_ds_ts:
        ch_freq, ch_power=welch(np.array(channel), ds_fs, nperseg=nperseg, noverlap=noverlap)

        #Saving powers and frequencies for averaging.
        power_list.append(ch_power)
        freq_list.append(freq_list)

        plot_psd(ch_freq, ch_power, ax=ax)

    mpl.rcParams['lines.linewidth'] = .8
    #average_psd=np.array([np.mean(x) for x in np.array(power_list).T]).T
    #average_psd=np.mean(power_list, axis=0)
    #plot_psd(freq_list[0], average_psd, ax=ax)

    ax.set_title('PSD', fontsize=titleSize)
    mpl.rcParams['lines.linewidth'] = 1

    '''
    Get spikes from high passed timeseries
    '''
    spikes=sd.detect_spikes(hp_ts, fs, standard_threshold=spike_threshold)
    '''
    If no spikes, do not pursue spike analysis.
    '''
    if len(np.concatenate(spikes).ravel())>0:
        '''
        Plot spike raster.
        '''
        ax = fig.add_subplot(gs[1, 1])
        new_spikes=[]
        for spike in spikes:
            new_spikes.append(np.array(spike)/fs)
        ax.eventplot(new_spikes)
        ax.set_title('Spike Raster', fontsize=titleSize)
        ax.set_ylabel('Channel number', fontsize=labelSize)
        ax.set_xlabel('Time (s)', fontsize=labelSize)

        '''
        Get spike waveforms
        '''
        t_ms=fs*1000
        waveforms=sd.collect_spikes(hp_ts, spikes, wave_size)
        ax = fig.add_subplot(gs[2, 0])
        for channel in waveforms:
            for waveform in channel:
                wave_t_ms=np.arange(len(waveform))/t_ms
                ax.plot(wave_t_ms, waveform, linewidth=.1)

        wave_average=sd.wave_average(waveforms)
        wave_t_ms=np.arange(len(wave_average))/t_ms

        ax.plot(wave_t_ms, wave_average, linewidth=2, color='red')
        ax.set_title('Spike Waveforms', fontsize=titleSize)
        ax.set_ylabel('Amplitude', fontsize=labelSize)
        ax.set_xlabel('Time (ms)', fontsize=labelSize)

        '''
        Get population spiking vector from channels with binned spikes
        '''
        bins=sd.bin_channels(np.array(spikes), bin_length)
        psv=sd.bin_sum(bins)
        ax = fig.add_subplot(gs[2, 1])
        ax.bar((np.arange(len(psv))*(bin_length/fs)), psv)
        ax.set_title('Population Spiking Vector (PSV)', fontsize=titleSize)
        ax.set_ylabel('Bins', fontsize=labelSize)
        ax.set_xlabel('Time (s)', fontsize=labelSize)

        '''
        Get autocorrelation for the population spiking vector
        '''
        psv_length=len(psv)
        y_auto=acf_sm = acf(psv, nlags=acf_lags, fft=True)
        x_auto=np.arange(len(y_auto))

        ax = fig.add_subplot(gs[3, 0])
        ax.plot(np.array(x_auto)*(bin_length/fs), (np.array(y_auto)/max(y_auto)))
        ax.set_title('Autocorrelation of PSV', fontsize=titleSize)
        ax.set_ylabel('Autocorrelation', fontsize=labelSize)
        ax.set_xlabel('Shifts (s)', fontsize=labelSize)

        '''
        Get the power spectral distribution for the population spiking vector
        '''
        psv_freq, psv_power=welch(np.array(psv), fs/bin_length, nperseg=spike_nperseg, noverlap=spike_noverlap)
        ax = fig.add_subplot(gs[3, 1])
        ax.set_title('PSD of PSV', fontsize=titleSize)
        plot_psd(psv_freq, psv_power, ax=ax)

        print('The summary statistics have finished computing.')
        plt.show()
    else:
        print('There are no spikes, ending analysis early. Please check your spike threshold.')
        plt.show()

def main():
    run_summary()

#if __name__ == '__main__':
#    main()
