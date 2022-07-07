# -*- coding: utf-8 -*-
"""An example: code for assessing video/audio/MEG synchronization.
    
    This script takes a triplet (fiff, audio, and video) of files and generates
    a bunch of pictures. Each picture describes a short piece of the
    recordings. The upper pane shows 3 consecutive video frames. The lower pane
    shows the corresponding pieces of audio and a single MEG channel. The black
    vertical lines mark the frame locations.
    
    ---------------------------------------------------------------------------
    Author: Andrey Zhdanov
    Copyright (C) 2014 BioMag Laboratory, Helsinki University Central Hospital

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import PIL
# from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import mne
from PyVideoMEG import pyvideomeg
from PyVideoMEG.bin import pvm_export_audio, pvm_data_converter

AUDIO_FNAME = '/net/tera2/data/neuro-data/megtms_naming/case_6184/220621/megtms_naming_sub06_run02_order1_setB_raw.audio.dat'
VIDEO_FNAME = '/net/tera2/data/neuro-data/megtms_naming/case_6184/220621/megtms_naming_sub06_run02_order1_setB_raw.video.dat'

MEG_FNAME = '/net/tera2/data/neuro-data/megtms_naming/case_6184/220621/megtms_naming_sub06_run02_order1_setB_raw.fif'
TIMING_CH = 'STI015'
MEG_CH = 'MEG1142'
FRAME_SZ = (640, 480)
OUT_FLDR = '/tmp'
WIND_WIDTH = 3  # in frames

# Percentiles to be used for vertical scaling (to avoid problems caused by
# outlers). Should be a float between 0 and 100
SCALE_PRCTILE_AUDIO = 99.99
SCALE_PRCTILE_MEG = 99.99
#--------------------------------------------------------------------------
# Load the data
#
raw = mne.io.Raw(MEG_FNAME, allow_maxshield=True)

# load the timing channel
picks_timing = mne.pick_types(raw.info, meg=False, include=[TIMING_CH])
dt_timing = raw[picks_timing,:][0].squeeze()

# load the MEG channel
picks_meg = mne.pick_types(raw.info, meg=False, include=[MEG_CH])
meg = raw[picks_meg,:][0].squeeze()

# compute the timestamps for the MEG channel
meg_ts = pyvideomeg.comp_tstamps(dt_timing, raw.info['sfreq'])

vid_file = pyvideomeg.VideoData(VIDEO_FNAME)
aud_file = pyvideomeg.AudioData(AUDIO_FNAME)

audio, audio_ts = aud_file.format_audio()
audio = audio[0,:].squeeze()    # use only the first audio channel

dot_aud_file = '/net/tera2/data/neuro-data/megtms_naming/case_6184/220621/megtms_naming_sub06_run02_order1_setB.aud'
pvm_data_converter.function(AUDIO_FNAME)
pvm_export_audio.export(dot_aud_file)
