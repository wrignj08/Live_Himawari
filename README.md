# Live Himawari
Live Himawari is a macOS menu bar application which sets your desktop wallpaper to the real time view from the Himawari 8 satellite. The imagery comes courtesy of <a href="https://himawari8.nict.go.jp">Himawari-8 Real-time</a>.

<a href="https://github.com/wrignj08/Live_Himawari/raw/main/Live%20Himawari.zip" style='font-size:2em' download>Download Live Himawari 🌏</a>

<img src="https://raw.githubusercontent.com/wrignj08/Live_Himawari/main/images/menu.jpg" alt="menu">
<br>
<br>

<img src="https://raw.githubusercontent.com/wrignj08/Live_Himawari/main/images/full%20screen.jpg" alt="full screen view">

<br>
<br>
This app was written in Python 3, the menu bar functionality is provided via <a href="https://rumps.readthedocs.io">rumps</a>.
The image handling is provided via <a href="https://pillow.readthedocs.io">Pillow</a>.
The wallpaper setting logic uses the AppKit Python library, helpfully demonstrated in this <a href="https://stackoverflow.com/a/65947716">answer by Ted Wrigley</a>.
The app packaging is done with <a href="https://pyinstaller.readthedocs.io">PyInstaller</a>.
