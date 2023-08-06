import os, re, glob, pyopenephys
from scipy.signal import resample_poly
from neurodsp.filt import filter_signal
import numpy as np
from fractions import gcd

def reference_channels(data, average='mean'):
    '''
    Subtract each channels average from itself element wise.
    '''
    print('Re-referencing channels to the mean...')
    referenced_channels=[]
    for signal in data:
        referenced_channels.append(reference_channel(signal))
    return referenced_channels
def reference_channel(data, average='mean'):
    '''
    Subtract the average from each value in the channel.
    '''
    if average=='mean':
        return np.array(data)-np.mean(data)
    if average=='median':
        return np.array(data)-np.median(data)
    else:
        print('something is going wrong')  
def filter_channels(data, fs, spike_filter=(300, 3000), mea_filter=1000):
    '''
    Filter all channels. Returns two filtered signals, one for spikes, the other is down sampled and low-pass filtered.
    '''
    print('Filtering and down sampling signal...')
    spike_lfp=[]
    mea_lfp=[]
    for channel in data:
        spike_lfp.append(filter_signal(channel, fs, 'bandpass', spike_filter, remove_edges=False))
        mea_lfp.append(resample_channel(channel, fs))
    return mea_lfp, spike_lfp

def resample_channel(channel, fs, mea_filter=1000):
    '''
    Resample lfp, first by upsampling then, downsampling. This is done to handle fractional down sample factors.
    '''
    up_sample_frequency=(mea_filter*fs)//gcd(mea_filter, fs)
    up_sample_factor=up_sample_frequency/fs
    down_sample_factor=up_sample_frequency/mea_filter
        
    return resample_poly(channel, up_sample_factor,  down_sample_factor)
    
def getSignals(dataLocation):
    '''
    From file location return data in a neater package.
    '''
    file = pyopenephys.File(dataLocation) 
    experiments=file.experiments
    experiment=experiments[0]
    recordings=experiment.recordings
    recording=recordings[0]
    channels=recording.analog_signals[0].signal
    fs=int(recording.sample_rate)
    data={'fs':fs,'channels':channels}
    return data
