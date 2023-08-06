#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
 Toolset to load IBM DVS Gesture preprocessed dataset.

Brainchip information:
        - AER2.0 specifications:
            https://inivation.com/support/software/fileformat/#bit-30-12
        - AER3.1 specifications:
            https://inivation.com/support/software/fileformat/#aedat-31
"""

import struct
import os
import re
import numpy as np

import sys
import tarfile
import urllib


def _parse_version_string(version_string):
    """Analyze string version from AEDAT file.

    Args:
        version_string (str): value contains file version.

    Returns:
        int: document major version.
    """
    v3 = re.compile('.*#!AER-DAT3.*')
    if v3.match(str(version_string)):
        return 3
    else:
        raise ValueError("Unrecognized or unsupported version: %s" %
                         str(version_string).strip(),
                         file=sys.stderr)


def _skip_ascii_header(file, version):
    """Going through header without reading data.

    Args:
        file (obj): opened AEDAT file
        version (int): AEDAT major version

    Returns:
        int: End of header bytes position.
    """
    bytes_pos = 0  # bytes position
    if version == 3:
        line = file.readline()
        bytes_pos += len(line)
        while line.startswith(b'#'):
            if line == b'#!END-HEADER\r\n':
                break
            else:
                line = file.readline()
                bytes_pos += len(line)
    else:
        raise ValueError("Unsupported version: %d" % version)
    return bytes_pos


def _read_event_v3(file, bytes_pos, trial_times, subj_num, light_cond):
    """Read event in AEDAT v3 format.

    Args:
        file (obj): opened AEDAT file.
        bytes_pos (int): starting events header position.
        trial_times (array): start/stop times for gestures from CSV label file.
        subj_num (int): subject id.
        light_cond (str): lighting condition.
    Returns:
        list: readed data are stored in dict and added to the returned list.
    """
    file.seek(bytes_pos)  # seek to end of header

    # init trials values and reference timestamps
    trials = []
    trial_ind = 1
    num_trials = len(trial_times)
    start_time = int(trial_times[trial_ind][1])
    stop_time = int(trial_times[trial_ind][2])

    ev_list = []
    ev_times = []
    while True:
        # events header part
        header = file.read(28)
        if not header or len(header) == 0:
            break

        # read header
        type = struct.unpack('H', header[0:2])[0]
        source = struct.unpack('H', header[2:4])[0]
        size = struct.unpack('I', header[4:8])[0]
        offset = struct.unpack('I', header[8:12])[0]
        tsoverflow = struct.unpack('I', header[12:16])[0]
        capacity = struct.unpack('I', header[16:20])[0]
        number = struct.unpack('I', header[20:24])[0]
        valid = struct.unpack('I', header[24:28])[0]

        data_length = capacity * size
        data = file.read(data_length)
        counter = 0

        if type == 1:
            while data[counter:counter + size]:
                # unpack data from bytes
                aer_data = struct.unpack('I', data[counter:counter + 4])[0]
                timestamp = struct.unpack(
                    'I', data[counter + 4:counter + 8])[0] | tsoverflow << 31
                x = (aer_data >> 17) & 0x00007FFF
                y = (aer_data >> 2) & 0x00007FFF
                pol = (aer_data >> 1) & 0x00000001
                counter = counter + size

                if timestamp >= start_time:
                    if timestamp < stop_time:
                        # Collect the events as a list (coordinates and times
                        # separately)
                        ev_list.append((x, y, pol))
                        ev_times.append(timestamp)
                    else:
                        # Once stop_time is reached,
                        # Collect the event lists and accompanying details as a
                        # dictionary
                        trial = {
                            'label': trial_times[trial_ind][0],
                            'subject': subj_num,
                            'lighting': light_cond,
                            'events': np.array(ev_list, dtype=np.uint8),
                            'ev_times': np.array(ev_times) - ev_times[0]
                        }
                        trials.append(trial)
                        # Then reset other values ready to collect the next
                        # trial
                        ev_list = []
                        ev_times = []
                        trial_ind += 1
                        if trial_ind < num_trials:
                            start_time = int(trial_times[trial_ind][1])
                            if start_time < stop_time:
                                print("Error on subject %d, with %s condition" %
                                      (subj_num, light_cond))
                                raise Exception(
                                    "New start time earlier than previous block stop time"
                                )
                            stop_time = int(trial_times[trial_ind][2])
                        else:
                            return trials
        else:
            # non-polarity event packet, not implemented
            raise NotImplementedError("Non polarity event packet not supported")
            pass
    return


def get_gesture_data(datafile, labelfile):
    """Creates gesture data dictionary from v3.1 aedat file.

    Args:
        datafile (str): absolute path to aedat file
        labelfile (int): absolute path to related label file.

    Returns:
        list: loaded data stored in multiple dict with gesture id, subject id,
            lighting condition, events and events time.
    """
    with open(labelfile) as f:
        # Get class labels and start + stop times from the _labels.csv file
        trial_times = [line.split(',') for line in f]

    if os.path.isfile(datafile):
        # Get subject id and lightning condition from filename
        subj_num = int(os.path.basename(datafile)[4:6])
        lighting_condition = os.path.basename(datafile)[7:-6]

        aef = open(datafile, 'rb')
        version = _parse_version_string(aef.readline())
        aef.seek(0, 0)  # rewind
        bytes_pos = _skip_ascii_header(aef, version)
        if version == 3:
            data = _read_event_v3(aef, bytes_pos, trial_times, subj_num,
                                  lighting_condition)
        else:
            raise ValueError("Unsupported version: %d" % version)
    return data


def generate_dataset(datadir, subject_list):
    """Generates data set for a subject id list.

    Args:
        datadir (str): filepath where aedat files are stored.
        subject_list (list): subject id list to compose the train/test set.

    Returns:
        list: dataset filled with all events data.
    """
    dataset = []
    for subj in subject_list:
        import glob
        datafile = glob.glob(
            os.path.join(datadir, 'DvsGesture',
                         'user' + '{0:0=2d}'.format(subj) + '*.aedat'))
        labelfile = glob.glob(
            os.path.join(datadir, 'DvsGesture',
                         'user' + '{0:0=2d}'.format(subj) + '*.csv'))
        datafile.sort()
        labelfile.sort()

        for idx in range(len(datafile)):
            dataset_tmp = get_gesture_data(datafile[idx], labelfile[idx])
            for data_dict in dataset_tmp:
                dataset.append(data_dict)
    return dataset


def download_and_extract_dataset(data_url, dest_directory):
    """Download and extract data set tar file.

    If the data set we're using doesn't already exist, this function
    downloads data from given url and unpacks it into a directory.
    If the data_url is none, don't download anything and expect the data
    directory to contain the correct files already.

    Args:
      data_url: Web location of the tar file containing the data set.
      dest_directory: File path to extract data to.
    """
    if not data_url:
        return
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = data_url.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):

        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' %
                             (filename, float(count * block_size) /
                              float(total_size) * 100.0))
            sys.stdout.flush()

        try:
            filepath, _ = urllib.request.urlretrieve(data_url, filepath,
                                                     _progress)
        except:
            raise RuntimeError(
                f"Failed to download URL: {data_url} to folder: "
                f"{filepath}\nPlease make sure you have enough free"
                f" space and an internet connection")
        print()
        statinfo = os.stat(filepath)
        print(f"Successfully downloaded {filename} ({statinfo.st_size} bytes)")
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)
