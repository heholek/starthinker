###########################################################################
#
#  Copyright 2017 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import subprocess
import argparse

from glob import glob
from time import sleep, strftime
from datetime import datetime

from util.project import get_project, is_scheduled
from util.storage import parse_filename
from setup import EXECUTE_PATH

ONE_HOUR_AND_ONE_SECOND = (60 * 60) + 1 # ensures no repeat in a single hour but never runs over in 24 hours

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--path', help='run all json files in the specified path', action="store")
  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--force', '-force', help='execute all scripts once then exit.', action='store_true')
  args = parser.parse_args()
  verbose = args.verbose

  try:
    while True:
      for filepath in glob('%s*.json' % args.path):
        if verbose: print 'PROJECT:', filepath

        project = get_project(filepath)

        if args.force or is_scheduled(project):

          # run it locally
          if project['setup'].get('local', True):
            command = 'python all/run.py %s --date TODAY' % filepath
            if verbose: command += ' --verbose'
            if verbose: print 'COMMAND:', command
            subprocess.call(command, shell=True, cwd=EXECUTE_PATH)

          # run it remotely
          elif project['setup'].get('remote'):
            command = 'python remote/run.py %s --date TODAY --verbose' % filepath
            if verbose: print 'COMMAND:', command
            subprocess.call(command, shell=True, cwd=EXECUTE_PATH)

      if args.force: break
      if verbose: print 'SLEEP:', ONE_HOUR_AND_ONE_SECOND
      sleep(ONE_HOUR_AND_ONE_SECOND)


  except KeyboardInterrupt:
    exit()