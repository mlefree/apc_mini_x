# APC mini mle3

Lateral cascade mode - one click fills an entire row from left to right automatically.

Based on **mle1** with automatic horizontal recording: press one pad, watch it cascade right recording each track to the right with the same bar length, then loop back to play. Perfect for building layered loops row by row.

## Philosophy

**mle3** takes the opinionated bar-length workflow of **mle1** and adds lateral (horizontal) cascading automation. Instead of manually recording each track, you trigger one pad and let the script build your horizontal loop stack automatically. This is ideal for:

- Building tracks layer-by-layer across columns
- Creating evolving arrangements that progress left to right
- Live performance where you need hands free for playing
- Rapid loop sketching horizontally

---

# User Guide

## How Lateral Cascade Works

### The Flow

```
You press Col 5, Row 5 → Records 4 bars (track 5)
                       ↓ (at 75% completion, blinks next)
            Auto-triggers Col 6, Row 5 → Records X bars (X depending and settings done in menu) (track 6)
                                      ↓ (at 75% completion, blinks next)
                          Auto-triggers Col 7, Row 5 → Records X bars (X depending and settings done in menu) (track 7)
                                                   ↓ (at 75% completion, blinks next)
                                        Auto-triggers Col 8, Row 5 → Records X bars (X depending and settings done in menu) (track 8)
```

### Example Session

**Row 5 (4-bar loops across tracks 4-7):**
1. Press Col 5, Row 5 → Records bass (4 bars)
2. *Automatically* Col 6 records → Add guitar X bars (X depending and settings done in menu) - Col 6 blinks just before
3. *Automatically* Col 7 records → Layer synth X bars (X depending and settings done in menu) - Col 7 blinks just before
4. *Automatically* Col 8 records → Add lead X bars (X depending and settings done in menu) - Col 8 blinks just before

All from **one button press**.

### Cascade Trigger Conditions

The cascade will **START** if:
- You press an **empty pad**
- AND all pads to the **left** in the same row are either filled OR there are no pads to the left

The cascade will **STOP** if:
- Reaches the rightmost column (Col 8)
- Encounters an already-occupied pad
- Then automatically plays the first clip

### Test Scenario

**Scenario 1: Full cascade (Col 5, Row 5)**
1. Press Col 5, Row 5 (assuming cols 1-4 in row 5 are filled or this is the leftmost)
2. Watch Col 6 blink at 75% progress
3. Col 6 starts recording while Col 5 finishes
4. Watch Col 7 blink at 75% progress
5. Col 7 starts recording while Col 6 finishes
6. Watch Col 8 blink at 75% progress
7. Col 8 starts recording while Col 7 finishes

**Scenario 2: Blocked cascade (Col 4, Row 5)**
1. If you press Col 4, Row 5 and Col 5, Row 5 already has a clip
2. Cascade stops immediately after Col 4 finishes

## APC mini Layout

```
┌─────────────────────────────────────┐
│  [Grid: 8x8 Pads]                   │
│  Each ROW = One cascade sequence    │
│  Each COLUMN = One track in cascade │
│                                      │
│  Track bar lengths:                 │
│  Col 0: 1 bar   (quick elements)    │
│  Col 1-2: 2 bars  (rhythms)         │
│  Col 3-4: 4 bars  (melodies)        │
│  Col 5-7: 8 bars  (atmospheres)     │
│                                      │
│  [Scene Launch Buttons]             │
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

### Cascade Recording

**Start a cascade**:
1. Press any **empty pad** where all pads to the left are filled or empty
2. Watch as it automatically:
   - Records that pad
   - Blinks the pad to the right (at 75% progress)
   - Moves to the pad to the right (same row, next column)
   - Records that pad
   - Repeats until hitting right edge or occupied slot

**What you do during cascade**:
- Keep playing your instrument
- Each track records automatically
- No need to press any buttons
- Watch for blinking pads as visual feedback

**Cascade stops when**:
- Reaches rightmost column (Col 8)
- Encounters an already-occupied pad
- Then automatically plays the first clip

### Standard Recording (Non-Cascade)

If you want to record **without** cascading:
- Record on a pad that already has a clip (replaces it)
- Record on a pad where there's an empty pad to the left (breaks cascade chain)

The cascade only triggers on **empty pads where all left pads are filled**.

### Playback & Session Control

Same as **mle1**:
- **Launch clips**: Press a pad to play/stop
- **Stop all**: Bottom scene button
- **Delete**: Shift + clip
- **Copy**: Shift + hold source + press destination
- **Quantize**: Double-tap clip (1/16 + 1/16T)
- **Undo**: Shift + scene 7 button
- **Metronome**: Shift + scene 6 button

## Advanced Menu

**Access**: Double-tap `SHIFT`

Same menu system as **mle1**:
1. **Bar Length** for tracks 6-8
2. **BPM/Tempo** adjustment and tap tempo
3. **Metronome** toggle
4. **Quantize Mode** configuration
5. **Paint Mode** (grid art)

See **mle1** documentation for full menu details.

## Workflow Examples

### Building a Track Horizontally (Row 3: 2-bar loops)

1. Fill Row 3, Cols 1-2 with drums
2. Press Row 3, Col 3 → Records bass (2 bars)
3. *Automatically* Col 4 records → Add guitar (2 bars) - Col 4 blinks
4. *Cascade complete* → Plays Col 3, both loops playing together

### Layered Progression (Row 5: 4-bar loops)

1. Press Row 5, Col 4 → Records chord progression (4 bars)
2. *Automatically* Col 5 records → Add melody layer (4 bars) - Col 5 blinks
3. *Automatically* Col 6 records → Add harmony (4 bars) - Col 6 blinks
4. *Automatically* Col 7 records → Add texture (4 bars) - Col 7 blinks
5. *Cascade complete* → Rich 4-layer track playing from Col 4

### Live Improvisation

- Start cascades on different rows
- They run independently
- Build entire arrangements hands-free
- Copy completed rows for variations

## Tips & Tricks

**Planning your rows**:
- Decide how many tracks you want before starting
- Fill earlier tracks to create the starting point for cascade

**Interrupting a cascade**:
- Record on a different row (cascades are per-row)
- Use Shift+Undo if you made a mistake
- Delete unwanted clips afterward

**Visual feedback**:
- Watch for blinking pads - they show the next recording target
- Blinking happens at 75% of current recording

**Performance flow**:
- Cascade frees your hands to keep playing
- Perfect for solo performers
- Great for live-looping competitions
- Allows continuous musical flow

---

# Developer Documentation

## Architecture

Extends **mle1** (`APC_mini_mle`) with lateral cascading record automation using **anticipatory firing** via polling.

### File Structure
```
mle3/
├── __init__.py              # Entry point (product ID: 40, same as mle1)
├── APC_mini_mle3.py         # Main script with lateral cascade logic
└── README.md                # This file
```

### Main Class: `APC_mini_mle3`

Extends `APC_Key_25` (via mle1 base) with lateral cascade state tracking and anticipatory firing mechanism.

**Additional attributes**:
```python
# Lateral cascading record state
cascade_active = False              # Is cascade running?
cascade_clip_index = -1             # Which row?
cascade_start_track_index = -1     # Starting column (for playback)
cascade_current_track_index = -1   # Current recording column
cascade_expected_beats = 0          # Expected length of recording (for anticipatory firing)
```

**Key innovation**: Instead of waiting for recording to finish, we fire the next clip during the **last bar** of the current recording, creating seamless transitions with no gap.


## Lateral Cascade State Machine

```
[IDLE]
  ↓ (user presses empty pad)
[START CASCADE]
  - cascade_active = True
  - cascade_expected_beats = beats
  - fire(beats) to start recording
  ↓
[WAIT FOR CLIP CREATION]
  - Retry every tick until clip exists
  ↓
[POLLING Track N - 0% to 75%]
  - Check clip.playing_position every tick
  - Monitor: current_beat < expected_beats * 0.75
  ↓
[ANTICIPATORY FIRING - at 75%]
  - BLINK next pad (visual feedback)
  - Fire NEXT clip while current still recording
  - _continue_cascade() called
  ↓
  ├─ Next slot empty & in bounds → [POLLING Track N+1] (loop back)
  │   - cascade_current_track_index++
  │   - Update cascade_expected_beats
  │   - fire(beats) for next track
  │
  └─ Next slot occupied OR track 7 reached → [COMPLETE CASCADE]
      - Stop last recorded clip
      - Fire first clip (cascade_start_track_index)
      - cascade_active = False
      ↓
     [PLAYBACK] → [IDLE]
```

## Key Differences from mle2

| Feature | mle2 (Vertical) | mle3 (Lateral) |
|---------|-----------------|----------------|
| Direction | Down (row + 1) | Right (track + 1) |
| Cascade check | Empty column | All left pads filled |
| Visual feedback | No blinking | Blinks next pad at 75% |
| Use case | Building layers vertically | Building tracks horizontally |
| Workflow | One click fills column | One click fills row |

## Customization Points

### Adjust anticipatory firing threshold

Same as mle2, modify `CASCADE_FIRE_THRESHOLD` constant at top of file.

### Change blink timing

In `_check_cascade_progress()`, adjust when blink happens (currently at 75%).

### Disable cascade for certain rows

```python
# In _applyShiftMenu(), before starting cascade:
if clipIndex in [0, 7]:  # Don't cascade on rows 0 and 7
    # Use original mle1 behavior
    track.arm = True
    clipSlot.fire(beats)
    return True
```

## Dependencies

Same as **mle1**:
- Ableton Live 11+ (tested with 12.2.6)
- `_Framework` module (built into Live)
- `APC_Key_25` parent class
- Python 2.7 (Live's embedded Python)

**Additional Live API usage**:
- `clip.playing_position` - Read current playback position during recording
- `clip.is_recording` - Check if clip is actively recording
- `schedule_message(ticks, callback)` - Schedule polling callbacks

---

*One click, cascade right - build your tracks horizontally*
