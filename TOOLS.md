# Developer Tools

This project is compatible with Ableton Live 9+ (tested with Live 12).

### Embedded file name:
- /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/__init__.py
- /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/APC_mini.py

### TO Debug
...and see messages like  `self.log_message("Starting record")` :

    tail -f ~/Library/Preferences/Ableton/Live\ <VERSION>/Log.txt

Replace `<VERSION>` with your Live version (e.g., `Live\ 12.1.6`, `Live\ 10.1.35`, etc.)

### APIs or examples :
- https://julienbayle.studio/PythonLiveAPI_documentation/Live10.1.19.xml
- https://nsuspray.github.io/Live_API_Doc/10.1.0.xml
- https://structure-void.com/PythonLiveAPI_documentation/Live10.0.1.xml
- https://github.com/gluon/AbletonLive9_RemoteScripts
