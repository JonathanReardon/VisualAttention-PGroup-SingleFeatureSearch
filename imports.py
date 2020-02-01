#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Title     :imports.py
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

# Create a circle stim centered in middle of screen, with radius of 200 px.
GAZE_OK_REGION = visual.Circle(win, radius=900, units='pix', lineColor="white")

# Make the eye-blocker square
BLOCK = visual.ShapeStim(win, units = 'deg', vertices = ((2,2),(8,2),(8,8),(2,8)), lineColor='red', fillColor='red')

# set upper right quadrant grid positions 
GRID1 = (2.82, 2.82) 
GRID2 = (4.75185165258, 3.337638090205)
GRID3 = (3.337638090205, 4.75185165258)
GRID4 = (6.68370330516, 3.8552761804099998)
GRID5 = (3.8552761804099998, 6.68370330516)

# make (simultanaeous) triangle wedge
TRIANGLE = visual.ShapeStim(win, units = 'deg', vertices = ((grid1),(grid3),(grid2)) , lineColor='black', fillColor='black')

# Set stimulus frame durations
def refresh_rate():
    
    global target_frames, stim_frames, grid_frames, ISI_frames, refresh_rate
    
    refresh_rate = 60.0
    target_dur =  .5
    stim_dur   = .25
    grid_dur   = .25
    ISInterval = 1

    target_frames = target_dur * refresh_rate
    target_frames = int(target_frames)

    stim_frames = stim_dur * refresh_rate
    stim_frames = int(stim_frames)

    grid_frames = grid_dur * refresh_rate
    grid_frames = int(grid_frames)
    
    ISI_frames  = ISInterval * refresh_rate
    ISI_frames  = int(ISI_frames)

# Sim presentation jitter
def jitter():
    
    global jitter_list
    
    list1 = .25
    list2 = .5
    list3 = .75
    list4 = 1
    list5 = 1.25

    jitter1 = list1 * refresh_rate
    jitter1 = int(jitter1)

    jitter2 = list2 * refresh_rate
    jitter2 = int(jitter2)

    jitter3 = list3 * refresh_rate
    jitter3 = int(jitter3)

    jitter4 = list4 * refresh_rate
    jitter4 = int(jitter4)

    jitter5 = list5 * refresh_rate
    jitter5 = int(jitter5)

    jitter_list = [jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   jitter1, jitter2, jitter3, jitter4, jitter5,
                   ]
                   
    random.shuffle(jitter_list)

grid_pos = [grid1, grid2, grid3, grid4, grid5]

# make intro screen grid position prompts
def attend1_intro_grid_prompts():
    
    global grid_prompts
    
    unit='deg'
    stim_rad = .8
    
    target_grid_prompt  = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid1), lineColor="white", fillColor="white")
    
    grid_prompt1        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid1), lineColor="white")
    grid_prompt2        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid2), lineColor="white")
    grid_prompt3        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid3), lineColor="white")
    grid_prompt4        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid4), lineColor="white")
    grid_prompt5        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid5), lineColor="white")
    
    grid_prompts = [target_grid_prompt, grid_prompt1, grid_prompt2, grid_prompt3, grid_prompt4, grid_prompt5]

def attend3_intro_grid_prompts():
    
    global grid_prompts
    
    unit='deg'
    stim_rad = .8
    
    target_grid_prompt1  = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid1), lineColor="white", fillColor="white")
    target_grid_prompt2  = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid2), lineColor="white", fillColor="white")
    target_grid_prompt3  = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid3), lineColor="white", fillColor="white")
    
    grid_prompt1        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid1), lineColor="white")
    grid_prompt2        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid2), lineColor="white")
    grid_prompt3        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid3), lineColor="white")
    grid_prompt4        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid4), lineColor="white")
    grid_prompt5        = visual.Circle(win, units=unit, radius=stim_rad, pos=(grid5), lineColor="white")
    
    grid_prompts = [target_grid_prompt1, target_grid_prompt2, target_grid_prompt3, grid_prompt1, grid_prompt2, grid_prompt3, grid_prompt4, grid_prompt5]

# make individual (sequential) wedges
def create_wedges():
    
    global wedge_list, outer_wedge_list
    
    wedge_list = []
    outer_wedge_list = []
    
    for i in range(5):
        i = visual.ShapeStim(win, units='', lineWidth=1.5, lineColor='black', lineColorSpace='rgb', fillColor="black", fillColorSpace='rgb', 
                             vertices=((0, 0), (1.93/2, 0.51/2), (0.51/2, 1.93/2)), closeShape=True, pos=grid_pos[i], size=1, interpolate=True, name=("wedge: ", i))
        wedge_list.append(i)
        
    j = 3
    for i in range(2):
        i = visual.ShapeStim(win, units='', lineWidth=1.5, lineColor='black', lineColorSpace='rgb', fillColor="black", fillColorSpace='rgb', 
                             vertices=((0, 0), (1.93/2, 0.51/2), (0.51/2, 1.93/2)), closeShape=True, pos=grid_pos[j], size=1, interpolate=True, name=("wedge", i))
        outer_wedge_list.append(i)
        j += 1
        
    for wedge in wedge_list:
        wedge.ori = random.randint(0,360)
    for wedge in outer_wedge_list:
        wedge.ori = random.randint(0,360)

# make fixation cross
class Fix_white(object): 
    
    def __init__(self): 
        """Create visual components of the fixation"""
        self.circle  = visual.Circle(win,radius=.5, edges=32, fillColor='black') 
        self.circle2 = visual.Circle(win,radius=.1, edges=32, fillColor='white') 
        self.linev   = visual.Line(win, start=(0,.8), end=(0,-.8), lineWidth=6, lineColor='white') 
        self.lineh   = visual.Line(win, start=(.8,0), end=(-.8,0), lineWidth=6, lineColor='white') 

        self.components = [self.circle,self.linev,self.lineh, self.circle2] 

    def draw(self): 
        """Draw all components of the fixation on the screen.""" 
        [component.draw() for component in self.components] 
        
class Fix_green(object): 
    
    def __init__(self): 
        """Create visual components of the fixation"""
        self.circle  = visual.Circle(win,radius=.5, edges=32, fillColor='black', lineColor="white")
        self.circle2 = visual.Circle(win,radius=.1, edges=32, fillColor='white', lineColor="white")
        self.linev   = visual.Line(win, start=(0,.8), end=(0,-.8), lineWidth=6, lineColor='white') 
        self.lineh   = visual.Line(win, start=(.8,0), end=(-.8,0), lineWidth=6, lineColor='white') 

        self.components = [self.circle,self.linev,self.lineh, self.circle2] 

    def draw(self): 
        """Draw all components of the fixation on the screen.""" 
        [component.draw() for component in self.components] 

# Make critical stimuli
def make_stims():
    
    global stimuli
    
    stim_rad = .8
    unit = 'deg'

    red_stim    = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="red",     fillColor="red",    lineColor="red")
    blue_stim   = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="blue",    fillColor="blue",   lineColor="blue")
    green_stim  = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="green",   fillColor="green",  lineColor="green")
    orange_stim = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="orange",  fillColor="orange", lineColor="orange")
    purple_stim = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="purple",  fillColor="purple", lineColor="purple")
    yellow_stim = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="yellow",  fillColor="yellow", lineColor="yellow")
    pink_stim   = visual.Circle(win, units=unit, radius=stim_rad, pos=(0,0), name="pink",    fillColor="pink",   lineColor="pink")

    stimuli = [red_stim, blue_stim, green_stim, orange_stim, purple_stim, yellow_stim, pink_stim]
    
    random.shuffle(stimuli)

# make target prompts
def make_target_prompts():
    
    global prompt1, prompt2, prompt3
    unit = 'deg'
    
    prompt1   = visual.Circle(win, units=unit, radius=2.2, pos=(0,0), name="prompt1", lineColor="white")
    prompt2   = visual.Circle(win, units=unit, radius=1.5, pos=(0,0), name="prompt2", lineColor="white")
    prompt3   = visual.Circle(win, units=unit, radius=.8, pos=(0,0), name="prompt3", lineColor="white")

# Intro display screen prior to participant start - ATTEND1
def attend1_wait():
    hello = visual.TextStim(win, text='\t\t  ATTEND 1 \nPRESS SPACEBAR TO BEGIN', font='', pos=(0.0, -4), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                            opacity=1.0, contrast=1.0, units='', ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
                            fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, name=None, autoLog=None)
    
    running = 1
    while running:         
        
        for frame in range(target_frames):
            hello.draw()
            FixW.draw()
            attend1_intro_grid_prompts()
            for grid in grid_prompts:
                grid.draw()
                    
            allKeys = event.getKeys(keyList = ('space'))
            for thisKey in allKeys:
                if thisKey == 'space':
                    running = 0
                        
            win.flip()
            
        for frame in range(target_frames):
            hello.draw()
            FixW.draw()
            for grid in grid_prompts[1:]:
                grid.draw()
                    
            allKeys = event.getKeys(keyList = ('space'))
            for thisKey in allKeys:
                if thisKey == 'space':
                    running = 0
                        
            win.flip()
               
    
    for frame in range(target_frames*2):
        FixW.draw()
        win.flip()
        
def attend3_wait():
    hello = visual.TextStim(win, text='\t\t  ATTEND 3 \nPRESS SPACEBAR TO BEGIN', font='', pos=(0.0, -4), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                            opacity=1.0, contrast=1.0, units='', ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
                            fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, name=None, autoLog=None)
    
    running = 1
    while running:         
        
        for frame in range(target_frames):
            hello.draw()
            FixW.draw()
            attend3_intro_grid_prompts()
            for grid in grid_prompts:
                grid.draw()
                    
            allKeys = event.getKeys(keyList = ('space'))
            for thisKey in allKeys:
                if thisKey == 'space':
                    running = 0
                        
            win.flip()
            
        for frame in range(target_frames):
            hello.draw()
            FixW.draw()
            for grid in grid_prompts[3:]:
                grid.draw()
                    
            allKeys = event.getKeys(keyList = ('space'))
            for thisKey in allKeys:
                if thisKey == 'space':
                    running = 0
                        
            win.flip()
               
    for frame in range(target_frames*2):
        FixW.draw()
        win.flip()

def get_sequential_stim_times():

    global gate, one_time, two_time, three_time, four_time, five_time, x, frame

    if  gate == 1 and frame == 0:
        one_time = x
        gate +=1
    elif gate == 2:
        two_time = x
        gate +=1
    elif gate == 3:
        three_time = x
        gate +=1
    elif gate == 4:
        four_time = x
        gate+=1
    elif gate == 5:
        five_time = x
        
def get_keys():

    global allKeys, keyTime, thisKey

    allKeys = event.getKeys(keyList = ('h','escape'))
    
    for thisKey in allKeys:
        if thisKey == 'h':
            keyTime=core.getTime()
        elif thisKey == 'escape':
            dataFile.close()
            tracker.setConnectionState(False)
            win.close()
            core.quit()
            
def check_eyes():
    global eyes, gaze_ok_region, block
    gpos = tracker.getLastGazePosition()
    if  not isinstance(gpos, (tuple, list)):
        pass
    elif  gaze_ok_region.contains(gpos):
        pass
    else:
        eyes = 0

def thank_you():
    hello = visual.TextStim(win, text='Thank you for taking part.', font='', pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                            opacity=1.0, contrast=1.0, units='', ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
                           fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, name=None, autoLog=None)
    
    running = 1
    while running:
        hello.draw()
        win.flip()
        
        allKeys = event.getKeys(keyList = ('space'))
        for thisKey in allKeys:
            if thisKey == 'space':
                dataFile.close()
                tracker.setConnectionState(False)
                io.quit()
                core.wait(1)
                core.quit()
                win.close()

########################################################################################################
###################################### CREATE SELECTION FUNCTIONS ######################################
########################################################################################################

# Select target item
def select_target():
    
    global target
    
    target = stimuli[0]
    target.pos = (0,0)

# Select stims
def select_stims(tabsent=1, attend=1):
    
    global stims, stim_display, attent
    
    if tabsent == 0: # target absent
   
        stims = stimuli[1:]
        random.shuffle(stims)

        stim1 = stims[1]
        stim2 = stims[2]
        stim3 = stims[3]
        stim4 = stims[4]
        stim5 = stims[5]
        
        if attend == 1:
            attent = "1"
            stim1.pos = grid_pos[0]
            stim2.pos = grid_pos[1]
            stim3.pos = grid_pos[2]
            stim4.pos = grid_pos[3]
            stim5.pos = grid_pos[4]
            
        elif attend == 3:
            attent = 3
            attend3_grids = [grid1, grid2, grid3]
            random.shuffle(attend3_grids)
            
            stim1.pos = attend3_grids[0]
            stim2.pos = attend3_grids[1]
            stim3.pos = attend3_grids[2]
            stim4.pos = grid_pos[3]
            stim5.pos = grid_pos[4]

        stim_display = [stim1, stim2, stim3, stim4, stim5]
        
    elif tabsent == 1: # target present
        
        stims = stimuli[1:]
        random.shuffle(stims)
        
        stim1 = stimuli[0]
        stim2 = stims[1]
        stim3 = stims[2]
        stim4 = stims[3]
        stim5 = stims[4]

        if attend == 1:
            attent = 1
            stim1.pos = grid_pos[0]
            stim2.pos = grid_pos[1]
            stim3.pos = grid_pos[2]
            stim4.pos = grid_pos[3]
            stim5.pos = grid_pos[4]
            
        elif attend == 3:
            attent = 3
            
            attend3_grids = [grid1, grid2, grid3]
            random.shuffle(attend3_grids)
            
            stim1.pos = attend3_grids[0]
            stim2.pos = attend3_grids[1]
            stim3.pos = attend3_grids[2]
            stim4.pos = grid_pos[3]
            stim5.pos = grid_pos[4]
        
        stim_display = [stim1, stim2, stim3, stim4, stim5]
        
# Display the target with circle prompts
def display_target():
    
    global target_time

    prompts = [prompt1, prompt2, prompt3, 
               prompt1, prompt2, prompt3,
               prompt1, prompt2, prompt3]
    
    target_time = core.getTime()
    for counter, prompt in enumerate(prompts):
        for frame in range(target_frames):
            prompt[counter].draw()
            target.draw()
            win.flip()
        
def eye_error_prompt():
    
    for frame in range(target_frames*4):
        FixG.draw()
        win.flip()

# Display ISI
def display_ISI():
    
    for frame in range(ISI_frames):
        FixW.draw()
        win.flip()

# Display the critical stimuli [upper right quadrant]
def display_stims(sim=1, pgroup=1):
    
    io.clearEvents()
    tracker.setRecordingState(True)
    
    global stick, stim_names, stim_times, gate, frame, x, simultan, pergroup, keyTime, RT, startTime, stim_display, eyes, gaze_ok_region, block

    keyTime="-"
    RT = "-"
    
    # SIM PRES & PERCEPTUAL GROUPING
    if sim == 1 and pgroup == 1: 
        
        running = 1

        while running == 1:
        
            eyes = 1
            sim = 1
            pgroup = 1
            attend = attent

            stim_names = []
            stim_times = []
            create_wedges()
            
            for frame in range(jitter_list[0]):
                FixG.draw()
                win.flip()
                
            startTime = core.getTime()
            for frame in range(stim_frames):
                
                if eyes == 1:
                    for stim in stim_display:
                        stim.draw()
                        stim_names.append(stim.name)
                    for wedge in outer_wedge_list:
                        wedge.draw()

                    if eyes == 1:
                        triangle.draw()
                        FixG.draw()
                        get_keys()
                        check_eyes()
                    
                        x = win.flip()
                        
                    if frame == 0:
                        Stim_onset = x
                        
                    if keyTime != "-":
                        RT = keyTime - startTime
                        
                    stim_times.append(Stim_onset)
                    
            for frame in range(ISI_frames*1):
                get_keys()
                FixG.draw()
                win.flip()
                    
            if eyes == 1:
                dataFile.write(f'{eyes}, {sim}, {pgroup}, {attend}, {targ[0]}, {startTime}',
                               f'{keyTime}, {RT}, {target.name}, {target.pos}, {target_time}', 
                               f'{stim_names[0]}, {stim_times[1]}, {stim_names[1]}, {stim_times[1]}', 
                               f'{stim_names[2]}, {stim_times[2]}, {stim_names[3]}, {stim_times[3]}',
                               f'{stim_names[4]}, {stim_times[4]}')
                running = 0
                
            elif eyes == 0:
                running = 1
                select_stims(targ[0], attention)
                display_stims(simult, pgr)
                eye_error_prompt()

            stim_names = []
            stim_times = []

    # SIM PRES & NO PERCEPTUAL GROUPING
    elif sim == 1 and pgroup == 0: 
        
        running = 1
        
        while running ==1:
            
            eyes = 1
            sim = 1
            prgroup = 0
            attend = attent

            stim_names = []
            stim_times = []
            create_wedges()
            
            for frame in range(jitter_list[0]):
                FixG.draw()
                win.flip()

            if eyes == 1:
                
                startTime = core.getTime()
                for frame in range(stim_frames):
                    for stim in stim_display:
                        stim.draw()
                        stim_names.append(stim.name)
                    for wedge in wedge_list:
                        wedge.draw()
                            
                    FixG.draw()
                    get_keys()
                    check_eyes()
                        
                    x = win.flip()
                    if frame == 0:
                        Stim_onset = x
                            
                    if keyTime != "-":
                        RT = keyTime - startTime
                            
                    stim_times.append(Stim_onset)
                    
            for frame in range(ISI_frames*1):
                get_keys()
                FixG.draw()
                win.flip()
                    
            if eyes == 1:
                dataFile.write(f'{eyes}, {sim}, {pgroup}, {attend}, {targ[0]}, {startTime}',
                               f'{keyTime}, {RT}, {target.name}, {target.pos}, {target_time}', 
                               f'{stim_names[0]}, {stim_times[1]}, {stim_names[1]}, {stim_times[1]}', 
                               f'{stim_names[2]}, {stim_times[2]}, {stim_names[3]}, {stim_times[3]}',
                               f'{stim_names[4]}, {stim_times[4]}')
                running = 0
                
            elif eyes == 0:
                running = 1
                select_stims(targ[0], attention)
                display_stims(simult, pgr)
                eye_error_prompt()
            
            stim_names = []
            stim_times = []

    # SEQ PRES & PERCEPTUAL GROUPING
    elif sim == 0 and pgroup  == 1:
        
        running = 1
        
        while running ==1:
            
            eyes = 1
            sim = 0
            prgroup = 0
            attend = attent
            
            create_wedges()
            shuffle_attend3 = stim_display[0:2]
            random.shuffle(shuffle_attend3)
            stim_display[0:2] = shuffle_attend3
            
            stim_names = []
            stim_times = []
            gate = 1
            
            if eyes == 1:
                startTime = core.getTime()
                for stim in stim_display:
                    
                    stim_names.append(stim.name)
                    
                    for frame in range(stim_frames):
                        stim.draw()
                        FixG.draw()
                        triangle.draw()
                        for wedge in outer_wedge_list:
                            wedge.draw()
                        get_keys()
                        check_eyes()
                        
                        x = win.flip()
                                        
                        if keyTime != "-":
                            RT = keyTime - startTime
                            
                        get_sequential_stim_times()
                        stim_times.append(x)
                  
            for frame in range(ISI_frames/2):
                FixG.draw()
                get_keys()
                win.flip()
            
                    
            if eyes == 1:
                dataFile.write(f'{eyes}, {sim}, {pgroup}, {attend}, {targ[0]}, {startTime}',
                               f'{keyTime}, {RT}, {target.name}, {target.pos}, {target_time}', 
                               f'{stim_names[0]}, {stim_times[1]}, {stim_names[1]}, {stim_times[1]}', 
                               f'{stim_names[2]}, {stim_times[2]}, {stim_names[3]}, {stim_times[3]}',
                               f'{stim_names[4]}, {stim_times[4]}')
                running = 0
            
            elif eyes == 0:
                running = 1
                select_stims(targ[0], attention)
                display_stims(simult, pgr)
                eye_error_prompt()
                
            stim_names = []
            stim_times = []
            
    # SEQ PRES & NO PERCEPTUAL GROUPING
    elif sim == 0 and pgroup  == 0:
        
        running = 1
        
        while running ==1:
            
            eyes = 1
            sim = 0
            pgroup = 0
            attend = attent
            
            create_wedges()
            shuffle_attend3 = stim_display[0:2]
            random.shuffle(shuffle_attend3)
            stim_display[0:2] = shuffle_attend3
            
            stim_names = []
            stim_times = []
            gate = 1
            
            if eyes == 1:
                startTime = core.getTime()
                for stim in stim_display:
                    
                    stim_names.append(stim.name)
                    
                    for frame in range(stim_frames):
                        stim.draw()
                        FixG.draw()
                        for wedge in wedge_list:
                            wedge.draw()
                        get_keys()
                        check_eyes()

                        x = win.flip()
                        
                        if keyTime != "-":
                            RT = keyTime - startTime
                        
                        get_sequential_stim_times()
                        stim_times.append(x)
                        
            for frame in range(ISI_frames):
                FixG.draw()
                get_keys()
                win.flip()
                    
            if eyes == 1:
                dataFile.write(f'{eyes}, {sim}, {pgroup}, {attend}, {targ[0]}, {startTime}',
                               f'{keyTime}, {RT}, {target.name}, {target.pos}, {target_time}', 
                               f'{stim_names[0]}, {stim_times[1]}, {stim_names[1]}, {stim_times[1]}', 
                               f'{stim_names[2]}, {stim_times[2]}, {stim_names[3]}, {stim_times[3]}',
                               f'{stim_names[4]}, {stim_times[4]}')
                running = 0
           
            elif eyes == 0:
                running = 1
                select_stims(targ[0], attention)
                display_stims(simult, pgr)
                eye_error_prompt()

            stim_names = []
            stim_times = []