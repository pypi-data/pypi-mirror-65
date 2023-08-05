""" Snitch entry point """

import logging as log
import sys
import argparse

from PyQt5.QtWidgets import QApplication

from .ui.controller import Controller
from . import LOG_LEVELS, DEFAULT_LOG_LEVEL, DEFAULT_LOG_FILE, __version__

def main():
    parser = argparse.ArgumentParser(prog='snitch', )
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('-v', '--verbosity',
        choices=LOG_LEVELS, default=DEFAULT_LOG_LEVEL,
        help='Set the logging verbosity level. ')
    parser.add_argument('-l', '--log-file',
        default=DEFAULT_LOG_FILE,
        help='The log file location. '
            'Default is in the user temp directory.')
    parser.add_argument('-f', '--file',
        help='The test case file. '
            'If this option is used, the GUI is not started and the test case is run automatically.')
    args = parser.parse_args()

    file_handler = log.FileHandler(args.log_file)
    stream_handler = log.StreamHandler(sys.stdout)
    log.basicConfig(handlers=(file_handler, stream_handler),
                    level=args.verbosity,
                    format='%(asctime)s.%(msecs)03d:%(levelname)-8s:%(module)-12s# %(message)s',
                    datefmt='%Y%m%d-%H%M%S'
                    )
    APP = QApplication(sys.argv)
    WIN = Controller()
    if args.file:
        # run test case
        print("Loading test case: {}".format(args.file))
        return_code = -1
        if WIN.load(args.file):
            print("Playing test case...")
            results = WIN.playback(include_snapshots=True)
            # the code is + for passed, - for failed, . for not applicable
            print('')
            print('IMG> '+''.join(['+' if x else '-' for x in results[0]]))
            print('OCR> '+''.join(['+' if x else '-' if x is False else '.' for x in results[1]]))
            print('')
            print("Summary:\n  - {}/{} matching screenshots\n  - {}/{} matching texts".format(
                results[0].count(True),
                len(results[0]),
                results[1].count(True),
                len(results[1])-results[1].count(None)
            ))
            print("Saving results...")
            WIN.save_result(args.file)

            # The return code is the number of non passing cases
            # A passing case is defined as a case where tre OCR matches or,
            # if no OCR is present, the captures match.
            #   - r[1] is the result of the OCR comparison (None if OCR not used)
            #   - r[0] is the result of the image comparison
            return_code = [r[1] if r[1] is not None else r[0] for r in list(zip(*results))].count(False)
            log.info("Return code set to %s after event replay.", return_code)
        else:
            print("Error loading test case, aborting.")

        APP.quit()
        sys.exit(return_code)
    else:
        WIN.show()
        sys.exit(APP.exec())

if __name__ == '__main__':
    main()
