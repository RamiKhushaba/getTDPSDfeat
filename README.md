Improving the Performance Against Force Variation of EMG Controlled Multifunctional Upper-Limb Prostheses for Transradial Amputees
==================================================================================================================================
getTDPSDfeat is a feature extraction algorithm for ***any kind of signals***, although this was mainly developed for myoelectric, a.k.a, Electromyogram (EMG), signal feature extraction for prostheses control. 

The algorithm extracts 6 features from each channel individually, and from the combination of NCC channels to extract few features including:

* 3 time-domain driven spectral moments 
* 1 Sparsiness measure
* 1 Irregularity factor
* 1 Waveform length ratio/difference
 

You will need to specify the window size and window increment. 

![Alt text](TDPSD.png?raw=true "TDPSD")

As this is a matlab function (adding a python version soon), then usage is really simple, just call this function by submitting the signals matrix (denoted as variable x) as input

	feat = getTDPSDfeat(x,winsize,wininc)

## Inputs
	x 		columns of signals (rows are samples and column are the signals).
	winsize 	window size.
	wininc		how much to slide the windows by.
	
## Outputs
	feat	extracted features from all channels/combinations of channels
