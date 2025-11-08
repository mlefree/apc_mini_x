# APC mini mle

Opinionated MIDI remote script for Ableton Live with fixed bar lengths per track and streamlined live looping workflow.

## Philosophy

**mle** is designed around a simple idea: different tracks have different purposes. Instead of fiddling with loop lengths mid-performance, tracks have predetermined bar counts optimized for typical live looping workflows:

- **Track 1**: Quick hits and fills (1 bar)
- **Tracks 2-3**: Rhythmic elements (2 bars)
- **Tracks 4-5**: Melodic loops (4 bars)
- **Tracks 6-8**: Extended loops - customizable via menu (default: 8 bars)

This lets you focus on playing, not configuring.

---

# User Guide

## APC mini Layout

```
┌─────────────────────────────────────┐
│  [Grid: 8x8 Pads]                   │
│  Rows 0-7 (top to bottom)           │
│  Cols 0-7 (left to right = Tracks)  │
│                                      │
│  [Scene Launch Buttons]             │
│  Row 5: (unused)                    │
│  Row 6: METRONOME (with Shift)      │
│  Row 7: UNDO (with Shift)           │
│  Row 8: STOP ALL CLIPS              │
│                                      │
│  [SHIFT] button (note 98)           │
│                                      │
│  [Faders 0-7] Track volumes         │
│  [Fader 8]    Master volume         │
└─────────────────────────────────────┘
```

## Basic Operations

### Recording
**One-touch record**: Press any empty pad to start recording immediately
- Track auto-arms
- Recording length determined by track position (see bar lengths above)
- No need to pre-configure

**Multi-track recording**: Record on multiple tracks simultaneously

### Playback
**Launch clips**: Press a pad with a clip to play/stop it
**Stop all**: Press the bottom scene launch button

### Clip Management

**Delete a clip**:
1. Hold `SHIFT`
2. Press the clip you want to delete
3. Release `SHIFT`

**Copy a clip**:
1. Hold `SHIFT`
2. Press and hold the source clip
3. While still holding `SHIFT` and source clip, press destination pad
4. Release all

**Quantize a clip**:
- Double-tap a clip to quantize it
- Quantize mode: 1/16 + 1/16T (triplet)

### Session Control

**Undo**:
1. Hold `SHIFT`
2. Press the button above `STOP ALL CLIPS` (scene 7)

**Toggle Metronome**:
1. Hold `SHIFT`
2. Press the button above `UNDO` (scene 6)
3. Tempo is auto-rounded to integer

## Advanced Menu

**Access**: Double-tap `SHIFT` button

The menu system displays visual feedback on the 8x8 grid using lit pads.

### Navigation
- **Button 64**: Enter current menu option
- **Button 65**: Exit menu
- **Button 66**: Previous option (←)
- **Button 67**: Next option (→)

### Menu Options

#### 1. Bar Length Setup
**Display**: Shows number on grid
**Controls**:
- Button 67: Increase bar length (+1)
- Button 66: Decrease bar length (-1, min: 1)
- Button 65: Save and exit

Sets the fixed bar length for tracks 6-8.

#### 2. BPM / Tempo
**Display**: Shows current BPM on grid
**Controls**:
- Button 67: Increase tempo (+1 BPM)
- Button 66: Decrease tempo (-1 BPM)
- Tap any grid pad: Tap tempo
- Button 65: Exit (tempo rounded to integer)

#### 3. Metronome Toggle
**Display**: "ON" or "OFF" on grid
**Controls**:
- Button 67 or any grid pad: Toggle metronome
- Button 65: Exit

#### 4. Paint Mode (Grid Editor)
**Display**: Your custom pattern
**Controls**:
- Press pads to cycle through brightness: 0 → 1 → 3 → 5 → 0
- Create visual patterns (for fun!)
- Button 65: Exit

## Workflow Tips

**Quick looping**:
1. Start with percussion on Track 1 (1 bar)
2. Add rhythm elements on Tracks 2-3 (2 bars)
3. Layer melodies on Tracks 4-5 (4 bars)
4. Add atmospheric loops on Tracks 6-8 (8 bars)

**Live jamming**:
- Use double-tap quantize to tighten up timing
- Copy variations across rows for quick arrangement changes
- Keep `SHIFT` + Undo ready for experimentation

---

# Developer Documentation

## Architecture

Built on Ableton's `APC_Key_25` control surface framework with custom MIDI handling.

### File Structure
```
mle/
├── __init__.py              # Entry point, capabilities
├── APC_mini_mle.py          # Main script
└── README.md                # This file
```

### Main Class: `APC_mini_mle`

Extends `APC_Key_25` with custom MIDI receive logic.

**Key attributes**:
```python
SESSION_HEIGHT = 8           # 8x8 grid
HAS_TRANSPORT = False        # No transport controls
RECORD_BAR_LENGTH = 4        # Default for tracks 6-8
quantizeMode = 5             # 1/16 quantization
```

**State tracking**:
```python
shiftPressed                 # Shift button state
firstShiftClickedNote        # For copy operation (source)
lastShiftClickedNote         # For copy operation (destination)
noteDoubleClickMillis        # Double-tap detection
mode                         # Current menu mode (None = normal)
```

## Core Components

### 1. Mode System

**Base class**: `ModeBase`
- Provides grid manipulation utilities
- Letter/number display on 8x8 grid
- Light control helpers

**Modes**:
- `ShiftedMenuMode`: Root menu navigator
- `RecordBarsMode`: Bar length configuration
- `TapTempoMode`: BPM adjustment
- `MetronomeMode`: Metronome toggle
- `PaintMode`: Grid painter (Easter egg)

Each mode implements:
- `getName()`: Returns mode identifier
- `syncLights()`: Updates grid LEDs
- `custom_receive_midi(midi_bytes)`: Handles MIDI input

### 2. MIDI Message Flow

```
receive_midi(midi_bytes)
  ↓
  Mode active? → mode.custom_receive_midi()
  ↓
  NOTE_OFF? → _releaseShiftMenu()
  ↓
  NOTE_ON? → _applyShiftMenu()
  ↓
  Not handled? → parent.receive_midi()
```

### 3. Recording Logic

Located in `_applyShiftMenu()` when `note < 64`:

```python
# Calculate bar length
bars = last_bars  # Default from menu
if trackIndex == 0:
    bars = 1
elif trackIndex == 1 or trackIndex == 2:
    bars = 2
elif trackIndex == 3 or trackIndex == 4:
    bars = 4

# Calculate beats
beatsPerBar = int(song.signature_numerator)
beats = bars * beatsPerBar

# Fire recording
if not clipSlot.has_clip:
    track.arm = True
    clipSlot.fire(beats)
```

**Key method**: `clipSlot.fire(beats)`
- Starts recording if slot is empty
- Records for exactly `beats` beats
- Auto-stops when done

### 4. Grid Coordinate System

**Note to position**:
```python
def getTrackIndex(note):
    return int(note % 8)  # Column (0-7)

def getClipIndex(note):
    return 7 - int((note - getTrackIndex(note)) / 8)  # Row (0-7)
```

**MIDI notes**: 0-63 for grid (8x8)
- Note 0 = Top-left
- Note 7 = Top-right
- Note 56 = Bottom-left
- Note 63 = Bottom-right

**Row mapping**:
```python
rowStarts = [56, 48, 40, 32, 24, 16, 8, 0]
# Index 0 = top row (notes 56-63)
# Index 7 = bottom row (notes 0-7)
```

### 5. Special MIDI Notes

```python
SHIFT_KEY = 98           # Shift button
NOTE_ON_STATUS = 144     # 0x90
NOTE_OFF_STATUS = 128    # 0x80
CC_STATUS = 176          # 0xB0

# Scene buttons
64-67: Scene launch (rows 5-8)
87: Scene 6 (Metronome with Shift)
88: Scene 7 (Undo with Shift)

# Volume/Pan/Send/Device (top buttons)
68: Volume
69: Pan
70: Send
71: Device
```

### 6. Light Control

**Direct MIDI send**:
```python
self.really_do_send_midi((NOTE_ON_STATUS, note, velocity))
```

**Velocity/Color values**:
- `0`: Off
- `1`: Green
- `3`: Yellow
- `5`: Red
- `2`: Green blinking

### 7. Menu System Implementation

**Double-tap Shift detection**:
```python
now = int(round(time.time() * 1000))
if now - self.lastShiftUpMillis < 500:  # 500ms window
    self.mode = self.rootMenu
    self.mode.syncLights()
```

**Mode override**: When `mode != None`:
- `_do_send_midi()` blocks normal updates
- All MIDI routed to `mode.custom_receive_midi()`
- Prevents Live's default clip launching

### 8. Product ID

```python
def _product_model_id_byte(self):
    return 40
```

Must match `__init__.py`:
```python
controller_id(vendor_id=2536, product_ids=[40],
              model_name='APC MINI MLE')
```

## Customization Points

### Change bar lengths
Edit `_applyShiftMenu()` around line 690:
```python
if trackIndex == 0:
    bars = 1  # ← Change this
```

### Change quantize mode
Edit class attribute:
```python
quantizeMode = 5  # 5 = 1/16, 2 = 1/8, 7 = 1/16T
```

### Add new menu modes
1. Create class extending `ModeBase`
2. Add to `ShiftedMenuMode.modes` list
3. Implement `getName()`, `syncLights()`, `custom_receive_midi()`

### Modify double-tap timing
Change 500ms threshold in:
- Shift detection (line ~602)
- Quantize detection (line ~659)

## Technical Notes

**Frame rate**: Parent class handles updates
**Thread safety**: All in main Live thread
**Listeners**: Can add clip/track listeners if needed
**Schedule callbacks**: Use `self.schedule_message(ticks, callback)`

## Dependencies

- Ableton Live 11
- `_Framework` module (Live's control surface framework)
- `APC_Key_25` parent class
- Python 2.7 (Live's embedded Python)

---

*Built for speed, designed for flow*

