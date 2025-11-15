from __future__ import with_statement, absolute_import, print_function, unicode_literals
from builtins import map
import time
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
import APC_Key_25.APC_Key_25 as APC_Key_25

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT_KEY = 98
CC_STATUS = 176

VOLUME_KEY = 68
PAN_KEY = 69
SEND_KEY = 70
DEVICE_KEY = 71

BAR_OFF = 0
BAR_ON = 1
BAR_BLINK = 2

# Scene launch buttons (global controls)
BUTTON_ENTER = 64
BUTTON_EXIT = 65
BUTTON_PREV = 66
BUTTON_NEXT = 67

# Scene buttons
BUTTON_SCENE_1 = 82
BUTTON_SCENE_5 = 86
BUTTON_METRONOME = 87
BUTTON_UNDO = 88

# Tempo constants
MIN_TEMPO = 20
MAX_TEMPO = 999
TAP_TEMPO_TIMEOUT_MS = 2000
DOUBLE_TAP_TIMEOUT_MS = 500

# Cascade constants
CASCADE_FIRE_THRESHOLD = 0.75

class ModeBase():

    def __init__(self, apc):
        self.apc = apc
        self.rowStarts = [56, 48, 40, 32, 24, 16, 8, 0]
        self.letters = {

            "1": [
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0]
            ],
            "2": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0]
            ],
            "bar": [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 5, 0, 1, 1],
                [1, 1, 1, 5, 0, 5, 1, 0],
                [0, 0, 0, 5, 5, 5, 1, 0],
                [0, 0, 0, 5, 0, 5, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "bpm": [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 5, 0, 0],
                [1, 0, 1, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 1, 0, 1],
                [0, 0, 0, 5, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 0, 1]
            ],
            "tap": [
                [1, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 0, 1],
                [0, 1, 0, 5, 0, 1, 1, 1],
                [0, 1, 5, 0, 5, 1, 0, 0],
                [0, 0, 5, 5, 5, 1, 0, 0],
                [0, 0, 5, 0, 5, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "undo": [
                [1, 0, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 1, 1, 0]
            ],
            "metronome": [
                [1, 0, 1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1, 0],
                [1, 1, 1, 5, 5, 0, 1, 0],
                [1, 0, 1, 5, 0, 0, 1, 0],
                [0, 0, 0, 5, 5, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 0, 0],
                [0, 0, 0, 5, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "edit": [
                [1, 1, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 5, 5, 5],
                [1, 1, 0, 5, 1, 0, 5, 0],
                [1, 0, 0, 5, 1, 0, 5, 0],
                [1, 1, 5, 5, 1, 0, 5, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small1": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small2": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small3": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small4": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0]
            ],
            "small5": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small6": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small7": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small8": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small9": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small0": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "on": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 0, 1, 0]
            ],
            "off": [
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 5, 5, 0, 0, 0],
                [1, 1, 1, 5, 0, 1, 1, 0],
                [0, 0, 0, 5, 5, 1, 0, 0],
                [0, 0, 0, 5, 0, 1, 1, 0],
                [0, 0, 0, 5, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0]
            ],
            "quantize": [
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 5, 5, 5, 0],
                [1, 0, 1, 0, 5, 0, 0, 0],
                [1, 1, 1, 0, 5, 5, 0, 0],
                [0, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 5, 5, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }

    def custom_receive_midi(self, midi_bytes):
        return True

    def clear_lights(self):
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 68, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 69, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 70, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 71, 0))

    def gotoRootMenu(self):
        self.apc.mode = self.apc.rootMenu
        self.apc.mode.syncLights()

    def exitMode(self):
        self.apc.mode = None
        # Refresh lights after exiting mode
        self.apc._update_hardware()

    def paintLetter(self, letter):
        for rowNum, rowArr in enumerate(letter):
            rowStart = self.rowStarts[rowNum]
            for colNum, val in enumerate(rowArr):
                self.apc.really_do_send_midi((NOTE_ON_STATUS, rowStart + colNum, val))

    def paintNumber(self, number):
        numberAsString = str(number)
        offset = 0
        combined_letter = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        color = 1
        inc = 2
        if len(numberAsString) >= 3:
            inc = 1
        for char in numberAsString:
            letter = self.letters["small" + char]
            lastCol = 0
            if inc == 1:
                # No space between digits - use color to differentiate
                if color == 1:
                    color = 5
                else:
                    color = 1
            for rowNum, rowArr in enumerate(letter):
                for colNum, val in enumerate(rowArr):
                    if val == 1:
                        lastCol = max(lastCol, colNum)
                        if offset + colNum <= 7:
                            combined_letter[rowNum][offset + colNum] = color
            offset = offset + lastCol + inc
        self.paintLetter(combined_letter)


class ShiftedMenuMode(ModeBase):
    modeNum = 0

    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.apc.show_message("menuMode")
        self.modes = [RecordBarsMode(apc), TapTempoMode(apc), MetronomeMode(apc), QuantizeMode(apc), PaintMode(apc)]
        self.modeNum = 0
        # self.syncLights()

    def syncLights(self):
        self.apc.log_message("Mode name")
        self.apc.log_message(self.modes[self.modeNum].getName())
        self.apc.log_message("grid")
        self.apc.log_message(self.letters[self.modes[self.modeNum].getName()])
        self.paintLetter(self.letters[self.modes[self.modeNum].getName()])

        # Set status of menu buttons
        self.clear_lights()

        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_EXIT, 1))
        if self.modeNum < len(self.modes) - 1:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 0))
        if self.modeNum > 0:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 0))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == BUTTON_EXIT:
                self.exitMode()
                return
            if note == BUTTON_ENTER:
                self.apc.mode = self.modes[self.modeNum]
                self.apc.mode.syncLights()
                return
            if note == BUTTON_PREV:
                self.modeNum = max(0, self.modeNum - 1)
                self.syncLights()
            if note == BUTTON_NEXT:
                self.modeNum = min(len(self.modes) - 1, self.modeNum + 1)
                self.syncLights()

        return False


class PaintMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def getName(self):
        return "edit"

    def syncLights(self):
        self.paintLetter(self.grid)
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_EXIT, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 0))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == BUTTON_EXIT:
                self.gotoRootMenu()
                return
            if note < 64:
                trackIndex = self.apc.getTrackIndex(note)
                clipIndex = self.apc.getClipIndex(note)
                note = self.grid[clipIndex][trackIndex]
                if note == 0:
                    self.grid[clipIndex][trackIndex] = 1
                elif note == 1:
                    self.grid[clipIndex][trackIndex] = 3
                elif note == 3:
                    self.grid[clipIndex][trackIndex] = 5
                elif note == 5:
                    self.grid[clipIndex][trackIndex] = 0
                self.syncLights()
        return False


class RecordBarsMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)

    def getName(self):
        return "bar"

    def syncLights(self):
        self.paintNumber(self.apc.fixed_record_bar_length())
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_EXIT, 1))
        if self.apc.fixed_record_bar_length() > 1:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 1))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == BUTTON_EXIT:
                self.gotoRootMenu()
            if note == BUTTON_NEXT:
                self.apc.set_fixed_record_bar_length(self.apc.fixed_record_bar_length() + 1)
                self.syncLights()
            if note == BUTTON_PREV and self.apc.fixed_record_bar_length() > 1:
                self.apc.set_fixed_record_bar_length(self.apc.fixed_record_bar_length() - 1)
                self.syncLights()
        return False


class TapTempoMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)

    def getName(self):
        return "bpm"

    def syncLights(self):
        song = self.apc.song()
        self.paintNumber(int(song.tempo))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 1))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == BUTTON_NEXT:
                self.apc.song().tempo = int(self.apc.song().tempo) + 1
                self.syncLights()
                return
            if note == BUTTON_PREV:
                self.apc.song().tempo = int(self.apc.song().tempo) - 1
                self.syncLights()
                return
            if note == BUTTON_EXIT:
                self.gotoRootMenu()
                song = self.apc.song()
                # Round down tempo when exiting
                song.tempo = int(song.tempo)
            else:
                # Tap tempo on any grid pad
                song = self.apc.song()
                song.tap_tempo()
                self.syncLights()

        return False


class MetronomeMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)

    def getName(self):
        return "metronome"

    def syncLights(self):
        song = self.apc.song()
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 0))
        if song.metronome:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, BAR_BLINK))
            self.paintLetter(self.letters["on"])
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, BAR_ON))
            self.paintLetter(self.letters["off"])

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            # Toggle on BUTTON_NEXT or any grid pad
            if note == BUTTON_NEXT or note < 64:
                self.apc.song().metronome = not self.apc.song().metronome
                self.syncLights()
                return
            if note == BUTTON_EXIT:
                self.gotoRootMenu()

        return False


class QuantizeMode(ModeBase):
    # Quantization mode names for display
    QUANTIZE_MODES = {
        0: "off",
        1: "1/4",
        2: "1/8",
        3: "1/8T",
        4: "1/8+T",
        5: "1/16",
        6: "1/16T",
        7: "1/16+T",
        8: "1/32"
    }

    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.apc.log_message("MLE2: QuantizeMode initialized")

    def getName(self):
        return "quantize"

    def syncLights(self):
        self.apc.log_message("MLE2: QuantizeMode syncLights - current mode=" + str(self.apc.quantizeMode) + " (" + self.QUANTIZE_MODES.get(self.apc.quantizeMode, "unknown") + ")")
        self.paintNumber(self.apc.quantizeMode)
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_ENTER, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_EXIT, 1))
        if self.apc.quantizeMode > 0:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_PREV, 0))
        if self.apc.quantizeMode < 8:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, BUTTON_NEXT, 0))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            self.apc.log_message("MLE2: QuantizeMode received note=" + str(note))
            if note == BUTTON_EXIT:
                self.apc.log_message("MLE2: QuantizeMode EXIT - going to root menu")
                self.gotoRootMenu()
            if note == BUTTON_NEXT and self.apc.quantizeMode < 8:
                old_mode = self.apc.quantizeMode
                self.apc.quantizeMode = self.apc.quantizeMode + 1
                self.apc.log_message("MLE2: QuantizeMode NEXT - changed from " + str(old_mode) + " to " + str(self.apc.quantizeMode))
                self.syncLights()
            if note == BUTTON_PREV and self.apc.quantizeMode > 0:
                old_mode = self.apc.quantizeMode
                self.apc.quantizeMode = self.apc.quantizeMode - 1
                self.apc.log_message("MLE2: QuantizeMode PREV - changed from " + str(old_mode) + " to " + str(self.apc.quantizeMode))
                self.syncLights()
        return False


class APC_mini_mle2(APC_Key_25):
    # @Overridden
    SESSION_HEIGHT = 8
    # @Overridden
    HAS_TRANSPORT = False

    RECORD_BAR_LENGTH = 4

    # State tracking
    shiftPressed = False
    __fixed_record_bar_length = RECORD_BAR_LENGTH
    lastShiftUpMillis = 0
    firstShiftClickedNote = -1
    lastShiftClickedNote = -1
    noteDoubleClickMillis = 0
    quantizeMode = 7  # 1/16 + 1/16T (configurable via menu)
    mode = None

    # Cascading record state
    cascade_active = False
    cascade_track_index = -1
    cascade_start_clip_index = -1
    cascade_current_clip_index = -1
    cascade_expected_beats = 0

    # Scene loop state
    scene_loop_active = False
    scene_loop_current_scene = 4  # Scene button 5 (clip index 4)
    scene_loop_last_tap_millis_activate = 0
    scene_loop_last_tap_millis_deactivate = 0
    scene_loop_session_id = 0

    # @Overridden
    def __init__(self, *a, **k):
        #super(APC_mini_mle2, self).__init__(*a, **k)
        (super(APC_mini_mle2, self).__init__)(*a, **k)
        with self.component_guard():
            self.register_disconnectable(SimpleLayerOwner(layer=Layer(_unused_buttons=(self.wrap_matrix(self._unused_buttons)))))

        self.log_message("MLE2 - Cascading Record Mode")
        self.set_fixed_record_bar_length(self.RECORD_BAR_LENGTH)
        self._suppress_send_midi = False
        self.mode = None
        self.rootMenu = ShiftedMenuMode(self)
        self.tempoTapMillis = 0

    # @Overridden
    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    # @Overridden
    def _create_controls(self):
        super(APC_mini_mle2, self)._create_controls()
        self._unused_buttons = list(map(self.make_shifted_button, self._scene_launch_buttons[5:7]))
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    # @Overridden
    def _create_mixer(self):
        mixer = super(APC_mini_mle2, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=(self._master_volume_control))
        return mixer

    # @Overridden
    def _product_model_id_byte(self):
        return 40

    ####

    def getTrackIndex(self, note):
        return int(note % 8)

    def getClipIndex(self, note):
        return 7 - int((note - self.getTrackIndex(note)) / 8)

    def _check_cascade_progress(self):
        """
        Poll recording progress and fire next clip anticipatorily.
        Fires next clip during last bar of current recording for seamless transitions.
        """
        if not self.cascade_active:
            return

        song = self.song()
        track = song.tracks[self.cascade_track_index]
        clip_slot = track.clip_slots[self.cascade_current_clip_index]

        if not clip_slot.has_clip:
            self.log_message("MLE2: WARNING - Clip disappeared during polling!")
            return

        clip = clip_slot.clip

        if clip.is_recording:
            # Monitor recording progress using clip.playing_position
            # Note: clip.length is unreliable during recording
            expected_length = self.cascade_expected_beats
            current_beat = clip.playing_position

            # Anticipatory firing: trigger next clip at 75% of current recording
            # For 4-bar loops: fires at beat 12 of 16, giving 4 beats overlap
            if current_beat >= expected_length * CASCADE_FIRE_THRESHOLD and not hasattr(self, 'cascade_next_fired'):
                self.log_message("MLE2: Cascade: Reached " + str(int(CASCADE_FIRE_THRESHOLD * 100)) + "% at beat " +
                               str(round(current_beat, 1)) + "/" + str(expected_length) + ", firing next clip")
                self.cascade_next_fired = True
                self._continue_cascade()
                return

            # Still recording, check again in 1 tick (~10-20ms)
            self.schedule_message(1, self._check_cascade_progress)
        else:
            # Recording finished - fallback if anticipatory firing didn't work
            if hasattr(self, 'cascade_next_fired'):
                delattr(self, 'cascade_next_fired')
            else:
                self.log_message("MLE2: Cascade: Clip finished recording at row " + str(self.cascade_current_clip_index))
                self._continue_cascade()

    def _continue_cascade(self):
        """
        Continue cascade to next row or complete and play first clip.
        Called at 75% of current recording (anticipatory) or when finished (fallback).
        """
        song = self.song()
        track = song.tracks[self.cascade_track_index]

        # Move to next row (cascading downward)
        next_clip_index = self.cascade_current_clip_index + 1

        # Check cascade completion: reached bottom or occupied slot
        if next_clip_index >= 8 or track.clip_slots[next_clip_index].has_clip:
            self.log_message("MLE2: Cascade: Complete! Playing first clip at row " + str(self.cascade_start_clip_index))
            self.cascade_active = False

            # Clean up state flags
            if hasattr(self, 'cascade_next_fired'):
                delattr(self, 'cascade_next_fired')

            # Stop the last recorded clip if it's playing
            current_clip_slot = track.clip_slots[self.cascade_current_clip_index]
            if current_clip_slot.has_clip and current_clip_slot.clip.is_playing:
                current_clip_slot.clip.stop()

            # Fire first clip to start playback
            first_clip_slot = track.clip_slots[self.cascade_start_clip_index]
            if first_clip_slot.has_clip:
                first_clip_slot.fire()
                self.log_message("MLE2: Cascade: Started playback from row " + str(self.cascade_start_clip_index))
            else:
                self.log_message("MLE2: Cascade: ERROR - First clip missing at row " + str(self.cascade_start_clip_index))
            return

        # Continue cascading
        if hasattr(self, 'cascade_next_fired'):
            delattr(self, 'cascade_next_fired')

        self.cascade_current_clip_index = next_clip_index
        next_clip_slot = track.clip_slots[next_clip_index]

        # Calculate bars for this track (same as mle1)
        last_bars = self.fixed_record_bar_length()
        if last_bars == 0:
            last_bars = 8

        bars = last_bars
        if self.cascade_track_index == 0:
            bars = 1
        elif self.cascade_track_index == 1 or self.cascade_track_index == 2:
            bars = 2
        elif self.cascade_track_index == 3 or self.cascade_track_index == 4:
            bars = 4

        beatsPerBar = int(song.signature_numerator)
        beats = bars * beatsPerBar

        self.log_message("MLE2: Cascade: Recording next clip at row " + str(next_clip_index) + " with " + str(beats) + " beats")

        # Store expected length for anticipatory firing
        self.cascade_expected_beats = beats

        # Start recording next clip
        track.arm = True
        next_clip_slot.fire(beats)

        # Wait for clip creation before polling
        self.schedule_message(2, lambda: self._start_cascade_polling(0))

    def _start_cascade_polling(self, retry_count=0):
        """
        Start polling once clip is created.
        Ableton needs a few ticks to create the clip object after fire(beats).
        """
        if not self.cascade_active:
            return

        song = self.song()
        track = song.tracks[self.cascade_track_index]
        clip_slot = track.clip_slots[self.cascade_current_clip_index]

        if clip_slot.has_clip:
            self.log_message("MLE2: Monitoring row " + str(self.cascade_current_clip_index))
            self._check_cascade_progress()
        else:
            # Retry up to 100 times (~2 seconds max)
            if retry_count < 100:
                self.schedule_message(1, lambda: self._start_cascade_polling(retry_count + 1))
            else:
                self.log_message("MLE2: ERROR - Clip creation timeout, aborting cascade")
                self.cascade_active = False

    def _get_scene_max_clip_length(self, scene_index):
        """
        Get max clip length in beats for a scene.
        Returns 0 if no clips found.
        """
        song = self.song()
        max_length = 0

        for track in song.tracks:
            if scene_index < len(track.clip_slots):
                clip_slot = track.clip_slots[scene_index]
                if clip_slot.has_clip:
                    clip = clip_slot.clip
                    if clip.length > max_length:
                        max_length = clip.length

        return max_length

    def _fire_scene_clips(self, scene_index):
        """
        Fire all clips in a scene. Scene_index is clip_slots index (0-7).
        """
        song = self.song()
        clips_fired = 0

        self.log_message("MLE2: Scene Loop: Firing clips at index " + str(scene_index) +
                        " (button " + str(scene_index + 1) + ")")

        for track in song.tracks:
            if scene_index < len(track.clip_slots):
                clip_slot = track.clip_slots[scene_index]
                if clip_slot.has_clip:
                    clip_slot.fire()
                    clips_fired += 1

        self.log_message("MLE2: Scene Loop: Fired " + str(clips_fired) + " clips")
        return clips_fired

    def _schedule_next_scene(self):
        """
        Schedule advancement to next scene based on clip length.
        Uses calculated delay instead of polling for more reliable timing.
        """
        if not self.scene_loop_active:
            return

        song = self.song()

        # Don't schedule if song stopped
        if not song.is_playing:
            self.log_message("MLE2: Scene Loop: Song stopped, not scheduling next scene")
            self._deactivate_scene_loop()
            return

        current_scene = self.scene_loop_current_scene

        # Get max clip length in current scene
        max_length_beats = self._get_scene_max_clip_length(current_scene)
        self.log_message("MLE2: Scene Loop: Scene " + str(current_scene) + " max length = " +
                        str(max_length_beats) + " beats")

        if max_length_beats == 0:
            # No clips, move to next immediately
            self.log_message("MLE2: Scene Loop: Scene " + str(current_scene) + " has no clips, advancing")
            self._advance_to_next_scene()
            return

        # Calculate delay in ticks
        # Ticks are ~100ms each, so ticks = seconds * 10
        tempo = song.tempo
        seconds = max_length_beats * (60.0 / tempo)
        ticks = int(seconds * 10)

        self.log_message("MLE2: Scene Loop: Will advance in " + str(round(seconds, 1)) +
                        " seconds (" + str(ticks) + " ticks at " + str(tempo) + " BPM)")

        # Schedule the advancement with current session ID
        current_session = self.scene_loop_session_id
        self.schedule_message(ticks, lambda: self._advance_to_next_scene(current_session))

    def _advance_to_next_scene(self, session_id):
        """
        Advance to next scene (5->6->7->8, indices 4->5->6->7).
        session_id invalidates old callbacks from previous sessions.
        """
        # Ignore callbacks from old sessions
        if session_id != self.scene_loop_session_id:
            self.log_message("MLE2: Scene Loop: Ignoring callback from old session (ID " +
                           str(session_id) + " vs current " + str(self.scene_loop_session_id) + ")")
            return

        if not self.scene_loop_active:
            return

        song = self.song()

        # If song stopped, deactivate
        if not song.is_playing:
            self.log_message("MLE2: Scene Loop: Song stopped, deactivating scene loop")
            self._deactivate_scene_loop()
            return

        # Move to next scene
        self.scene_loop_current_scene += 1

        # Wrap back to scene button 5 (clip index 4) after scene button 8 (clip index 7)
        if self.scene_loop_current_scene > 7:
            self.scene_loop_current_scene = 4
            self.log_message("MLE2: Scene Loop: Looping back to scene button 5 (index 4)")

        # Reset timing tracking
        if hasattr(self, '_scene_loop_started'):
            delattr(self, '_scene_loop_started')
        if hasattr(self, '_scene_loop_start_time'):
            delattr(self, '_scene_loop_start_time')

        # Fire clips in the new scene
        self._fire_scene_clips(self.scene_loop_current_scene)

        # Schedule advancement to next scene
        self._schedule_next_scene()

    def _activate_scene_loop(self):
        """
        Activate scene loop - loop through scene buttons 5-8 (clip indices 4-7).
        """
        self.log_message("MLE2: ACTIVATING SCENE LOOP MODE")

        # Increment session ID to invalidate pending callbacks from previous sessions
        self.scene_loop_session_id += 1
        self.log_message("MLE2: Scene Loop: New session ID = " + str(self.scene_loop_session_id))

        self.scene_loop_active = True
        self.scene_loop_current_scene = 4  # Scene button 5 = clip index 4

        # Clean up any previous state
        if hasattr(self, '_scene_loop_started'):
            delattr(self, '_scene_loop_started')
        if hasattr(self, '_scene_loop_start_time'):
            delattr(self, '_scene_loop_start_time')

        song = self.song()

        # Start transport if not playing
        if not song.is_playing:
            self.log_message("MLE2: Scene Loop: Starting transport")
            song.start_playing()

        # Fire clips in scene button 5 (clip index 4) to start
        self._fire_scene_clips(self.scene_loop_current_scene)

        # Schedule advancement to next scene
        self._schedule_next_scene()

        self.show_message("Scene Loop: Active (buttons 5-8)")

    def _deactivate_scene_loop(self):
        """
        Deactivate scene loop - return to normal operation.
        """
        self.log_message("MLE2: DEACTIVATING SCENE LOOP MODE")
        self.scene_loop_active = False

        # Clean up state
        if hasattr(self, '_scene_loop_started'):
            delattr(self, '_scene_loop_started')
        if hasattr(self, '_scene_loop_start_time'):
            delattr(self, '_scene_loop_start_time')

        self.show_message("Scene Loop: Deactivated")

    def _releaseShiftMenu(self, midi_bytes):

        song = self.song()
        note = midi_bytes[1]

        if note != SHIFT_KEY:
            return False

        self.shiftPressed = False

        # Double tap on shift => show advanced menu
        now = int(round(time.time() * 1000))
        if now - self.lastShiftUpMillis < DOUBLE_TAP_TIMEOUT_MS:
            self.mode = self.rootMenu
            self.mode.syncLights()

        self.lastShiftUpMillis = now

        if self.firstShiftClickedNote >= 0:
            firstNote = self.firstShiftClickedNote
            lastNote = self.lastShiftClickedNote
            self.firstShiftClickedNote = -1
            self.lastShiftClickedNote = -1
            fromTrackIndex = self.getTrackIndex(firstNote)
            fromTrack = song.tracks[fromTrackIndex]
            fromClipIndex = self.getClipIndex(firstNote)
            fromClipSlot = fromTrack.clip_slots[fromClipIndex]
            fromClip = fromClipSlot.clip
            if fromClip is not None:
                if lastNote < 0:
                    fromClipSlot.delete_clip()
                else:
                    toTrackIndex = self.getTrackIndex(lastNote)
                    toTrack = song.tracks[toTrackIndex]
                    toClipIndex = self.getClipIndex(lastNote)
                    toClipSlot = toTrack.clip_slots[toClipIndex]

                    # fromTrack.duplicate_clip_slot(fromClipIndex)
                    fromClipSlot.duplicate_clip_to(toClipSlot)

        self.show_message("")
        return False

    def _applyShiftMenu(self, midi_bytes):

        song = self.song()
        note = midi_bytes[1]

        self.log_message("MLE2: _applyShiftMenu: note=" + str(note))

        if note == SHIFT_KEY:
            self.shiftPressed = True
            self.show_message("Shift + row 6 = metronome, row 7= undo")
            self.log_message("MLE2: SHIFT pressed")

        # Scene button 5 - Double tap to activate scene loop
        if note == BUTTON_SCENE_5:
            now = int(round(time.time() * 1000))
            if now - self.scene_loop_last_tap_millis_activate < DOUBLE_TAP_TIMEOUT_MS:
                self._activate_scene_loop()
                self.scene_loop_last_tap_millis_activate = 0  # Prevent triple-tap
                return True
            else:
                self.scene_loop_last_tap_millis_activate = now
                return False

        # Scene button 1 - Double tap to deactivate scene loop
        if note == BUTTON_SCENE_1:
            now = int(round(time.time() * 1000))
            if now - self.scene_loop_last_tap_millis_deactivate < DOUBLE_TAP_TIMEOUT_MS:
                self._deactivate_scene_loop()
                self.scene_loop_last_tap_millis_deactivate = 0  # Prevent triple-tap
                return True
            else:
                self.scene_loop_last_tap_millis_deactivate = now
                return False

        if note == BUTTON_UNDO and self.shiftPressed:
            self.log_message("MLE2: UNDO triggered")
            song.undo()
            return True

        if note == BUTTON_METRONOME and self.shiftPressed:
            self.log_message("MLE2: METRONOME toggle")
            song.tempo = round(song.tempo)
            song.metronome = not song.metronome
            return True

        # Global controls (SHIFT + scene buttons)
        if self.shiftPressed:
            # SHIFT + BUTTON_ENTER: Tempo up
            if note == BUTTON_ENTER:
                old_tempo = song.tempo
                current_rounded = int(round(song.tempo))
                song.tempo = min(current_rounded + 1, MAX_TEMPO)
                new_tempo = song.tempo
                self.log_message("MLE2: *** TEMPO UP *** old=" + str(old_tempo) + " new=" + str(new_tempo))
                self.show_message("Tempo: " + str(int(song.tempo)))
                return True

            # SHIFT + BUTTON_EXIT: Tempo down
            if note == BUTTON_EXIT:
                old_tempo = song.tempo
                current_rounded = int(round(song.tempo))
                song.tempo = max(current_rounded - 1, MIN_TEMPO)
                new_tempo = song.tempo
                self.log_message("MLE2: *** TEMPO DOWN *** old=" + str(old_tempo) + " new=" + str(new_tempo))
                self.show_message("Tempo: " + str(int(song.tempo)))
                return True

            # SHIFT + BUTTON_PREV: Tempo tap
            if note == BUTTON_PREV:
                now = int(round(time.time() * 1000))
                self.log_message("MLE2: *** TEMPO TAP *** now=" + str(now) + " last=" + str(self.tempoTapMillis))
                if self.tempoTapMillis > 0 and now - self.tempoTapMillis < TAP_TEMPO_TIMEOUT_MS:
                    interval = now - self.tempoTapMillis
                    new_tempo = 60000.0 / interval
                    self.log_message("MLE2: TAP interval=" + str(interval) + "ms, calculated_tempo=" + str(new_tempo))
                    if MIN_TEMPO <= new_tempo <= MAX_TEMPO:
                        song.tempo = new_tempo
                        self.log_message("MLE2: TAP tempo set to " + str(song.tempo))
                        self.show_message("Tempo: " + str(int(song.tempo)) + " (tapped)")
                    else:
                        self.log_message("MLE2: TAP tempo out of range, ignored")
                else:
                    self.log_message("MLE2: TAP first tap or timeout, recording timestamp")
                self.tempoTapMillis = now
                return True

            # SHIFT + BUTTON_NEXT: Start/Stop song
            if note == BUTTON_NEXT:
                was_playing = song.is_playing
                self.log_message("MLE2: *** TRANSPORT START/STOP *** was_playing=" + str(was_playing))
                if song.is_playing:
                    song.stop_playing()
                    self.log_message("MLE2: Transport STOPPED")
                    self.show_message("Stopped")
                else:
                    song.start_playing()
                    self.log_message("MLE2: Transport STARTED")
                    self.show_message("Playing")
                return True

        # Double tap on grid pad => quantize
        now = int(round(time.time() * 1000))
        if note < 64:
            self.log_message("MLE2: Grid pad pressed, note=" + str(note))

            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]
            if now - self.noteDoubleClickMillis < DOUBLE_TAP_TIMEOUT_MS:
                if clipSlot.has_clip:
                    mode_names = {0: "off", 1: "1/4", 2: "1/8", 3: "1/8T", 4: "1/8+T", 5: "1/16", 6: "1/16T", 7: "1/16+T", 8: "1/32"}
                    mode_name = mode_names.get(self.quantizeMode, "unknown")
                    self.log_message("MLE2: Double-tap QUANTIZE - mode=" + str(self.quantizeMode) + " (" + mode_name + "), track=" + str(trackIndex) + ", clip=" + str(clipIndex))
                    clipSlot.clip.quantize(self.quantizeMode, 1)
                    self.show_message("Quantized: " + mode_name)
                    return True

            if clipSlot.has_clip:
                self.noteDoubleClickMillis = now

        # Catch note selected with Shift
        if note < 64 and self.shiftPressed:
            if self.firstShiftClickedNote < 0:
                self.firstShiftClickedNote = note
                return True
            else:
                self.lastShiftClickedNote = note
                return True

        # Recording launch
        if note < 64:
            self.log_message("MLE2: Entering recording logic for note " + str(note))
            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]

            self.log_message("MLE2: Track=" + str(trackIndex) + ", Clip=" + str(clipIndex) +
                           ", has_clip=" + str(clipSlot.has_clip) +
                           ", is_group=" + str(clipSlot.is_group_slot))

            last_bars = self.fixed_record_bar_length()
            if last_bars == 0:
                last_bars = 8

            # Fixed track bar lengths (same as mle1)
            bars = last_bars
            if trackIndex == 0:
                bars = 1
            elif trackIndex == 1 or trackIndex == 2:
                bars = 2
            elif trackIndex == 3 or trackIndex == 4:
                bars = 4

            beatsPerBar = int(song.signature_numerator)
            beats = bars * beatsPerBar
            self.log_message("MLE2: Calculated bars=" + str(bars) + ", beats=" + str(beats))

            if not clipSlot.has_clip and not clipSlot.is_group_slot:
                # Start cascading record mode
                self.log_message("MLE2: STARTING CASCADE RECORD!")
                self.cascade_active = True
                self.cascade_track_index = trackIndex
                self.cascade_start_clip_index = clipIndex
                self.cascade_current_clip_index = clipIndex

                # Reset cascade flags
                if hasattr(self, 'cascade_next_fired'):
                    delattr(self, 'cascade_next_fired')
                if hasattr(self, 'cascade_completed'):
                    delattr(self, 'cascade_completed')

                self.log_message("MLE2: Cascade: Starting at row " + str(clipIndex))

                # Store expected length for anticipatory firing
                self.cascade_expected_beats = beats

                track.arm = True
                self.log_message("MLE2: Track armed, firing clip with " + str(beats) + " beats")
                clipSlot.fire(beats)

                # Start polling
                self.schedule_message(2, lambda: self._start_cascade_polling(0))

                return True
            else:
                self.log_message("MLE2: Clip exists or is group slot, stopping session_record")
                song.session_record = False

        return False

    # @Overridden _do_send_midi
    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        if self.mode != None:
            return
        super(APC_mini_mle2, self)._do_send_midi(midi_bytes)

    # Used by edit modes to echo edit ops as lighting messages unrelated to usual Live clip events
    def really_do_send_midi(self, midi_bytes):
        super(APC_mini_mle2, self)._do_send_midi(midi_bytes)

    # @Overridden receive_midi
    def receive_midi(self, midi_bytes):

        self.log_message("MLE2: receive_midi: " + str(midi_bytes))
        extra_conf_applied = False

        # Custom Modes
        if self.mode is not None:
            self.log_message("MLE2: *** IN MENU MODE - Press button 65 to exit ***")
            self.mode.custom_receive_midi(midi_bytes)
            return

        # Shift released or applied
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            self.log_message("MLE2: NOTE_OFF detected")
            extra_conf_applied = self._releaseShiftMenu(midi_bytes)
        elif midi_bytes[0] & 240 == NOTE_ON_STATUS:
            self.log_message("MLE2: NOTE_ON detected - calling _applyShiftMenu")
            extra_conf_applied = self._applyShiftMenu(midi_bytes)

        # Transfer to Parent
        if not extra_conf_applied:
            self.log_message("MLE2: Passing to parent class")
            super(APC_mini_mle2, self).receive_midi(midi_bytes)
        else:
            self.log_message("MLE2: Handled by mle2 logic")

    def fixed_record_bar_length(self):
        return self.__fixed_record_bar_length

    def set_fixed_record_bar_length(self, barLength):
        self.__fixed_record_bar_length = barLength
