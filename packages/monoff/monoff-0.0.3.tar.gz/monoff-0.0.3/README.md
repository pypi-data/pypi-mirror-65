# monoff
When run via "python -m monoff", will turn off all monitors. 
Typing on the keyboard or moving the mouse should bring the monitors back.
If your monitors auto-detect digital inputs, they should switch to another source if one is available.
May be used to switch all monitors in one command in this manner as opposed to individually selecting sources on each monitor.

Should work for Windows, Linux, and Mac. Not tested for Mac.

## Notes for different platforms

### Windows:
	Requires pywin32 (not installed automatically)
	Uses pywin32 to broadcast an SC_MONITORPOWER
	[https://docs.microsoft.com/en-us/windows/win32/menurc/wm-syscommand](Microsoft Documentation)

### Linux:
	Uses "xset dpms force off"

### Mac (not tested):
	Uses "pmset displaysleepnow"
