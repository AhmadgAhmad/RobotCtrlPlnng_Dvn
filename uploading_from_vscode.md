# Uploading Code to Your ACEBOTT Robot from VSCode

No ACECode needed! Follow these steps every time you want to upload a new program.

---

## Before You Start

- Robot car is **powered on** and connected via **USB**
- Your code file (e.g. `week2_speed_control.py`) is open in VSCode
- You know where the file is saved on your Mac

---

## Step 1 — Open the Terminal in VSCode

In VSCode, press:

```
Ctrl + `
```

(That's the backtick key, top-left of your keyboard, under Escape)

Or go to the menu: **Terminal → New Terminal**

A terminal panel will open at the bottom of VSCode.

---

## Step 2 — Check the Robot is Connected

Run this command to confirm your robot shows up:

```bash
ls /dev/tty.*
```

You should see this in the list:

```
/dev/tty.wchusbserial110
```

If you don't see it, unplug and replug the USB cable and try again.

---

## Step 3 — Navigate to Your File

If your file is in the same folder that's open in VSCode, run:

```bash
cd <drag your project folder here from Finder>
```

Or if it's in Downloads:

```bash
cd ~/Downloads
```

Confirm the file is there:

```bash
ls
```

You should see `week2_speed_control.py` (or whatever your file is named).

---

## Step 4 — Upload the File to the Robot

This copies your `.py` file onto the robot as `main.py`.
MicroPython automatically runs `main.py` every time the robot boots.

```bash
mpremote connect /dev/tty.wchusbserial110 fs cp week2_speed_control.py :main.py
```

> The `:` before `main.py` means "copy to the robot". Don't leave it out!

You should see:

```
cp week2_speed_control.py :main.py
```

---

## Step 5 — Run the Program

To run the file immediately without rebooting:

```bash
mpremote connect /dev/tty.wchusbserial110 run week2_speed_control.py
```

The robot will start moving right away and you'll see all the `print()` messages in the terminal.

---

## Step 6 — Watch Live Output (Optional)

To open a live console and see everything the robot prints in real time:

```bash
mpremote connect /dev/tty.wchusbserial110
```

To exit the live console, press **Ctrl + X**.

---

## Quick Reference

| What you want to do | Command |
|---|---|
| Check robot is connected | `ls /dev/tty.*` |
| Upload file to robot | `mpremote connect /dev/tty.wchusbserial110 fs cp week2_speed_control.py :main.py` |
| Run file immediately | `mpremote connect /dev/tty.wchusbserial110 run week2_speed_control.py` |
| Open live console | `mpremote connect /dev/tty.wchusbserial110` |
| Exit live console | `Ctrl + X` |

---

## Troubleshooting

**Port not found (`/dev/tty.wchusbserial110` missing)**
Unplug and replug the USB cable. Run `ls /dev/tty.*` again.
If it still doesn't show, try a different USB cable — some cables are charge-only.

**`mpremote` command not found**
Run this once to install it:
```bash
pip install mpremote
```

**Upload seems to hang or freeze**
Hold the **BOOT button** on the ESP32 board, run the upload command,
then release BOOT once you see activity in the terminal.

**Robot does nothing after upload**
Make sure the filename on the robot is exactly `main.py` (with the colon in the command).
MicroPython only auto-runs a file named `main.py`.

---

*Curious Cardinals Mentorship Program — Mentor: Ahmad Ahmad*
