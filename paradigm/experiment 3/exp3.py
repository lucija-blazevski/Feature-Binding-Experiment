"""
Created on Mon May 23rd, 2023

Project:         Feature binding is slow: temporal integration explains apparent ultrafast binding - Experiment 2
Authors:         Lucija Blaževski
Notes:           Version of the experiment with 3 (SF: low, medium, and high) x 2 (mask: high or low) x 2 (Cycle number: 1, 2, 3)
                 factors to calculate the minimum stimulus duration necessary for 75% accuracy in reports.
Acknowledgments: Special thanks to Nicolas Sanchez-Fuenzalida for providing the staircase
                 function.
                 
"""

# ==============================================================================
# IMPORT STATEMENTS
# ==============================================================================
# Import necessary Python libraries and PsychoPy modules for the experiment
from psychopy import visual, event, tools, data, core, gui, logging, __version__, monitors
from psychopy.tools.colorspacetools import dkl2rgb
from psychopy.hardware import keyboard
import numpy as np
import random, os

# ==============================================================================
# MONITOR SETUP
# ==============================================================================
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
# PRACTICE CHOICE
# ==============================================================================
practice = True

# ==============================================================================
# DATA AND GUI SETUP
# ==============================================================================
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Create data folder if it does not exist
if not os.path.isdir('data'):
    os.mkdir('data')

# Store info about the experiment session
psychopyVersion = __version__
expName = 'Exp3'

# Default values for gui
expInfo = {"Gender": ["Female", "Male", 'Other', 'Prefer not to say'],
           "Handedness": ["Right", "Left"],
           "Age": 0,

           'frame_rate': 165,
           'participant': '00',
           'session': 'Exp3'}

# Open gui
if True:
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if not dlg.OK:
        core.quit()  # user pressed cancel

expInfo['date'] = data.getDateStr()  # Add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
# Save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
# An ExperimentHandler isn't essential but helps with data saving
this_exp = data.ExperimentHandler(name=expName, version='',
                                  extraInfo=expInfo,
                                  runtimeInfo=None,
                                  originPath=_thisDir + '/Exp3.py',
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

# Covers in the color of the background used to cover one part of the circle and get a semi-circle
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

# Grating resolution
grating_res = 1024

# 'cycles' argument determines the spatial frequency here
# It can be combined with the 'sf' argument of visual.GratingStim, but it is suggested to change only one
grating_lowSF = visual.filters.makeGrating(res=grating_res, cycles=1, gratType='sqr')
grating_medSF = visual.filters.makeGrating(res=grating_res, cycles=3, gratType='sqr')
grating_highSF = visual.filters.makeGrating(res=grating_res, cycles=5, gratType='sqr')



# Low Spatial Frequency White Texture
hsv_tex_white_low = np.ones((grating_res, grating_res, 3))
hsv_tex_white_low[..., 1] = 0  # Saturation to 0 for white
hsv_tex_white_low[..., 2] = (grating_lowSF + 1) / 2.0 * 0.5 + 0.5  # Value based on low SF

# High Spatial Frequency White Texture
hsv_tex_white_high = np.ones((grating_res, grating_res, 3))
hsv_tex_white_high[..., 1] = 0  # Saturation to 0 for white
hsv_tex_white_high[..., 2] = (grating_highSF + 1) / 2.0 * 0.5 + 0.5  # Value based on high SF

# Medium Spatial Frequency White Texture
hsv_tex_white_med = np.ones((grating_res, grating_res, 3))
hsv_tex_white_med[..., 1] = 0  # Saturation to 0 for white
hsv_tex_white_med[..., 2] = (grating_medSF + 1) / 2.0 * 0.5 + 0.5  # Value based on medium SF

# Generate visual stimuli for white textures
# Upper visual field, low, medium, and high SF, oriented at 45 and 135 degrees
si_white_low_135_up, si_white_low_45_up, si_white_med_135_up, si_white_med_45_up, si_white_high_135_up, si_white_high_45_up = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, 0.3), tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in zip([135, 45, 135, 45, 135, 45], [hsv_tex_white_low, hsv_tex_white_low, hsv_tex_white_med, hsv_tex_white_med, hsv_tex_white_high, hsv_tex_white_high])
]

# Lower visual field, low, medium, and high SF, oriented at 45 and 135 degrees
si_white_low_135_down, si_white_low_45_down, si_white_med_135_down, si_white_med_45_down, si_white_high_135_down, si_white_high_45_down = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, -0.3), tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in zip([135, 45, 135, 45, 135, 45], [hsv_tex_white_low, hsv_tex_white_low, hsv_tex_white_med, hsv_tex_white_med, hsv_tex_white_high, hsv_tex_white_high])
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

# Medium Spatial Frequency Black Texture
hsv_tex_black_med = np.zeros((grating_res, grating_res, 3))
hsv_tex_black_med[..., 2] = (grating_medSF + 1) / 2.0 * 0.5  # Value based on medium SF

# Generate visual stimuli for black textures
# Upper visual field, low, medium, and high SF, oriented at 45 and 135 degrees
si_black_low_45_up, si_black_low_135_up, si_black_med_45_up, si_black_med_135_up, si_black_high_45_up, si_black_high_135_up = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, 0.3), tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in zip([45, 135, 45, 135, 45, 135], [hsv_tex_black_low, hsv_tex_black_low, hsv_tex_black_med, hsv_tex_black_med, hsv_tex_black_high, hsv_tex_black_high])
]

# Lower visual field, low, medium, and high SF, oriented at 45 and 135 degrees
si_black_low_45_down, si_black_low_135_down, si_black_med_45_down, si_black_med_135_down, si_black_high_45_down, si_black_high_135_down = [
    visual.GratingStim(win=win, units="deg", ori=orientation, size=2.178, mask='circle', pos=(0, -0.3), tex=tools.colorspacetools.hsv2rgb(texture))
    for orientation, texture in zip([45, 135, 45, 135, 45, 135], [hsv_tex_black_low, hsv_tex_black_low, hsv_tex_black_med, hsv_tex_black_med, hsv_tex_black_high, hsv_tex_black_high])
]


# ==============================================================================
# MASKING STIMULI
# ==============================================================================
# Define the number of images to show per trial
num_images = 41  # Closest multiple of 6.606 to 250ms

# Load the HIGH SF masks
image1_high = visual.ImageStim(win, name='black_high_45',
                               image=_thisDir + '/masks_texturized/masks_exact_texturized/black_high_45.jpg', size=3.5)
image2_high = visual.ImageStim(win, name='black_high_135',
                               image=_thisDir + '/masks_texturized/masks_exact_texturized/black_high_135.jpg', size=3.5)
image3_high = visual.ImageStim(win, name='white_high_135',
                               image=_thisDir + '/masks_texturized/masks_exact_texturized/white_high_45.jpg', size=3.5)
image4_high = visual.ImageStim(win, name='white_high_135',
                               image=_thisDir + '/masks_texturized/masks_exact_texturized/white_high_135.jpg', size=3.5)

# Load the LOW SF masks
image1_low = visual.ImageStim(win, name='black_low_45',
                              image=_thisDir + '/masks_texturized/masks_exact_texturized/black_low_45.jpg', size=3.5)
image2_low = visual.ImageStim(win, name='black_low_135',
                              image=_thisDir + '/masks_texturized/masks_exact_texturized/black_low_135.jpg', size=3.5)
image3_low = visual.ImageStim(win, name='white_low_45',
                              image=_thisDir + '/masks_texturized/masks_exact_texturized/white_low_45.jpg', size=3.5)
image4_low = visual.ImageStim(win, name='white_low_135',
                              image=_thisDir + '/masks_texturized/masks_exact_texturized/white_low_135.jpg', size=3.5)

# Create a list of images and dictionary to reference it later
mask_list_high = [image1_high, image2_high, image3_high, image4_high]
mask_list_low = [image1_low, image2_low, image3_low, image4_low]
masks = {'high': mask_list_high, 'low': mask_list_low}

# ==============================================================================
# EXPERIMENTAL QUESTION
# ==============================================================================
question = visual.TextStim(win,
                           pos=(0, 0),
                           text="Was black paired with left or right?",
                           height=.07,
                           units='norm',
                           color='black')


# Collect response function in the main experiment
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
    return accuracy


# Feedback as part of practice
correctStim = visual.TextStim(win, text="CORRECT!", height=0.07, units='norm', color="green", pos=(0, 0))
incorrectStim = visual.TextStim(win, text="INCORRECT!", height=0.07, units='norm', color="red", pos=(0, 0))


# Collect response function in the practice
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


# Instructions function
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


# Break function
def display_break(text):
    instructions.text = text
    instructions.draw()
    win.flip()


# Blank screen
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


# Slightly adjusted screen set-up to allow example images
def display_example_instructions(text: object, left_image: object, right_image: object, position: object) -> object:
    """Display instructions with example stimuli."""
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
    # frame loop first gabor
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
# STAIRCASE
# ==============================================================================
# Staircase helper
class staircaseHandle:

    # Initialize staircase
    def __init__(self,
                 start_value: float = 5,
                 aimed_performance: float = .75,
                 reversals: list = [5, 25],
                 step_sizes: list = [1, 1],
                 power_law: float = 1,
                 perceived_space: int = None,
                 min_value_correction: float = 1,
                 max_value_correction: float = None,
                 name: str = 'staircase',
                 siam: bool = True,
                 custom_payoff_matrix: dict = None) -> object:
        """

        :param start_value: Value for first trial.
        :param aimed_performance: Expected hit-rate (0-1) for estimated threshold.
        :param reversals: Number of reversals to run before staircase ends. First reversals are discarded
                            when calculating the threshold.
        :param step_sizes: Step sizes to use for each number of reversals.
        :param power_law: Transformation to apply on staircased value (staircase_value ** power_law). Set to 1 when
                            perceived and absolute value is equal.
        :param perceived_space: Use this to make the step size a fraction of the current perceived staircase_value
                            (step_size = (staircase_value**power_law) / perceived_space). Set to None to use step_sizes
                            as absolute values.
        :param min_value_correction: staircase_value cannot go below this value
        :param max_value_correction: staircase_value cannot go above this value
        :param name: Staircase name for logging or for when you run multiple staircases
        :param siam: Use Kaernbach, C. (1990) single‐interval adjustment‐matrix (SIAM).
        :param custom_payoff_matrix: Alternative any contignency table can be feeded to inform the step sizes. This
                                        should be a dictionary (e.g. {'hit': -1, 'miss': 4, 'fa': 5, 'cr': 0})
                                        indicating each step size. Feeding a custom payoff matrix will override
                                        the siam argument.
        """

        # Set defaults
        if reversals is None:
            reversals = [5, 15]
        if step_sizes is None:
            step_sizes = [1, .5]

        # Save inputs
        self.name = name
        self.dv = start_value  # Staircase start value
        self.p = aimed_performance  # Goal hit-rate
        self.reversals = reversals  # Total reversals
        self.step_sizes = step_sizes  # Step sizes for first and second phase
        self.current_step_size = self.step_sizes[0]  # Assign first step size
        self.powers_law = power_law  # Power law to transform to perceived scale
        self.perceived_space = perceived_space
        self.min_corr = min_value_correction
        self.max_corr = max_value_correction
        self.siam = siam
        # Trackers
        self.phase = 0  # Only reversal values in phase 2 are used to get threshold
        self.dvs = []  # Track all staircased values
        self.dvs_on_rev = []  # Track staircased values on reversals
        self.trial_number = 0  # Trial counter
        self.revn = 0  # Reversal counter
        self.reversal_on_trial = []  # Reversal trial
        self.is_correct_track = []  # Track corr/incorr booleans
        self.stim_track = []  # Track corr/incorr booleans
        # Indicators
        self.staircase_over = False  # Staircase over?
        self.first_trial = True  # Is first trial?

        # Last ans trackers
        self.previous_is_correct = None
        self.isRev = False

        # SIAM Adjustment matrix =====================================
        # These contingency tables (except for 85) are taken from Table 1 in Kaernbach, C. (1990).
        # A single‐interval adjustment‐matrix (SIAM) procedure for unbiased adaptive testing. The
        # Journal of the Acoustical Society of America, 88(6), 2645–2655. https://doi.org/10.1121/1.399985
        self.payoff_matrices = {
            '25': {'hit': -3, 'miss': 1, 'fa': 4, 'cr': 0},
            '33': {'hit': -2, 'miss': 1, 'fa': 3, 'cr': 0},
            '50': {'hit': -1, 'miss': 1, 'fa': 2, 'cr': 0},
            '66': {'hit': -1, 'miss': 2, 'fa': 3, 'cr': 0},
            '75': {'hit': -1, 'miss': 3, 'fa': 4, 'cr': 0},
            '85': {'hit': -1, 'miss': 4, 'fa': 5, 'cr': 0}
        }

        # Either use SIAM payoff matrices defined above
        if siam:
            self.payoffs = self.payoff_matrices[str(int(aimed_performance * 100))]
        else:
            # In principle this gets you proportionally the same values as in the
            # SIAM procedure above. The only difference seems to be that all values
            # are increased until there are no decimal step sizes. So, for example,
            # when the aimed hit-rate is .25 you multiply all values by 3 to get
            # the step sizes in the SIAM procedure
            self.payoffs = {'hit': -1, 'miss': aimed_performance / (1 - aimed_performance),
                            'fa': 1 / (1 - aimed_performance), 'cr': 0}

        # Set custom payoff matrix
        if isinstance(custom_payoff_matrix, dict):
            self.payoffs = custom_payoff_matrix
            import warnings
            warnings.warn('custom_payoff_matrix detected, overriding SIAM argument.')

    def new_trial(self, is_correct: bool, stim: bool):
        """

        :param is_correct: Was the current trial correct?
        :param stim: Was the target present? Alternatively this can be used for category A
                        and B in discrimination settings.
        """
        # If staircase not over -----------------------------
        if not self.staircase_over:

            # Update trial count and save current dv
            self.trial_number += 1  # trial number
            self.dvs.append(self.dv)  # track value of current trial

            # track is correct
            self.is_correct_track.append(is_correct)
            self.stim_track.append(stim)

            # Check if first trial -----------------------------

            # In the first trial we can't check for reversals
            # because there are no previous trials.
            if not self.first_trial:

                # Check if reversal -----------------------
                if is_correct != self.previous_is_correct:
                    self.isRev = True
                    # reversal counter
                    self.revn += 1
                    # log trial with reversal
                    self.reversal_on_trial.append(self.trial_number)
                    # Only record values when in the second phase
                    if self.phase == 1:
                        # append dev value on reversal
                        self.dvs_on_rev.append(self.dv)
                else:
                    self.isRev = False

            # Confusion matrix label. This is used to get the step size
            if is_correct:
                if stim:
                    conf_mat = 'hit'
                else:
                    conf_mat = 'cr'
            else:
                if stim:
                    conf_mat = 'miss'
                else:
                    conf_mat = 'fa'

            # Update dv -----------------------------------------

            # Convert contrast to perceived contrast
            perceived = self.dv ** self.powers_law

            # When perceived_space is set the step_size is a fraction of the current
            # perceived staircase value. This is handy when the perceived scale of
            # the value being staircased is not linear. Otherwise, step_size is set to 1
            # so step_sizes are use as absolute values.
            if self.perceived_space is None:
                # Add linear step size to perceived space dv
                step_size = 1
            else:
                # Calculate step size based on current value
                step_size = perceived / self.perceived_space

            # Update value
            perceived_new = perceived + (self.payoffs[conf_mat] * self.current_step_size) * step_size

            # Convert new perceived to contrast space
            self.dv = perceived_new ** (1 / self.powers_law)

            # Min/max corrections
            if self.min_corr or self.min_corr == 0:
                if self.dv < self.min_corr: self.dv = self.min_corr
            if self.max_corr:
                if self.dv > self.max_corr: self.dv = self.max_corr

            # if max. number of reversals end staircase
            if self.revn >= sum(self.reversals):
                self.staircase_over = True

            # if first portion of reversals done continue to second phase
            if self.revn >= self.reversals[0]:
                self.phase = 1
                self.current_step_size = self.step_sizes[self.phase]

            # first trial over
            self.first_trial = False
            # store last correct/incorrect answer
            self.previous_is_correct = is_correct

    def get_threshold(self):
        """
        The staircase threshold can be calculated only when all the reversals are done. Alternatively, set
        staircase.staircase_over = True and then call staircase.get_threshold().

        :return: Staircase threshold.
        """

        if self.staircase_over:
            return np.median(self.dvs_on_rev)
        else:
            return 'Staircase is not over.'

    def print_staircase(self):
        # Print staircase info to console, use after calling new_trial

        print('\n###############################\n')
        print(self.name)
        print('Trial number: ' + str(self.trial_number))
        print('Current trial is correct: ' + str(self.previous_is_correct))
        print('Current dv value: ' + str(round(self.dv, 5)))
        print('Reversal count: ' + str(self.revn))
        print('Phase: ' + str(self.phase))
        print('Staircase over? ' + str(self.staircase_over))
        print('\n###############################\n')


# Function to log staircase
def log_staircase_info(stair):
    this_exp.addData('staircase_dv', stair.dv)
    this_exp.addData('staircase_trial_num', stair.trial_number)
    this_exp.addData('staircase_previous_correct', stair.previous_is_correct)
    #   Commented out the logging of reversals because it is delayed for one row, will save it manually during the trial
    #   this_exp.addData('staircase_reversal', stair.isRev)
    #   this_exp.addData('staircase_reversal_num', stair.revn)
    this_exp.addData('staircase_phase', stair.phase)
    this_exp.addData('staircase_step_size', stair.current_step_size)
    this_exp.addData('staircase_powers_law', stair.powers_law)
    this_exp.addData('staircase_siam', stair.siam)
    this_exp.addData('staircase_over', stair.staircase_over)
    this_exp.addData('staircase_name', stair.name)
    this_exp.addData('staircase_conv_p', stair.p)
    # Step sizes
    this_exp.addData('staircase_step_hit', stair.payoffs['hit'])
    this_exp.addData('staircase_step_miss', stair.payoffs['miss'])


# Create staircases
staircase_low_1_mask_low = staircaseHandle(name='low_1_mask_low', start_value=8)
staircase_low_2_mask_low = staircaseHandle(name='low_2_mask_low', start_value=3)
staircase_low_3_mask_low = staircaseHandle(name='low_3_mask_low', start_value=3)

staircase_low_1_mask_high = staircaseHandle(name='low_1_mask_high', start_value=8)
staircase_low_2_mask_high = staircaseHandle(name='low_2_mask_high', start_value=3)
staircase_low_3_mask_high = staircaseHandle(name='low_3_mask_high', start_value=3)

staircase_high_1_mask_low = staircaseHandle(name='high_1_mask_low', start_value=12)
staircase_high_2_mask_low = staircaseHandle(name='high_2_mask_low', start_value=8)
staircase_high_3_mask_low = staircaseHandle(name='high_3_mask_low', start_value=8)

staircase_high_1_mask_high = staircaseHandle(name='high_1_mask_high', start_value=12)
staircase_high_2_mask_high = staircaseHandle(name='high_2_mask_high', start_value=8)
staircase_high_3_mask_high = staircaseHandle(name='high_3_mask_high', start_value=8)

staircase_med_1_mask_low = staircaseHandle(name='med_1_mask_low', start_value=12)
staircase_med_2_mask_low = staircaseHandle(name='med_2_mask_low', start_value=8)
staircase_med_3_mask_low = staircaseHandle(name='med_3_mask_low', start_value=8)

staircase_med_1_mask_high = staircaseHandle(name='med_1_mask_high', start_value=12)
staircase_med_2_mask_high = staircaseHandle(name='med_2_mask_high', start_value=8)
staircase_med_3_mask_high = staircaseHandle(name='med_3_mask_high', start_value=8)

stairs = [staircase_low_1_mask_low, staircase_low_2_mask_low, staircase_low_3_mask_low,
          staircase_low_1_mask_high, staircase_low_2_mask_high, staircase_low_3_mask_high,
          staircase_high_1_mask_low, staircase_high_2_mask_low, staircase_high_3_mask_low,
          staircase_high_1_mask_high, staircase_high_2_mask_high, staircase_high_3_mask_high,
          staircase_med_1_mask_low, staircase_med_2_mask_low, staircase_med_3_mask_low,
          staircase_med_1_mask_high, staircase_med_2_mask_high, staircase_med_3_mask_high]

# ==============================================================================
# COUNTER-BALANCING AND TRIAL PREPARATION
# ==============================================================================
color = ['white', 'black']
spatial_frequency = ['low', 'med', 'high']
side = ['135', '45']
visual_field = ['up', 'down']
stimuli = {f'{a}_{b}_{c}_{d}': [f'si_{a}_{b}_{c}_{d}', f'wedge_cover_{d}'] for a in color for b in spatial_frequency for
           c in side for d in visual_field}

# Main experiment conditions (x for SF, y for the number of cycles, z for the SF of the mask)
conditions = [[x, y, z] for x in ['low', 'high', 'med'] for y in [1, 2, 3] for z in ['low', 'high']]
trial_list = conditions * 100
np.random.shuffle(trial_list)

# Practice 3 conditions
practice3_conditions = [[x, y, z, u] for x in ['low', 'high', 'med'] for y in [1, 2, 3] for z in [5] for u in
                        ['high', 'low']]
practice3_trial_list = practice3_conditions
np.random.shuffle(practice3_trial_list)

# ==============================================================================
# START
# ==============================================================================
if practice:

    # INSTRUCTIONS
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

    display_example_instructions(
        'On every trial, each color will always be paired with only one orientation. For example, '
        'in one trial you can see black leftward-pointing stripes alternating with white '
        'rightward-pointing '
        'stripes, as illustrated bellow.'
        '\n\n\n\n\n\n\n\n\n\n\n\nPress SPACE to continue.', left_image=example_black_left_up,
        right_image=example_white_right_up, position=(0, 0))

    display_example_instructions(
        'In another trial, this can be reversed and you could see white leftward-pointing stripes '
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
    # PRACTICE SESSION 1
    # ==============================================================================
    # Trial and correct answers counter
    hit_counter = 0
    while True:
        if hit_counter >= 10:
            break

        practice1_conditions = [[x, y, z, u] for x in ['low', 'high', 'med'] for y in [1] for z in [160] for u in
                                ['high', 'low']]
        practice1_trial_list = practice1_conditions * 5
        np.random.shuffle(practice1_trial_list)
        practice_trial_count = -1
        hit_counter = 0

        # Run trials
        while True:
            practice_trial_count += 1
            this_trial_practice = practice1_trial_list.pop()

            # Mask
            mask_practice = this_trial_practice[3]
            this_mask = masks[mask_practice]
            random.shuffle(this_mask)

            # Cycle number
            cycle_number_practice = this_trial_practice[1]

            # Get the phase
            phase = random.random()

            # Color of the first stimulus
            first_color_practice = np.random.choice(['black', 'white'])
            first_orientation_practice = np.random.choice(['135', '45'])
            if first_orientation_practice == '45' and first_color_practice == 'black':  # Save right-left to simplify analysis
                correct_response = 'right'
            elif first_orientation_practice == '135' and first_color_practice == 'black':
                correct_response = 'left'
            elif first_orientation_practice == '45' and first_color_practice == 'white':
                correct_response = 'left'
            elif first_orientation_practice == '135' and first_color_practice == 'white':
                correct_response = 'right'
            this_side_practice = np.random.choice(['up', 'down'])
            this_spatial_frequency_practice = this_trial_practice[0]
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
            for i in range(41):  # Define the duration of the blank screen, 250 ms
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

            # Define duration of the individual stimulus
            stimulus_frame_duration_practice = this_trial_practice[2]

            # Show stimuli sequence
            for c in range(cycle_number_practice):
                show_stim(first_stim_practice, stimulus_frame_duration_practice)
                show_stim(second_stim_practice, stimulus_frame_duration_practice)

            # Show mask
            for i in range(num_images):
                image = this_mask[i % len(this_mask)]
                image.draw()
                win.flip()

            # Blank screen
            for i in range(41):  # Define the duration of the blank screen, 250 ms
                blank.draw()
                win.flip()

            # Was left paired with left or right?
            input = display_question_practice()
            hit_counter += input

            # Reset hit_counter if error
            if not input:
                hit_counter = 0

            # Stop if 10 hits reached
            if hit_counter >= 10:
                break

            # When all trials are done break loop
            if practice_trial_count == 30:
                display_instr('In the last 30 trials, you did not succeed to have 10 correct responses in a row. '
                              'Please call the experimentator. ')
                break

    display_instr('This is the end of the first practice block. You responded correctly on 10 trials in a row.'
                  '\n\n\n\nPress SPACE to continue')

    # ==============================================================================
    # PRACTICE SESSION 2
    # ==============================================================================
    display_instr('The next practice block will resemble the actual experiment more. Your task remains the same - '
                  'You should detect the orientation of black stripes and respond with the LEFT or RIGHT arrow key '
                  'accordingly. You will still receive feedback. You will be able to continue with the experiment only '
                  'if you perform well enough on this practice block.'
                  '\n\n\n\nPress SPACE to start the second practice block')

    # Trial and correct answers counter
    practice_trial_count = -1
    hit_counter = 0
    while True:
        if ((practice_trial_count + 1) > 10) and (hit_counter / (practice_trial_count + 1) >= 0.8):
            break
        practice2_conditions = [[x, y, z, u] for x in ['low', 'high', 'med'] for y in [2, 3, 4] for z in [40, 80] for u
                                in
                                ['high', 'low']]
        practice2_trial_list = practice2_conditions * 80
        np.random.shuffle(practice2_trial_list)
        practice_trial_count = -1
        hit_counter = 0

        # Run trials
        while True:
            if hit_counter >= 10:
                break

            while True:
                practice_trial_count += 1
                this_trial_practice = practice2_trial_list.pop()

                # Mask
                mask_practice = this_trial_practice[3]
                this_mask = masks[mask_practice]
                random.shuffle(this_mask)

                # Get the phase
                phase = random.random()

                cycle_number_practice = this_trial_practice[1]
                first_color_practice = np.random.choice(['black', 'white'])
                first_orientation_practice = np.random.choice(['135', '45'])
                if first_orientation_practice == '45' and first_color_practice == 'black':  # Save right-left to simplify analysis
                    correct_response = 'right'
                elif first_orientation_practice == '135' and first_color_practice == 'black':
                    correct_response = 'left'
                elif first_orientation_practice == '45' and first_color_practice == 'white':
                    correct_response = 'left'
                elif first_orientation_practice == '135' and first_color_practice == 'white':
                    correct_response = 'right'
                this_side_practice = np.random.choice(['up', 'down'])
                this_spatial_frequency_practice = this_trial_practice[0]
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
                for i in range(41):  # Define the duration of the blank screen, 250 ms
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

                stimulus_frame_duration_practice = this_trial_practice[2]

                for c in range(cycle_number_practice):
                    show_stim(first_stim_practice, stimulus_frame_duration_practice)
                    show_stim(second_stim_practice, stimulus_frame_duration_practice)

                # Show mask
                for i in range(num_images):
                    image = this_mask[i % len(this_mask)]
                    image.draw()
                    win.flip()

                # Blank screen
                for i in range(41):  # Define the duration of the blank screen, 250 ms
                    blank.draw()
                    win.flip()

                # Was left paired with left or right
                input = display_question_practice()
                hit_counter += input

                if ((practice_trial_count + 1) > 10) and (hit_counter / (practice_trial_count + 1) >= 0.8):
                    break

                # When all trials are done break loop
                if practice_trial_count == 30:
                    display_instr('In the last 30 trials, you did not succeed to have 80% correct responses. '
                                  'Please call the experimentator. ')
                    break

    display_instr('This is the end of the second practice block. You performed well enough to continue with the '
                  'experiment.'
                  '\n\n\n\nPress SPACE to continue')

    # ==============================================================================
    # PRACTICE SESSION 3
    # ==============================================================================
    display_instr('In the final practice block you will see examples from the actual experiment. As you will see,'
                  ' stimuli are sometimes shown very quickly and, thus, the orientation might be difficult to detect. '
                  'You should respond as accurately as possible, but try not thinking too much about your response. '
                  '\n\n\n\nPress SPACE to start the third practice block')
    practice_trial_count = -1

    # Run trials
    while True:
        practice_trial_count += 1
        this_trial_practice = practice3_trial_list.pop()

        # Mask
        mask_practice = this_trial_practice[3]
        this_mask = masks[mask_practice]
        random.shuffle(this_mask)

        # Get the phase
        phase = random.random()

        cycle_number_practice = this_trial_practice[1]
        first_color_practice = np.random.choice(['black', 'white'])
        first_orientation_practice = np.random.choice(['135', '45'])
        if first_orientation_practice == '45' and first_color_practice == 'black':  # Save right-left to simplify analysis
            correct_response = 'right'
        elif first_orientation_practice == '135' and first_color_practice == 'black':
            correct_response = 'left'
        elif first_orientation_practice == '45' and first_color_practice == 'white':
            correct_response = 'left'
        elif first_orientation_practice == '135' and first_color_practice == 'white':
            correct_response = 'right'
        this_side_practice = np.random.choice(['up', 'down'])
        this_spatial_frequency_practice = this_trial_practice[0]
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
        for i in range(41):  # Define the duration of the blank screen, 250 ms
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

        stimulus_frame_duration_practice = this_trial_practice[2]

        for c in range(cycle_number_practice):
            show_stim(first_stim_practice, stimulus_frame_duration_practice)
            show_stim(second_stim_practice, stimulus_frame_duration_practice)

        # Show mask
        for i in range(num_images):
            image = this_mask[i % len(this_mask)]
            image.draw()
            win.flip()

        # Blank screen
        for i in range(41):  # Define the duration of the blank screen, 250 ms
            blank.draw()
            win.flip()

        # Was left paired with left or right
        display_question_practice()

        # When all trials are done break loop
        if practice_trial_count == 6:
            break

    display_instr("This is the end of the last practice session."
                  " Now you will start with the actual experiment. You will not receive the feedback anymore. "
                  "You will have 6 breaks throughout the task. "
                  ""
                  "\n\n\nRemember to "
                  "respond using LEFT or RIGHT arrow keys, according to the orientation of BLACK stripes. "
                  'You should respond as accurately as possible, but try not thinking too much about your response. '
                  "\n\n\n\nPRESS SPACE TO START THE EXPERIMENT")

# ==============================================================================
# EXPERIMENT
# ==============================================================================
# Trial counter
trial_count = -1

# Initial value for the loop to start
all_staircases_over = False

while True:

    # Increase the trial count
    trial_count += 1
    this_exp.addData('trial_number', trial_count)

    # Choose the condition
    this_trial = trial_list.pop()
    this_exp.addData('trial_type', this_trial)

    # Actual trial
    cycle_number = this_trial[1]
    this_exp.addData('cycle_number', cycle_number)

    # Color of the first stimulus
    first_color = np.random.choice(['black', 'white'])
    this_exp.addData('first_color', first_color)

    # Get the phase
    phase = random.random()
    this_exp.addData('phase', phase)

    # Orientation of the first stimulus
    first_orientation = np.random.choice(['135', '45'])
    this_exp.addData('first_orientation', first_orientation)

    # Correct response
    if first_orientation == '45' and first_color == 'black':  # Save right-left to simplify analysis
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

    # Type of mask
    mask_type = this_trial[2]
    this_exp.addData('mask_type', mask_type)
    this_mask = masks[mask_type]
    random.shuffle(this_mask)
    this_exp.addData('mask_images', '-'.join([x.name for x in this_mask]))

    # Prepare stimulus sequence from the dictionary of all possible stimuli
    first_stim_name = list(
        filter(lambda x: first_color in x and first_orientation in x and this_side in x and this_spatial_frequency in x,
               list(stimuli.keys())))[0]
    second_stim_name = list(
        filter(lambda x: first_color not in x and first_orientation not in x and this_side in x and
                         this_spatial_frequency in x, list(stimuli.keys())))[0]

    first_stim = stimuli[first_stim_name]
    first_stim = [eval(first_stim[0]), eval(first_stim[1])]
    first_stim[0].phase = phase

    second_stim = stimuli[second_stim_name]
    second_stim = [eval(second_stim[0]), eval(second_stim[1])]
    second_stim[0].phase = phase

    this_exp.addData('first_stim', first_stim_name)
    this_exp.addData('second_stim', second_stim_name)

    # Get staircase
    current_staircase = eval(f'staircase_{this_spatial_frequency}_{cycle_number}_mask_{mask_type}')

    # Get number of frames with staircase; staircase object.dv will be stimulus_frame_duration input
    stimulus_frame_duration = current_staircase.dv
    this_exp.addData('stimulus_frame_duration', stimulus_frame_duration)

    # Blank screen
    for i in range(41):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Duration of fixation
    flength = 1 + random.random()
    this_exp.addData('fixation_duration', flength)
    my_clock.reset()
    while my_clock.getTime() < flength:
        fix.draw()
        kb.clearEvents(eventType='keyboard')
        kb.clock.reset()
        win.flip()

    # Show stimuli sequence
    for c in range(cycle_number):
        show_stim(first_stim, stimulus_frame_duration)
        show_stim(second_stim, stimulus_frame_duration)

    # Prepare saving of the mask
    time_mask = {'mask_start': None, 'mask_end': None}
    win.timeOnFlip(time_mask, 'mask_start')

    # Show the mask
    # Loop over the images and present each one for one frame
    for i in range(num_images):
        image = this_mask[i % len(this_mask)]
        image.draw()
        win.flip()

    # End of mask timing
    win.timeOnFlip(time_mask, 'mask_end')

    # Blank screen
    for i in range(41):  # Define the duration of the blank screen, 250 ms
        blank.draw()
        win.flip()

    # Calculate the duration of the mask
    mask_duration = time_mask['mask_end'] - time_mask['mask_start']
    this_exp.addData('mask_duration', mask_duration)

    # Was left paired with left or right
    input = display_question()

    # Log staircase
    log_staircase_info(stair=current_staircase)

    # Update staircase
    current_staircase.new_trial(is_correct=input, stim=True)

    # Manually save reversals because the function has a lag
    this_exp.addData('staircase_reversal', current_staircase.isRev)
    this_exp.addData('staircase_reversal_num', current_staircase.revn)

    # If all staircases are over
    if all([x.staircase_over for x in stairs]):
        all_staircases_over = True

        # Log staircase threshold
        this_exp.addData('threshold_low1_mask_low', staircase_low_1_mask_low.get_threshold())
        this_exp.addData('threshold_low2_mask_low', staircase_low_2_mask_low.get_threshold())
        this_exp.addData('threshold_low3_mask_low', staircase_low_3_mask_low.get_threshold())

        this_exp.addData('threshold_high1_mask_low', staircase_high_1_mask_low.get_threshold())
        this_exp.addData('threshold_high2_mask_low', staircase_high_2_mask_low.get_threshold())
        this_exp.addData('threshold_high3_mask_low', staircase_high_3_mask_low.get_threshold())

        this_exp.addData('threshold_low1_mask_high', staircase_low_1_mask_high.get_threshold())
        this_exp.addData('threshold_low2_mask_high', staircase_low_2_mask_high.get_threshold())
        this_exp.addData('threshold_low3_mask_high', staircase_low_3_mask_high.get_threshold())

        this_exp.addData('threshold_high1_mask_high', staircase_high_1_mask_high.get_threshold())
        this_exp.addData('threshold_high2_mask_high', staircase_high_2_mask_high.get_threshold())
        this_exp.addData('threshold_high3_mask_high', staircase_high_3_mask_high.get_threshold())

        this_exp.addData('threshold_med1_mask_low', staircase_med_1_mask_low.get_threshold())
        this_exp.addData('threshold_med2_mask_low', staircase_med_2_mask_low.get_threshold())
        this_exp.addData('threshold_med3_mask_low', staircase_med_3_mask_low.get_threshold())

        this_exp.addData('threshold_med1_mask_high', staircase_med_1_mask_high.get_threshold())
        this_exp.addData('threshold_med2_mask_high', staircase_med_2_mask_high.get_threshold())
        this_exp.addData('threshold_med3_mask_high', staircase_med_3_mask_high.get_threshold())

    # Proceed to next line of the output file
    this_exp.nextEntry()

    # Break halfway through the block
    my_clock.reset()
    if trial_count in [250, 500, 750, 1000, 1250, 1500]:
        while my_clock.getTime() < 60:
            display_break('You reached a 1-minute break.')
        else:
            display_instr('Press SPACE when you are ready to continue with the experiment')

    # If all staircases are over break
    if all_staircases_over:
        break

    # When all trials are done break loop
    if not len(trial_list):
        # Log staircase threshold
        staircase_low_1_mask_low.staircase_over = True
        this_exp.addData('threshold_low1_mask_low', staircase_low_1_mask_low.get_threshold())
        staircase_low_2_mask_low.staircase_over = True
        this_exp.addData('threshold_low2_mask_low', staircase_low_2_mask_low.get_threshold())
        staircase_low_3_mask_low.staircase_over = True
        this_exp.addData('threshold_low3_mask_low', staircase_low_3_mask_low.get_threshold())

        staircase_low_1_mask_high.staircase_over = True
        this_exp.addData('threshold_low1_mask_high', staircase_low_1_mask_high.get_threshold())
        staircase_low_2_mask_high.staircase_over = True
        this_exp.addData('threshold_low2_mask_high', staircase_low_2_mask_high.get_threshold())
        staircase_low_3_mask_high.staircase_over = True
        this_exp.addData('threshold_low3_mask_high', staircase_low_3_mask_high.get_threshold())

        staircase_high_1_mask_low.staircase_over = True
        this_exp.addData('threshold_high1_mask_low', staircase_high_1_mask_low.get_threshold())
        staircase_high_2_mask_low.staircase_over = True
        this_exp.addData('threshold_high2_mask_low', staircase_high_2_mask_low.get_threshold())
        staircase_high_3_mask_low.staircase_over = True
        this_exp.addData('threshold_high3_mask_low', staircase_high_3_mask_low.get_threshold())

        staircase_high_1_mask_high.staircase_over = True
        this_exp.addData('threshold_high1_mask_high', staircase_high_1_mask_high.get_threshold())
        staircase_high_2_mask_high.staircase_over = True
        this_exp.addData('threshold_high2_mask_high', staircase_high_2_mask_high.get_threshold())
        staircase_high_3_mask_high.staircase_over = True
        this_exp.addData('threshold_high3_mask_high', staircase_high_3_mask_high.get_threshold())

        staircase_med_1_mask_low.staircase_over = True
        this_exp.addData('threshold_med1_mask_low', staircase_med_1_mask_low.get_threshold())
        staircase_med_2_mask_low.staircase_over = True
        this_exp.addData('threshold_med2_mask_low', staircase_med_2_mask_low.get_threshold())
        staircase_med_3_mask_low.staircase_over = True
        this_exp.addData('threshold_med3_mask_low', staircase_med_3_mask_low.get_threshold())

        staircase_med_1_mask_high.staircase_over = True
        this_exp.addData('threshold_med1_mask_high', staircase_med_1_mask_high.get_threshold())
        staircase_med_2_mask_high.staircase_over = True
        this_exp.addData('threshold_med2_mask_high', staircase_med_2_mask_high.get_threshold())
        staircase_med_3_mask_high.staircase_over = True
        this_exp.addData('threshold_med3_mask_high', staircase_med_3_mask_high.get_threshold())
        break

# ==============================================================================
# CIAO!
# ==============================================================================
display_instr('This is the END of the experiment. '
              '\n\n\n\n Press SPACE to close the experiment')


