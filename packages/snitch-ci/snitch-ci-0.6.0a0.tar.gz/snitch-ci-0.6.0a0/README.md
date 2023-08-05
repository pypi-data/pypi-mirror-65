Snitch, an input event recorder and player
==========================================

Snitch is a Python3 program using the Qt5 framework for GUI and the pyautogui
and pynput modules for automation.


## Prerequisites

A working installation of Python3 with pip package installer.

### Linux

In order to record and control the mouse on Linux systems, the packages
`python3-tk` and `python3-dev` are required.

The `pyautogui` module on Linux relies on the `scrot` utility to perform screen
captures, it must be installed separately. See the note about XWayland [at the
end of this document](#XWayland).

### Windows

The installation of the `scikit-image` module on Windows requires the
[_Microsoft Build Tools 2015_ (C++ compiler)](https://www.microsoft.com/en-us/download/details.aspx?id=48159)
to be installed.

### macOS

The use of Python 3.8 is recommended for the menubar to behave properly.

### OCR features

Snitch-CI provides OCR features through the use of the [Tesseract](https://github.com/tesseract-ocr/)
OCR software, which must be installed separately. The minimum recommended version is 4.1 (prior versions don't support the use of a custom target character set).

-   On Ubuntu (the official package only provides the 4.0 version, thus the need of adding an external PPA):
    ```bash
    sudo add-apt-repository ppa:alex-p/tesseract-ocr
    sudo apt-get update
    sudo apt-get install tesseract-ocr
    ```
-   On Windows download the installer at https://digi.bib.uni-mannheim.de/tesseract/
-   On macOS, with Homebrew:
    ```bash
    brew install tesseract
    ```


## Installation

Snitch is [available on PyPI](https://pypi.org/project/snitch-ci/) under the
name `snitch-ci`. You can install it by running the command:

    pip install snitch-ci

Once installed, start the program by simply running the commamd `snitch`.


## Building from sources

After having insstalled the prerequisites, use the following commands to
respectively:

-   install the required python packages dependencies
-   generate the python code for the Qt ui and rc files
-   start the program

```bash
pip install -r requirements.txt
bash build.sh
python -m snitch
```


## Usage

### Preparing a test case

#### Event recording

Click on the `Record` button. From now on, all the input events from the mouse
and the keyboard are recorded. Similar events may be gouped together, _e.g._
multiple letters typed consecutively are merged into a single TextEvent. All the
recorded events appear in the uper table in the Snitch inteface. The following
events are recognized:

-   Mouse move
-   Mouse click
-   Mouse double click
-   Mouse click with secondary button (so called right-click)
-   Mouse drag
-   Any of the above, with keys pressed
-   Text entry
-   Key pressed
-   Shortcuts (simultaneous press of a key and modifiers: Ctrl, Alt, …)

To stop the recording, just click on the stop button. This last click is
automatically removed from the list of the recorded events.


#### Manual event edition

On the right hand side of the recorded events list, the Snitch UI shows the
properties (such as click location, which keys are pressed, …) of the currently
selected event and buttons to add, remove and reorder events in the list.


#### Event playback

To start the playback of a recorded sequence, click on the `Play` button in the
upper part of the Snitch UI. The events are played with a default time delay of
0.2s. Each event is selected while played so you can follow the progression of
the sequence. You can also stop the playback by pressing `Esc`.

**Note:** For technical reasons, keyboard events can't be recorded while events
are played back. So the only time the press on the `Esc` key can be caught is
between two events. As a consequence, multiple press on the `Esc` may be
required for the sequence to stop.


#### Capturing areas of interest

The lower part of the Snitch UI is dedicated to the screenshots management. To
record a region of the screen as a reference to compare to the state of the
tested application after an automatic playback sequence, click on the `Add
result` button. The screen darkens a bit and the mouse cursor becomes a
crosshair. Define the area of interest by drawin a rectangle area around it
(click and drag).

On mouse button release, the capture is performend and appears in the list of
screenshots. When selecting a screenshot, a preview is displayed on the right
hand side of the UI along with its properties (size, position) and buttons to
add, remove and reorder the screenshots. Adding a screenshot with the add button
is exactly the same as using `Add result`.

 P
#### Saving / loading test cases

You can save the recorded sequence of events by clicking on the `Save…` button
or by selecting the `File > Save…` menu option. The formats available are JSON
(the images are Base64 encoded) and Pickle.

Load a previously saved file by selecting the `File > Open…` menu option.


#### Examples

The following video presents some of the various features for events recording:

![event-recording](doc/snitch-event-recording.mp4)

This video shows how the the screen captures of the results are taken, and how
the differces between the reference image and the test result are displayed.

![image-diff](doc/snitch-image-compare.mp4)


### Running a batch of test cases

Feature under development.

#### Docker

[See CI documentation](doc/ci.md#docker-compose-docker-composeyml)


#### GitLab integration

[See CI documentation](doc/ci.md#ci-configuration-gitlab-ciyml)


## Known issues

### Typing speed

While recording keystrokes, typing too fast, especially with key modifiers, can
result in skipping the modifier, or assinging it to the next key. Typing slowly
can avoid the problem. You can also edit the event manually afterwards and enter
the intended text.

### Context menus

While using context menus with submenus be sure to click on every submenu title
to record a mouse position on the item an prevent the cursor to skip steps on
playback.


### XWayland

The most recent versions of gnome-shell are based on XWayland instead of X11 as
display server. One of the main features of Wayland is the application
separation, _i.e._ each application is isolated from one another and is not
allowed to access graphical properties (window size, position, …) of others. As
a consequence, the applications running with the native gnome-shell framework
are invisible to Snitch.

Moreover for those versions, even if the actions can be recorded for the native
X11 applications, the scrot utility (used by `pyautogui` to perform screenshots)
produces only black pictures. As a workaround, it's possible to install the
Gnome native capture utility `gnome-screenshot` and create a wrapper script
acting as `scrot`. The most basic way to do that is putting the following script
in the `/usr/bin/scrot` file (and granting it execution permissions):

```bash
#! /bin/bash
gnome-screenshot -f $@
```
