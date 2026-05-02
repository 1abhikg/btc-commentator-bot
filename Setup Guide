# 🚀 Complete Setup Guide
# BTC Commentator Bot — Windows 7 / 10 / 11

=======================================================

## STEP 1 — Download & Install Python 3.8

👉 Click to Download:
https://www.python.org/downloads/release/python-3810/

- Scroll down and click:
  Windows x86-64 executable installer
- Run the downloaded file

⚠️ VERY IMPORTANT:
Before clicking Install — tick the box at the bottom
that says "Add Python to PATH"

- Click Install Now
- Wait for it to finish
- Click Close

=======================================================

## STEP 2 — Download & Install VB-Audio Virtual Cable

👉 Click to Download:
https://vb-audio.com/Cable/index.htm

- Click:  Download VBCABLE_Driver_Pack43.zip
- Extract the ZIP file
- Right click VBCABLE_Setup_x64.exe
- Click Run as Administrator
- Click Install Driver
- RESTART your PC after install

=======================================================

## STEP 3 — Download & Install VTube Studio (Character)

👉 Click to Download (Steam — Free):
https://store.steampowered.com/app/1325860/VTube_Studio/

OR Direct Download (No Steam):
https://denchisoft.com/

- Install VTube Studio
- Open it and load your character model
- Go to Settings → Microphone
- Set Microphone to:  CABLE Output (VB-Audio Virtual Cable)
- Your character mouth will now move when bot speaks

=======================================================

## STEP 4 — Create Your Bot Folder

- Open My Computer
- Go to C: Drive
- Right click empty space
- Click New → Folder
- Name it:  btc-bot

Your folder path will be:
C:\btc-bot

=======================================================

## STEP 5 — Download Bot File From This Repo

- Click the green CODE button on this page
- Click Download ZIP
- Open your Downloads folder
- Right click the ZIP → Extract All
- Copy this file into C:\btc-bot

  btc_bot.py   ← Bitcoin commentator bot

=======================================================

## STEP 6 — Open Command Prompt

- Press Windows key + R on your keyboard
- Type:  cmd
- Press Enter
- A black window will open

=======================================================

## STEP 7 — Install All Required Libraries

Copy and paste this into Command Prompt and press Enter:

pip install pyttsx3 yfinance pygame websocket-client pywin32

Wait for it to finish.
You will see "Successfully installed" at the end.

=======================================================

## STEP 8 — Fix pywin32

After libraries finish, paste this into Command Prompt
Replace YOUR_USERNAME with your actual Windows username:

python "C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python38\Scripts\pywin32_postinstall.py" -install

You should see this when it works:
Copied pythoncom38.dll to C:\Windows\system32\
Copied pywintypes38.dll to C:\Windows\system32\
The pywin32 extensions were successfully installed.

=======================================================

## STEP 9 — Check What Voices Are Installed

- Open Python IDLE from Start Menu
- Click File → New File
- Paste this and press F5:

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(i, voice.name, voice.id)

This prints all voices with index numbers.
Look for a male voice — usually index 0 or 1.

=======================================================

## STEP 10 — Install Free Male Voice (If Needed)

If your voice sounds female, download eSpeak:

👉 Click to Download eSpeak:
http://espeak.sourceforge.net/download.html

- Click:  espeak-1.48.04-setup.exe
- Install it
- RESTART your PC
- Run Step 9 again — eSpeak will now appear in list

=======================================================

## STEP 11 — Set Male Voice In The Bot

- Open btc_bot.py in IDLE
- Find this line near the top:

  VOICE_INDEX = 0

- Change the number to match the male voice index
  from your Step 9 results
- Save the file with Ctrl + S

=======================================================

## STEP 12 — Set Audio Output To Virtual Cable

- Open btc_bot.py in IDLE
- Find the audio output section
- Make sure output is set to:
  CABLE Input (VB-Audio Virtual Cable)

This routes the bot voice through the virtual cable
so OBS and VTube Studio can pick it up.

=======================================================

## STEP 13 — Setup OBS

- Open OBS Studio
- Click + under Audio Mixer
- Add Audio Input Capture
- Set device to:
  CABLE Output (VB-Audio Virtual Cable)
- The bot voice will now appear in your stream audio

=======================================================

## STEP 14 — Run The Bot

- Open Python IDLE
- Click File → Open
- Go to C:\btc-bot
- Open btc_bot.py
- Press F5

The startup banner will appear in the shell window.
Bot will speak automatically on first BTC price move.

=======================================================

## STEP 15 — Full Stream Setup Order

Start everything in this exact order:

1. Start VB-Audio Virtual Cable  (runs in background)
2. Open VTube Studio            (load your character)
3. Open OBS Studio              (set up your scene)
4. Run btc_bot.py in IDLE       (press F5)
5. Go Live                      (start your stream)

=======================================================

## ⚠️ ERROR FIXES

ERROR: No module named pywintypes
FIX: Run Step 8 again

ERROR: DLL load failed
FIX: Run this in Command Prompt:
pip install onnxruntime==1.16.3

ERROR: No module named pip
FIX: Reinstall Python 3.8 — tick Add Python to PATH

ERROR: Voice stops after 2 announcements
FIX: Already fixed in latest bot version — redownload

ERROR: Voice sounds female
FIX: Follow Step 10

ERROR: Character mouth not moving
FIX: Check VTube Studio microphone is set to
     CABLE Output (VB-Audio Virtual Cable)

ERROR: Bot voice not in OBS
FIX: Check OBS audio input is set to
     CABLE Output (VB-Audio Virtual Cable)

ERROR: No such file or directory
FIX: Check your username spelling in the path

ERROR: Path broken with space in username
FIX: Always wrap the full path inside quotes " "

=======================================================

## 📦 All Download Links

Python 3.8:
https://www.python.org/downloads/release/python-3810/

VB-Audio Virtual Cable (Free):
https://vb-audio.com/Cable/index.htm

VTube Studio on Steam (Free):
https://store.steampowered.com/app/1325860/VTube_Studio/

VTube Studio Direct (No Steam):
https://denchisoft.com/

eSpeak Male Voice (Free):
http://espeak.sourceforge.net/download.html

OBS Studio (Free):
https://obsproject.com/download

pip upgrade — paste in Command Prompt:
python -m pip install --upgrade pip

=======================================================

## ❓ Still Stuck?

Open an Issue on this repo and paste your exact
error message — I will help you fix it step by step.

=======================================================
