# APC mini mle2

Cascading record mode - one click fills the entire column automatically.

Based on **mle1** with automatic vertical recording: press one pad, watch it cascade down recording each row below with the same bar length, then loop back to play. Perfect for hands-free layered loop building.

## Philosophy

**mle2** takes the opinionated bar-length workflow of **mle1** and adds cascading automation. Instead of manually recording each layer, you trigger one pad and let the script build your vertical loop stack automatically. This is ideal for:

- Building complex layers without breaking flow
- Creating evolving textures that develop over time
- Live performance where you need hands free for playing
- Rapid loop sketching and experimentation

---

# User Guide

## How Cascading Works

### The Flow

```
You press Row 0 (top) → Records 4 bars
                     ↓ (when finished)
            Auto-triggers Row 1 → Records 4 bars
                              ↓ (when finished)
                     Auto-triggers Row 2 → Records 4 bars
                                       ↓ (and so on...)
                              Until Row 7 or occupied pad
                                       ↓ (then...)
                           Loops back and PLAYS Row 0
```

### Example Session

**Track 3 (2-bar loops):**
1. Press Row 0 → Records percussion (2 bars)
2. *Automatically* Row 1 records → Add hi-hats (2 bars)
3. *Automatically* Row 2 records → Layer snare (2 bars)
4. *Automatically* Row 3 records → Add percussion fill (2 bars)
5. *Cascade complete* → Plays Row 0, all 4 loops playing together

All from **one button press**.

## APC mini Layout

```
┌─────────────────────────────────────┐
│  [Grid: 8x8 Pads]                   │
│  Each COLUMN = One cascade sequence │
│  Each ROW = One layer in cascade    │
│                                      │
│  Track bar lengths:                 │
│  Col 0: 1 bar   (quick elements)    │
│  Col 1-2: 2 bars  (rhythms)         │
│  Col 3-4: 4 bars  (melodies)        │
│  Col 5-7: 8 bars  (atmospheres)     │
│                                      │
│  [Scene Launch Buttons]             │
│  Row 1: SCENE LOOP OFF (double-tap) │
│  Row 5: SCENE LOOP ON (double-tap)  │
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
1. Press any **empty pad** in an empty column
2. Watch as it automatically:
   - Records that pad
   - Moves to the pad below (same column, next row)
   - Records that pad
   - Repeats until hitting bottom or occupied slot
   - Returns to first pad and plays it

**What you do during cascade**:
- Keep playing your instrument
- Each layer records automatically with the same bar length
- No need to press any buttons

**Cascade stops when**:
- Reaches bottom row (row 7)
- Encounters an already-occupied pad
- Then automatically plays the first clip

The cascade only triggers on **empty pads**.

### Standard Recording (Non-Cascade)

If you want to record **without** cascading, record on a pad that:
- Already has a clip (replaces it)
- Is in a column with existing clips

### Playback & Session Control

Same as **mle1**:
- **Launch clips**: Press a pad to play/stop
- **Stop all**: Bottom scene button
- **Delete**: Shift + clip
- **Copy**: Shift + hold source + press destination
- **Quantize**: Double-tap clip (1/16 + 1/16T)
- **Undo**: Shift + scene 7 button
- **Metronome**: Shift + scene 6 button

### Scene Loop Mode

A powerful performance feature that cycles through scenes 5-8 automatically:

**Activate**: Double-tap scene button 5
**Deactivate**: Double-tap scene button 1

**How it works**:
1. Double-tap scene button 5 to start the loop
2. All clips in scene 5 (row 5) start playing
3. After the maximum clip length in scene 5 completes, scene 6 automatically starts
4. This continues through scenes 5 → 6 → 7 → 8 → back to 5
5. The loop continues until you deactivate it by double-tapping scene button 1

**Use cases**:
- Create evolving song sections that automatically progress
- Build verse → chorus → bridge → outro sequences
- Live performance arrangements with hands-free transitions
- Layered textures that develop over time

**Tips**:
- Scenes can have different length clips - the system waits for the longest clip to finish
- Empty scenes are skipped automatically
- You can still trigger other clips/scenes manually while the loop is running

## Advanced Menu

**Access**: Double-tap `SHIFT`

Same menu system as **mle1**:
1. **Bar Length** for tracks 6-8
2. **BPM/Tempo** adjustment and tap tempo
3. **Metronome** toggle
4. **Paint Mode** (grid art)

See **mle1** documentation for full menu details.

## Workflow Examples

### Building a Beat (Track 1: 1-bar loops)
1. Press Row 0, Track 1
2. Play kick drum for 1 bar → *cascade triggers*
3. Play hi-hat for 1 bar → *cascade triggers*
4. Play snare for 1 bar → *cascade triggers*
5. Play percussion for 1 bar → *cascade completes*
6. All 4 loops play together, you're already playing the next part

### Layered Pads (Track 5: 4-bar loops)
1. Press Row 0, Track 5
2. Play chord progression (4 bars) → *cascade triggers*
3. Add harmony layer (4 bars) → *cascade triggers*
4. Add texture/movement (4 bars) → *cascade triggers*
5. Add high melody (4 bars) → *cascade completes*
6. Rich 4-layer pad playing, ready for next track

### Live Improvisation
- Start multiple cascades on different tracks
- They run independently
- Build entire arrangements hands-free
- Copy completed columns across rows for variations

## Tips & Tricks

**Planning your columns**:
- Decide how many layers you want before starting
- Leave occupied pads to create shorter cascades (3-4 layers instead of 8)

**Interrupting a cascade**:
- Record on a different track (cascades are per-column)
- Use Shift+Undo if you made a mistake
- Delete unwanted clips afterward

**Performance flow**:
- Cascade frees your hands to keep playing
- Perfect for solo performers
- Great for live-looping competitions
- Allows continuous musical flow

---

# Developer Documentation

## Architecture

Extends **mle1** (`APC_mini_mle`) with cascading record automation using **anticipatory firing** via polling.

### File Structure
```
mle2/
├── __init__.py              # Entry point (product ID: 40, same as mle1)
├── APC_mini_mle2.py         # Main script with cascade logic
└── README.md                # This file
```

### Main Class: `APC_mini_mle2`

Extends `APC_mini_mle` with cascade state tracking and anticipatory firing mechanism.

**Additional attributes**:
```python
# Cascading record state
cascade_active = False              # Is cascade running?
cascade_track_index = -1            # Which track (column)?
cascade_start_clip_index = -1      # Starting row (for playback)
cascade_current_clip_index = -1    # Current recording row
cascade_expected_beats = 0          # Expected length of recording (for anticipatory firing)

# Scene loop state
scene_loop_active = False           # Is scene loop running?
scene_loop_current_scene = 5        # Current scene being played (5-8)
scene_loop_last_tap_millis_activate = 0    # Double-tap detection for scene 5
scene_loop_last_tap_millis_deactivate = 0  # Double-tap detection for scene 1
```

**Key innovation**: Instead of waiting for recording to finish, we fire the next clip during the **last bar** of the current recording, creating seamless transitions with no gap.

## Core Cascade Components

### 1. Cascade Trigger (Modified Recording)

Located in `_applyShiftMenu()` around line 840:

```python
if not clipSlot.has_clip and not clipSlot.is_group_slot:
    # Start cascading record mode
    self.cascade_active = True
    self.cascade_track_index = trackIndex
    self.cascade_start_clip_index = clipIndex
    self.cascade_current_clip_index = clipIndex
    self.cascade_expected_beats = beats  # Track expected length

    track.arm = True
    clipSlot.fire(beats)

    # Schedule polling to monitor progress
    self.schedule_message(2, lambda: self._start_cascade_polling(0))
```

**Key differences from mle1**:
- Sets `cascade_expected_beats` to track recording length
- Starts polling instead of waiting for clip to finish

### 2. Polling-Based Progress Monitoring

**Method**: `_check_cascade_progress()`

**Called**: Every tick (~10-20ms) while recording

**Logic - Anticipatory Firing**:
```python
def _check_cascade_progress(self):
    if clip.is_recording:
        expected_length = self.cascade_expected_beats  # e.g., 16 beats
        current_beat = clip.playing_position           # e.g., 12.5

        CASCADE_FIRE_THRESHOLD = 0.75  # 75%

        # Fire next clip during last bar (seamless transition)
        if current_beat >= expected_length * CASCADE_FIRE_THRESHOLD:
            self._continue_cascade()  # Fire next clip NOW
            return

        # Still recording, check again next tick
        self.schedule_message(1, self._check_cascade_progress)
```

**Key insight**:
- For 16-beat recording: fires next at beat **12** (75%)
- Next clip starts recording while current finishes last bar
- Creates **seamless overlap** with zero gap

**Why not use `clip.length`?**
During recording, `clip.length` returns a huge internal value (63072000) instead of beats. We track the expected length ourselves in `cascade_expected_beats`.

### 3. Cascade Continuation

**Method**: `_continue_cascade()`

**Responsibilities**:
1. Calculate next clip index (current + 1)
2. Check boundary conditions
3. Either:
   - Record next clip + add listener
   - Or end cascade + play first clip

**Completion conditions**:
```python
next_clip_index = self.cascade_current_clip_index + 1

# Stop cascade if:
if next_clip_index >= 8 or \
   track.clip_slots[next_clip_index].has_clip:

    # End cascade: stop last clip, play first clip
    self.cascade_active = False
    current_clip_slot.clip.stop()
    track.clip_slots[self.cascade_start_clip_index].fire()
    return

# Otherwise, continue to next row...
self.cascade_current_clip_index = next_clip_index
self.cascade_expected_beats = beats  # Update for next clip
track.arm = True
next_clip_slot.fire(beats)
self.schedule_message(2, lambda: self._start_cascade_polling(0))
```

### 4. Polling Initialization

**Method**: `_start_cascade_polling(retry_count=0)`

**Why retry?**: Clip doesn't exist immediately after `fire(beats)` - needs a few ticks.

```python
def _start_cascade_polling(self, retry_count=0):
    clip_slot = track.clip_slots[self.cascade_current_clip_index]

    if clip_slot.has_clip:
        # Clip created, start monitoring progress
        self._check_cascade_progress()
    else:
        # Clip not ready yet, retry (up to 100 times)
        if retry_count < 100:
            self.schedule_message(1, lambda: self._start_cascade_polling(retry_count + 1))
        else:
            # Timeout - abort cascade
            self.cascade_active = False
```

**Retry mechanism**: Waits up to ~2 seconds for Ableton to create the clip object.

## Cascade State Machine

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
[POLLING Row N - 0% to 75%]
  - Check clip.playing_position every tick
  - Monitor: current_beat < expected_beats * 0.75
  ↓
[ANTICIPATORY FIRING - at 75%]
  - Fire NEXT clip while current still recording
  - _continue_cascade() called
  ↓
  ├─ Next slot empty & in bounds → [POLLING Row N+1] (loop back)
  │   - cascade_current_clip_index++
  │   - Update cascade_expected_beats
  │   - fire(beats) for next row
  │
  └─ Next slot occupied OR row 7 reached → [COMPLETE CASCADE]
      - Stop last recorded clip
      - Fire first clip (cascade_start_clip_index)
      - cascade_active = False
      ↓
     [PLAYBACK] → [IDLE]
```

**Key timing**: Next clip fires at 75% of current recording, creating 25% overlap (1 bar for 4-bar loops).

## Scene Loop Components

### 1. Activation/Deactivation

**Method**: `_activate_scene_loop()` / `_deactivate_scene_loop()`

**Triggered by**: Double-tap on scene button 5 (note 86) to activate, scene button 1 (note 82) to deactivate

```python
# In _applyShiftMenu():
if note == 86:  # Scene button 5
    now = int(round(time.time() * 1000))
    if now - self.scene_loop_last_tap_millis_activate < 500:
        self._activate_scene_loop()  # Double-tap detected
```

**Activation logic**:
1. Set `scene_loop_active = True`
2. Reset to scene 5
3. Fire all clips in scene 5
4. Start progress monitoring

### 2. Scene Clip Management

**Method**: `_fire_scene_clips(scene_index)`

Fires all clips across all tracks in a given scene (row):
```python
for track in song.tracks:
    if scene_index < len(track.clip_slots):
        clip_slot = track.clip_slots[scene_index]
        if clip_slot.has_clip:
            clip_slot.fire()
```

**Method**: `_get_scene_max_clip_length(scene_index)`

Finds the longest clip in a scene to determine when to advance:
```python
max_length = 0
for track in song.tracks:
    if clip_slot.has_clip:
        if clip.length > max_length:
            max_length = clip.length
return max_length
```

### 3. Progress Monitoring

**Method**: `_check_scene_loop_progress()`

**Called**: Every 5 ticks (~50-100ms) while scene loop is active

**Logic**:
1. Get maximum clip length in current scene
2. Track elapsed time since scene started
3. When elapsed time >= max_length, advance to next scene
4. Skip empty scenes automatically

```python
current_time = song.get_current_beats_song_time().beats
elapsed = current_time - self._scene_loop_start_time

if elapsed >= max_length:
    self._advance_to_next_scene()
```

### 4. Scene Progression

**Method**: `_advance_to_next_scene()`

**Progression pattern**: 5 → 6 → 7 → 8 → 5 (loop)

```python
self.scene_loop_current_scene += 1
if self.scene_loop_current_scene > 8:
    self.scene_loop_current_scene = 5  # Wrap back
```

**Actions on advancement**:
1. Increment scene index (with wraparound)
2. Reset timing tracking
3. Fire all clips in new scene
4. Resume progress monitoring

## Scene Loop State Machine

```
[IDLE]
  ↓ (user double-taps scene button 5)
[ACTIVATE SCENE LOOP]
  - scene_loop_active = True
  - scene_loop_current_scene = 5
  - Fire all clips in scene 5
  ↓
[MONITORING Scene 5]
  - Track elapsed time vs max clip length
  - Poll every 5 ticks
  ↓
[SCENE COMPLETE - at max_length]
  - scene_loop_current_scene = 6
  - Fire all clips in scene 6
  ↓
[MONITORING Scene 6] → ... → [Scene 7] → [Scene 8]
  ↓
[SCENE 8 COMPLETE]
  - Wrap back to scene 5
  - Continue loop
  ↓ (or user double-taps scene button 1)
[DEACTIVATE]
  - scene_loop_active = False
  - Clean up state
  ↓
[IDLE]
```

## Technical Implementation Details

### Anticipatory Firing Mechanism

**The Problem**: Waiting for recording to finish creates a gap between recordings.

**The Solution**: Fire the next clip BEFORE the current one finishes.

**How It Works**:
1. Track expected recording length in `cascade_expected_beats` (e.g., 16 beats)
2. Poll `clip.playing_position` every tick (~10-20ms)
3. When position reaches 75% (beat 12 of 16), fire next clip
4. Next clip starts recording while current finishes its last bar
5. Result: seamless transition with overlapping recordings

**Why 75%?**
- For 4-bar loops (16 beats): fires at beat 12, gives 4 beats (1 bar) overlap
- Enough time for Ableton to arm track and start recording
- Not too early (would cut off current recording)
- Adjustable via `CASCADE_FIRE_THRESHOLD` constant

**Why Not Use `clip.length`?**
During recording, `clip.length` returns a huge internal value (63072000.0) instead of the actual beat count. We must track the expected length ourselves.

### Clip Lifecycle & Timing

**Ableton Live clip states**:
1. `clipSlot.fire(beats)` called
2. Clip created (not immediate - takes 2-10 ticks, ~20-100ms)
3. `clip.is_recording = True`, `clip.playing_position` starts incrementing
4. Recording progresses: position 0 → 1 → 2 → ... → beats
5. **At 75% position**: Next clip fired (anticipatory)
6. Recording continues to `beats`, then stops
7. `clip.is_playing = True`, `clip.is_recording = False`
8. Clip loops and plays

**Polling timing**:
- Check every 1 tick (~10-20ms depending on buffer size)
- Runs on Live's main thread (safe to call Live API)
- State checks (`cascade_active`) prevent stale callbacks

### Edge Cases Handled

**Multiple cascades**: Only one cascade can run at a time (per `cascade_active` flag)
- Starting a new cascade stops any active cascade
- Each cascade is column-independent

**User interrupts**:
- Recording on different column: No interference (cascade continues on original column)
- Deleting clips during cascade: State checks prevent crashes
- Undo during cascade: Cascade continues (might create unexpected state)
- Pressing occupied pad during cascade: Starts normal recording (stops cascade)

**Performance**:
- Lightweight polling (~every 10-20ms)
- Only active during cascade recording
- No memory leaks (flags cleaned up on completion)
- Minimal CPU impact (simple float comparison per tick)

### Product ID

```python
def _product_model_id_byte(self):
    return 40  # Same as mle1
```

Must match `__init__.py`:
```python
controller_id(vendor_id=2536, product_ids=[40],
              model_name='APC MINI MLE2')
```

**Important**: Uses same product ID as mle1 (40). Only one can be active at a time in Ableton.

## Customization Points

### Adjust anticipatory firing threshold

In `_check_cascade_progress()`, modify the `CASCADE_FIRE_THRESHOLD` constant:

```python
CASCADE_FIRE_THRESHOLD = 0.75  # Default: 75%

# Options:
# 0.75 = Fire at last 25% (1 bar for 4-bar loops) - RECOMMENDED
# 0.5  = Fire at halfway (2 bars for 4-bar loops) - More overlap
# 0.9  = Fire at last 10% - Tighter timing, may cause issues
# 0.85 = Fire at last 15% - Slight delay but safer
```

**Effect on timing** (for 16-beat recording):
- `0.75`: Fires at beat 12, 4 beats overlap
- `0.5`: Fires at beat 8, 8 beats overlap
- `0.9`: Fires at beat 14.4, 1.6 beats overlap (tight!)

### Change cascade direction

Currently cascades **down** (row + 1). To cascade **up**:

```python
# In _continue_cascade():
next_clip_index = self.cascade_current_clip_index - 1  # Change + to -

# Update boundary check:
if next_clip_index < 0 or ...  # Change >= 8 to < 0
```

### Cascade across columns (horizontal)

Modify `_continue_cascade()`:
```python
# Keep same row, increment track
next_track_index = self.cascade_track_index + 1
# ... boundary checks ...
# Fire on: song.tracks[next_track_index].clip_slots[same_row]
```

### Variable bar lengths per row

Currently uses same bar length for entire column. To vary by row:

```python
# In _continue_cascade():
bars = self.get_bars_for_row(next_clip_index)  # Custom method

def get_bars_for_row(self, row_index):
    if row_index < 2:
        return 1
    elif row_index < 4:
        return 2
    else:
        return 4
```

### Add visual feedback

Blink the pad currently recording:

```python
# In _on_clip_playing_status_changed():
# Before continuing cascade:
note = self.cascade_current_clip_index * 8 + self.cascade_track_index
self.really_do_send_midi((NOTE_ON_STATUS, note, 2))  # Blink
```

### Disable cascade for certain tracks

```python
# In _applyShiftMenu(), before starting cascade:
if trackIndex in [0, 7]:  # Don't cascade on tracks 0 and 7
    # Use original mle1 behavior
    track.arm = True
    clipSlot.fire(beats)
    return True
```

## Debugging

**Log messages**: Check Live's Log.txt at:
- macOS: `~/Library/Preferences/Ableton/Live X.X.X/Log.txt`
- Windows: `%USERPROFILE%\AppData\Roaming\Ableton\Live X.X.X\Log.txt`

**Key log messages to watch**:
```
MLE2: STARTING CASCADE RECORD!
MLE2 Cascade: Starting at row X
MLE2: Monitoring row X
MLE2 Cascade: Reached 75% at beat Y/Z, firing next clip
MLE2 Cascade: Recording next clip at row X with N beats
MLE2 Cascade: Complete! Playing first clip at row X
MLE2 Cascade: Started playback from row X
```

**Add debug logging to polling**:

```python
# In _check_cascade_progress(), add:
self.log_message("MLE2 DEBUG: position=" + str(current_beat) +
                 " / expected=" + str(expected_length) +
                 " / threshold=" + str(expected_length * CASCADE_FIRE_THRESHOLD))
```

**Common issues**:
- "Clip creation timeout": Ableton slow to create clip, increase retry count
- No "Reached 75%" log: Check `cascade_expected_beats` is set correctly
- Gaps between recordings: Lower `CASCADE_FIRE_THRESHOLD` (e.g., 0.7 instead of 0.75)

## Known Limitations

**Only one cascade at a time**: Starting a new cascade aborts any active cascade

**No mid-cascade pause**: Once started, cascade runs until completion or boundary

**Undo during cascade**: Will undo last clip but cascade continues (can create gaps)

**Tempo changes**: If tempo changes during cascade, remaining clips record at new tempo (can cause timing issues)

**Quantization**: Not applied automatically during cascade (apply manually after completion)

**Anticipatory firing precision**: Depends on Ableton's buffer size and system load (typical variation: ±1-2 beats)

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

**No event listeners used** - polling approach is more reliable for our use case.

## Differences from mle1

| Feature | mle1 | mle2 |
|---------|-----|------|
| Recording trigger | Manual per pad | Auto-cascade down column (one click) |
| Transition | Immediate per-clip | Seamless anticipatory firing |
| Monitoring | None | Active polling during recording |
| State tracking | Shift/copy state only | + Cascade state + expected beats + Scene loop state |
| Scene loop | Not available | Double-tap scene 5 to activate, scene 1 to deactivate |
| Product ID | 40 | 40 (same, mutually exclusive) |
| Workflow | Hands-on per-layer control | Hands-free cascading layers + automated scene progression |
| Performance | Direct clip manipulation | +Polling overhead (minimal) |

---

*One click, infinite layers - let the grid do the work*
