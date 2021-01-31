#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import external libraries
import os
import glob
import logging
import pathlib

# Metadata
__author__ = "Rodrigo Villamil Pérez"
__copyright__ = "RVP"
__license__ = "MIT License"

import re
from datetime import datetime
import ciso8601

_logger = logging.getLogger(__name__)


class HEVCConverter:
    """ API for HEVCConverter
    """
    XMP_EXTENSION = "xmp"
    OUTPUTFILE_EXTENSION = "mp4"

    XML_NODE_REGEX = r"photoshop:DateCreated>(.*)</photoshop:DateCreated"

    def HEVCConverter(self, current_path):
        self._xmp_files_length = 0
        self._current_path = current_path

    def all_xmp_files(self):
        os.chdir(self._current_path)
        return glob.glob("*." + self.XMP_EXTENSION)

    def extract_creation_date_from_xmp_file(self, xmp_file_path):
        creation_date = None
        content_file = open(xmp_file_path, 'r').read()
        matches = re.finditer(self.XML_NODE_REGEX, content_file, re.MULTILINE)
        for match_num, match in enumerate(matches, start=1):
            _logger.debug("Match {matchNum} was found at {start}-{end}: {match}".format(
                matchNum=match_num, start=match.start(), end=match.end(), match=match.group()))
            for group_num in range(0, len(match.groups())):
                group_num = group_num + 1
                _logger.debug("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=group_num,
                                                                                        start=match.start(group_num), end=match.end(group_num), group=match.group(group_num)))
                creation_date = match.group(group_num)
        return creation_date

    def create_output_path(self, output_path):
        _logger.debug("Creating output path '%s'" % output_path)
        pathlib.Path(self._current_path + os.sep +
                     output_path).mkdir(parents=True, exist_ok=True)

    def run(self, xmp_file_list):
        os.chdir(self._current_path)
        total_processed = 1
        for xmp_file in xmp_file_list:
            _logger.debug("Processing '%d' of '%d'" %
                          (total_processed, self._xmp_files_length))
            filename_without_extension, extension = os.path.splitext(xmp_file)
            input_file_extension = self.__detect_input_file_extension(
                filename_without_extension)
            creation_date_str = self.extract_creation_date_from_xmp_file(
                xmp_file)
            self.__convert_file(input_file_extension,
                                filename_without_extension,
                                creation_date_str)
            total_processed += 1
        return total_processed

    # -------------- Privated --------------
    def __detect_input_file_extension(self, filename_without_extension):
        files_list = glob.glob(("%s.*" % filename_without_extension))
        files_list.remove(filename_without_extension +
                          '.' + self.XMP_EXTENSION)
        return (files_list[0].split('.')[1])

    def __datetime_str_to_datetime(self, my_date_time_str):
        my_datetime_object = ciso8601.parse_datetime(my_date_time_str)
        return my_datetime_object.strftime("%m/%d/%Y %H:%M:%S")

    def __change_creation_date_on_macos(self, full_path_outputfile, new_creation_datetime):
        from subprocess import call
        _logger.info("Setting creation date on file '%s' to '%s'" %
                     (full_path_outputfile, new_creation_datetime))
        command = 'SetFile -d "' + new_creation_datetime + \
            '" "' + full_path_outputfile + '"'
        _logger.debug("Running command '%s'" % command)
        call(command, shell=True)

    def __ffmepg_convert_file(self, filename_without_extension, input_file_extension):
        # See: https://aaron.cc/ffmpeg-hevc-apple-devices/
        #   ffmpeg -i input.avi -c:v libx265 -crf 28 -c:a aac -b:a 128k -tag:v hvc1 output.mp4
        from subprocess import call
        input_filename = filename_without_extension + '.' + input_file_extension
        output_filename = filename_without_extension + '.' + self.OUTPUTFILE_EXTENSION
        full_path_imputfile = self._current_path + os.sep + input_filename
        full_path_outputfile = self._current_path + os.sep + \
            self.OUTPUT_DIR_NAME + os.sep + output_filename
        _logger.info("Converting file '%s' to file '%s'" %
                     (input_filename, output_filename))
        command = "ffmpeg -i '{full_path_imputfile}' -c:v libx265 -preset medium -crf 22 -c:a aac -b:a 192k -vtag hvc1 -pix_fmt yuv420p -r 30000/1001 '{full_path_outputfile}'".format(
            full_path_imputfile=full_path_imputfile, full_path_outputfile=full_path_outputfile)
        _logger.debug("Running comamnd '%s'" % command)
        call(command, shell=True)

    def __convert_file(self, input_file_extension, filename_without_extension, creation_date_str):
        input_filename = filename_without_extension + "." + input_file_extension,
        _logger.info("Converting file '{input_file}' and setting '{creation_date_str}' as creation date".format(
            input_file=input_filename, creation_date_str=creation_date_str))
        new_creation_datetime = self.__datetime_str_to_datetime(
            creation_date_str)
        _logger.debug("New Date time %s" % new_creation_datetime)
        full_path_outputfile = self._current_path + os.sep + self.OUTPUT_DIR_NAME + \
            os.sep + filename_without_extension + '.' + self.OUTPUTFILE_EXTENSION
        if os.path.exists(full_path_outputfile):
            _logger.warn(
                "WARN!! File '%s' already_exist! ...skipping .." % full_path_outputfile)
        else:
            self.__ffmepg_convert_file(
                filename_without_extension, input_file_extension)
            self.__change_creation_date_on_macos(
                full_path_outputfile, new_creation_datetime)
