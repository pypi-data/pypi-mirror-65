"""
Module providing tools to replay recorded  inputs sequences.
"""
import logging as log
import time

import cv2
import imutils
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
from skimage.measure import compare_ssim

from .model.data.screenshot import ImageConverter
from .model.data.events import Delay
from .settings import CFG
from .ui.diff import Diff
from . import ocr


######## ##     ## ######## ##    ## ########  ######
##       ##     ## ##       ###   ##    ##    ##    ##
##       ##     ## ##       ####  ##    ##    ##
######   ##     ## ######   ## ## ##    ##     ######
##        ##   ##  ##       ##  ####    ##          ##
##         ## ##   ##       ##   ###    ##    ##    ##
########    ###    ######## ##    ##    ##     ######


class EventPlayer(QObject):
    """ Class handling the event replay """
    def __init__(self, event_list, parent=None):
        """
        :param delay: The interval, in seconds, between two repalyed events. If -1, the
                        recording interval is used.
        """
        super().__init__(parent)

        self._event_list = event_list
        self._playing = False
        self._current_event = None

    def play(self, start_at=0, event_played_callback=None, key_event_catcher=None):
        """
        Executes sequentially all the events in the list
        :param start_at: The index of the event in the list to start playing from
        :param event_played_callback: A callback function, taking an event as parameter,
            and called after each event play
        :param key_event_catcher: A KeyEventCatcher object, on which the stop method
            will be called before executing the event, and restarted just after
        :return: the last event played
        """
        first_event = max(0, start_at)
        log.info('Starting playback from event %d/%d', first_event, self._event_list.size())
        last_event = None
        self._playing = True
        for event in self._event_list.events[first_event:]:
            self._current_event = event
            if self._playing:
                if last_event is None:
                    delay = 0
                elif CFG['replay_delay'] == -1:
                    delay = event.time - last_event.time
                else:
                    delay = CFG['replay_delay']

                time.sleep(delay)


                if key_event_catcher and not isinstance(event, Delay):
                    key_event_catcher.stop()
                else:
                    log.debug('keep recording')

                event.execute()
                if key_event_catcher and event.block_events_on_exec:
                    key_event_catcher.start()

                last_event = event
                if event_played_callback:
                    event_played_callback(last_event)
            else:
                break

    def stop(self):
        """ Stop the replay sequence """
        if hasattr(self._current_event, 'kill'):
            self._current_event.kill()
        self._playing = False


 ######  ##    ##    ###    ########   ######  ##     ##  #######  ########  ######
##    ## ###   ##   ## ##   ##     ## ##    ## ##     ## ##     ##    ##    ##    ##
##       ####  ##  ##   ##  ##     ## ##       ##     ## ##     ##    ##    ##
 ######  ## ## ## ##     ## ########   ######  ######### ##     ##    ##     ######
      ## ##  #### ######### ##              ## ##     ## ##     ##    ##          ##
##    ## ##   ### ##     ## ##        ##    ## ##     ## ##     ##    ##    ##    ##
 ######  ##    ## ##     ## ##         ######  ##     ##  #######     ##     ######


class SnapshotPlayer(QObject):
    """ Class handling snapshot reenactment and comparison """

    def __init__(self, snap_list, parent=None):
        """
        :type snap_list: list of Screenshot objects
        """
        super().__init__(parent)

        self._snap_list = snap_list

        # Originals, results and results with diff must be ImageConverter objects
        self._originals = []
        self._results = []
        self._results_with_diff = []

        self._diff_win = None

    def play(self):
        """
        Reperforms all the recorded snapshots and performs the diff. In addition,
        if the field ocr_expected is filled, the character recognition is performed
        as well.
        :return: A tuple of two lists, the first list indicating
            if the images matches (up to the defined threshold), the second if
            the OCR matches, or None if not required
        """
        self._originals = [ImageConverter(s.as_image()) for s in self._snap_list.snaps]
        self._results.clear()

        ocr_results = []
        for i, snap in enumerate(self._snap_list.snaps):
            snap.do_capture('result')
            self._results.append(ImageConverter(snap.as_image('result')))
            if snap.ocr_expected:
                self.compute_ocr(i)
                ocr_results.append(snap.ocr_expected == snap.ocr_result)
            else:
                ocr_results.append(None)

        img_results = self._diff()

        return (img_results, ocr_results)


    def load(self):
        """ Loads the previously recorded snapshot results and performs the diff """
        self._originals = [ImageConverter(s.as_image()) for s in self._snap_list.snaps]
        self._results.clear()

        for snap in self._snap_list.snaps:
            image = None
            if snap.result:
                image = ImageConverter(snap.as_image('result'))
            self._results.append(image)

    def _diff(self):
        """
        Computes the differences between the reference image and the result one.
        :return: A list of boolean containing True for each comparison with no difference
        """
        if not self._results:
            log.error("No results to compare. Try launching a replay sequence.")
            return False

        if len(self._results) != self._snap_list.size():
            log.error("Results snapshot count does not match testcase, aboritng diff.")
            return False

        self._results_with_diff.clear()

        for orig, res in zip(self._originals, self._results):
            original = orig.opencv
            gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

            result = res.opencv
            gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            # compute the Structural Similarity Index (SSIM) between the two
            # images, ensuring that the difference image is returned
            (score, diff) = compare_ssim(gray_original, gray_result, full=True)

            diff = (diff * 255).astype("uint8")
            log.info("Diff score = %f", score)

            # if the score is below the threshold defifed in the settings,
            # we consider the test has failed
            if score * 100 < CFG['diff_threshold']:

                # threshold the difference image, followed by finding contours to
                # obtain the regions of the two input images that differ
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)

                # loop over the contours
                for c in cnts:
                    # compute the bounding box of the contour and then draw the
                    # bounding box on both input images to represent where the two
                    # images differ
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

                self._results_with_diff.append(ImageConverter(result))
            else:
                self._results_with_diff.append(None)

        return [not bool(diff) for diff in self._results_with_diff]

    def show_diff(self, snap_id):
        """ Shows the window with images side by side. """
        dont_forget = self.tr("Don’t forget to click the play button after playing back the events.")
        self.load()

        if not self._results or self._results[snap_id] is None:
            message = self.tr("Can't perform diff, nothing to compare with.\n") + dont_forget
            QMessageBox.warning(self.parent(), "Snitch", message)
            return

        self._diff()

        snap = self._snap_list.snaps[snap_id]
        orig, res, diff = list(zip(self._originals, self._results, self._results_with_diff))[snap_id]
        # orig, res and diff are ImageConverter objects.
        # if the original image and the test image are the same, the
        # result_with_diff image is none.
        if orig and res:
            # we show the difference
            self._diff_win = Diff(orig.pixmap, res.pixmap, diff.pixmap if diff else None,
                snap.ocr_image, snap.ocr_result, None)
            self._diff_win.show()
        else:
            # something's wrong in the matrix
            message = self.tr("Some of the screenshot are missing.\n") + dont_forget
            QMessageBox.information(self.parent(), "Snitch", message)

    def compute_ocr(self, snap_id):
        self.load()
        snap = self._snap_list.snaps[snap_id]

        if snap_id < len(self._originals) and self._originals[snap_id]:
            snap.ocr_image = ocr.process_image(self._originals[snap_id].opencv, character_subset=snap.ocr_characters)
        if snap_id < len(self._results) and self._results[snap_id]:
            snap.ocr_result = ocr.process_image(self._results[snap_id].opencv, character_subset=snap.ocr_characters)

        return snap.ocr_image == snap.ocr_result
