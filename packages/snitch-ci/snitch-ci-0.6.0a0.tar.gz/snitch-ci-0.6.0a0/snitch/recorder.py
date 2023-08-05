"""
Module providing tools for recordin user inputs (mouse clicks and keyboard strokes)
"""
import time
import logging as log
import traceback
import sys
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

import pyautogui
from pynput.keyboard import Key, KeyCode
from pynput.keyboard import Listener as KbdListener
from pynput.mouse import Button
from pynput.mouse import Listener as MouseListener

from .model.data.events import KeyPressed, TextEntered, Shortcut, MouseAltClick, MouseClick, MouseDrag, MODIFIERS
from .settings import CFG

#pylint: disable=unused-argument

def print_err():
    """ Prints error message after exception """
    t, message, trace = sys.exc_info()
    log.error("%s: %s", t.__name__, message)
    log.error("\n".join(traceback.format_tb(trace)))

class SnapInfo:
    """
    Class containing informations about various sizes used to
    perform screen captures.
    """

    CAPTURE_SIZE = 100
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

    @staticmethod
    def get_area(x, y):
        """
        :return: A 4-item tuple containing the left, top, width, height of a square
                 area of CAPTURE_SIZ side length and centered in (x, y). If the click
                 is too close from the border of the screen, the area captured is
                 preserved, but the click is not centered
        """
        return (max(0, min(x-SnapInfo.CAPTURE_SIZE, SnapInfo.SCREEN_WIDTH)),
                max(0, min(y-SnapInfo.CAPTURE_SIZE, SnapInfo.SCREEN_HEIGHT)),
                SnapInfo.CAPTURE_SIZE,
                SnapInfo.CAPTURE_SIZE)


class KeyEventCatcher:
    """
    A one-shot key combination catcher.
    Starts to listen to key events on call to method start
    or on creation if used through the `with` keyword.
    """

    def __init__(self, keys, callback):
        """
        :type keys: list of set of pressed keys
        :type callback: callable to call when keys are pressed
        """

        self._shortcut = keys
        self._callback = callback
        self._pressed_keys = set()
        self._kl = None
        self._is_running = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        log.debug('KeyEventCatcher START')
        self._kl = KbdListener(on_press=self.on_press,
                               on_release=self.on_release)
        self._kl.start()
        self._is_running = True

    def stop(self):
        log.debug('KeyEventCatcher STOP')
        self._kl.stop()
        self._is_running = False

    def on_press(self, key):
        """ Callback for keyboard press events """
        if not self._is_running:
            log.info('PressEvent occured on stopped state, killing listener.')
            raise KbdListener.StopException()
        try:
            log.debug('!vvv %s', key)
            self._pressed_keys.add(key)
            log.debug('    : %s',
                     list(map(lambda l: l.name if isinstance(l, Key) else l.char, self._pressed_keys))
                     )

            if self._pressed_keys in self._shortcut:
                log.debug('Shortcut detected, triggering callback')
                self.stop()
                self._callback()
        #pylint: disable=bare-except
        except:
            print_err()

    def on_release(self, key):
        if not self._is_running:
            log.info('ReleaseEvent occured on stopped state, killing listener.')
            raise KbdListener.StopException()
        log.debug('!^^^ %s (%s)', key, type(key))
        if key in self._pressed_keys:
            self._pressed_keys.remove(key)



class EventRecorder(QObject):
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    recording_paused = pyqtSignal()

    """ Class recording user input event into an EventList """
    def __init__(self, event_list, snap_click=False, parent=None):
        """
        :type event_list: EventList
        :param snap_click: If true, each mouse click generaetes a small screen capture
                           at the click location.
        """
        super().__init__(parent)

        self.event_list = event_list
        self.is_recording = False
        self._init_listeners()
        self._snap_on_click = snap_click
        self._pressed_keys = set()
        self._press_position = (0, 0)
        self._ignore_next = set()

    def _init_listeners(self):
        """ Creates new listener objects for mouse and keyboard """
        self._ml = MouseListener(on_click=self.on_click)
        self._kl = KbdListener(on_press=self.on_press,
                               on_release=self.on_release)


##     ##  #######  ##     ##  ######  ########
###   ### ##     ## ##     ## ##    ## ##
#### #### ##     ## ##     ## ##       ##
## ### ## ##     ## ##     ##  ######  ######
##     ## ##     ## ##     ##       ## ##
##     ## ##     ## ##     ## ##    ## ##
##     ##  #######   #######   ######  ########


    def on_click(self, x, y, button, pressed):
        """ Callback for click events """
        x, y = round(x), round(y)
        try:
            pressed_modifiers = {m for m in MODIFIERS if m in self._pressed_keys}
            if self._snap_on_click:
                image = pyautogui.screenshot(region=SnapInfo.get_area(x, y))
                image.save('{0}-click-at-{1}x{2}.png'.format(round(time.time()*1000), x, y), 'PNG')
            event = None
            if pressed:
                self._press_position = (x, y)
                if button == Button.left:
                    event = MouseClick(x, y)
                else: # Button.right
                    event = MouseAltClick(x, y)
            else:
                if button == Button.left and self._press_position != (x, y):
                    press = self.event_list.pop()
                    event = MouseDrag(x0=press.x, y0=press.y, x1=x, y1=y)
                #else: pass, this is a regular click

            if event:
                event.modifiers = tuple(m.name for m in pressed_modifiers)
                self.event_list.push(event)

        #pylint: disable=bare-except
        except:
            print_err()


##    ## ######## ##    ## ########   #######     ###    ########  ########
##   ##  ##        ##  ##  ##     ## ##     ##   ## ##   ##     ## ##     ##
##  ##   ##         ####   ##     ## ##     ##  ##   ##  ##     ## ##     ##
#####    ######      ##    ########  ##     ## ##     ## ########  ##     ##
##  ##   ##          ##    ##     ## ##     ## ######### ##   ##   ##     ##
##   ##  ##          ##    ##     ## ##     ## ##     ## ##    ##  ##     ##
##    ## ########    ##    ########   #######  ##     ## ##     ## ########


    def on_press(self, key):
        """ Callback for keyboard press events """
        try:
            self._pressed_keys.add(key)
            log.debug('vvv %s (%s): %s', key, type(key).__name__, self._get_pressed_names())

            modifiers = {k for k in self._pressed_keys if k in MODIFIERS}

            if not key in MODIFIERS:
                if modifiers:
                    self.event_list.push(Shortcut(key, modifiers))
                else:
                    if isinstance(key, Key):
                        self.event_list.push(KeyPressed(key))
                    elif isinstance(key, KeyCode):
                        if key.char:
                            self.event_list.push(TextEntered(key.char))
                        else:
                            self.event_list.push(KeyPressed(key))
                    else:
                        self.event_list.push(TextEntered(key))
        #pylint: disable=bare-except
        except:
            print_err()

    def on_release(self, key):
        """ Callback for keyboard release events """
        try:
            if key in self._pressed_keys:
                self._pressed_keys.remove(key)
            log.debug('^^^ %s: %s', key, self._get_pressed_names())

        #pylint: disable=bare-except
        except:
            print_err()

    def _get_pressed_names(self):
        return list(map(lambda l: l.name if isinstance(l, Key) else l.char, self._pressed_keys))

########  ########  ######   #######  ########  ########  #### ##    ##  ######
##     ## ##       ##    ## ##     ## ##     ## ##     ##  ##  ###   ## ##    ##
##     ## ##       ##       ##     ## ##     ## ##     ##  ##  ####  ## ##
########  ######   ##       ##     ## ########  ##     ##  ##  ## ## ## ##   ####
##   ##   ##       ##       ##     ## ##   ##   ##     ##  ##  ##  #### ##    ##
##    ##  ##       ##    ## ##     ## ##    ##  ##     ##  ##  ##   ### ##    ##
##     ## ########  ######   #######  ##     ## ########  #### ##    ##  ######


    @pyqtSlot()
    def start(self):
        """ Starts the event recording """
        self.is_recording = True
        self._ml.start()
        self._kl.start()

        if CFG['minimize_on_record']:
            self.parent().setWindowState(self.parent().windowState() | Qt.WindowMinimized)
        self.recording_started.emit()

    @pyqtSlot()
    def pause(self):
        """ Pauses the event recording """
        self.is_recording = False
        self._ml.stop()
        self._kl.stop()
        self.event_list.pop()
        self.recording_paused.emit()

    @pyqtSlot()
    def stop(self):
        """ Stops the event recording """
        self.is_recording = False
        self._ml.stop()
        self._kl.stop()
        self._init_listeners()
        self.event_list.pop()
        if CFG['minimize_on_record']:
            self.parent().setWindowState(self.parent().windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

        self._ignore_next.clear()
        self._pressed_keys.clear()

        self.recording_stopped.emit()

    def reset(self):
        """ Clears the event recording """
        self.event_list.clear()
