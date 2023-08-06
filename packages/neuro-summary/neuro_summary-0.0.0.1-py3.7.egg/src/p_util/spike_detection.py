from neurodsp.filt.filter import filter_signal
import copy
import scipy.signal as signal
import numpy as np
def bin_sum(binned_channels):
    '''
    Sum spikes across bins to get the population spiking vectors
    '''
    print('Summing the bins across channels...')
    summed_bins=[]
    #Equalize lengths of channel bins
    greatest_length=len(max(binned_channels, key=len))
    equal_channels=[]
    for channel in binned_channels:
        channel_difference=greatest_length-len(channel)
        equal_channels.append(np.append(channel, np.zeros(channel_difference).tolist()))
    #Sum up the bins
    for tbin in np.transpose(equal_channels):
        summed_bins.append(sum(tbin))
    return summed_bins
def bin_channels(channels, bin_length):
    '''
    Computes the bin function on a 64 channel electrode array
    '''
    print('Binning spikes in to %s size bins for each channel...' % bin_length)
    bins=[] #bins each channel separately in the format of: channels[], bins{}, sums
    for channel in channels:
        bins.append(bin_channel(channel, bin_length))
    return bins
def bin_channel(spikes, bin_length):
    '''
    Put spike timings into bins
    '''
    bins=np.zeros(1).tolist()
    if len(spikes)>0:
        bin_ceil=np.ceil(spikes[-1]/bin_length)*bin_length
        number_bins=int(bin_ceil/bin_length)+1
        bins=np.zeros(number_bins).tolist()
        for spike in spikes:
            spikes_bin=int(np.ceil(spike/bin_length))
            bins[spikes_bin] += 1
    return bins
def wave_average(channels):
    '''
    Averages each channels average wave.
    '''
    print('Getting the average waveform across channels...')
    average_wave=[]
    for channel in channels:
        average_wave.append(wave_averages(channel))
    average_wave=[x for x in average_wave if len(x)>0]
    return wave_averages(average_wave)
def wave_averages(waves_channel):
    '''
    It takes in the product of one channel from the function collect_spikes() and produce a single average spike waveform
    '''
    average_wave=[]
    for twave in np.transpose(waves_channel):
        average_wave.append(np.mean(twave))
    return average_wave

def collect_spikes(data, location, window_length):
    '''
    data: is the time series data organized in channels, amplitudes. 
    location: is the spike time locations, organized in a 2d array of channels, locations.
    window_length: A tuple of how much on each side of the spike to collect. Both values are positive. 0 index being how much on the left the spike
    '''
    channels=[]
    for ichannel, channel in  enumerate(location):
        waveforms=[]
        for ispike, spike in enumerate(channel):
            try:
                waveforms.append(np.transpose(data[ichannel][(spike-window_length[0]):(spike+window_length[1])]))
            except:
                print('Spike window: %d outside data range' % spike)
        channels.append(waveforms)
    return channels 

def detect_spikes(data, fs, standard_threshold=5):
    '''
    '''
    print('Detecting spikes...')
    
    minimum_peak_distance=np.ceil(.002*fs)
    number_channels=len(data)
    spikes=[None]*number_channels

    for channel in range(0, number_channels):
        threshold=np.median(np.abs(data[channel])/.6745)*standard_threshold
        max_value = np.amax(np.abs(data[channel]))
        if max_value > threshold:
            spikes[channel], properties = signal.find_peaks(np.abs(data[channel]), distance=minimum_peak_distance, threshold=threshold)
            print('Channel %s spikes:\t%s'%(channel, spikes[channel]))
        else:
            spikes[channel]=np.array([])
            print('No spikes on channel: %d' % channel)
    return spikes
