############################################################################################################################################
# Game Title:
# Super Sky Squadron II - The Flying Ace Follies
# 
# High Scores (missions):
# Ace Aviators - for the "high scores" screen from missions?
#
# For the missions - Aerial Ace Adventures
# For the pvp - Biplane Battle Royale
# For the pvp - Sky Saviors: The Biplane Brawl
# For the pvp - Dogfight Dash
#
# https://kenney.itch.io/ship-mixer
#
# Transporter-5
# MDowOjAvMTA6MDowLzM6MDowLzk6MDowLzA6MDowL3wwOjEzLzE6MTMvMjoxMy8zOjAvNDo1LzU6LTEv
#############################################################################################################################################
import pygame
import argparse

import xml.etree.ElementTree as element_tree

#Import of Key Constants to make evaluation a bit easier
from pygame.locals import (
    K_ESCAPE, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12,
    K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_MINUS, K_PLUS,
    K_w, K_a, K_s, K_d,
    K_m,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_SPACE, K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_LSHIFT, K_RSHIFT,
    KMOD_SHIFT, KMOD_CTRL, KMOD_ALT,
    KEYDOWN, KEYUP, QUIT
)

######################################################################
# Classes Created to support game objects
######################################################################
class Plane(pygame.sprite.Sprite):
  PLANE_DEATH_TTL = 1000

  def __init__(self, x, y, rotation, style):
    super().__init__()
    self.x = x
    self.y = y
    self.speed_x = 0
    self.speed_y = 0
    self.health = 0
    self.rotation = rotation
    self.style = style

  def set_location(self, x, y):
    self.x = x
    self.y = y

  def set_location_delta(self, x, y):
    self.set_location(self.x + x, self.y + y)

  def set_rotation(self, rotation):
    self.rotation = rotation
    if self.rotation < 0:
      self.rotation = 0
    if self.rotation > 360:
      self.rotation = 360
  
  def set_rotation_delta(self, rotation):
    self.set_rotation(self.rotation + rotation)

  def copy(self):
    plane = Plane(self.x, self.y, self.rotation, self.style)
    return plane

######################################################################
# Rotate from Center 
# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
######################################################################
def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  
    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

######################################################################
# Functions Created to support game initialization and transitions
######################################################################
def reset_game_state():
  global GAME_STATE
  GAME_STATE['LAYER_1'] = True 
  GAME_STATE['LAYER_2'] = True 
  GAME_STATE['LAYER_3'] = True 
  GAME_STATE['LAYER_4'] = True 
  GAME_STATE['LAYER_5'] = True 
  GAME_STATE['RUNNING'] = True 
  GAME_STATE['GAME_OVER'] = False
  GAME_STATE['PAUSED'] = False
  GAME_STATE['MULTIPLAYER'] = False

def reset_screens():
  global GAME_STATE
  GAME_STATE['TITLE_SCREEN'] = False
  GAME_STATE['GAME_MODE_SCREEN'] = False
  GAME_STATE['INSTRUCTIONS_SCREEN'] = False
  GAME_STATE['DOG_FIGHT'] = False
  GAME_STATE['MISSION'] = False

def reset_transitions():
  global GAME_STATE
  GAME_STATE['TRANSITION_TO_TITLE_SCREEN'] = False
  GAME_STATE['TRANSITION_TO_GAME_MODE_SCREEN'] = False
  GAME_STATE['TRANSITION_TO_INSTRUCTIONS_SCREEN'] = False
  GAME_STATE['TRANSITION_TO_DOGFIGHT_MODE'] = False
  GAME_STATE['TRANSITION_TO_MISSION_MODE'] = False
  GAME_STATE_TRANSITION_TTL['TRANSITION_TO_TITLE_SCREEN'] = TTL_DEFAULTS['TRANSITION_TO_TITLE_SCREEN']
  GAME_STATE_TRANSITION_TTL['TRANSITION_TO_GAME_MODE_SCREEN'] = TTL_DEFAULTS['TRANSITION_TO_GAME_MODE_SCREEN']
  GAME_STATE_TRANSITION_TTL['TRANSITION_TO_INSTRUCTIONS_SCREEN'] = TTL_DEFAULTS['TRANSITION_TO_INSTRUCTIONS_SCREEN']
  GAME_STATE_TRANSITION_TTL['TRANSITION_TO_DOGFIGHT_MODE'] = TTL_DEFAULTS['TRANSITION_TO_DOGFIGHT_MODE']
  GAME_STATE_TRANSITION_TTL['TRANSITION_TO_MISSION_MODE'] = TTL_DEFAULTS['TRANSITION_TO_MISSION_MODE']

def stop_all_sounds():
  return

def destroy_dogfight_objects():
  return

def destroy_mission_objects():
  return

def destroy_mission_level_objects():
  return

def destroy_all():
  return

def reset_players():
  return

def reset_for_game_state_transition():
  destroy_all()
  reset_screens()
  reset_transitions()
  stop_all_sounds()

def initialize_title_screen():
  global GAME_STATE
  global press_start_color
  global press_start_blink_ttl

  press_start_color = GAME_COLORS['SHMUP_ROYAL_PURPLE']
  press_start_blink_ttl = TTL_DEFAULTS['PRESS_START_BLINK']

  reset_for_game_state_transition()
  reset_players()
  
  GAME_STATE['TITLE_SCREEN'] = True


######################################################################
# ***LESSON 0 - Argument Parsing***
#
# Argument parsing to make running the game in different modes 
# slightly easier
######################################################################

argument_parser = argparse.ArgumentParser(description="CodeMash 2025 Divez - So you want to make video games? - Super Sky Squadron II: The Flying Ace Follies")

argument_parser.add_argument("--test", "--test-mode", help="Enter Test/Dev Mode (Also turned on with any debug flag)", action="store_true", dest="test_mode")
argument_parser.add_argument("--debug", help="Enter Debug Mode", action="store_true", dest="debug")
argument_parser.add_argument("--debug-grid", help="Show Debug Grid", action="store_true", dest="debug_grid")
argument_parser.add_argument("--debug-to-console", help="Debug to Console only (does not need to be used in conjunction with --debug, does not debug events)", action="store_true", dest="debug_to_console")
argument_parser.add_argument("--debug-events", help="Debug Events to Console (does not need --debug or --debug-to-console)", action="store_true", dest="debug_events")
argument_parser.add_argument("--debug-events-verbose", help="Debug All Events with its Data to Console (does not need --debug or --debug-to-console or --debug-events)", action="store_true", dest="debug_events_verbose")
argument_parser.add_argument("--mute-audio", help="Mute all Sounds", action="store_true", dest="mute_audio")
argument_parser.add_argument("--no-frame", help="Remove any windowing system framing", action="store_true", dest="no_frame")
argument_parser.add_argument("--full-screen", help="Go Full Screen Mode", action="store_true", dest="full_screen")
argument_parser.add_argument("--double-buffer", help="Enable Double Buffering", action="store_true", dest="double_buffer")
argument_parser.add_argument("--disable-joystick", help="Disable Joystick Activity", action="store_true", dest="disable_joystick")

######################################################################
# PARSE GAME CLI ARGUMENTS
######################################################################
GAME_CLI_ARGUMENTS = argument_parser.parse_args()

#Game Constants are generally held within this dictionary
#These are 'indexed' by GAME_CONSTANTS['KEY']
######################################################################
# ***LESSON 3*** - SCREEN COORDINATES
######################################################################
GAME_CONSTANTS = {'SCREEN_WIDTH': 1280, 'SCREEN_HEIGHT': 720, 'SCREEN_FLAGS': 0, 'SQUARE_SIZE': 32,
                  'MAX_CONNECTED_JOYSTICKS': 2}

####### Generate the Debug Grid in a clever way
GAME_CONSTANTS['DEBUG_GRID'] = []
for width in range(0,int(GAME_CONSTANTS['SCREEN_WIDTH']/GAME_CONSTANTS['SQUARE_SIZE'])):
  GAME_CONSTANTS['DEBUG_GRID'].append([width * GAME_CONSTANTS['SQUARE_SIZE'], 0])
  GAME_CONSTANTS['DEBUG_GRID'].append([width * GAME_CONSTANTS['SQUARE_SIZE'], GAME_CONSTANTS['SCREEN_HEIGHT']])
  GAME_CONSTANTS['DEBUG_GRID'].append([(width+1) * GAME_CONSTANTS['SQUARE_SIZE'], GAME_CONSTANTS['SCREEN_HEIGHT']])
  GAME_CONSTANTS['DEBUG_GRID'].append([(width+1) * GAME_CONSTANTS['SQUARE_SIZE'], 0])
  GAME_CONSTANTS['DEBUG_GRID'].append([(width+2) * GAME_CONSTANTS['SQUARE_SIZE'], 0])
for height in range(0,int(GAME_CONSTANTS['SCREEN_HEIGHT']/GAME_CONSTANTS['SQUARE_SIZE'])):
  GAME_CONSTANTS['DEBUG_GRID'].append([0, height * GAME_CONSTANTS['SQUARE_SIZE']])
  GAME_CONSTANTS['DEBUG_GRID'].append([GAME_CONSTANTS['SCREEN_WIDTH'], height * GAME_CONSTANTS['SQUARE_SIZE']])
  GAME_CONSTANTS['DEBUG_GRID'].append([GAME_CONSTANTS['SCREEN_WIDTH'], (height+1) * GAME_CONSTANTS['SQUARE_SIZE']])
  GAME_CONSTANTS['DEBUG_GRID'].append([0, (height+1) * GAME_CONSTANTS['SQUARE_SIZE']])
  GAME_CONSTANTS['DEBUG_GRID'].append([0, (height+2) * GAME_CONSTANTS['SQUARE_SIZE']])

#Primiative Colors are held within this dictionary
#These are 'indexed' by GAME_COLORS['KEY']
GAME_COLORS = {'DEEP_PURPLE': (58, 46, 63),
               'BLACK': (0, 0, 0),
               'NOT_QUITE_BLACK': (31, 36, 38),
               'RED': (255, 0, 0),
               'GREEN': (0, 255, 0),
               'BLUE': (0, 0, 255),
               'ALMOST_BLACK': (29, 25, 35),
               'STEEL_BLUE': (94, 129, 161),
               'SHMUP_BLUE': (51, 153, 218),
               'SHMUP_RED': (218, 52, 72),
               'SHMUP_ORANGE': (218, 116, 52),
               'SHMUP_YELLOW': (218, 199, 52),
               'SHMUP_ROYAL_PURPLE': (75, 52, 218),
               'SHMUP_PURPLE': (51, 153, 218),
               'SHMUP_BLACK': (51, 51, 51)
               }

#Time to live defaults are within this dictionary
# ***LESSON***
TTL_DEFAULTS = {'TRANSITION_TO_TITLE_SCREEN': 5000, 'TRANSITION_TO_GAME_MODE_SCREEN': 1000, 'TRANSITION_TO_INSTRUCTIONS_SCREEN': 1000, 'TRANSITION_TO_DOGFIGHT_MODE': 1000, 'TRANSITION_TO_MISSION_MODE': 1000,
                'PRESS_START_BLINK': 750}

######################################################################
# SET GAME DEFAULTS
# ***LESSON 4*** - State Machine
######################################################################
#Game State is generally held within this dictionary
#These are 'indexed' by GAME_STATE['KEY']
GAME_STATE = {'DEBUG': GAME_CLI_ARGUMENTS.debug, 'DEBUG_GRID': GAME_CLI_ARGUMENTS.debug_grid, 'DEBUG_TO_CONSOLE': GAME_CLI_ARGUMENTS.debug_to_console, 'DEBUG_EVENTS': GAME_CLI_ARGUMENTS.debug_events, 'DEBUG_EVENTS_VERBOSE': GAME_CLI_ARGUMENTS.debug_events_verbose, 
              'TEST_MODE': GAME_CLI_ARGUMENTS.test_mode or GAME_CLI_ARGUMENTS.debug or GAME_CLI_ARGUMENTS.debug_grid or GAME_CLI_ARGUMENTS.debug_to_console or GAME_CLI_ARGUMENTS.debug_events or GAME_CLI_ARGUMENTS.debug_events_verbose,
              'LAYER_1': True, 'LAYER_2': True, 'LAYER_3': True, 'LAYER_4': True, 'LAYER_5': True,
              'RUNNING': True, 'GAME_OVER': False, 'PAUSED': False,
              'MULTIPLAYER': False,
              'TITLE_SCREEN': False, 'GAME_MODE_SCREEN': False, 'INSTRUCTIONS_SCREEN': False, 'DOG_FIGHT': False, 'MISSION': False, 
              'TRANSITION_TO_TITLE_SCREEN': False, 'TRANSITION_TO_GAME_MODE_SCREEN': False, 'TRANSITION_TO_INSTRUCTIONS_SCREEN': False, 'TRANSITION_TO_DOGFIGHT_MODE': False, 'TRANSITION_TO_MISSION_MODE': False,
             }

GAME_STATE_TRANSITION_TTL = {'TRANSITION_TO_TITLE_SCREEN': TTL_DEFAULTS['TRANSITION_TO_TITLE_SCREEN'], 'TRANSITION_TO_GAME_MODE_SCREEN': TTL_DEFAULTS['TRANSITION_TO_GAME_MODE_SCREEN'], 'TRANSITION_TO_INSTRUCTIONS_SCREEN': TTL_DEFAULTS['TRANSITION_TO_INSTRUCTIONS_SCREEN'], 'TRANSITION_TO_DOGFIGHT_MODE': TTL_DEFAULTS['TRANSITION_TO_DOGFIGHT_MODE'], 'TRANSITION_TO_MISSION_MODE': TTL_DEFAULTS['TRANSITION_TO_MISSION_MODE']}

######################################################################
# INITIALIZE PYGAME AND OTHER ELEMENTS FOR THE GAME
######################################################################
if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] Initializing Pygame")
(init_pass, init_fail) = pygame.init()
if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] Complete!  (P: {init_pass} // F: {init_fail})")

#We create a separate dictionary for the game controls so we can do stuff according to the state of the controls
# ***LESSON***
#'indexed' by GAME_CONTROLS['key']
GAME_CONTROLS = {'PLAYER_1': {'UP': False, 'LEFT': False, 'DOWN' : False, 'RIGHT': False,
                              'GREEN': False, 'BLUE': False, 'RED': False, 'YELLOW': False},
                 'PLAYER_2': {'UP': False, 'LEFT': False, 'DOWN' : False, 'RIGHT': False,
                              'GREEN': False, 'BLUE': False, 'RED': False, 'YELLOW': False},

                 'w': False, 'a': False, 's': False, 'd': False,
                 'up_arrow': False, 'left_arrow': False, 'down_arrow': False, 'right_arrow': False,
                 'space_bar': False, 'left_alt': False, 'right_alt': False, 
                 'left_ctrl': False, 'right_ctrl': False, 'left_shift': False, 'right_shift': False,

                 'JOYSTICK_1': { 'hat_up': False, 'hat_left': False, 'hat_down': False, 'hat_right': False,
                                 'dpad_up': False, 'dpad_left': False, 'dpad_down': False, 'dpad_right': False,
                                 'axis_0': 0.0, 'axis_1': 0.0, 'axis_2': 0.0, 'axis_3': 0.0, 'axis_4': 0.0, 'axis_5': 0.0,
                                 'controller_a': False, 'controller_b': False, 'controller_x': False, 'controller_y': False,
                                 'controller_lb': False, 'controller_rb': False, 'controller_back': False, 'controller_start': False
                               },
                 'JOYSTICK_2': { 'hat_up': False, 'hat_left': False, 'hat_down': False, 'hat_right': False,
                                 'dpad_up': False, 'dpad_left': False, 'dpad_down': False, 'dpad_right': False,
                                 'axis_0': 0.0, 'axis_1': 0.0, 'axis_2': 0.0, 'axis_3': 0.0, 'axis_4': 0.0, 'axis_5': 0.0,
                                 'controller_a': False, 'controller_b': False, 'controller_x': False, 'controller_y': False,
                                 'controller_lb': False, 'controller_rb': False, 'controller_back': False, 'controller_start': False
                               },
                }

#For joystick controllers
JOYSTICKS = {}
JOYSTICK_MAPPER = {}

#Load our Fonts
if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [FONTS] Loading")

######################################################################
# LOAD IMAGES AND IMAGE SHEETS
# Game fonts are held within this dictionary
# These are 'indexed' by GAME_FONTS['KEY']
######################################################################

GAME_FONTS = {'KENNEY_MINI_16': pygame.font.Font('./fonts/Kenney Mini.ttf', 16),
              'KENNEY_MINI_32': pygame.font.Font('./fonts/Kenney Mini.ttf', 32),
              'KENNEY_MINI_SQUARE_16': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 16),
              'KENNEY_MINI_SQUARE_32': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 32),
              'KENNEY_MINI_SQUARE_48': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 48),
              'KENNEY_MINI_SQUARE_64': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 64),
              'KENNEY_MINI_SQUARE_80': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 80),
              'KENNEY_MINI_SQUARE_96': pygame.font.Font('./fonts/Kenney Mini Square.ttf', 96),
              'KENNEY_PIXEL_16': pygame.font.Font('./fonts/Kenney Pixel.ttf', 16),
              'KENNEY_PIXEL_SQUARE_16': pygame.font.Font('./fonts/Kenney Pixel Square.ttf', 16),
              'KENNEY_BLOCKS_16': pygame.font.Font('./fonts/Kenney Blocks.ttf', 16),
              'KENNEY_FUTURE_16': pygame.font.Font('./fonts/Kenney Future.ttf', 16),
              'KENNEY_FUTURE_NARROW_16': pygame.font.Font('./fonts/Kenney Future Narrow.ttf', 16)
             }

if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [FONTS] Completed")

######################################################################
# LOAD IMAGES AND IMAGE SHEETS AND CONVERT TO GAME SURFACES
#
# **** LESSON ****
#
# After the full sheet is loaded we are then going to pull out the parts of the spritesheet (subsurface) that we want and we're making them twice as large (scale)
# GAME_SURFACES['INPUT_PROMPTS']['W_WHITE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(18*16, 2*16, 16, 16)), (32, 32)) #18,2
# GAME_SURFACES['INPUT_PROMPTS']['W_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(18*16, 10*16, 16, 16)), (32, 32)) #18,10
# GAME_SURFACES['INPUT_PROMPTS']['A_WHITE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(18*16, 3*16, 16, 16)), (32, 32)) #18,3
# GAME_SURFACES['INPUT_PROMPTS']['A_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(18*16, 11*16, 16, 16)), (32, 32)) #18,11
# GAME_SURFACES['INPUT_PROMPTS']['S_WHITE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(19*16, 3*16, 16, 16)), (32, 32)) #19,3
# GAME_SURFACES['INPUT_PROMPTS']['S_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(19*16, 11*16, 16, 16)), (32, 32)) #19,11
# GAME_SURFACES['INPUT_PROMPTS']['D_WHITE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(20*16, 3*16, 16, 16)), (32, 32)) #20,3
# GAME_SURFACES['INPUT_PROMPTS']['D_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(20*16, 11*16, 16, 16)), (32, 32)) #20,11
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(13*16, 1*16, 16, 16)), (32, 32)) #13, 1
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(14*16, 1*16, 16, 16)), (32, 32)) #14, 1
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(15*16, 1*16, 16, 16)), (32, 32)) #15, 1
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(16*16, 1*16, 16, 16)), (32, 32)) #16, 1
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_COLOR'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(4*16, 0*16, 16, 16)), (32, 32)) #4, 0
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_COLOR'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(5*16, 0*16, 16, 16)), (32, 32)) #5, 0
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_COLOR'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(6*16, 0*16, 16, 16)), (32, 32)) #6, 0
# GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_COLOR'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(7*16, 0*16, 16, 16)), (32, 32)) #7, 0
# GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(0*16, 20*16, 16, 16)), (32, 32)) #0, 20
# GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(28*16, 20*16, 16, 16)), (32, 32)) #28, 20
# GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE'] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(28*16, 21*16, 16, 16)), (32, 32)) #28, 21
######################################################################
GAME_SURFACES = {}

if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [TEXTURE] Loading")

if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [TEXTURE-LOAD] [FULL-SHEET]: input-prompts-pixel-16")
GAME_SURFACES['INPUT_PROMPTS'] = {}
GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'] = pygame.image.load("./sprites/input-prompts/pixel-16/tilemap_packed.png")

input_prompts_pixel_16_xml_subtextures = element_tree.parse("./sprites/input-prompts/pixel-16/tilemap_sheet.xml").getroot().findall("SubTexture")
for subtexture in input_prompts_pixel_16_xml_subtextures:
  subsurface_name = subtexture.attrib['name'].upper().split(".")[0]
  if GAME_CLI_ARGUMENTS.debug_to_console:
    print(f"[INIT] [TEXTURE-LOAD] [SUBSURFACE]: {subsurface_name}")
  subsurface_x = int(subtexture.attrib['x'])
  subsurface_y = int(subtexture.attrib['y'])
  subsurface_width = int(subtexture.attrib['width'])
  subsurface_height = int(subtexture.attrib['height'])
  # Here we are pulling out the parts of the spritesheet that we want and we're making them twice as large
  GAME_SURFACES['INPUT_PROMPTS'][subsurface_name] = pygame.transform.scale(GAME_SURFACES['INPUT_PROMPTS']['FULL_SHEET'].subsurface(pygame.Rect(subsurface_x, subsurface_y, subsurface_width, subsurface_height)), (subsurface_width*2, subsurface_height*2))

# if GAME_CLI_ARGUMENTS.debug_to_console:
#   print(f"[INIT] [TEXTURE-LOAD] [FULL-SHEET]: space-shooter-redux")
# GAME_SURFACES['SPACE_SHOOTER_REDUX'] = {}
# GAME_SURFACES['SPACE_SHOOTER_REDUX']['FULL_SHEET'] = pygame.image.load("./sprites/space-shooter-redux/sheet.png")
# space_shooter_redux_xml_subtextures = element_tree.parse("./sprites/space-shooter-redux/sheet.xml").getroot().findall("SubTexture")
# for subtexture in space_shooter_redux_xml_subtextures:
#   subsurface_name = subtexture.attrib['name'].upper().split(".")[0]
#   if GAME_CLI_ARGUMENTS.debug_to_console:
#     print(f"[INIT] [TEXTURE-LOAD] [SUBSURFACE]: {subsurface_name}")
#   subsurface_x = int(subtexture.attrib['x'])
#   subsurface_y = int(subtexture.attrib['y'])
#   subsurface_width = int(subtexture.attrib['width'])
#   subsurface_height = int(subtexture.attrib['height'])
#   GAME_SURFACES['SPACE_SHOOTER_REDUX'][subsurface_name] = GAME_SURFACES['SPACE_SHOOTER_REDUX']['FULL_SHEET'].subsurface(pygame.Rect(subsurface_x, subsurface_y, subsurface_width, subsurface_height))

##### CONSIDER REFACTORING THIS INTO A METHOD/FUNCTION IN A SEPARATE FILE
if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [TEXTURE-LOAD] [FULL-SHEET]: pixel-shmup-tiles")
GAME_SURFACES['PIXEL_SHMUP_TILES'] = {}
GAME_SURFACES['PIXEL_SHMUP_TILES']['FULL_SHEET'] = pygame.image.load("./sprites/pixel-shmup/tiles_packed.png") #192x160
pixel_shmup_tiles_xml_subtextures = element_tree.parse("./sprites/pixel-shmup/tiles_sheet.xml").getroot().findall("SubTexture")
for subtexture in pixel_shmup_tiles_xml_subtextures:
  subsurface_name = subtexture.attrib['name'].upper().split(".")[0]
  if GAME_CLI_ARGUMENTS.debug_to_console:
    print(f"[INIT] [TEXTURE-LOAD] [SUBSURFACE]: {subsurface_name}")
  subsurface_x = int(subtexture.attrib['x'])
  subsurface_y = int(subtexture.attrib['y'])
  subsurface_width = int(subtexture.attrib['width'])
  subsurface_height = int(subtexture.attrib['height'])
  GAME_SURFACES['PIXEL_SHMUP_TILES'][subsurface_name] = GAME_SURFACES['PIXEL_SHMUP_TILES']['FULL_SHEET'].subsurface(pygame.Rect(subsurface_x, subsurface_y, subsurface_width, subsurface_height))

if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [TEXTURE-LOAD] [FULL-SHEET]: pixel-shmup-ships")
GAME_SURFACES['PIXEL_SHMUP_SHIPS'] = {}
GAME_SURFACES['PIXEL_SHMUP_SHIPS']['FULL_SHEET'] = pygame.image.load("./sprites/pixel-shmup/ships_packed.png") #128x192
pixel_shmup_ships_xml_subtextures = element_tree.parse("./sprites/pixel-shmup/ships_sheet.xml").getroot().findall("SubTexture")
for subtexture in pixel_shmup_ships_xml_subtextures:
  subsurface_name = subtexture.attrib['name'].upper().split(".")[0]
  if GAME_CLI_ARGUMENTS.debug_to_console:
    print(f"[INIT] [TEXTURE-LOAD] [SUBSURFACE]: {subsurface_name}")
  subsurface_x = int(subtexture.attrib['x'])
  subsurface_y = int(subtexture.attrib['y'])
  subsurface_width = int(subtexture.attrib['width'])
  subsurface_height = int(subtexture.attrib['height'])
  GAME_SURFACES['PIXEL_SHMUP_SHIPS'][subsurface_name] = GAME_SURFACES['PIXEL_SHMUP_SHIPS']['FULL_SHEET'].subsurface(pygame.Rect(subsurface_x, subsurface_y, subsurface_width, subsurface_height))

if GAME_CLI_ARGUMENTS.debug_to_console:
  print(f"[INIT] [TEXTURE] Completed")

######################################################################
# TRANSLATE THE MAP INTO INDEXABLE ELEMETS FOR EASIER "MAPPING"
######################################################################



######################################################################
# SETUP THE DISPLAY
######################################################################
GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] = 0 #|pygame.NOFRAME|pygame.RESIZABLE

if GAME_CLI_ARGUMENTS.full_screen:
  GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] = GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] | pygame.FULLSCREEN
  print(f"[CLI] Full Screen Mode")

if GAME_CLI_ARGUMENTS.no_frame:
  GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] = GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] | pygame.NOFRAME
  print(f"[CLI] Removing Window Frames")

if GAME_CLI_ARGUMENTS.double_buffer:
  GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] = GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'] | pygame.DOUBLEBUF
  print(f"[CLI] Setting Double Buffering")

pygame.display.set_caption("CodeMash 2025 Divez - So you want to make video games? - Super Sky Squadron II: The Flying Ace Follies")

# Create the main screen object
THE_SCREEN = pygame.display.set_mode((GAME_CONSTANTS['SCREEN_WIDTH'], GAME_CONSTANTS['SCREEN_HEIGHT']), GAME_CONSTANTS['PYGAME_SCREEN_FLAGS'])
THE_SCREEN.fill(GAME_COLORS['DEEP_PURPLE'])
pygame.display.update()

print(f"PyGame Driver:  {pygame.display.get_driver()}")
print(f"PyGame Display Info:\n{pygame.display.Info()}")

# LESSON - Initialize other game elements
CAMERA = {'X': 0, 'Y': 0}

MAP = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]

press_start_color = GAME_COLORS['SHMUP_ROYAL_PURPLE']
press_start_blink_ttl = TTL_DEFAULTS['PRESS_START_BLINK']

# Initialize Players

# Set to Title Screen
initialize_title_screen()

######################################################################
# ***LESSON 2*** ESTABLISH THE GAME CLOCK
#
# The game clock and ELAPSED_MS will be used for most, if not all
# our calculations for how all elements are to progress in the game,
# for each frame.
# At the end of our game loop, we have the game clock tick near 60fps
# as best as the hardware we're running off of can go.
######################################################################
GAME_CLOCK = pygame.time.Clock()
ELAPSED_MS = GAME_CLOCK.tick()
ELAPSED_S = ELAPSED_MS / 1000.0
#FRAME_COUNTER = 0

######################################################################
# MAIN GAME LOOP
# ***LESSON 1*** ***GAME LOOP***
######################################################################
while GAME_STATE['RUNNING']:
  ####################################################################
  # RESET THE SCREEN COLOR
  #
  # ***LESSON 6***
  # For the screen to be "wiped clean" so we can start fresh.  This
  # fill operation needs to take place.
  ####################################################################
  THE_SCREEN.fill(GAME_COLORS['DEEP_PURPLE'])

  ####################################################################
  # HANDLE EVENTS
  #
  # ***LESSON 5***
  # We need to handle user I/O as that's the main way the player
  # interacts with the game.  Every button press, key press or 
  # direction movement that we care about needs to be evaluated for
  # the game engine to take the appropriate action that we define.
  ####################################################################
  for the_event in pygame.event.get():
    if GAME_STATE['DEBUG_EVENTS_VERBOSE']:
      print(f"[EVENT-VERBOSE] {the_event}")
    if the_event.type == QUIT:  #If we have evaluated that QUIT has happened as an event, then we need to state that the GAME_STATE of running is now False
      GAME_STATE['RUNNING'] = False
      if GAME_STATE['DEBUG_EVENTS']:
        print("[EVENT] [QUIT]")

    ##################################################################
    # HANDLE USER I/O (KEYBOARD)
    ##################################################################
    if the_event.type == KEYDOWN:
      if GAME_STATE['DEBUG_EVENTS']:
        print(f"[EVENT] [KEYBOARD] [KEYDOWN] {the_event.key}")
    
      # The game wil exit / quit if someone hits the SHFIT+ESCAPE key sequence
      if the_event.key == K_ESCAPE and (the_event.mod & KMOD_SHIFT):
        GAME_STATE['RUNNING'] = False

      if the_event.key == K_UP:
        GAME_CONTROLS['up_arrow'] = True
      if the_event.key == K_LEFT:
        GAME_CONTROLS['left_arrow'] = True
      if the_event.key == K_DOWN:
        GAME_CONTROLS['down_arrow'] = True
      if the_event.key == K_RIGHT:
        GAME_CONTROLS['right_arrow'] = True

      if the_event.key == K_w:
        GAME_CONTROLS['w'] = True
      if the_event.key == K_a:
        GAME_CONTROLS['a'] = True
      if the_event.key == K_s:
        GAME_CONTROLS['s'] = True
      if the_event.key == K_d:
        GAME_CONTROLS['d'] = True

      if the_event.key == K_SPACE:
        GAME_CONTROLS['space_bar'] = True
      if the_event.key == K_LALT:
        GAME_CONTROLS['left_alt'] = True
      if the_event.key == K_RALT:
        GAME_CONTROLS['right_alt'] = True
      if the_event.key == K_RCTRL:
        GAME_CONTROLS['right_ctrl'] = True
      if the_event.key == K_LCTRL:
        GAME_CONTROLS['left_ctrl'] = True
      if the_event.key == K_RSHIFT:
        GAME_CONTROLS['right_shift'] = True
      if the_event.key == K_LSHIFT:
        GAME_CONTROLS['left_shift'] = True

      #If we are in TEST_MODE a bunch of additional keys not generally available are now activated for us to manage the
      #game to test various things out.  Helpful if we need to test a level and we don't want to have to play through
      #the game to get there (or even test out powerups / score / other things / and final boss battles!)
      #
      #Enter test mode by hitting the SHIFT+F12 key sequence
      if GAME_STATE['TEST_MODE']:
        if the_event.key == K_1 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [LAYER_1] MODE TOGGLED TO {(str(not GAME_STATE['LAYER_1'])).upper()}")
          GAME_STATE['LAYER_1'] = not GAME_STATE['LAYER_1']
        if the_event.key == K_2 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [LAYER_2] MODE TOGGLED TO {(str(not GAME_STATE['LAYER_2'])).upper()}")
          GAME_STATE['LAYER_2'] = not GAME_STATE['LAYER_2']
        if the_event.key == K_3 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [LAYER_3] MODE TOGGLED TO {(str(not GAME_STATE['LAYER_3'])).upper()}")
          GAME_STATE['LAYER_3'] = not GAME_STATE['LAYER_3']
        if the_event.key == K_4 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [LAYER_4] MODE TOGGLED TO {(str(not GAME_STATE['LAYER_4'])).upper()}")
          GAME_STATE['LAYER_4'] = not GAME_STATE['LAYER_4']
        if the_event.key == K_5 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [LAYER_5] MODE TOGGLED TO {(str(not GAME_STATE['LAYER_5'])).upper()}")
          GAME_STATE['LAYER_5'] = not GAME_STATE['LAYER_5']

        if the_event.key == K_m and (the_event.mod & KMOD_SHIFT) and (the_event.mod & KMOD_CTRL):
          GAME_STATE['MULTIPLAYER'] = not GAME_STATE['MULTIPLAYER']

        if the_event.key == K_F8:
          print(f"[TEST-MODE] [DEBUG-GRID] MODE TOGGLED TO {(str(not GAME_STATE['DEBUG_GRID'])).upper()}")
          GAME_STATE['DEBUG_GRID'] = not GAME_STATE['DEBUG_GRID']
        if the_event.key == K_F9:
          print(f"[TEST-MODE] [DEBUG-TO-CONSOLE] MODE TOGGLED TO {(str(not GAME_STATE['DEBUG_TO_CONSOLE'])).upper()}")
          GAME_STATE['DEBUG_TO_CONSOLE'] = not GAME_STATE['DEBUG_TO_CONSOLE']
        if the_event.key == K_F10:
          print(f"[TEST-MODE] [DEBUG-EVENTS] MODE TOGGLED TO {(str(not GAME_STATE['DEBUG_EVENTS'])).upper()}")
          GAME_STATE['DEBUG_EVENTS'] = not GAME_STATE['DEBUG_EVENTS']
        if the_event.key == K_F11:
          print(f"[TEST-MODE] [DEBUG-EVENTS-VERBOSE] MODE TOGGLED TO {(str(not GAME_STATE['DEBUG_EVENTS_VERBOSE'])).upper()}")
          GAME_STATE['DEBUG_EVENTS_VERBOSE'] = not GAME_STATE['DEBUG_EVENTS_VERBOSE']
        if the_event.key == K_F12 and not (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] [DEBUG] MODE TOGGLED TO {(str(not GAME_STATE['DEBUG'])).upper()}")
          GAME_STATE['DEBUG'] = not GAME_STATE['DEBUG']
        if the_event.key == K_F12 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] DEACTIVATED")
          print(f"[TEST-MODE] [DEBUG] DEACTIVATED")
          print(f"[TEST-MODE] [DEBUG-GRID] DEACTIVATED")
          print(f"[TEST-MODE] [DEBUG-TO-CONSOLE] DEACTIVATED")
          print(f"[TEST-MODE] [DEBUG-EVENTS] DEACTIVATED")
          print(f"[TEST-MODE] [DEBUG-EVENTS-VERBOSE] DEACTIVATED")
          GAME_STATE['TEST_MODE'] = False
          GAME_STATE['DEBUG'] = False
          #GAME_STATE['DEBUG_GRID'] = False
          GAME_STATE['DEBUG_TO_CONSOLE'] = False
          GAME_STATE['DEBUG_EVENTS'] = False
          GAME_STATE['DEBUG_EVENTS_VERBOSE'] = False

          #Turn back on all the layers
          print(f"[TEST-MODE] [LAYER_ALL] ACTIVATED")
          GAME_STATE['LAYER_1'] = True
          GAME_STATE['LAYER_2'] = True
          GAME_STATE['LAYER_3'] = True
          GAME_STATE['LAYER_4'] = True
          GAME_STATE['LAYER_5'] = True
      else:
        if the_event.key == K_F12 and (the_event.mod & KMOD_SHIFT):
          print(f"[TEST-MODE] ACTIVATED")
          print(f"[TEST-MODE] [DEBUG] ACTIVATED")
          print(f"[TEST-MODE] [DEBUG-GRID] ACTIVATED")
          GAME_STATE['TEST_MODE'] = True
          GAME_STATE['DEBUG'] = True
          #GAME_STATE['DEBUG_GRID'] = True

    if the_event.type == KEYUP:
      if GAME_STATE['DEBUG_EVENTS']:
        print(f"[EVENT] [KEYBOARD] [KEYUP] {the_event.key}")

      if the_event.key == K_UP:
        GAME_CONTROLS['up_arrow'] = False
      if the_event.key == K_LEFT:
        GAME_CONTROLS['left_arrow'] = False
      if the_event.key == K_DOWN:
        GAME_CONTROLS['down_arrow'] = False
      if the_event.key == K_RIGHT:
        GAME_CONTROLS['right_arrow'] = False

      if the_event.key == K_w:
        GAME_CONTROLS['w'] = False
      if the_event.key == K_a:
        GAME_CONTROLS['a'] = False
      if the_event.key == K_s:
        GAME_CONTROLS['s'] = False
      if the_event.key == K_d:
        GAME_CONTROLS['d'] = False

      if the_event.key == K_SPACE:
        GAME_CONTROLS['space_bar'] = False
      if the_event.key == K_LALT:
        GAME_CONTROLS['left_alt'] = False
      if the_event.key == K_RALT:
        GAME_CONTROLS['right_alt'] = False
      if the_event.key == K_RCTRL:
        GAME_CONTROLS['right_ctrl'] = False
      if the_event.key == K_LCTRL:
        GAME_CONTROLS['left_ctrl'] = False
      if the_event.key == K_RSHIFT:
        GAME_CONTROLS['right_shift'] = False
      if the_event.key == K_LSHIFT:
        GAME_CONTROLS['left_shift'] = False

    ##################################################################
    # HANDLE USER I/O (JOYSTICK)
    # 
    # ***LESSON 5a*** 
    #
    # https://www.pygame.org/docs/ref/joystick.html
    # Xbox 360 Controller - a =0, b=1, x=2, y=3, lb=4, rb=5, back=6, start=7, xbox=10, leftaxis=8, rightaxis=9
    #                axis - axis-4 is left trigger, axis-5 is right trigger (-1 -> 1 [fully pressed])
    #                       0 - is left/right on the left axis, 1 is up/down on the left axis (minus is up and left, positive is down and right from 1.0 <-> -1.0)
    #                       2 - is left/right on the right axis, 3 is up/down on the right axis
    #                hat  - (0,0) - center, (0,1) - up, (0,-1) - down, (1,0) - right, (-1,0) - left
    # PowerA NSW Wired Controller - a=0 , b=1 , x=2 , y=3 , dpad-up=11, dpad-down=12, dpad-left=13, dpad-right=14, 
    #                               square/circle=15, home=5, minus=4, plus=6, L=9, R=10, leftaxis=7, rightaxis=8 
    #                             - ZL=Axis-4, ZR=Axis-5, leftaxis-left/right=0, leftaxis-up/down=1, rightaxis-left/right=2, rightaxis-up/down=3
    #                             - up=negative1, down=positive1, left=negative1, right=positive1
    #                             - ZL=pressed=-1.0,released=0.9999969482421875
    ##################################################################
    
    # Handle hotplugging
    # This event will be generated when the program starts for every
    # joystick, filling up the list without needing to create them manually.
    if not GAME_CLI_ARGUMENTS.disable_joystick and the_event.type == pygame.JOYDEVICEADDED:
      if GAME_STATE['DEBUG_EVENTS'] or True:
        print(f"[EVENT] [JOYSTICK-{the_event.device_index}] [CONNECT] ID:{the_event.device_index}")

      #Get the joystick that caused this event  
      joystick = pygame.joystick.Joystick(the_event.device_index)
      joystick_instance_id = joystick.get_instance_id()
      JOYSTICK_MAPPER[joystick_instance_id] = {'JOYSTICK': joystick, 'PLAYER': 0}

      if len(JOYSTICKS) < GAME_CONSTANTS['MAX_CONNECTED_JOYSTICKS']:
        if GAME_STATE['DEBUG_EVENTS'] or True:
          print(f"[EVENT] [JOYSTICK-{joystick.get_instance_id()}] [CONNECT] ID:{joystick.get_instance_id()} - {joystick} - {joystick.get_name()} - Patching into JOYSTICK")
        #Check if we have player 1's Joystick attached, if not, add the connected joystick for that player
        if JOYSTICKS.get(1) == None:
          JOYSTICK_MAPPER[joystick_instance_id]['PLAYER'] = 1
          if GAME_STATE['DEBUG_EVENTS'] or True:
            print(f"[EVENT] [JOYSTICK-{joystick.get_instance_id()}] [CONNECT] ID:{joystick.get_instance_id()} - {joystick} - {joystick.get_name()} - PLAYER 1 JOYSTICK CONNECTED")
        #Check if we have player 2's Joystick attached, if not, add the connected joystick for that player
        elif JOYSTICKS.get(2) == None:
          JOYSTICK_MAPPER[joystick_instance_id]['PLAYER'] = 2
          if GAME_STATE['DEBUG_EVENTS'] or True:
            print(f"[EVENT] [JOYSTICK-{joystick.get_instance_id()}] [CONNECT] ID:{joystick.get_instance_id()} - {joystick} - {joystick.get_name()} - PLAYER 2 JOYSTICK CONNECTED")

        #Patch the joystick into the old code
        JOYSTICKS[JOYSTICK_MAPPER[joystick_instance_id]['PLAYER']] = joystick

        if GAME_STATE['DEBUG_EVENTS'] or True:
          print(f"[EVENT] [JOYSTICK-{joystick.get_instance_id()}] [CONNECT] ID:{joystick.get_instance_id()} - {joystick} - {joystick.get_name()} - PATCHED AS {JOYSTICK_MAPPER[joystick_instance_id]['PLAYER']}")

    if not GAME_CLI_ARGUMENTS.disable_joystick and the_event.type == pygame.JOYDEVICEREMOVED:
      if GAME_STATE['DEBUG_EVENTS'] or True:
        print(f"[EVENT] [JOYSTICK-{the_event.instance_id}] [DISCONNECT] ID:{the_event.instance_id} FOR PLAYER {JOYSTICK_MAPPER[the_event.instance_id]['PLAYER']}")
      
      joystick_instance_id = the_event.instance_id

      if JOYSTICK_MAPPER.get(joystick_instance_id) != None:
        del JOYSTICKS[JOYSTICK_MAPPER[joystick_instance_id]['PLAYER']]
        del JOYSTICK_MAPPER[joystick_instance_id]

      #Check if we need to do any kind of remapping for additional controllers that may have been attached (Maybe? - or we just force it to the next one added, which may already happen)

    if not GAME_CLI_ARGUMENTS.disable_joystick and len(JOYSTICKS) <= GAME_CONSTANTS['MAX_CONNECTED_JOYSTICKS'] and (the_event.type == pygame.JOYBUTTONDOWN or the_event.type == pygame.JOYBUTTONUP or the_event.type == pygame.JOYAXISMOTION or the_event.type == pygame.JOYHATMOTION):
      if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{the_event.instance_id}] [EVENT_PROCESSING]")
      
      controller_instance_id = the_event.instance_id
      actual_player_controller = JOYSTICK_MAPPER[controller_instance_id]
      actual_player = actual_player_controller['PLAYER']

      if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{controller_instance_id}] [MAPPING] ")

      if the_event.type == pygame.JOYBUTTONDOWN:
        if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{controller_instance_id}] [BUTTONDOWN] {the_event.button}")

        if JOYSTICKS[actual_player].get_name() == 'Xbox 360 Controller' or JOYSTICKS[actual_player].get_name() == 'PowerA NSW Wired controller':
          if the_event.button == 0:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_a'] = True
          if the_event.button == 1:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_b'] = True
          if the_event.button == 2:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_x'] = True
          if the_event.button == 3:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_y'] = True

        if JOYSTICKS[actual_player].get_name() == 'PowerA NSW Wired controller':
          if the_event.button == 11:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_up'] = True
          if the_event.button == 12:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_down'] = True
          if the_event.button == 13:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_left'] = True
          if the_event.button == 14:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_right'] = True

      if the_event.type == pygame.JOYBUTTONUP:
        if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{controller_instance_id}] [BUTTONUP] {the_event.button}")

        if JOYSTICKS[actual_player].get_name() == 'Xbox 360 Controller' or JOYSTICKS[actual_player].get_name() == 'PowerA NSW Wired controller':
          if the_event.button == 0:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_a'] = False
          if the_event.button == 1:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_b'] = False
          if the_event.button == 2:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_x'] = False
          if the_event.button == 3:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['controller_y'] = False

        if JOYSTICKS[actual_player].get_name() == 'PowerA NSW Wired controller':
          if the_event.button == 11:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_up'] = False
          if the_event.button == 12:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_down'] = False
          if the_event.button == 13:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_left'] = False
          if the_event.button == 14:
            GAME_CONTROLS[f'JOYSTICK_{actual_player}']['dpad_right'] = False

      if the_event.type == pygame.JOYAXISMOTION:
        if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{actual_player}] [AXISMOTION] {the_event.axis} value {the_event.value}")
        GAME_CONTROLS[f'JOYSTICK_{actual_player}'][f'axis_{the_event.axis}'] = the_event.value

      if the_event.type == pygame.JOYHATMOTION:
        if GAME_STATE['DEBUG_EVENTS']:
          print(f"[EVENT] [JOYSTICK-{actual_player}] [HATMOTION] ({the_event.value[0]}, {the_event.value[1]})")

        if the_event.value[0] == 0:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_left'] = False
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_right'] = False
        elif the_event.value[0] == 1:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_left'] = False
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_right'] = True
        elif the_event.value[0] == -1:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_left'] = True
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_right'] = False
        if the_event.value[1] == 0:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_up'] = False
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_down'] = False
        elif the_event.value[1] == 1:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_up'] = True
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_down'] = False
        elif the_event.value[1] == -1:
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_up'] = False
          GAME_CONTROLS[f'JOYSTICK_{actual_player}']['hat_down'] = True

    ###################################
    #
    # Apply I/O to actual Game Controls
    # Not sure why this won't work when it's pulled out of the i/o loop
    # 
    # ***LESSON 5b***
    # Note here that we have slightly different controls for single player mode and multiplayer mode.
    ###################################
    directional_axis_tolleration = 0.50

    if not GAME_STATE['MULTIPLAYER']:
      GAME_CONTROLS['PLAYER_1']['UP'] = GAME_CONTROLS['w'] or GAME_CONTROLS['up_arrow'] or GAME_CONTROLS['JOYSTICK_1']['hat_up'] or GAME_CONTROLS['JOYSTICK_1']['dpad_up'] or GAME_CONTROLS['JOYSTICK_1']['axis_1'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_3'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['hat_up'] or GAME_CONTROLS['JOYSTICK_2']['dpad_up'] or GAME_CONTROLS['JOYSTICK_2']['axis_1'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_3'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['LEFT'] = GAME_CONTROLS['a'] or GAME_CONTROLS['left_arrow'] or GAME_CONTROLS['JOYSTICK_1']['hat_left'] or GAME_CONTROLS['JOYSTICK_1']['dpad_left'] or GAME_CONTROLS['JOYSTICK_1']['axis_0'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_2'] < -directional_axis_tolleration  or GAME_CONTROLS['JOYSTICK_2']['hat_left'] or GAME_CONTROLS['JOYSTICK_2']['dpad_left'] or GAME_CONTROLS['JOYSTICK_2']['axis_0'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_2'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['DOWN'] = GAME_CONTROLS['s'] or GAME_CONTROLS['down_arrow'] or GAME_CONTROLS['JOYSTICK_1']['hat_down'] or GAME_CONTROLS['JOYSTICK_1']['dpad_down'] or GAME_CONTROLS['JOYSTICK_1']['axis_1'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_3'] > directional_axis_tolleration  or GAME_CONTROLS['JOYSTICK_2']['hat_down'] or GAME_CONTROLS['JOYSTICK_2']['dpad_down'] or GAME_CONTROLS['JOYSTICK_2']['axis_1'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_3'] > directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['RIGHT'] = GAME_CONTROLS['d'] or GAME_CONTROLS['right_arrow'] or GAME_CONTROLS['JOYSTICK_1']['hat_right'] or GAME_CONTROLS['JOYSTICK_1']['dpad_right'] or GAME_CONTROLS['JOYSTICK_1']['axis_0'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_2'] > directional_axis_tolleration  or GAME_CONTROLS['JOYSTICK_2']['hat_right'] or GAME_CONTROLS['JOYSTICK_2']['dpad_right'] or GAME_CONTROLS['JOYSTICK_2']['axis_0'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_2'] > directional_axis_tolleration

      GAME_CONTROLS['PLAYER_1']['GREEN'] = GAME_CONTROLS['space_bar'] or GAME_CONTROLS['right_shift'] or GAME_CONTROLS['left_shift'] or GAME_CONTROLS['JOYSTICK_1']['controller_a'] or GAME_CONTROLS['JOYSTICK_2']['controller_a']
      GAME_CONTROLS['PLAYER_1']['RED'] = GAME_CONTROLS['left_alt'] or GAME_CONTROLS['right_alt'] or GAME_CONTROLS['left_ctrl'] or GAME_CONTROLS['right_ctrl'] or GAME_CONTROLS['JOYSTICK_1']['controller_b'] or GAME_CONTROLS['JOYSTICK_2']['controller_b']
      GAME_CONTROLS['PLAYER_1']['BLUE'] = GAME_CONTROLS['JOYSTICK_1']['controller_x'] or GAME_CONTROLS['JOYSTICK_2']['controller_x']
      GAME_CONTROLS['PLAYER_1']['YELLOW'] = GAME_CONTROLS['JOYSTICK_1']['controller_y'] or GAME_CONTROLS['JOYSTICK_2']['controller_y']
    else:
      GAME_CONTROLS['PLAYER_1']['UP'] = GAME_CONTROLS['w'] or GAME_CONTROLS['JOYSTICK_1']['hat_up'] or GAME_CONTROLS['JOYSTICK_1']['dpad_up'] or GAME_CONTROLS['JOYSTICK_1']['axis_1'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_3'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['LEFT'] = GAME_CONTROLS['a'] or GAME_CONTROLS['JOYSTICK_1']['hat_left'] or GAME_CONTROLS['JOYSTICK_1']['dpad_left'] or GAME_CONTROLS['JOYSTICK_1']['axis_0'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_2'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['DOWN'] = GAME_CONTROLS['s'] or GAME_CONTROLS['JOYSTICK_1']['hat_down'] or GAME_CONTROLS['JOYSTICK_1']['dpad_down'] or GAME_CONTROLS['JOYSTICK_1']['axis_1'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_3'] > directional_axis_tolleration
      GAME_CONTROLS['PLAYER_1']['RIGHT'] = GAME_CONTROLS['d'] or GAME_CONTROLS['JOYSTICK_1']['hat_right'] or GAME_CONTROLS['JOYSTICK_1']['dpad_right'] or GAME_CONTROLS['JOYSTICK_1']['axis_0'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_1']['axis_2'] > directional_axis_tolleration

      GAME_CONTROLS['PLAYER_1']['GREEN'] = GAME_CONTROLS['left_shift'] or GAME_CONTROLS['JOYSTICK_1']['controller_a']
      GAME_CONTROLS['PLAYER_1']['RED'] = GAME_CONTROLS['left_ctrl'] or GAME_CONTROLS['JOYSTICK_1']['controller_b']
      GAME_CONTROLS['PLAYER_1']['BLUE'] = GAME_CONTROLS['left_alt'] or GAME_CONTROLS['JOYSTICK_1']['controller_x']
      GAME_CONTROLS['PLAYER_1']['YELLOW'] = GAME_CONTROLS['JOYSTICK_1']['controller_y']

      GAME_CONTROLS['PLAYER_2']['UP'] = GAME_CONTROLS['up_arrow'] or GAME_CONTROLS['JOYSTICK_2']['hat_up'] or GAME_CONTROLS['JOYSTICK_2']['dpad_up'] or GAME_CONTROLS['JOYSTICK_2']['axis_1'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_3'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_2']['LEFT'] = GAME_CONTROLS['left_arrow'] or GAME_CONTROLS['JOYSTICK_2']['hat_left'] or GAME_CONTROLS['JOYSTICK_2']['dpad_left'] or GAME_CONTROLS['JOYSTICK_2']['axis_0'] < -directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_2'] < -directional_axis_tolleration
      GAME_CONTROLS['PLAYER_2']['DOWN'] = GAME_CONTROLS['down_arrow'] or GAME_CONTROLS['JOYSTICK_2']['hat_down'] or GAME_CONTROLS['JOYSTICK_2']['dpad_down'] or GAME_CONTROLS['JOYSTICK_2']['axis_1'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_3'] > directional_axis_tolleration
      GAME_CONTROLS['PLAYER_2']['RIGHT'] = GAME_CONTROLS['right_arrow'] or GAME_CONTROLS['JOYSTICK_2']['hat_right'] or GAME_CONTROLS['JOYSTICK_2']['dpad_right'] or GAME_CONTROLS['JOYSTICK_2']['axis_0'] > directional_axis_tolleration or GAME_CONTROLS['JOYSTICK_2']['axis_2'] > directional_axis_tolleration

      GAME_CONTROLS['PLAYER_2']['GREEN'] = GAME_CONTROLS['right_shift'] or GAME_CONTROLS['JOYSTICK_2']['controller_a']
      GAME_CONTROLS['PLAYER_2']['RED'] = GAME_CONTROLS['right_ctrl'] or GAME_CONTROLS['JOYSTICK_2']['controller_b']
      GAME_CONTROLS['PLAYER_2']['BLUE'] = GAME_CONTROLS['right_alt'] or GAME_CONTROLS['JOYSTICK_2']['controller_x']
      GAME_CONTROLS['PLAYER_2']['YELLOW'] = GAME_CONTROLS['JOYSTICK_2']['controller_y']

    ##################################################################
    # WINDOW FOCUS LOSS / GAIN
    #
    # Probably should pause the game on focus loss
    ##################################################################
    if the_event.type == pygame.WINDOWFOCUSLOST:
      if GAME_STATE['DEBUG_EVENTS']:
        print(f"[EVENT] [WINDOW] [FOCUSLOST]")
    
    if the_event.type == pygame.WINDOWFOCUSGAINED:
      if GAME_STATE['DEBUG_EVENTS']:
        print(f"[EVENT] [WINDOW] [FOCUSGAINED]")

  ####################################################################
  # *** LESSON ***
  # 
  # Out of the I/O section of the game loop, now we're going to see
  # where we are at in terms of game state to figure out what to do
  #
  #
  #
  #
  #
  ####################################################################

  if GAME_STATE['TITLE_SCREEN']:
    
    press_start_blink_ttl = press_start_blink_ttl - ELAPSED_MS
    if press_start_blink_ttl < 1:
      press_start_blink_ttl = TTL_DEFAULTS['PRESS_START_BLINK']
      if press_start_color == GAME_COLORS['SHMUP_ROYAL_PURPLE']:
        press_start_color = GAME_COLORS['ALMOST_BLACK']
      else:
        press_start_color = GAME_COLORS['SHMUP_ROYAL_PURPLE']

    potozniak_electronics = GAME_FONTS['KENNEY_MINI_SQUARE_64'].render(f"POTOZNIAK ELECTRONICS", True, GAME_COLORS['SHMUP_BLUE'])
    THE_SCREEN.blit(potozniak_electronics, potozniak_electronics.get_rect(midtop = (GAME_CONSTANTS['SCREEN_WIDTH'] / 2, GAME_CONSTANTS['SCREEN_HEIGHT'] / 8)))
    presents = GAME_FONTS['KENNEY_MINI_SQUARE_64'].render(f"PRESENTS", True, GAME_COLORS['SHMUP_BLUE'])
    THE_SCREEN.blit(presents, presents.get_rect(midtop = (GAME_CONSTANTS['SCREEN_WIDTH'] / 2, (GAME_CONSTANTS['SCREEN_HEIGHT'] / 8) + (GAME_CONSTANTS['SQUARE_SIZE'] * 2))))

    game_title = GAME_FONTS['KENNEY_MINI_SQUARE_64'].render(f"Super Sky Squadron II:", True, GAME_COLORS['SHMUP_RED'])
    THE_SCREEN.blit(game_title, game_title.get_rect(midtop = (GAME_CONSTANTS['SCREEN_WIDTH'] / 2, GAME_CONSTANTS['SCREEN_HEIGHT'] / 8 * 3)))
    game_title_2 = GAME_FONTS['KENNEY_MINI_SQUARE_64'].render(f"The Flying Ace Follies", True, GAME_COLORS['SHMUP_ORANGE'])
    THE_SCREEN.blit(game_title_2, game_title_2.get_rect(midtop = (GAME_CONSTANTS['SCREEN_WIDTH'] / 2, (GAME_CONSTANTS['SCREEN_HEIGHT'] / 8 * 3) + (GAME_CONSTANTS['SQUARE_SIZE'] * 2))))

    blitRotate(THE_SCREEN, 
               pygame.transform.scale(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_A_FIGHTER'], (64, 64)), 
               (GAME_CONSTANTS['SCREEN_WIDTH'] / 4 + GAME_CONSTANTS['SQUARE_SIZE'] / 2, GAME_CONSTANTS['SCREEN_HEIGHT'] / 8 * 5.5 + GAME_CONSTANTS['SQUARE_SIZE']), 
               (32, 32), 
               270)
    blitRotate(THE_SCREEN,
               pygame.transform.scale(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_A_FIGHTER'], (64, 64)), 
               (GAME_CONSTANTS['SCREEN_WIDTH'] / 4 * 3 - GAME_CONSTANTS['SQUARE_SIZE'] / 2, GAME_CONSTANTS['SCREEN_HEIGHT'] / 8 * 5.5 + GAME_CONSTANTS['SQUARE_SIZE']), 
               (32, 32), 
               90)

    press_start = GAME_FONTS['KENNEY_MINI_SQUARE_64'].render(f"PRESS START", True, press_start_color)
    THE_SCREEN.blit(press_start, press_start.get_rect(midtop = (GAME_CONSTANTS['SCREEN_WIDTH'] / 2, GAME_CONSTANTS['SCREEN_HEIGHT'] / 8 * 5.5 - GAME_CONSTANTS['SQUARE_SIZE'] / 2)))

  ####################################################################
  # Draw Layer One (The Map Tiles)
  #
  #
  ####################################################################
  if GAME_STATE['LAYER_1']:
    a = 1


  ####################################################################
  # Draw the HUD (Heads Up Display)
  #
  # This is the last (before debug) set of things to add to the
  # screen.  This is here because we want this on top of everything
  # else from the game.
  ####################################################################
  if GAME_STATE['LAYER_5']:
    #Top HUD
    pygame.draw.rect(THE_SCREEN, GAME_COLORS['STEEL_BLUE'], pygame.Rect(0,0,1280,32))

    top_hud_player_one = GAME_FONTS['KENNEY_MINI_SQUARE_32'].render(f"PLAYER 1", True, GAME_COLORS['ALMOST_BLACK'])
    THE_SCREEN.blit(top_hud_player_one, top_hud_player_one.get_rect(topleft = (16, -6)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER_GRAY'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER_GRAY'].get_rect(topleft = (160, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER_GRAY'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER_GRAY'].get_rect(topleft = (192, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'].get_rect(topleft = (224, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'].get_rect(topleft = (256, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['RED_B_FIGHTER'].get_rect(topleft = (288, 0)))

    top_hud_player_two = GAME_FONTS['KENNEY_MINI_SQUARE_32'].render(f"PLAYER 2", True, GAME_COLORS['ALMOST_BLACK'])
    THE_SCREEN.blit(top_hud_player_two, top_hud_player_two.get_rect(topleft = (912, -6)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER_GRAY'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER_GRAY'].get_rect(topleft = (1056+16, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER_GRAY'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER_GRAY'].get_rect(topleft = (1088+16, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'].get_rect(topleft = (1120+16, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'].get_rect(topleft = (1152+16, 0)))
    THE_SCREEN.blit(GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'], GAME_SURFACES['PIXEL_SHMUP_SHIPS']['BLUE_B_FIGHTER'].get_rect(topleft = (1184+16, 0)))
    

    top_hud_high_score_text = GAME_FONTS['KENNEY_MINI_SQUARE_32'].render(f"HI-SCORE:", True, GAME_COLORS['ALMOST_BLACK'])
    THE_SCREEN.blit(top_hud_high_score_text, top_hud_high_score_text.get_rect(topleft = (480, -6)))

    top_hud_high_score = GAME_FONTS['KENNEY_MINI_SQUARE_32'].render(f"000000000", True, GAME_COLORS['ALMOST_BLACK'])
    THE_SCREEN.blit(top_hud_high_score, top_hud_high_score.get_rect(topleft = (640, -6)))

    #Mini Map HUD


    #Bottom HUD
    pygame.draw.rect(THE_SCREEN, GAME_COLORS['STEEL_BLUE'], pygame.Rect(0,640,1280,80))

    # bottom_hud_test = GAME_FONTS['KENNEY_MINI_SQUARE_32'].render(f"TEST", True, GAME_COLORS['ALMOST_BLACK'])
    # THE_SCREEN.blit(bottom_hud_test, bottom_hud_test.get_rect(topleft = (32, 640)))

    # bottom_hud_test = GAME_FONTS['KENNEY_MINI_32'].render(f"TEST", True, GAME_COLORS['ALMOST_BLACK'])
    # THE_SCREEN.blit(bottom_hud_test, bottom_hud_test.get_rect(topleft = (32, 672)))


  ####################################################################
  # Draw the DEBUG
  #
  # This is last, becasue we want all of this on top of everything
  # else!
  ####################################################################
  if GAME_STATE['DEBUG']:

    debug_x_offset = 0
    debug_y_offset = 80

    ######################################################################
    # Show "Game Information" that we care about
    #
    # Milliseconds elapsed between each frame
    #
    # ***LESSON***
    # A surface is created when the render method is called from our Font object.  Render takes in text, Anti-aliasing, color.
    # https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
    #
    # ***LESSON*** Blit - What is blitting?  Blit stands for 
    # Copies the contents of one surface to another.
    # In our example here, we are copying the contents of time_passed_ms_text_surface to our THE_SCREEN surface.
    # Effectively this will "paint" time_passed_ms_text_surface on THE_SCREEN in the location we tell it to (and we craete the rect for the surface and use that).
    ######################################################################
    time_passed_ms_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"{ELAPSED_MS}ms", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(time_passed_ms_text_surface, time_passed_ms_text_surface.get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 5 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    ######################################################################
    # Show "Game Information" that we care about
    #
    # Game State Information, Visible Layers
    ######################################################################
    game_state_running_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"RUNNING", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['RUNNING']:
      game_state_running_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"RUNNING", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_running_text_surface, game_state_running_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 512 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 590 - debug_y_offset)))

    game_state_game_over_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"GAME OVER", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['GAME_OVER']:
      game_state_game_over_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"GAME OVER", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_game_over_text_surface, game_state_game_over_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 416 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 590 - debug_y_offset)))

    game_state_paused_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"PAUSED", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['PAUSED']:
      game_state_paused_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"PAUSED", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_paused_text_surface, game_state_paused_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 288 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 590 - debug_y_offset)))

    game_state_multiplayer_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"MULTIPLAYER", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['MULTIPLAYER']:
      game_state_multiplayer_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"MULTIPLAYER", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_multiplayer_text_surface, game_state_multiplayer_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 192 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 590 - debug_y_offset)))

    game_state_title_screen_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"TITLE SCREEN", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['TITLE_SCREEN']:
      game_state_title_screen_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"TITLE SCREEN", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_title_screen_text_surface, game_state_running_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 512 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 574 - debug_y_offset)))

    game_state_game_mode_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"GAME MODE SCREEN", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['GAME_MODE_SCREEN']:
      game_state_game_mode_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"GAME MODE SCREEN", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_game_mode_text_surface, game_state_game_mode_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 384 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 574 - debug_y_offset)))

    game_state_dog_fight_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"DOG FIGHT", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['DOG_FIGHT']:
      game_state_dog_fight_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"DOG FIGHT", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_dog_fight_text_surface, game_state_dog_fight_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 192 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 574 - debug_y_offset)))

    game_state_mission_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"MISSION", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['MISSION']:
      game_state_mission_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"MISSION", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_state_mission_text_surface, game_state_mission_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 96 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 574 - debug_y_offset)))

    game_layer_1_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 1", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['LAYER_1']:
      game_layer_1_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 1", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_layer_1_text_surface, game_layer_1_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 512 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    game_layer_2_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 2", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['LAYER_2']:
      game_layer_2_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 2", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_layer_2_text_surface, game_layer_2_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 416 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    game_layer_3_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 3", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['LAYER_3']:
      game_layer_3_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 3", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_layer_3_text_surface, game_layer_3_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 320 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    game_layer_4_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 4", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['LAYER_4']:
      game_layer_4_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 4", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_layer_4_text_surface, game_layer_4_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 224 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    game_layer_5_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 5", True, GAME_COLORS['NOT_QUITE_BLACK'])
    if GAME_STATE['LAYER_5']:
      game_layer_5_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"LAYER 5", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(game_layer_5_text_surface, game_layer_5_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 128 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 526 - debug_y_offset)))

    ######################################################################
    # Show "Game Information" that we care about
    #
    # Camera details
    # *** LESSON ***
    ######################################################################
    camera_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"CAMERA X: {CAMERA['X']}", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(camera_text_surface, camera_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 170 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 496 - debug_y_offset)))
    camera_text_surface = GAME_FONTS['KENNEY_MINI_16'].render(f"CAMERA Y: {CAMERA['Y']}", True, GAME_COLORS['GREEN'])
    THE_SCREEN.blit(camera_text_surface, camera_text_surface.get_rect(bottomleft = (GAME_CONSTANTS['SCREEN_WIDTH'] - 170 - debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 478 - debug_y_offset)))

    ######################################################################
    # Show the Player Controls Debug
    ######################################################################

    wasd_debug_x_offset = 152 + debug_x_offset
    wasd_debug_y_offset = 3 + debug_y_offset

    arrow_debug_x_offset = 48 + debug_x_offset
    arrow_debug_y_offset = 3 + debug_y_offset

    left_shift_debug_x_offset = 222 + debug_x_offset
    left_shift_debug_y_offset = 126 + debug_y_offset

    right_shift_debug_x_offset = -2 + debug_x_offset
    right_shift_debug_y_offset = 126 + debug_y_offset

    left_ctrl_debug_x_offset = 222 + debug_x_offset
    left_ctrl_debug_y_offset = 96 + debug_y_offset

    left_alt_debug_x_offset = 170 + debug_x_offset
    left_alt_debug_y_offset = 96 + debug_y_offset

    right_alt_debug_x_offset = 32 + debug_x_offset
    right_alt_debug_y_offset = 96 + debug_y_offset

    right_ctrl_debug_x_offset = -12 + debug_x_offset
    right_ctrl_debug_y_offset = 96 + debug_y_offset

    if GAME_STATE['MULTIPLAYER']:
      wasd_debug_x_offset = 1188 + debug_x_offset
      wasd_debug_y_offset = 67 + debug_y_offset

      arrow_debug_x_offset = 3 + debug_x_offset
      arrow_debug_y_offset = 67 + debug_y_offset

      left_shift_debug_x_offset = 1212 + debug_x_offset
      left_shift_debug_y_offset = 174 + debug_y_offset

      right_shift_debug_x_offset = 6 + debug_x_offset
      right_shift_debug_y_offset = 174 + debug_y_offset

      left_ctrl_debug_x_offset = 1212 + debug_x_offset
      left_ctrl_debug_y_offset = 144 + debug_y_offset

      left_alt_debug_x_offset = 1160 + debug_x_offset
      left_alt_debug_y_offset = 144 + debug_y_offset

      right_alt_debug_x_offset = 40 + debug_x_offset
      right_alt_debug_y_offset = 144 + debug_y_offset

      right_ctrl_debug_x_offset = -4 + debug_x_offset
      right_ctrl_debug_y_offset = 144 + debug_y_offset  

    # Show input keys from keyboard

    # WASD KEYS
    if GAME_CONTROLS['w']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['W_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['W_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 30 - wasd_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['W_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['W_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 30 - wasd_debug_y_offset)))
    if GAME_CONTROLS['a']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['A_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['A_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 56 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['A_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['A_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 56 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))
    if GAME_CONTROLS['s']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['S_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['S_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['S_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['S_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))
    if GAME_CONTROLS['d']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['D_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['D_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 0 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['D_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['D_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 0 - wasd_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - wasd_debug_y_offset)))

    # ARROW KEYS
    if GAME_CONTROLS['up_arrow']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 30 - arrow_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 30 - arrow_debug_y_offset)))
    if GAME_CONTROLS['left_arrow']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 56 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 56 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))
    if GAME_CONTROLS['down_arrow']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 28 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))
    if GAME_CONTROLS['right_arrow']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 0 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - 0 - arrow_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - 0 - arrow_debug_y_offset)))

    # SHIFT / CTRLl / AlT / SPACEBAR 
    if GAME_CONTROLS['left_shift']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SHIFT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['SHIFT_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_shift_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_shift_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SHIFT_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['SHIFT_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_shift_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_shift_debug_y_offset)))

    if GAME_CONTROLS['right_shift']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SHIFT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['SHIFT_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_shift_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_shift_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SHIFT_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['SHIFT_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_shift_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_shift_debug_y_offset)))

    if GAME_CONTROLS['left_ctrl']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['CTRL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['CTRL_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_ctrl_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_ctrl_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['CTRL_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['CTRL_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_ctrl_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_ctrl_debug_y_offset)))

    if GAME_CONTROLS['left_alt']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['ALT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['ALT_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_alt_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_alt_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['ALT_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['ALT_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - left_alt_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - left_alt_debug_y_offset)))

    if not GAME_STATE['MULTIPLAYER']:
      spacebar_debug_x_offset = 94 + debug_x_offset
      spacebar_debug_y_offset = 96 + debug_y_offset
      if GAME_CONTROLS['space_bar']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SPACEBAR_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['SPACEBAR_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - spacebar_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - spacebar_debug_y_offset)))
      else:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['SPACEBAR_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['SPACEBAR_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - spacebar_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - spacebar_debug_y_offset)))

    if GAME_CONTROLS['right_alt']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['ALT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['ALT_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_alt_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_alt_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['ALT_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['ALT_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_alt_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_alt_debug_y_offset)))

    if GAME_CONTROLS['right_ctrl']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['CTRL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['CTRL_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_ctrl_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_ctrl_debug_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['CTRL_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['CTRL_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - right_ctrl_debug_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - right_ctrl_debug_y_offset)))
      
      #If we have a joystick plugged in, we will show the joystick controls
    
    if len(JOYSTICKS) > 0:
      if not GAME_STATE['MULTIPLAYER']:
        joystick_buttons_x_offset = 176 + debug_x_offset
        joystick_buttons_y_offset = 160 + debug_y_offset

        if GAME_CONTROLS['JOYSTICK_1']['controller_a'] or GAME_CONTROLS['JOYSTICK_2']['controller_a']:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        else:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        if GAME_CONTROLS['JOYSTICK_1']['controller_b'] or GAME_CONTROLS['JOYSTICK_2']['controller_b']:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        else:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        if GAME_CONTROLS['JOYSTICK_1']['controller_x'] or GAME_CONTROLS['JOYSTICK_2']['controller_x']:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        else:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        if GAME_CONTROLS['JOYSTICK_1']['controller_y'] or GAME_CONTROLS['JOYSTICK_2']['controller_y']:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))
        else:
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_buttons_y_offset)))

        #Left Axis
        joystick_axis_x_offset = 256 + debug_x_offset
        joystick_axis_y_offset = 3 + debug_y_offset
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset)))
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_2']['axis_0'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_2']['axis_1'] * 8)))
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_1']['axis_0'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_1']['axis_1'] * 8)))

        #Right Axis
        joystick_axis_x_offset = 0 + debug_x_offset
        joystick_axis_y_offset = 3 + debug_y_offset
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset)))
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_2']['axis_2'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_2']['axis_3'] * 8)))
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_1']['axis_2'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_1']['axis_3'] * 8)))

        joystick_dpad_x_offset = 128 + debug_x_offset
        joystick_dpad_y_offset = 48 + debug_y_offset
        
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
        for joystick_to_debug in JOYSTICKS:
          #Xbox Hat
          if JOYSTICKS[joystick_to_debug].get_name() == 'Xbox 360 Controller':
            if GAME_CONTROLS['JOYSTICK_1']['hat_up'] or GAME_CONTROLS['JOYSTICK_2']['hat_up']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset - 16)))
            if GAME_CONTROLS['JOYSTICK_1']['hat_down'] or GAME_CONTROLS['JOYSTICK_2']['hat_down']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
            if GAME_CONTROLS['JOYSTICK_1']['hat_left'] or GAME_CONTROLS['JOYSTICK_2']['hat_left']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
            if GAME_CONTROLS['JOYSTICK_1']['hat_right'] or GAME_CONTROLS['JOYSTICK_2']['hat_right']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
          #PowerA D-Pad
          if JOYSTICKS[joystick_to_debug].get_name() == 'PowerA NSW Wired controller':
            if GAME_CONTROLS['JOYSTICK_1']['dpad_up'] or GAME_CONTROLS['JOYSTICK_2']['dpad_up']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset - 16)))
            if GAME_CONTROLS['JOYSTICK_1']['dpad_down'] or GAME_CONTROLS['JOYSTICK_2']['dpad_down']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
            if GAME_CONTROLS['JOYSTICK_1']['dpad_left'] or GAME_CONTROLS['JOYSTICK_2']['dpad_left']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
            if GAME_CONTROLS['JOYSTICK_1']['dpad_right'] or GAME_CONTROLS['JOYSTICK_2']['dpad_right']:
              THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_dpad_y_offset)))
      else: #MULTIPLAYER
        if JOYSTICKS.get(1) != None: #Player 2 has a controller plugged in
          joystick_1_buttons_x_offset = 1072 + debug_x_offset
          joystick_1_buttons_y_offset = 128 + debug_y_offset

          if GAME_CONTROLS['JOYSTICK_1']['controller_a']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_1']['controller_b']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_1']['controller_x']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_1']['controller_y']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_buttons_y_offset)))

          #Left Axis
          joystick_1_axis_x_offset = 1088 + debug_x_offset
          joystick_1_axis_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_axis_y_offset)))        
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_1']['axis_0'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_1']['axis_1'] * 8)))

          #Right Axis
          joystick_1_axis_x_offset = 960 + debug_x_offset
          joystick_1_axis_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_axis_y_offset)))
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_1']['axis_2'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_1']['axis_3'] * 8)))

          #D-Pad
          joystick_1_dpad_x_offset = 1024 + debug_x_offset
          joystick_1_dpad_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
          for joystick_1_to_debug in JOYSTICKS:
            #Xbox Hat
            if JOYSTICKS[joystick_1_to_debug].get_name() == 'Xbox 360 Controller':
              if GAME_CONTROLS['JOYSTICK_1']['hat_up']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset - 16)))
              if GAME_CONTROLS['JOYSTICK_1']['hat_down']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_1']['hat_left']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_1']['hat_right']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
            #PowerA D-Pad
            if JOYSTICKS[joystick_1_to_debug].get_name() == 'PowerA NSW Wired controller':
              if GAME_CONTROLS['JOYSTICK_1']['dpad_up']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset - 16)))
              if GAME_CONTROLS['JOYSTICK_1']['dpad_down']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_1']['dpad_left']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_1']['dpad_right']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_1_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_1_dpad_y_offset)))

        if JOYSTICKS.get(2) != None: #Player 2 has a controller plugged in

          joystick_2_buttons_x_offset = 272 + debug_x_offset
          joystick_2_buttons_y_offset = 128 + debug_y_offset

          if GAME_CONTROLS['JOYSTICK_2']['controller_a']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GREEN_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_A_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_2']['controller_b']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_RED_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_B_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_2']['controller_x']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_BLUE_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_X_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          if GAME_CONTROLS['JOYSTICK_2']['controller_y']:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_YELLOW_WHITE'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))
          else:
            THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_BUTTON_Y_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_buttons_y_offset)))

          #Left Axis
          joystick_2_axis_x_offset = 288 + debug_x_offset
          joystick_2_axis_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_axis_y_offset)))        
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_2']['axis_0'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_2']['axis_1'] * 8)))

          #Right Axis
          joystick_2_axis_x_offset = 160 + debug_x_offset
          joystick_2_axis_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_axis_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_axis_y_offset)))
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['JOY_AXIS_DIRECTIONAL_WHITE'].get_rect(center = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_axis_x_offset - 15 + GAME_CONTROLS['JOYSTICK_2']['axis_2'] * 8, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_axis_y_offset - 16 + GAME_CONTROLS['JOYSTICK_2']['axis_3'] * 8)))

          #D-Pad
          joystick_2_dpad_x_offset = 224 + debug_x_offset
          joystick_2_dpad_y_offset = 96 + debug_y_offset
          THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'], GAME_SURFACES['INPUT_PROMPTS']['JOY_DPAD_BASE_GRAY'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
          for joystick_2_to_debug in JOYSTICKS:
            #Xbox Hat
            if JOYSTICKS[joystick_2_to_debug].get_name() == 'Xbox 360 Controller':
              if GAME_CONTROLS['JOYSTICK_2']['hat_up']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset - 16)))
              if GAME_CONTROLS['JOYSTICK_2']['hat_down']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_2']['hat_left']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_2']['hat_right']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
            #PowerA D-Pad
            if JOYSTICKS[joystick_2_to_debug].get_name() == 'PowerA NSW Wired controller':
              if GAME_CONTROLS['JOYSTICK_2']['dpad_up']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['UP_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset - 16)))
              if GAME_CONTROLS['JOYSTICK_2']['dpad_down']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['DOWN_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_2']['dpad_left']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['LEFT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset - 16, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))
              if GAME_CONTROLS['JOYSTICK_2']['dpad_right']:
                THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'], GAME_SURFACES['INPUT_PROMPTS']['RIGHT_ARROW_GOLD'].get_rect(bottomright = (GAME_CONSTANTS['SCREEN_WIDTH'] - joystick_2_dpad_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - joystick_2_dpad_y_offset)))

    #Show Actual Game Control Inputs for Player 1
    player_one_direction_x_offset = 10 + debug_x_offset
    player_one_direction_y_offset = 10 + debug_y_offset
    THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_BASE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_BASE'].get_rect(bottomleft = (player_one_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_direction_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['UP']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_UP_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_UP_WHITE'].get_rect(bottomleft = (player_one_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_direction_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['LEFT']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_LEFT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_LEFT_WHITE'].get_rect(bottomleft = (player_one_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_direction_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['DOWN']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_DOWN_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_DOWN_WHITE'].get_rect(bottomleft = (player_one_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_direction_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['RIGHT']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_RIGHT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_RIGHT_WHITE'].get_rect(bottomleft = (player_one_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_direction_y_offset)))

    player_one_game_buttons_x_offset = 48 + debug_x_offset
    player_one_game_buttons_y_offset = 8 + debug_y_offset
    if GAME_CONTROLS['PLAYER_1']['GREEN']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_DOWN'].get_rect(bottomleft = (player_one_game_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_UP'].get_rect(bottomleft = (player_one_game_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['RED']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_DOWN'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_UP'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    if GAME_CONTROLS['PLAYER_1']['BLUE']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_DOWN'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_UP'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))

    if GAME_CONTROLS['PLAYER_1']['YELLOW']:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_DOWN'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))
    else:
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_UP'].get_rect(bottomleft = (player_one_game_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_one_game_buttons_y_offset)))

    #If we are in multiplayer mode show actual game control inputs for Player 2
    if GAME_STATE['MULTIPLAYER']:
      player_two_direction_x_offset = 1098 + debug_x_offset
      player_two_direction_y_offset = 10 + debug_y_offset
      THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_BASE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_BASE'].get_rect(bottomleft = (player_two_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_direction_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['UP']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_UP_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_UP_WHITE'].get_rect(bottomleft = (player_two_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_direction_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['LEFT']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_LEFT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_LEFT_WHITE'].get_rect(bottomleft = (player_two_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_direction_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['DOWN']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_DOWN_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_DOWN_WHITE'].get_rect(bottomleft = (player_two_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_direction_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['RIGHT']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_RIGHT_WHITE'], GAME_SURFACES['INPUT_PROMPTS']['DIRECTION_RIGHT_WHITE'].get_rect(bottomleft = (player_two_direction_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_direction_y_offset)))

      player_two_game_buttons_x_offset = 1136 + debug_x_offset
      player_two_game_buttons_y_offset = 8 + debug_y_offset
      if GAME_CONTROLS['PLAYER_2']['GREEN']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_DOWN'].get_rect(bottomleft = (player_two_game_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      else:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['GREEN_BUTTON_UP'].get_rect(bottomleft = (player_two_game_buttons_x_offset, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['RED']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_DOWN'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      else:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['RED_BUTTON_UP'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 32, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      if GAME_CONTROLS['PLAYER_2']['BLUE']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_DOWN'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      else:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['BLUE_BUTTON_UP'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 64, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))

      if GAME_CONTROLS['PLAYER_2']['YELLOW']:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_DOWN'], GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_DOWN'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))
      else:
        THE_SCREEN.blit(GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_UP'], GAME_SURFACES['INPUT_PROMPTS']['YELLOW_BUTTON_UP'].get_rect(bottomleft = (player_two_game_buttons_x_offset + 96, GAME_CONSTANTS['SCREEN_HEIGHT'] - player_two_game_buttons_y_offset)))

    ####################################################################
    # Debug Grid, useful for lining things up
    ####################################################################
    if GAME_STATE['DEBUG_GRID']:
      pygame.draw.lines(THE_SCREEN, GAME_COLORS['GREEN'], False, GAME_CONSTANTS['DEBUG_GRID'], width=1)

  ####################################################################
  # FINAL UPDATES FOR OUR GAME LOOP
  #
  # ***LESSON 1*** ***GAME LOOP***
  #
  # Tell the game to update what's on screen visually.
  #
  # Calculate how much time has elapsed so we can update our game
  # on the next frame.
  ####################################################################
  if GAME_CLI_ARGUMENTS.double_buffer:
    pygame.display.flip() #Updates the whole screen, with double buffering, we want to use flip
  else:
    pygame.display.update() #show the updates
  
  ELAPSED_MS = GAME_CLOCK.tick(60)
  ELAPSED_S = ELAPSED_MS / 1000.0
  #FRAME_COUNTER = FRAME_COUNTER + 1

pygame.quit()