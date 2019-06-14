# Import necessary variables
from psychopy import visual, core, gui, event, sound
from psychopy.data import getDateStr
import os
import glob
import csv
import random
from psychopy.data import getDateStr
from psychopy import core, visual
from psychopy.iohub.client import launchHubServer

########################### IOHUB settings ###########################

# Start ioHub event monitoring process, using the eyelink eyetracker
# Note: No iohub config .yaml files are needed here
# Since no experiment or session code is given, no iohub hdf5 file
# will be saved, but device events are still available at runtime.
runtime_settings = dict()
runtime_settings['sampling_rate'] = 500
runtime_settings['track_eyes'] = 'RIGHT'
iohub_config = {'eyetracker.hw.sr_research.eyelink.EyeTracker':
                {'name': 'tracker',
                 #'simulation_mode': True,
                 'model_name': 'EYELINK 1000 DESKTOP',
                 'runtime_settings': runtime_settings
                 },
                }
# Uncomment experiment_code setting to enable saving data to hdf5 file.
#iohub_config['experiment_code'] = 'et_simple'

io = launchHubServer(**iohub_config)

# Get some iohub devices for future access.
keyboard = io.devices.keyboard
display = io.devices.display
tracker = io.devices.tracker

# run eyetracker calibration
r = tracker.runSetupProcedure()

# Initialize window
win = visual.Window([800,600],color=(-1,-1,-1),colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=True)

# Create a circle stim centered in middle of screen, with radius of 200 px.
# Change the radius to whatever suits you...
gaze_ok_region = visual.Circle(win, radius=250, units='pix')

def check_eyes():
    global eyes, gaze_ok_region, block
    gpos = tracker.getLastGazePosition()
    if  not isinstance(gpos, (tuple, list)):
        pass
    elif  gaze_ok_region.contains(gpos):
        pass
    else:
        eyes = 0
        print "eyes outside area"
        block2.draw()
        win.flip()

# Make the eye-blocker square
block1 = visual.ShapeStim(win, units = 'deg', vertices = ((-10,-8),(-10,8),(10,8),(10,-8)), lineColor='red', fillColor='red')
block2 = visual.ShapeStim(win, units = 'deg', vertices = ((-10,-8),(-10,8),(10,8),(10,-8)), lineColor='red', fillColor='white')

refresh_rate = 60.0
target_dur =  10

target_frames = target_dur * refresh_rate
target_frames = int(target_frames)

eyes = 1

io.clearEvents()
tracker.setRecordingState(True)

for frame in range(target_frames):
    block1.draw()
    
    check_eyes()
    
    win.flip()
    
print("eyes :", eyes)
    
tracker.setConnectionState(False)
io.quit()
    
core.quit()
win.close()

