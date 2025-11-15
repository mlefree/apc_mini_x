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
        self.apc.log_message("MLE: QuantizeMode initialized")

    def getName(self):
        return "quantize"

    def syncLights(self):
        self.apc.log_message("MLE: QuantizeMode syncLights - current mode=" + str(self.apc.quantizeMode) + " (" + self.QUANTIZE_MODES.get(self.apc.quantizeMode, "unknown") + ")")
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
            self.apc.log_message("MLE: QuantizeMode received note=" + str(note))
            if note == BUTTON_EXIT:
                self.apc.log_message("MLE: QuantizeMode EXIT - going to root menu")
                self.gotoRootMenu()
            if note == BUTTON_NEXT and self.apc.quantizeMode < 8:
                old_mode = self.apc.quantizeMode
                self.apc.quantizeMode = self.apc.quantizeMode + 1
                self.apc.log_message("MLE: QuantizeMode NEXT - changed from " + str(old_mode) + " to " + str(self.apc.quantizeMode))
                self.syncLights()
            if note == BUTTON_PREV and self.apc.quantizeMode > 0:
                old_mode = self.apc.quantizeMode
                self.apc.quantizeMode = self.apc.quantizeMode - 1
                self.apc.log_message("MLE: QuantizeMode PREV - changed from " + str(old_mode) + " to " + str(self.apc.quantizeMode))
                self.syncLights()
        return False


class APC_mini_mle3(APC_Key_25):
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

    # Lateral cascade state
    cascade_active = False
    cascade_clip_index = -1
    cascade_start_track_index = -1
    cascade_current_track_index = -1
    cascade_expected_beats = 0

    # @Overridden
    def __init__(self, *a, **k):
        (super(APC_mini_mle3, self).__init__)(*a, **k)
        with self.component_guard():
            self.register_disconnectable(SimpleLayerOwner(layer=Layer(_unused_buttons=(self.wrap_matrix(self._unused_buttons)))))

        self.log_message("=" * 60)
        self.log_message("MLE3 INITIALIZATION - Lateral Cascade Mode")
        self.log_message("Version: 1.0")
        self.log_message("Product ID: 40")
        self.log_message("Installation successful!")
        self.log_message("=" * 60)
        self.set_fixed_record_bar_length(self.RECORD_BAR_LENGTH)
        self._suppress_send_midi = False
        self.mode = None
        self.rootMenu = ShiftedMenuMode(self)
        self.tempoTapMillis = 0
        self.log_message("MLE3: Initialization complete")

    # @Overridden
    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    # @Overridden
    def _create_controls(self):
        super(APC_mini_mle3, self)._create_controls()
        self._unused_buttons = list(map(self.make_shifted_button, self._scene_launch_buttons[5:7]))
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    # @Overridden
    def _create_mixer(self):
        mixer = super(APC_mini_mle3, self)._create_mixer()
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
            self.log_message("MLE3 Cascade: Polling stopped - cascade not active")
            return

        song = self.song()
        track = song.tracks[self.cascade_current_track_index]
        clip_slot = track.clip_slots[self.cascade_clip_index]

        if not clip_slot.has_clip:
            self.log_message("MLE3: WARNING - Clip disappeared during polling!")
            return

        clip = clip_slot.clip

        if clip.is_recording:
            # Monitor recording progress
            expected_length = self.cascade_expected_beats
            current_beat = clip.playing_position

            # Log progress every 4 beats for visibility
            if int(current_beat) % 4 == 0 and int(current_beat) > 0:
                progress_pct = int((current_beat / expected_length) * 100)
                self.log_message("MLE3 Cascade: Recording progress - beat " + str(round(current_beat, 1)) +
                               "/" + str(expected_length) + " (" + str(progress_pct) + "%)")

            # Anticipatory firing: trigger next clip at 75% of current recording
            if current_beat >= expected_length * CASCADE_FIRE_THRESHOLD and not hasattr(self, 'cascade_next_fired'):
                # Blink next pad as visual feedback
                # next_track_index = self.cascade_current_track_index + 1
                # if next_track_index < 8:
                #     song = self.song()
                #     if next_track_index < len(song.tracks):
                #         next_clip_slot = song.tracks[next_track_index].clip_slots[self.cascade_clip_index]
                #         if not next_clip_slot.has_clip:
                #             # Blink next pad
                #             next_note = self.cascade_clip_index * 8 + next_track_index
                #             rowStart = self.rowStarts[7 - self.cascade_clip_index]
                #             next_note_corrected = rowStart + next_track_index
                #             self.really_do_send_midi((NOTE_ON_STATUS, next_note_corrected, BAR_BLINK))
                #             self.log_message("MLE3 Cascade: Blinking next pad at track " + str(next_track_index))

                self.log_message("=" * 60)
                self.log_message("MLE3 Cascade: THRESHOLD REACHED!")
                self.log_message("  Current beat: " + str(round(current_beat, 1)))
                self.log_message("  Expected: " + str(expected_length))
                self.log_message("  Progress: " + str(int(CASCADE_FIRE_THRESHOLD * 100)) + "%")
                self.log_message("  Firing next clip...")
                self.log_message("=" * 60)
                self.cascade_next_fired = True
                self._continue_cascade()
                return

            # Still recording, check again in 1 tick
            self.schedule_message(1, self._check_cascade_progress)
        else:
            # Recording finished - fallback if anticipatory firing didn't work
            if hasattr(self, 'cascade_next_fired'):
                delattr(self, 'cascade_next_fired')
            else:
                self.log_message("MLE3 Cascade: Clip finished recording at track " + str(self.cascade_current_track_index))
                self._continue_cascade()

    def _continue_cascade(self):
        """
        Continue cascade to next track (right) or complete and play first clip.
        Called at 75% of current recording (anticipatory) or when finished (fallback).
        """
        song = self.song()

        # Move to next track (cascading right)
        next_track_index = self.cascade_current_track_index + 1

        # Check cascade completion: reached right edge or occupied slot
        if next_track_index >= 8 or next_track_index >= len(song.tracks):
            self.log_message("=" * 60)
            self.log_message("MLE3 Cascade: COMPLETE!")
            self.log_message("  Reached right edge at track " + str(self.cascade_current_track_index))
            self.log_message("  Playing first clip at track " + str(self.cascade_start_track_index))
            self.log_message("=" * 60)
            self.cascade_active = False

            # Clean up state flags
            if hasattr(self, 'cascade_next_fired'):
                delattr(self, 'cascade_next_fired')

            # # Stop the last recorded clip if playing
            # current_track = song.tracks[self.cascade_current_track_index]
            # current_clip_slot = current_track.clip_slots[self.cascade_clip_index]
            # if current_clip_slot.has_clip and current_clip_slot.clip.is_playing:
            #     current_clip_slot.clip.stop()

            # # Fire first clip to start playback
            # first_track = song.tracks[self.cascade_start_track_index]
            # first_clip_slot = first_track.clip_slots[self.cascade_clip_index]
            # if first_clip_slot.has_clip:
            #     first_clip_slot.fire()
            #     self.log_message("MLE3 Cascade: Started playback from track " + str(self.cascade_start_track_index))
            # else:
            #     self.log_message("MLE3 Cascade: ERROR - First clip missing at track " + str(self.cascade_start_track_index))
            # return

        # Check if next slot is occupied
        next_track = song.tracks[next_track_index]
        next_clip_slot = next_track.clip_slots[self.cascade_clip_index]
        if next_clip_slot.has_clip:
            self.log_message("=" * 60)
            self.log_message("MLE3 Cascade: STOPPED - occupied slot detected")
            self.log_message("  Next slot at track " + str(next_track_index) + " is occupied")
            self.log_message("  Playing first clip at track " + str(self.cascade_start_track_index))
            self.log_message("=" * 60)
            self.cascade_active = False

            # Clean up
            if hasattr(self, 'cascade_next_fired'):
                delattr(self, 'cascade_next_fired')

            # # Fire first clip
            # first_track = song.tracks[self.cascade_start_track_index]
            # first_clip_slot = first_track.clip_slots[self.cascade_clip_index]
            # if first_clip_slot.has_clip:
            #     first_clip_slot.fire()
            #     self.log_message("MLE3 Cascade: Started playback from track " + str(self.cascade_start_track_index))
            # return

        # Continue cascading
        if hasattr(self, 'cascade_next_fired'):
            delattr(self, 'cascade_next_fired')

        self.cascade_current_track_index = next_track_index

        # Calculate bars for this track (same as mle1)
        last_bars = self.fixed_record_bar_length()
        if last_bars == 0:
            last_bars = 8

        bars = last_bars
        if next_track_index == 0:
            bars = 1
        elif next_track_index == 1 or next_track_index == 2:
            bars = 2
        elif next_track_index == 3 or next_track_index == 4:
            bars = 4

        beatsPerBar = int(song.signature_numerator)
        beats = bars * beatsPerBar

        self.log_message("=" * 60)
        self.log_message("MLE3 Cascade: CONTINUING to next track")
        self.log_message("  Track: " + str(next_track_index))
        self.log_message("  Bars: " + str(bars))
        self.log_message("  Beats: " + str(beats))
        self.log_message("=" * 60)

        # Store expected length for anticipatory firing
        self.cascade_expected_beats = beats

        # Start recording next clip
        next_track.arm = True
        next_clip_slot.fire(beats)

        # Wait for clip creation before polling
        self.schedule_message(2, lambda: self._start_cascade_polling(0))

    def _start_cascade_polling(self, retry_count=0):
        """
        Start polling once clip is created.
        Ableton needs a few ticks to create the clip object after fire(beats).
        """
        if not self.cascade_active:
            self.log_message("MLE3: Polling cancelled - cascade not active")
            return

        song = self.song()
        track = song.tracks[self.cascade_current_track_index]
        clip_slot = track.clip_slots[self.cascade_clip_index]

        if clip_slot.has_clip:
            self.log_message("=" * 60)
            self.log_message("MLE3: CLIP CREATED - Starting monitoring")
            self.log_message("  Track: " + str(self.cascade_current_track_index))
            self.log_message("  Row: " + str(self.cascade_clip_index))
            self.log_message("  Expected beats: " + str(self.cascade_expected_beats))
            self.log_message("=" * 60)
            self._check_cascade_progress()
        else:
            # Retry up to 100 times (~2 seconds max)
            if retry_count < 100:
                if retry_count % 10 == 0:  # Log every 10 retries
                    self.log_message("MLE3: Waiting for clip creation... (retry " + str(retry_count) + "/100)")
                self.schedule_message(1, lambda: self._start_cascade_polling(retry_count + 1))
            else:
                self.log_message("=" * 60)
                self.log_message("MLE3: ERROR - Clip creation timeout!")
                self.log_message("  Track: " + str(self.cascade_current_track_index))
                self.log_message("  Aborting cascade")
                self.log_message("=" * 60)
                self.cascade_active = False

    # Need rowStarts for blinking calculation
    rowStarts = [56, 48, 40, 32, 24, 16, 8, 0]

    def _releaseShiftMenu(self, midi_bytes):

        song = self.song()
        note = midi_bytes[1]

        if note != SHIFT_KEY:
            return False

        self.shiftPressed = False

        # Double tap on shift key => show advanced menu
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

        self.log_message("MLE _applyShiftMenu: note=" + str(note))

        if note == SHIFT_KEY:
            self.shiftPressed = True
            self.show_message("Shift + row 6 = metronome, row 7= undo")
            self.log_message("MLE: SHIFT pressed")

        if note == BUTTON_UNDO and self.shiftPressed:
            self.log_message("MLE: UNDO triggered")
            song.undo()
            return True

        if note == BUTTON_METRONOME and self.shiftPressed:
            self.log_message("MLE: METRONOME toggle")
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
                self.log_message("MLE: *** TEMPO UP *** old=" + str(old_tempo) + " new=" + str(new_tempo))
                self.show_message("Tempo: " + str(int(song.tempo)))
                return True

            # SHIFT + BUTTON_EXIT: Tempo down
            if note == BUTTON_EXIT:
                old_tempo = song.tempo
                current_rounded = int(round(song.tempo))
                song.tempo = max(current_rounded - 1, MIN_TEMPO)
                new_tempo = song.tempo
                self.log_message("MLE: *** TEMPO DOWN *** old=" + str(old_tempo) + " new=" + str(new_tempo))
                self.show_message("Tempo: " + str(int(song.tempo)))
                return True

            # SHIFT + BUTTON_PREV: Tempo tap
            if note == BUTTON_PREV:
                now = int(round(time.time() * 1000))
                self.log_message("MLE: *** TEMPO TAP *** now=" + str(now) + " last=" + str(self.tempoTapMillis))
                if self.tempoTapMillis > 0 and now - self.tempoTapMillis < TAP_TEMPO_TIMEOUT_MS:
                    interval = now - self.tempoTapMillis
                    new_tempo = 60000.0 / interval
                    self.log_message("MLE: TAP interval=" + str(interval) + "ms, calculated_tempo=" + str(new_tempo))
                    if MIN_TEMPO <= new_tempo <= MAX_TEMPO:
                        song.tempo = new_tempo
                        self.log_message("MLE: TAP tempo set to " + str(song.tempo))
                        self.show_message("Tempo: " + str(int(song.tempo)) + " (tapped)")
                    else:
                        self.log_message("MLE: TAP tempo out of range, ignored")
                else:
                    self.log_message("MLE: TAP first tap or timeout, recording timestamp")
                self.tempoTapMillis = now
                return True

            # SHIFT + BUTTON_NEXT: Start/Stop song
            if note == BUTTON_NEXT:
                was_playing = song.is_playing
                self.log_message("MLE: *** TRANSPORT START/STOP *** was_playing=" + str(was_playing))
                if song.is_playing:
                    song.stop_playing()
                    self.log_message("MLE: Transport STOPPED")
                    self.show_message("Stopped")
                else:
                    song.start_playing()
                    self.log_message("MLE: Transport STARTED")
                    self.show_message("Playing")
                return True

        # Double tap on note key => quantize
        now = int(round(time.time() * 1000))
        if note < 64:
            self.log_message("MLE: Grid pad pressed, note=" + str(note))

            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]
            if now - self.noteDoubleClickMillis < DOUBLE_TAP_TIMEOUT_MS:
                if clipSlot.has_clip:
                    mode_names = {0: "off", 1: "1/4", 2: "1/8", 3: "1/8T", 4: "1/8+T", 5: "1/16", 6: "1/16T", 7: "1/16+T", 8: "1/32"}
                    mode_name = mode_names.get(self.quantizeMode, "unknown")
                    self.log_message("MLE: Double-tap QUANTIZE - mode=" + str(self.quantizeMode) + " (" + mode_name + "), track=" + str(trackIndex) + ", clip=" + str(clipIndex))
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
            self.log_message("MLE3: Entering recording logic for note " + str(note))
            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]

            self.log_message("MLE3: Track=" + str(trackIndex) + ", Clip=" + str(clipIndex) +
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
            self.log_message("MLE3: Calculated bars=" + str(bars) + ", beats=" + str(beats))

            # Cascade conditions: empty slot
            if not clipSlot.has_clip and not clipSlot.is_group_slot:
                # Start lateral cascading record mode
                self.log_message("=" * 60)
                self.log_message("MLE3: STARTING LATERAL CASCADE RECORD!")
                self.log_message("  Row (clip_index): " + str(clipIndex))
                self.log_message("  Starting column (track): " + str(trackIndex))
                self.log_message("  Expected beats: " + str(beats))
                self.log_message("  Threshold (75%): " + str(beats * CASCADE_FIRE_THRESHOLD) + " beats")
                self.log_message("=" * 60)

                self.cascade_active = True
                self.cascade_clip_index = clipIndex
                self.cascade_start_track_index = trackIndex
                self.cascade_current_track_index = trackIndex

                # Reset cascade flags
                if hasattr(self, 'cascade_next_fired'):
                    delattr(self, 'cascade_next_fired')

                self.log_message("MLE3 Cascade: Starting at track " + str(trackIndex))

                # Store expected length for anticipatory firing
                self.cascade_expected_beats = beats

                track.arm = True
                self.log_message("MLE3: Track armed, firing clip with " + str(beats) + " beats")
                clipSlot.fire(beats)

                # Start polling
                self.schedule_message(2, lambda: self._start_cascade_polling(0))

                return True

        return False

    # @Overridden _do_send_midi
    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        if self.mode != None:
            return
        super(APC_mini_mle3, self)._do_send_midi(midi_bytes)

    # Used by edit modes to echo edit ops as lighting messages unrelated to usual Live clip events
    def really_do_send_midi(self, midi_bytes):
        super(APC_mini_mle3, self)._do_send_midi(midi_bytes)

    # @Overridden receive_midi
    def receive_midi(self, midi_bytes):

        self.log_message("MLE3 receive_midi: " + str(midi_bytes))
        extra_conf_applied = False

        # Custom Modes
        if self.mode is not None:
            self.log_message("MLE3: *** IN MENU MODE - Press button 65 to exit ***")
            self.mode.custom_receive_midi(midi_bytes)
            return

        # Shift released or applied
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            self.log_message("MLE3: NOTE_OFF detected")
            extra_conf_applied = self._releaseShiftMenu(midi_bytes)
        elif midi_bytes[0] & 240 == NOTE_ON_STATUS:
            self.log_message("MLE3: NOTE_ON detected - calling _applyShiftMenu")
            extra_conf_applied = self._applyShiftMenu(midi_bytes)

        # Transfer to Parent
        if not extra_conf_applied:
            self.log_message("MLE3: Passing to parent class")
            super(APC_mini_mle3, self).receive_midi(midi_bytes)
        else:
            self.log_message("MLE3: Handled by mle3 logic")

    def fixed_record_bar_length(self):
        return self.__fixed_record_bar_length

    def set_fixed_record_bar_length(self, barLength):
        self.__fixed_record_bar_length = barLength
