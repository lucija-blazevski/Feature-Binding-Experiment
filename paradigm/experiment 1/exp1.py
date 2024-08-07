"""
Created on Tue January 10, 2023


Project:         Feature binding is slow: temporal integration explains apparent ultrafast binding - Experiment 1
Notes:           Version of the experiment with 2 (SF: low and high) x 5 (Cycle number: 1, 2, 3, 4, and 6)
                 factors to calculate the minimum stimulus duration necessary for 75% accuracy in reports.
Author:          Lucija Blaževski

"""

# ==============================================================================
# IMPORT STATEMENTS
# ==============================================================================
# Import necessary Python libraries and PsychoPy modules for the experiment
import os
import random
import numpy as np
from psychopy import visual, event, tools, data, core, gui, logging, __version__, monitors
from psychopy.hardware import keyboard
from psychopy.tools.colorspacetools import dkl2rgb

# ==============================================================================
# MONITOR SETUP
# ==============================================================================
# Define and configure the monitor parameters for the experiment
monitor_name = 'lab_monitor'
screen_width_cm = 61.42  # Width of the monitor in cm
screen_resolution = [2560, 1440]  # Screen resolution in pixels
viewing_distance_cm = 75  # Viewing distance in cm

# Create the monitor object
mon = monitors.Monitor(monitor_name)
mon.setWidth(screen_width_cm)
mon.setSizePix(screen_resolution)
mon.setDistance(viewing_distance_cm)

# ==============================================================================
# DATA AND GUI SETUP
# ==============================================================================
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Create data folder if doesn't exist
if not os.path.isdir('data'):
    os.mkdir('data')

# Store info about the experiment session
psychopyVersion = __version__
expName = 'binding_pilot'
expInfo = {"Gender": ["Female", "Male", 'Other', 'Prefer not to say'],
           "Handedness": ["Right", "Left"],
           "Age": 0,
           'frame_rate': 120,
           'participant': '00',
           'session': 'pilot'}

# Open GUI
if True:
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if not dlg.OK:
        core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # Add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# Log file
logFile = logging.LogFile(filename + '.log', level=logging.EXP)

# PsychoPys experiment handler
this_exp = data.ExperimentHandler(name=expName, version='',
                                  extraInfo=expInfo,
                                  runtimeInfo=None,
                                  originPath=_thisDir + '/feature_binding_pilot.py',
                                  savePickle=False, saveWideText=True,
                                  dataFileName=filename)

# ==============================================================================
# VISUAL COMPONENTS SETUP
# ==============================================================================
# Create window
win = visual.Window(size=[2560, 1440], fullscr=True, monitor=mon, screen=0,
                    color=[0, 0, 0], units='deg')

# Store frame rate of monitor if we can measure it
expInfo['frame_rate_detected'] = win.getActualFrameRate()

# Create fixation cross
fix = visual.TextStim(win, text="+", color='black', units='deg', height=0.4, pos=(0, 0))

# Covers in the color of the background used to cover one part of the circle and get a semicircle
# 1 is upper visual field cover, so used with a 'down' visual field
wedge_cover_down = visual.Polygon(
    win=win, name='polygon',
    edges=128, size=(4, 4),
    ori=90.0, pos=(0, -0.3),
    lineWidth=1.0, colorSpace='rgb', lineColor=[0, 0, 0], fillColor=[0, 0, 0],
    opacity=None, interpolate=True)
wedge_cover_down.vertices = wedge_cover_down.vertices[65:128]
wedge_cover_down.needVertexUpdate = True

# 2 is lower visual field cover, so used with the 'up' visual field
wedge_cover_up = visual.Polygon(
    win=win, name='polygon',
    edges=128, size=(4, 4),
    ori=90.0, pos=(0, 0.3),
    lineWidth=1.0, colorSpace='rgb', lineColor=[0, 0, 0], fillColor=[0, 0, 0],
    opacity=None, interpolate=True)
wedge_cover_up.vertices = wedge_cover_up.vertices[:65]
wedge_cover_up.needVertexUpdate = True

# ==============================================================================
# STIMULI CONFIGURATION
# ==============================================================================
# Define 16 combinations of stimuli required for the experiment.
# These combinations involve varying:
# - Visual field position (upper, lower)
# - Spatial frequency (low, high)
# - Initial color (black, white)
# - Left/right orientation of color

# Grating texture settings
grating_res = 512  # Resolution of the grating texture

# Create grating textures with low and high spatial frequencies
grating_lowSF = visual.filters.makeGrating(res=grating_res, cycles=1, gratType='sqr')
grating_highSF = visual.filters.makeGrating(res=grating_res, cycles=5, gratType='sqr')

# ==============================================================================
# WHITE STIMULI CREATION
# ==============================================================================
# Create textures for white stimuli on gray background at both low and high spatial frequencies

# Low Spatial Frequency White Texture
hsv_tex_white_low = np.ones((grating_res, grating_res, 3))
hsv_tex_white_low[..., 1] = 0  # Saturation to 0 for white
hsv_tex_white_low[..., 2] = (grating_lowSF + 1) / 2.0 * 0.5 + 0.5  # Value based on low SF

# High Spatial Frequency White Texture
hsv_tex_white_high = np.ones((grating_res, grating_res, 3))
hsv_tex_white_high[..., 1] = 0  # Saturation to 0 for white
hsv_tex_white_high[..., 2] = (grating_highSF + 1) / 2.0 * 0.5 + 0.5  # Value based on high SF

# Generate visual stimuli for white textures
# Upper visual field, low and high SF, oriented at 45 and 135 degrees
si_white_low_135_up, si_white_low_45_up, si_white_high_135_up, si_white_high_45_up = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, 0.3),
                       tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in
    zip([135, 45, 135, 45], [hsv_tex_white_low, hsv_tex_white_low, hsv_tex_white_high, hsv_tex_white_high])
]

# Lower visual field, low and high SF, oriented at 45 and 135 degrees
si_white_low_135_down, si_white_low_45_down, si_white_high_135_down, si_white_high_45_down = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, -0.3),
                       tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in
    zip([135, 45, 135, 45], [hsv_tex_white_low, hsv_tex_white_low, hsv_tex_white_high, hsv_tex_white_high])
]

# ==============================================================================
# BLACK STIMULI CREATION
# ==============================================================================
# Create textures for black stimuli on gray background at both low and high spatial frequencies

# Low Spatial Frequency Black Texture
hsv_tex_black_low = np.zeros((grating_res, grating_res, 3))
hsv_tex_black_low[..., 2] = (grating_lowSF + 1) / 2.0 * 0.5  # Value based on low SF

# High Spatial Frequency Black Texture
hsv_tex_black_high = np.zeros((grating_res, grating_res, 3))
hsv_tex_black_high[..., 2] = (grating_highSF + 1) / 2.0 * 0.5  # Value based on high SF

# Generate visual stimuli for black textures
# Upper visual field, low and high SF, oriented at 45 and 135 degrees
si_black_low_45_up, si_black_low_135_up, si_black_high_45_up, si_black_high_135_up = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, 0.3),
                       tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in
    zip([45, 135, 45, 135], [hsv_tex_black_low, hsv_tex_black_low, hsv_tex_black_high, hsv_tex_black_high])
]

# Lower visual field, low and high SF, oriented at 45 and 135 degrees
si_black_low_45_down, si_black_low_135_down, si_black_high_45_down, si_black_high_135_down = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, -0.3),
                       tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in
    zip([45, 135, 45, 135], [hsv_tex_black_low, hsv_tex_black_low, hsv_tex_black_high, hsv_tex_black_high])
]

# ==============================================================================
# MASKING STIMULI
# ==============================================================================
# Create masking stimuli for both upper and lower visual fields
mask_up, mask_down = [
    visual.NoiseStim(win=win, name=f"mask_{position}", pos=(0, y_pos), size=(3, 1.5), color=[1, 1, 1], colorSpace='rgb',
                     noiseType='White', noiseElementSize=[0.0625])
    for position, y_pos in zip(['up', 'down'], [0.95, -0.95])
]
mask_up.buildNoise()
mask_down.buildNoise()

# ==============================================================================
# EXPERIMENTAL QUESTION
# ==============================================================================
# Define the question after stimuli presentation
question = visual.TextStim(win, pos=(0, 0), text="Was black paired with left or right?", height=.07, units='norm',
                           color='black')


def display_question():
    """Display the question to the participant and collect their response."""
    question.draw()
    kb.clearEvents(eventType="keyboard")
    kb.clock.reset()
    win.flip()
    keys = kb.waitKeys(keyList=['left', 'right', 'escape'], waitRelease=False, clear=True)
    if 'escape' in keys:
        core.quit()
    # Parse answer and rt
    answer = keys[-1].name
    rt = keys[-1].rt
    this_exp.addData('answer', answer)
    this_exp.addData('rt', rt)
    if answer == correct_response:
        accuracy = 1
    else:
        accuracy = 0
    this_exp.addData('accuracy', accuracy)


# Feedback as part of practice
correctStim = visual.TextStim(win, text="CORRECT!", height=0.07, units='norm', color="green", pos=(0, 0))
incorrectStim = visual.TextStim(win, text="INCORRECT!", height=0.07, units='norm', color="red", pos=(0, 0))


def display_question_practice():
    """Display the question during practice sessions and provide feedback."""
    question.draw()
    kb.clearEvents(eventType="keyboard")
    kb.clock.reset()
    win.flip()
    keys = kb.waitKeys(keyList=['left', 'right', 'escape'], waitRelease=False, clear=True)
    if 'escape' in keys:
        core.quit()
    # Parse answer and rt
    answer = keys[-1].name
    rt = keys[-1].rt
    if answer == correct_response:
        accuracy = 1
        correctStim.draw()
    else:
        accuracy = 0
        incorrectStim.draw()
    win.flip()
    core.wait(1)
    return accuracy


# ==============================================================================
# INSTRUCTIONS AND BREAK FUNCTIONS
# ==============================================================================
instructions = visual.TextStim(win,
                               # pos=(0, 0),
                               text='',
                               height=.06,
                               units='norm',
                               color='black')


def display_instr(text):
    """Show text-only instructions and wait for SPACE."""
    instructions.text = text
    instructions.pos = (0, 0)
    instructions.draw()
    win.flip()
    event.clearEvents(eventType="keyboard")
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        core.quit()


# Break
def display_break(text):
    instructions.text = text
    instructions.draw()
    win.flip()


blank = visual.TextStim(win,
                        text="",
                        pos=(0, 0),
                        height=0)

# ==============================================================================
# PRACTICE STIMULI EXAMPLES
# ==============================================================================
example_black_right_up = visual.ImageStim(win,
                                          size=(4.5, 4.5),
                                          pos=(-2.5, -2),
                                          image=_thisDir + "/black_right_up.jpg")

example_white_left_up = visual.ImageStim(win,
                                         size=(4.5, 4.5),
                                         pos=(2.5, -2),
                                         image=_thisDir + "/white_left_up.jpg")

example_black_left_up = visual.ImageStim(win,
                                         size=(4.5, 4.5),
                                         pos=(-2.5, -2),
                                         image=_thisDir + "/black_left_up.jpg")

example_white_right_up = visual.ImageStim(win,
                                          size=(4.5, 4.5),
                                          pos=(2.5, -2),
                                          image=_thisDir + "/white_right_up.jpg")

example_black_right_down = visual.ImageStim(win,
                                            size=(4.5, 4.5),
                                            pos=(-2.5, -2),
                                            image=_thisDir + "/black_right_down.jpg")

example_white_left_down = visual.ImageStim(win,
                                           size=(4.5, 4.5),
                                           pos=(2.5, -2),
                                           image=_thisDir + "/white_left_down.jpg")

example_black_left_down = visual.ImageStim(win,
                                           size=(4.5, 4.5),
                                           pos=(-2.5, -2),
                                           image=_thisDir + "/black_left_down.jpg")

example_white_right_down = visual.ImageStim(win,
                                            size=(4.5, 4.5),
                                            pos=(2.5, -2),
                                            image=_thisDir + "/white_right_down.jpg")


def display_example_instructions(text: object, left_image: object, right_image: object, position: object) -> object:
    """Display instructions with example stimuli."""
    instructions.text = text
    instructions.text = text
    instructions.pos = position
    instructions.draw()
    left_image.draw()
    right_image.draw()
    win.flip()
    event.clearEvents(eventType="keyboard")
    keys = event.waitKeys(keyList=['right', 'left', 'space', 'escape'])
    if 'escape' in keys:
        core.quit()


# ==============================================================================
# STIMULUS PRESENTATION SEQUENCE FUNCTION
# ==============================================================================
def show_stim(stim, cycle_duration):
    """Show alternating stimuli for n cycles."""
    # Frame loop first gabor
    frame_number = -2
    while True:
        frame_number = frame_number + 1  # number of completed frames (so 0 is the first frame)

        if frame_number == cycle_duration:
            fix.setAutoDraw(False)
            break
        if frame_number == -1:
            [x.setAutoDraw(True) for x in stim]
            fix.setAutoDraw(True)
        elif frame_number == (cycle_duration - 1):
            [x.setAutoDraw(False) for x in stim]

        win.flip()


# ==============================================================================
# OTHER UTILITIES
# ==============================================================================
# Prepare the keyboard module
kb = keyboard.Keyboard()

# Create clock
my_clock = core.Clock()

# Hide a mouse
win.mouseVisible = False

# ==============================================================================
# START
# ==============================================================================
# Instructions
display_instr('Welcome to the experiment! \n\n\n\n Press SPACE to start the instructions.')

display_example_instructions(
    'In this experiment, you will be presented with semicircles made of black or white stripes. '
    'They will be presented at the center of the screen in a sequence. So, in every trial you will see black '
    'and white stripes alternating. These stripes will be pointing either to the left or to the right. To figure out '
    'if '
    'stripes are pointing to the left or to the right, you should figure out in which corner of the screen is '
    'the upper end of the shape pointing. '
    'Below you see and example of black semicircle pointing to the left and white semicircle orientated '
    'to the right.'
    '\n\n\n\n\n\n\n\n\n\n\n\nPress SPACE to continue.', left_image=example_black_left_down,
    right_image=example_white_right_down,
    position=(0, 0))

display_example_instructions('On every trial, each color will always be paired with only one orientation. For example, '
                             'in one trial you can see black leftward-pointing stripes alternating with white '
                             'rightward-pointing '
                             'stripes, as illustrated bellow.'
                             '\n\n\n\n\n\n\n\n\n\n\n\nPress SPACE to continue.', left_image=example_black_left_up,
                             right_image=example_white_right_up, position=(0, 0))

display_example_instructions('In another trial, this can be reversed and you could see white leftward-pointing stripes '
                             'alternating with black-rightward pointing stripes. Whether black is paired with left or '
                             'right will '
                             'change from trial to trial. '
                             '\n\n\n\n\n\n\n\n\n\n\n\nPress SPACE to continue.', position=(0, 0),
                             left_image=example_white_left_up, right_image=
                             example_black_right_up)

display_instr('The number of times black and white stripes are presented will change from trial to trial. '
              'Regardless of how many times black and white semicircles are presented, '
              'each color will always be pointing either to the left or to the right. Your task is to '
              'detect the orientation of BLACK stripes. '
              '\n\n\n\nPress SPACE to continue.')

display_instr('At the beginning of a trial, you should look at the fixation cross (+) at the center of the screen. '
              'At the end of each trial, you will be asked "Was black paired with leftward or rightward orientation?" '
              'This will not always be easy; Sometimes stripes will be presented so briefly that you will barely see '
              'them. '
              'You should not think too much about your response, but respond according to your first impression. '

              '\n\nTo respond, you should use left and right arrow keys located at the bottom right of the keyboard. '
              'If you think BLACK stripes were pointing to the LEFT, you should press the LEFT arrow key. Likewise, '
              'if you think BLACK stripes were pointing to the RIGHT, you should press the RIGHT arrow key. '
              '\n\n\n\nPress SPACE to continue.')

display_example_instructions(
    text='This is an example of one trial. Bellow you see BLACK stripes that are pointing to the right '
         'and WHITE stripes that are pointing to the left. These two stimuli will be alternating on the screen. '
         'Because your task is to detect in which direction are '
         'BLACK stripes pointing, the correct response here would be RIGHT, and you would, thus, press the '
         'RIGHT arrow key.'
         '\n\n\n\n\n\n\n\n\n\nPress RIGHT arrow key to continue.',
    left_image=example_black_right_up, position=(0, 0),
    right_image=example_white_left_up)

display_example_instructions('In another trial, you can see BLACK stripes pointing to the LEFT and WHITE stripes '
                             'pointing to the RIGHT. '
                             'Again, because you will be asked "Was black paired with left or right?", the correct '
                             'response in this '
                             'would be LEFT, and you should press the LEFT arrow key. '
                             '\n\n\n\n\n\n\n\n\n\n\n\nPress LEFT arrow key to continue.',
                             left_image=example_black_left_up, position=(0, 0),
                             right_image=example_white_right_up)

display_example_instructions(
    text='Stimuli could also appear below the fixation cross. '
         'Again, you should focus on where are black stripes pointing. '
         'This is the example of the trial where BLACK stripes are pointing to the RIGHT and WHITE stripes pointing to '
         'the LEFT. The correct response to "Was black paired with left or right?" in '
         'this trial would be RIGHT, and you should press the RIGHT arrow key. '
         '\n\n\n\n\n\n\n\n\n\nPress RIGHT arrow key to continue.', position=(0, 0),
    left_image=example_black_right_down,
    right_image=example_white_left_down)

display_example_instructions(
    text='In another trial in which stimuli appear below the fixation cross, as illustrated here, '
         'BLACK stripes could be pointing to the LEFT and '
         'WHITE stripes to the RIGHT. The correct response in this trial would be LEFT, '
         'and you should press the LEFT arrow key. '
         '\n\n\n\n\n\n\n\n\n\n\n\nPress LEFT arrow key to continue.', position=(0, 0),
    left_image=example_black_left_down,
    right_image=example_white_right_down)

display_instr('To familiarize yourself with the task, you will first go through the practice session. In the '
              'first block of the practice session stimuli will be shown way slower than in the actual experiment. '
              'The purpose of this practice block is to ensure that you understand what is the RIGHT and what is the '
              'LEFT '
              'orientation. If you will be needing a reminder, please check the guide you see on your desk. '
              '\n\n To be able to continue with the experiment, you need to have 10 correct trials in a row. You will'
              'receive a feedback after each trial. Remember to respond using LEFT or RIGHT arrow keys, according to '
              'the orientation of BLACK stripes. '
              '\n\n\n\nPress SPACE to start the first practice block.')

# ==============================================================================
# COUNTER-BALANCING AND TRIAL PREPARATION
# ==============================================================================
color = ['white', 'black']
spatial_frequency = ['low', 'high']
side = ['135', '45']
visual_field = ['up', 'down']

stimuli = {f'{a}_{b}_{c}_{d}': [f'si_{a}_{b}_{c}_{d}', f'wedge_cover_{d}'] for a in color for b in spatial_frequency for
           c in side for d in visual_field}

conditions = [[x, y, z, True] for x in ['low', 'high'] for y in [1, 2, 3, 4, 8, 16, 32, 64] for z in [2]]
conditions = conditions + [[x, y, z, False] for x in ['low', 'high'] for y in [1] for z in [2]]
check = [[x, y, z, False] for x in ['high'] for y in [3] for z in [60]]  # Super easy trials as attention checks
trial_list = conditions * 50 + check * 30
np.random.shuffle(trial_list)

practice3_conditions = [[x, y, z, True] for x in ['low', 'high'] for y in [1, 2, 3, 4, 8, 16, 32, 64] for z in [2]]
practice3_trial_list = practice3_conditions
np.random.shuffle(practice3_trial_list)

# ==============================================================================
# PRACTICE SESSION 1
# ==============================================================================
# Trial and correct answers counter
hit_counter = 0
while True:
    if hit_counter >= 10: break

    practice1_conditions = [[x, y, z, True] for x in ['low', 'high'] for y in [1] for z in [120]]
    practice1_trial_list = practice1_conditions * 30
    np.random.shuffle(practice1_trial_list)
    practice_trial_count = -1
    hit_counter = 0

    # Run trials
    while True:
        practice_trial_count += 1
        this_trial_practice = practice1_trial_list.pop()
        is_masked_practice = this_trial_practice[3]

        # Cycle number
        cycle_number_practice = this_trial_practice[1]

        # Get the phase
        phase = random.random()

        # Get the first color and orientation
        first_color_practice = np.random.choice(['black', 'white'])
        first_orientation_practice = np.random.choice(['135', '45'])

        # Save right-left to simplify analysis
        if first_orientation_practice == '45' and first_color_practice == 'black':
            correct_response = 'right'
        elif first_orientation_practice == '135' and first_color_practice == 'black':
            correct_response = 'left'
        elif first_orientation_practice == '45' and first_color_practice == 'white':
            correct_response = 'left'
        elif first_orientation_practice == '135' and first_color_practice == 'white':
            correct_response = 'right'

        # Get visual field
        this_side_practice = np.random.choice(['up', 'down'])

        # Get SF
        this_spatial_frequency_practice = this_trial_practice[0]

        # Pull the stimulus with previously defined parameters
        first_stim_name_practice = list(
            filter(lambda
                       x: first_color_practice in x and first_orientation_practice in x and this_side_practice in x and
                          this_spatial_frequency_practice in x, list(stimuli.keys())))[0]
        second_stim_name_practice = list(
            filter(lambda
                       x: first_color_practice not in x and first_orientation_practice not in x and this_side_practice in x and
                          this_spatial_frequency_practice in x, list(stimuli.keys())))[0]

        first_stim_practice = stimuli[first_stim_name_practice]
        first_stim_practice = [eval(first_stim_practice[0]), eval(first_stim_practice[1])]
        first_stim_practice[0].phase = phase

        second_stim_practice = stimuli[second_stim_name_practice]
        second_stim_practice = [eval(second_stim_practice[0]), eval(second_stim_practice[1])]
        second_stim_practice[0].phase = phase

        # Blank screen
        for i in range(30):  # Define the duration of the blank screen, 250 ms
            blank.draw()
            win.flip()

        # Duration of fixation
        flength = 1 + random.random()
        my_clock.reset()
        while my_clock.getTime() < flength:
            fix.draw()
            kb.clearEvents(eventType='keyboard')
            kb.clock.reset()
            win.flip()

        # Pull duration of stimuli
        stimulus_frame_duration_practice = this_trial_practice[2]

        # Finally, show stimuli
        for c in range(cycle_number_practice):
            show_stim(first_stim_practice, stimulus_frame_duration_practice)
            show_stim(second_stim_practice, stimulus_frame_duration_practice)

        # Show mask
        if is_masked_practice:
            for i in range(30):  # Define the duration of the mask in frames, 250 ms
                fix.draw()
                mask_up.draw()
                mask_down.draw()
                win.flip()

        # Blank screen
        for i in range(30):  # Define the duration of the blank screen, 250 ms
            blank.draw()
            win.flip()

        # Was left paired with left or right?
        input = display_question_practice()
        hit_counter += input

        # Reset hit_counter if error
        if not input:
            hit_counter = 0

        # Stop if 10 in row correct
        if hit_counter >= 10:
            break

        # When all trials are done break loop
        if practice_trial_count == 30:
            display_instr('In the last 30 trials, you did not succeed to have 10 correct responses in a row. '
                          'Please call the experimentator. ')
            break

display_instr('This is the end of the first practice block. You responded correctly on 10 trials in a row.'
              '\n\n\n\nPress SPACE to continue.')

# ==============================================================================
# PRACTICE SESSION 2
# ==============================================================================
display_instr('The next practice block will resemble the actual experiment more. Your task remains the same - '
              'You should detect the orientation of black stripes and respond with the LEFT or RIGHT arrow key '
              'accordingly. You will still receive feedback. You will be able to continue with the experiment only '
              'if you perform well enough on this practice block.'
              '\n\n\n\nPress SPACE to start the second practice block.')

# Trial and correct answers counter
practice_trial_count = -1
hit_counter = 0
while True:
    if ((practice_trial_count + 1) > 10) and (hit_counter / (practice_trial_count + 1) >= 0.8):
        break
    practice2_conditions = [[x, y, z, True] for x in ['low', 'high'] for y in [2, 3, 4, 8] for z in [30, 60]]
    practice2_trial_list = practice2_conditions * 100
    np.random.shuffle(practice2_trial_list)
    practice_trial_count = -1
    hit_counter = 0

    # Run trials
    while True:
        if hit_counter >= 10: break

        while True:
            practice_trial_count += 1
            this_trial_practice = practice2_trial_list.pop()

            # Masked or unmasked?
            is_masked_practice = this_trial_practice[3]

            # How many cycles?
            cycle_number_practice = this_trial_practice[1]

            # What is the color and orientation of the first stimulus?
            first_color_practice = np.random.choice(['black', 'white'])
            first_orientation_practice = np.random.choice(['135', '45'])

            # Save right-left to simplify analysis
            if first_orientation_practice == '45' and first_color_practice == 'black':
                correct_response = 'right'
            elif first_orientation_practice == '135' and first_color_practice == 'black':
                correct_response = 'left'
            elif first_orientation_practice == '45' and first_color_practice == 'white':
                correct_response = 'left'
            elif first_orientation_practice == '135' and first_color_practice == 'white':
                correct_response = 'right'

            # Visual field
            this_side_practice = np.random.choice(['up', 'down'])

            # SF
            this_spatial_frequency_practice = this_trial_practice[0]

            # Get the current stimuli name
            first_stim_name_practice = list(
                filter(lambda
                           x: first_color_practice in x and first_orientation_practice in x and this_side_practice in x and
                              this_spatial_frequency_practice in x, list(stimuli.keys())))[0]
            second_stim_name_practice = list(
                filter(lambda
                           x: first_color_practice not in x and first_orientation_practice not in x and this_side_practice in x and
                              this_spatial_frequency_practice in x, list(stimuli.keys())))[0]

            first_stim_practice = stimuli[first_stim_name_practice]
            first_stim_practice = [eval(first_stim_practice[0]), eval(first_stim_practice[1])]

            second_stim_practice = stimuli[second_stim_name_practice]
            second_stim_practice = [eval(second_stim_practice[0]), eval(second_stim_practice[1])]

            # Blank screen
            for i in range(30):  # Define the duration of the blank screen, 250 ms
                blank.draw()
                win.flip()

            # Duration of fixation
            flength = 1 + random.random()
            my_clock.reset()
            while my_clock.getTime() < flength:
                fix.draw()
                kb.clearEvents(eventType='keyboard')
                kb.clock.reset()
                win.flip()

            # Duration of each stimulus
            stimulus_frame_duration_practice = this_trial_practice[2]

            # Finally, show stimuli
            for c in range(cycle_number_practice):
                show_stim(first_stim_practice, stimulus_frame_duration_practice)
                show_stim(second_stim_practice, stimulus_frame_duration_practice)

            # Show mask
            if is_masked_practice:
                for i in range(30):  # Define the duration of the mask in frames, 250 ms
                    fix.draw()
                    mask_up.draw()
                    mask_down.draw()
                    win.flip()

            # Blank screen
            for i in range(30):  # Define the duration of the blank screen, 250 ms
                blank.draw()
                win.flip()

            # Was left paired with left or right
            input = display_question_practice()
            hit_counter += input

            # Stop after at least 10 trials when accuracy is 80%
            if ((practice_trial_count + 1) > 10) and (hit_counter / (practice_trial_count + 1) >= 0.8):
                break

            # When all trials are done break loop
            if practice_trial_count == 30:
                display_instr('In the last 30 trials, you did not succeed to have 80% correct responses. '
                              'Please call the experimentator. ')
                break

display_instr('This is the end of the second practice block. You performed well enough to continue with the '
              'experiment.'
              '\n\n\n\nPress SPACE to continue.')

# ==============================================================================
# PRACTICE SESSION 3
# ==============================================================================
display_instr('In the final practice block you will see examples from the actual experiment. As you will see,'
              ' stimuli are sometimes shown very quickly and, thus, the orientation might be difficult to detect. '
              'You should respond as accurately as possible, but try not thinking too much about your response. '
              '\n\n\n\nPress SPACE to start the third practice block.')

practice_trial_count = -1

# Run trials
while True:
    practice_trial_count += 1
    this_trial_practice = practice3_trial_list.pop()

    # Masked or unmasked?
    is_masked_practice = this_trial_practice[3]

    # How many cycles?
    cycle_number_practice = this_trial_practice[1]

    # Whar is the color and orientation of the first stimulus?
    first_color_practice = np.random.choice(['black', 'white'])
    first_orientation_practice = np.random.choice(['135', '45'])

    # Save right-left to simplify analysis
    if first_orientation_practice == '45' and first_color_practice == 'black':
        correct_response = 'right'
    elif first_orientation_practice == '135' and first_color_practice == 'black':
        correct_response = 'left'
    elif first_orientation_practice == '45' and first_color_practice == 'white':
        correct_response = 'left'
    elif first_orientation_practice == '135' and first_color_practice == 'white':
        correct_response = 'right'

    # Visual field
    this_side_practice = np.random.choice(['up', 'down'])

    # SF
    this_spatial_frequency_practice = this_trial_practice[0]

    # Define the current stimuli
    first_stim_name_practice = list(
        filter(lambda
                   x: first_color_practice in x and first_orientation_practice in x and this_side_practice in x and
                      this_spatial_frequency_practice in x, list(stimuli.keys())))[0]
    second_stim_name_practice = list(
        filter(lambda
                   x: first_color_practice not in x and first_orientation_practice not in x and this_side_practice in x and
                      this_spatial_frequency_practice in x, list(stimuli.keys())))[0]

    first_stim_practice = stimuli[first_stim_name_practice]
    first_stim_practice = [eval(first_stim_practice[0]), eval(first_stim_practice[1])]

    second_stim_practice = stimuli[second_stim_name_practice]
    second_stim_practice = [eval(second_stim_practice[0]), eval(second_stim_practice[1])]

    # Blank screen
    for i in range(30):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Duration of fixation
    flength = 1 + random.random()
    my_clock.reset()
    while my_clock.getTime() < flength:
        fix.draw()
        kb.clearEvents(eventType='keyboard')
        kb.clock.reset()
        win.flip()

    # Duration of stimuli
    stimulus_frame_duration_practice = this_trial_practice[2]

    # Finally show stimuli
    for c in range(cycle_number_practice):
        show_stim(first_stim_practice, stimulus_frame_duration_practice)
        show_stim(second_stim_practice, stimulus_frame_duration_practice)

    # Show mask
    if is_masked_practice:
        for i in range(30):  # Define the duration of the mask in frames, 250 ms
            fix.draw()
            mask_up.draw()
            mask_down.draw()
            win.flip()

    # Blank screen
    for i in range(30):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Was left paired with left or right
    display_question_practice()

    # When all trials are done break loop
    if practice_trial_count == 6:
        break

display_instr("This is the end of the last practice session."
              " Now you will start with the actual experiment. You will not receive the feedback anymore. "
              "You will have 3 breaks throughout the task. "
              ""
              "\n\n\nRemember to "
              "respond using LEFT or RIGHT arrow keys, according to the orientation of BLACK stripes. "
              'You should respond as accurately as possible, but try not thinking too much about your response. '
              "\n\n\n\nPRESS SPACE TO START THE EXPERIMENT.")

# ==============================================================================
# EXPERIMENT
# ==============================================================================
# Trial counter
trial_count = -1
while True:

    # Count trials
    trial_count += 1
    this_exp.addData('trial_number', trial_count)

    # Type of trial
    this_trial = trial_list.pop()
    this_exp.addData('trial_type', this_trial)

    # Is trial masked or not?
    is_masked = this_trial[3]
    this_exp.addData('mask_present', is_masked)

    # Number of cycles
    cycle_number = this_trial[1]
    this_exp.addData('cycle_number', cycle_number)

    # Color of the first stimulus
    first_color = np.random.choice(['black', 'white'])
    this_exp.addData('first_color', first_color)

    # Orientation of the first stimulus
    first_orientation = np.random.choice(['135', '45'])
    this_exp.addData('first_orientation', first_orientation)

    # Save right-left to simplify analysis
    if first_orientation == '45' and first_color == 'black':
        correct_response = 'right'
    elif first_orientation == '135' and first_color == 'black':
        correct_response = 'left'
    elif first_orientation == '45' and first_color == 'white':
        correct_response = 'left'
    elif first_orientation == '135' and first_color == 'white':
        correct_response = 'right'
    this_exp.addData('correct_response', correct_response)

    # Visual field
    this_side = np.random.choice(['up', 'down'])
    this_exp.addData('visual_field', this_side)

    # Spatial frequency
    this_spatial_frequency = this_trial[0]
    this_exp.addData('spatial_frequency', this_spatial_frequency)

    # Prepare stimulus sequence from the dictionary of all possible stimuli
    first_stim_name = list(
        filter(lambda x: first_color in x and first_orientation in x and this_side in x and this_spatial_frequency in x,
               list(stimuli.keys())))[0]
    second_stim_name = list(
        filter(lambda x: first_color not in x and first_orientation not in x and this_side in x and
                         this_spatial_frequency in x, list(stimuli.keys())))[0]

    first_stim = stimuli[first_stim_name]
    first_stim = [eval(first_stim[0]), eval(first_stim[1])]

    second_stim = stimuli[second_stim_name]
    second_stim = [eval(second_stim[0]), eval(second_stim[1])]

    this_exp.addData('first_stim', first_stim_name)
    this_exp.addData('second_stim', second_stim_name)

    # Blank screen
    for i in range(30):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Duration of fixation
    flength = 1 + random.random()

    # Draw a fixation cross
    my_clock.reset()
    while my_clock.getTime() < flength:
        fix.draw()
        kb.clearEvents(eventType='keyboard')
        kb.clock.reset()
        win.flip()

    # Duration of individual stimulus
    stimulus_frame_duration = this_trial[2]
    this_exp.addData('stimulus_frame_duration', stimulus_frame_duration)

    # Draw stimuli in rapid alternation
    for c in range(cycle_number):
        show_stim(first_stim, stimulus_frame_duration)
        show_stim(second_stim, stimulus_frame_duration)

    # Draw a mask if the trial is masked
    if is_masked:
        for i in range(30):  # Define the duration of the mask in frames, 250 ms
            fix.draw()
            mask_up.draw()
            mask_down.draw()
            win.flip()

    # Blank screen
    for i in range(30):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Was black paired with left or right
    display_question()

    # Proceed to next line of the output file
    this_exp.nextEntry()

    # When all trials are done break loop
    if not len(trial_list):
        break

    # Breaks
    my_clock.reset()
    if trial_count == 200 or trial_count == 400 or trial_count == 600:
        while my_clock.getTime() < 60:
            display_break('You reached a 1-minute break.')
        else:
            display_instr('Press SPACE when you are ready to continue with the experiment.')

# ==============================================================================
# CIAO!
# ==============================================================================
display_instr('This is the END of the experiment.'
              '\n\n\n\n Press SPACE to close the experiment.')
