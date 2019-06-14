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

####################################################################################################################################################################
################################################################# MAKE ALL VISUAL ELEMENTS #########################################################################
####################################################################################################################################################################

# Open a writeable data file
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["Eyes 1=good", "SIM (1=yes, 0=no", "PGROUP 1=yes, 0=no", "ATTEND 1/3", "Target Pres", "START TIME", "KEYTIME", "RT", "TARGET NAME", "TARGET POSITION", "TARGET ONSET TIME", 
                 "STIM1 NAME", "STIM 1 ONSET", "STIM2 NAME", "STIM2 ONSET", "STIM3 NAME", "STIM3 ONSET", "STIM4 NAME", "STIM4 ONSET", "STIM5 NAME", "STIM5 ONSET"])

# Initialize window
win = visual.Window([800,600],color=(-1,-1,-1),colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=True)

# Create a circle stim centered in middle of screen, with radius of 200 px.
# Change the radius to whatever suits you...
gaze_ok_region = visual.Circle(win, radius=220, units='pix', lineColor="white")

# Make the eye-blocker square
block = visual.ShapeStim(win, units = 'deg', vertices = ((2,2),(8,2),(8,8),(2,8)), lineColor='red', fillColor='red')

# Set stimulus frame durations
def refresh_rate():
    
    global target_frames, stim_frames, grid_frames, ISI_frames
    
    refresh_rate = 60.0
    target_dur =  .5
    stim_dur   = .25
    grid_dur   = .25
    ISInterval = 1
    
    #target_dur =  .1
    #stim_dur   =  .1
    #grid_dur   =  .1
    #ISInterval =  .1

    target_frames = target_dur * refresh_rate
    target_frames = int(target_frames)

    stim_frames = stim_dur * refresh_rate
    stim_frames = int(stim_frames)

    grid_frames = grid_dur * refresh_rate
    grid_frames = int(grid_frames)
    
    ISI_frames  = ISInterval * refresh_rate
    ISI_frames  = int(ISI_frames)
    
refresh_rate()

# set upper right quadrant grid positions 
grid1 = (2.82, 2.82) 
grid2 = (4.75185165258, 3.337638090205)
grid3 = (3.337638090205, 4.75185165258)
grid4 = (6.68370330516, 3.8552761804099998)
grid5 = (3.8552761804099998, 6.68370330516)

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
        
# make (simultanaeous) triangle wedge
triangle = visual.ShapeStim(win, units = 'deg', vertices = ((grid1),(grid3),(grid2)) , lineColor='black', fillColor='black')

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
        
create_wedges()

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
        self.circle  = visual.Circle(win,radius=.5, edges=32, fillColor='black', lineColor="green")
        self.circle2 = visual.Circle(win,radius=.1, edges=32, fillColor='green', lineColor="green")
        self.linev   = visual.Line(win, start=(0,.8), end=(0,-.8), lineWidth=6, lineColor='green') 
        self.lineh   = visual.Line(win, start=(.8,0), end=(-.8,0), lineWidth=6, lineColor='green') 

        self.components = [self.circle,self.linev,self.lineh, self.circle2] 

    def draw(self): 
        """Draw all components of the fixation on the screen.""" 
        [component.draw() for component in self.components] 
        
FixW =  Fix_white()
FixG =  Fix_green()

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
    
make_stims()

def make_target_prompts():
    
    global prompt1, prompt2, prompt3
    unit = 'deg'
    
    prompt1   = visual.Circle(win, units=unit, radius=2.2, pos=(0,0), name="prompt1", lineColor="white")
    prompt2   = visual.Circle(win, units=unit, radius=1.5, pos=(0,0), name="prompt2", lineColor="white")
    prompt3   = visual.Circle(win, units=unit, radius=.8, pos=(0,0), name="prompt3", lineColor="white")
    
make_target_prompts()

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
            

###################################################################################################################################
############################################### CREATE SELECTION FUNCTIONS ########################################################
###################################################################################################################################

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
    
    target_time = core.getTime()
    for frame in range(target_frames):
        prompt1.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt1.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt1.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        target.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
        target.draw()
        win.flip()
        
def eye_error_prompt():
    
    for frame in range(target_frames):
        prompt1.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt1.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt1.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt2.draw()
        FixG.draw()
        win.flip()
        
    for frame in range(target_frames):
        prompt3.draw()
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
    
    keyTime="-"
    RT = "-"
    
    global stim_names, stim_times, gate, frame, x, simultan, pergroup, keyTime, RT, startTime, stim_display, eyes, gaze_ok_region, block
    
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
            
            for frame in range(ISI_frames*1):
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
                        
                    triangle.draw()
                    FixG.draw()
                    get_keys()
                    check_eyes()
                    
                    if eyes == 0:
                        block.draw()
                        
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
                dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n'%(eyes, sim, pgroup, attend, targ[0], startTime, keyTime, RT, target.name, target.pos, target_time, stim_names[0],
                                                                                                                 stim_times[1], stim_names[1], stim_times[1], stim_names[2], stim_times[2], stim_names[3], stim_times[3], 
                                                                                                                 stim_names[4], stim_times[4]))
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
            
            for frame in range(ISI_frames*1):
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
                    
                    if eyes == 0:
                        block.draw()
                        
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
                dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n'%(eyes, sim, pgroup, attend, targ[0], startTime, keyTime, RT, target.name, target.pos, target_time, stim_names[0],
                                                                                                                 stim_times[1], stim_names[1], stim_times[1], stim_names[2], stim_times[2], stim_names[3], stim_times[3], 
                                                                                                                 stim_names[4], stim_times[4]))
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
                        if eyes == 0:
                            block.draw()
                        x = win.flip()
                                        
                        if keyTime != "-":
                            RT = keyTime - startTime
                            
                        get_sequential_stim_times()
                        stim_times.append(x)
            
                    
            if eyes == 1:
                dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n'%(eyes, sim, pgroup, attend, targ[0], startTime, keyTime, RT, target.name, target.pos, target_time, stim_names[0],
                                                                                                                 stim_times[1], stim_names[1], stim_times[1], stim_names[2], stim_times[2], stim_names[3], stim_times[3], 
                                                                                                                 stim_names[4], stim_times[4]))
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
                        if eyes == 0:
                            block.draw()
                        x = win.flip()
                        
                        if keyTime != "-":
                            RT = keyTime - startTime
                        
                        get_sequential_stim_times()
                        stim_times.append(x)
                    
            if eyes == 1:
                dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n'%(eyes, sim, pgroup, attend, targ[0], startTime, keyTime, RT, target.name, target.pos, target_time, stim_names[0],
                                                                                                                 stim_times[1], stim_names[1], stim_times[1], stim_names[2], stim_times[2], stim_names[3], stim_times[3], 
                                                                                                                 stim_names[4], stim_times[4]))
                running = 0
           
            elif eyes == 0:
                running = 1
                select_stims(targ[0], attention)
                display_stims(simult, pgr)
                eye_error_prompt()

            stim_names = []
            stim_times = []
            
###################################################################################################################################
#################################################### MAIN ROUTINE #################################################################
###################################################################################################################################

trial_amount=5

def do_trials():

    for i in range(trial_amount):

        select_stims(targ[0], attention)
        display_stims(simult, pgr)
        
        targ.pop(0)
        
def block1():
    global targ, attention, simult, pgr
    
    running = 1
    block   = 1

    while running==1:

        trials = [1,2,3,4]
        random.shuffle(trials)
       
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

                targ        = [1,1,0,0,0] 
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

                targ        = [1,1,0,0,0]  
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

                targ        = [1,1,0,0,0] 
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

                targ        = [1,1,0,0,0]  
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

                targ        = [1,1,0,0,0] 
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

                targ        = [1,1,0,0,0]  
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

                targ        = [1,1,0,0,0]  
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

                targ        = [1,1,0,0,0]  
                random.shuffle(targ)
                attention   = 3
                simult      = 0
                pgr         = 0
                
                do_trials()
                
            trials.pop(0)

            block += 1

        running = 0
    
balance = [1,2]
#random.shuffle(balance)

if balance[0] == 1:
    block1()
    
    block3()
    
elif balance[0] == 2 :
    block3()
    
    block1()
    

thank_you()
    
dataFile.close()
tracker.setConnectionState(False)
io.quit()
core.quit()
win.close()
