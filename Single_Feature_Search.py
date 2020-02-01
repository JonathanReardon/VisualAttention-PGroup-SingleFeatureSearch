#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Title     :Single_Feature_Search.py
    Author    :Jonathan Reardon
    Email     :jonathanjreardon@gmail.com
'''

import os
import glob
import csv
import random
from psychopy import visual, core, gui, event, sound
from psychopy.data import getDateStr
from psychopy.data import getDateStr
from psychopy import core, visual
from psychopy.iohub.client import launchHubServer
# import own functions/classes
from imports import *

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

# Open a writeable data file
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["Eyes 1=good", "SIM (1=yes, 0=no", "PGROUP 1=yes, 0=no", "ATTEND 1/3", "Target Pres", 
                 "START TIME", "KEYTIME", "RT", "TARGET NAME", "TARGET POSITION", "TARGET ONSET TIME", 
                 "STIM1 NAME", "STIM 1 ONSET", "STIM2 NAME", "STIM2 ONSET", "STIM3 NAME", "STIM3 ONSET", 
                 "STIM4 NAME", "STIM4 ONSET", "STIM5 NAME", "STIM5 ONSET"])

# Initialize window
win = visual.Window([800,600],color=(-1,-1,-1),colorSpace='rgb', allowGUI=True, 
                    monitor='testMonitor', units='deg', fullscr=True)

         
refresh_rate()

# set upper right quadrant grid positions 
grid1 = (2.82, 2.82) 
grid2 = (4.75185165258, 3.337638090205)
grid3 = (3.337638090205, 4.75185165258)
grid4 = (6.68370330516, 3.8552761804099998)
grid5 = (3.8552761804099998, 6.68370330516)

# make (simultanaeous) triangle wedge
triangle = visual.ShapeStim(win, units = 'deg', vertices = ((grid1),(grid3),(grid2)) , lineColor='black', fillColor='black')
        
create_wedges()  
FixW =  Fix_white()
FixG =  Fix_green()
make_stims()
make_target_prompts()
            
###################################################################################################################################
#################################################### MAIN ROUTINE #################################################################
###################################################################################################################################

trial_amount=60

def do_trials():
    
    jitter()

    for i in range(trial_amount):

        select_stims(targ[0], attention)
        display_stims(simult, pgr)
        
        targ.pop(0)
        jitter_list.pop(0)
        
def block1():
    global targ, attention, simult, pgr
    
    running = 1
    block   = 1

    while running==1:

        trials = [1,2,3,4]
        #random.shuffle(trials)
       
        while block < 5:
            
            if trials[0] == 1:
                
                attend1_wait()
               
                make_stims()
                select_target()
                display_target()
                
                for frame in range(ISI_frames*2):
                    FixW.draw()
                    win.flip()
                for frame in range(ISI_frames*2):
                    FixG.draw()
                    win.flip()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
                random.shuffle(targ)
                attention   = 1
                simult      = 1
                pgr         = 1
        
                do_trials()
                
            display_ISI()
            
            if trials[0] == 2:
                
                attend1_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
                random.shuffle(targ)
                attention   = 1
                simult      = 1
                pgr         = 0
                
                do_trials()
                
            display_ISI()
            
            if trials[0] == 3:
                
                attend1_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
                random.shuffle(targ)
                attention   = 1 
                simult      = 0
                pgr         = 1
                
                do_trials()
                
            if trials[0] == 4:
                
                attend1_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
                random.shuffle(targ)
                attention   = 1
                simult      = 0
                pgr         = 0
                
                do_trials()
                
            trials.pop(0)

            block += 1
            
        running = 0
        
def block3():
    global targ, attention, simult, pgr
    
    running = 1
    block   = 1

    while running==1:

        trials = [1,2,3,4]
        random.shuffle(trials)
       
        while block < 5:
            
            if trials[0] == 1:
                
                attend3_wait()
               
                make_stims()
                select_target()
                display_target()
                
                for frame in range(ISI_frames*2):
                    FixW.draw()
                    win.flip()
                for frame in range(ISI_frames*2):
                    FixG.draw()
                    win.flip()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
                random.shuffle(targ)
                attention   = 3
                simult      = 1
                pgr         = 1
        
                do_trials()
                
            display_ISI()
            
            if trials[0] == 2:
                
                attend3_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
                random.shuffle(targ)
                attention   = 3
                simult      = 1
                pgr         = 0
                
                do_trials()
                
            display_ISI()
            
            if trials[0] == 3:
                
                attend3_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
                random.shuffle(targ)
                attention   = 3 
                simult      = 0
                pgr         = 1
                
                do_trials()
                
            if trials[0] == 4:
                
                attend3_wait()
                
                make_stims()
                select_target()
                display_target()

                targ        = [1,1,1,1,1,1,1,1,1,1,1,1,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
                               
                random.shuffle(targ)
                attention   = 3
                simult      = 0
                pgr         = 0
                
                do_trials()
                
            trials.pop(0)

            block += 1

        running = 0
    
block1()

thank_you()
    
dataFile.close()
tracker.setConnectionState(False)
io.quit()
core.quit()
win.close()
