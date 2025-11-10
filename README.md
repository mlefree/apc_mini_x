# APC mini X

MIDI remote scripts that turn your APC mini into a live looping powerhouse for Ableton Live.

## Requirements

- Ableton Live 9+ (tested with Live 12)

## Quick Start

1. **Shut down** Ableton Live
2. **Edit** `install.sh` and set your `ABLETON_HOME` path
3. **Run** `./install.sh` to copy scripts
4. **Restart** Live and select your control surface in Preferences:

![Control Surface Setup](ableton_live_control.png)

## Developer Tools

See [TOOLS.md](./TOOLS.md) for debugging and development information.

## The Flavors

Pick your vibe:

| Script                       | What it does                             | Watch                                            | Props                                                                                  |
|------------------------------|------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------|
| **[mle](./mle/README.md)**   | Opinionated bar looping (**foundation**) | —                                                | @mat_cloud                                                                             |
| **[mle2](./mle2/README.md)** | Cascading record                         | —                                                | @mat_cloud                                                                             |
| **plus**                     | Bar control + metronome + undo           | [▶](https://youtu.be/Rrd3BDDvSlc)                | [PaulBriere](https://gitlab.com/Paulybri/apc_mini_plus)                                |
| **mh**                       | Live looping essentials                  | [▶](https://www.youtube.com/watch?v=Nd9lvAHpqTE) | [markharwood](https://github.com/markharwood/MH_APC_mini)                              |
| **jojo**                     | Classic setup                            | —                                                | [JOJ0](https://github.com/JOJ0/ableton-live9-remote-scripts/tree/master/APC_mini_jojo) |

## TODO

- rename `mle` in `mle1`
- edit `mle1` to give access to: 
     tempo up/down with buttons used in different menus to go up/down. 
     tempo tap with button used to choose different menus and going to left. 
     start/stop song with button used to choose menus and going to right.
- when it's working, report this behaviour to `mle2` too
- add a new `mle3` that, based on `mle1`, can do `lateral cascade mode`: 
    from the left to the right (using the same row, and moving columns), each pad is filled and continue to play.

---

*Compatible with Ableton Live 9+ (tested with Live 12) • Hit the pads, loop the beats*
