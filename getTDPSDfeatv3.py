"""
% get Khushaba's time-domain power spectrum descriptors (TD-PSD).
%
% feat = getTDPSDfeat(x,winsize,wininc,datawin,dispstatus)
%
% Author Rami Khushaba 
%
% This function computes the time-domain spectral moments feature of the signals in x,
% x is made of columns, each representing a channel/sensor. 
% For example if you get 5 sec of data from 8 channels/sensors at 1000 Hz 
% then x should be 5000 x 8. A windowing scheme is used here to extract features 
%
% The signals in x are divided into multiple windows of size
% winsize and the windows are spaced wininc apart.
%
%
% Inputs
%    x: 		columns of signals
%    winsize:	window size (length of x)
%    wininc:	spacing of the windows (winsize)
%    datawin:   window for data (e.g. Hamming, default rectangular)
%               must have dimensions of (winsize,1)
%    dispstatus:zero for no waitbar (default)
%
% Outputs
%    feat:     Spectral momements (6 features per channel)
%              dim1 window
%              dim2 feature
%
% Modifications
% 23/06/2004   AC: template created http://www.sce.carleton.ca/faculty/chan/index.php?page=matlab
% 17/11/2013   RK: Spectral moments first created.
% 01/03/2014   AT: Rami Sent me this on 1-3-14 to go with normalised KSM_V1

% References
% [1] A. Al-Timemy, R. N. Khushaba, G. Bugmann, and J. Escudero, "Improving the Performance Against Force Variation of EMG Controlled Multifunctional Upper-Limb Prostheses for Transradial Amputees", 
%     IEEE Transactions on Neural Systems and Rehabilitation Engineering, DOI: 10.1109/TNSRE.2015.2445634, 2015.
% [2] R. N. Khushaba, Maen Takruri, Jaime Valls Miro, and Sarath Kodagoda, "Towards limb position invariant myoelectric pattern recognition using time-dependent spectral features", 
%     Neural Networks, vol. 55, pp. 42-58, 2014. 

"""

import numpy as np

def getTDPSDfeatv3(x,*slidingParams):
    
    # x should be a numpy array
    x = np.array(x)
    
    # Make sure you have the correct number of parameters passed
    if len(slidingParams) <2:
        raise TypeError('getTDPSDfeat expected winsize and wininc to be passed, got %d parameters instead' %len(slidingParams))
    if slidingParams:
        winsize = slidingParams[0]
        wininc = slidingParams[1]
        
    datasize = x.shape[0];
    Nsignals = x.shape[1];
    numwin = np.int(np.floor((datasize - winsize)/wininc)+1)
    NFPC = 6
    
    # allocate memory
    feat = np.zeros((numwin,Nsignals*NFPC))
    
    st = 0
    en = winsize  
    
    for i in range(numwin):
        # define your current window
        curwin = x[st:en,:]
        
        # Step1: Extract features from original signal and a nonlinear version of it
        ebp=KSM1(curwin)
        efp=KSM1(np.log(curwin**2+np.spacing(1)))
        
        # Step2: Correlation analysis
        num = -2 * np.multiply(efp,ebp)
        den = np.multiply(efp,efp) + np.multiply(ebp,ebp)
        
        # feature extraction goes here
        feat[i,:] = num-den
        st = st + wininc
        en = en + wininc
        
    return feat

def  KSM1(S):
    """
    % Time-domain power spectral moments (TD-PSD)
    % Using Fourier relations between time domina and frequency domain to
    % extract power spectral moments dircetly from time domain.
    %
    % Modifications
    % 17/11/2013  RK: Spectral moments first created.
    % 02/03/2014  AT: I added 1 to the function name to differentiate it from other versions from Rami
    % 
    % References
    % [1] A. Al-Timemy, R. N. Khushaba, G. Bugmann, and J. Escudero, "Improving the Performance Against Force Variation of EMG Controlled Multifunctional Upper-Limb Prostheses for Transradial Amputees", 
    %     IEEE Transactions on Neural Systems and Rehabilitation Engineering, DOI: 10.1109/TNSRE.2015.2445634, 2015.
    % [2] R. N. Khushaba, Maen Takruri, Jaime Valls Miro, and Sarath Kodagoda, "Towards limb position invariant myoelectric pattern recognition using time-dependent spectral features", 
    %     Neural Networks, vol. 55, pp. 42-58, 2014. 
    """
    
    # Get the size of the input signal
    samples,channels = S.shape
    
    if channels>samples:
        S  = np.transpose(S);
        samples,channels = S.shape
    
    # Root squared zero order moment normalized
    m0     = np.sqrt(np.sum(S**2,axis=0))[:,np.newaxis]
    m0     = m0**.1 / .1;
    
    # Prepare derivatives for higher order moments
    d1     = np.diff(S,n=1,axis=0)
    d2     = np.diff(d1,n=1,axis=0)
    
    # Root squared 2nd and 4th order moments normalized
    m2     = np.sqrt(np.sum(d1**2,axis=0)/(samples-1))[:,np.newaxis]
    m2     = m2**.1/.1
    
    m4     = np.sqrt(np.sum(d2**2,axis=0)/(samples-1))[:,np.newaxis]
    m4     = m4**.1/.1;
    
    # Sparseness
    sparsi = m0/np.sqrt(np.abs((m0-m2)*(m0-m4)))
    
    # Irregularity Factor
    IRF    = m2/np.sqrt(np.multiply(m0,m4))
    
    # Waveform length ratio
    WLR    = np.sum(np.abs(d1),axis=0)-np.sum(np.abs(d2),axis=0)
    WLR = WLR[:,np.newaxis]
    # All features together
    Feat   = np.concatenate((m0, m0-m2, m0-m4,sparsi, IRF, WLR), axis=0)
    Feat   = np.log(np.abs(Feat)).flatten()
    
    return Feat

