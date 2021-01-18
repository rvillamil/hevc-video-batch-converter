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


def pretty_print(text):
    print("\U0001F412 {text}".format(text=text))


class HEVCConverter:
    """ API for HEVCConverter
    """
    XMP_EXTENSION           = "xmp"
    OUTPUTFILE_EXTENSION    = "mp4"
    OUTPUT_DIR_NAME         = "output"
    XML_NODE_REGEX          = r"photoshop:DateCreated>(.*)</photoshop:DateCreated"    

    def print_all_convertible_files_in_dir(self, dir):
        os.chdir(dir)
        for file in glob.glob("*." + self.XMP_EXTENSION):
            creation_date = self.extract_creation_date_from_xmp_file(file)
            pretty_print("File '{file}' created on '{creation_date}'".format(
                file=file, creation_date=creation_date))

    def extract_creation_date_from_xmp_file(self, filepath):
        creation_date = None
        content_file = open(filepath, 'r').read()
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

    def detect_input_file_extension (self,filename_without_extension):
        files_list=glob.glob( ("%s.*" % filename_without_extension)  )
        files_list.remove (filename_without_extension + '.' + self.XMP_EXTENSION)
        return (files_list[0].split('.')[1])

    def datetime_str_to_datetime(self, my_date_time_str):
        my_datetime_object = ciso8601.parse_datetime(my_date_time_str)
        return my_datetime_object.strftime("%m/%d/%Y %H:%M:%S")

    def change_creation_date_on_macos(self, full_path_outputfile, new_creation_datetime):
        from subprocess import call
        pretty_print("Setting creation date on file '%s' to '%s'" % (full_path_outputfile, new_creation_datetime))
        command = 'SetFile -d "' + new_creation_datetime + '" "' + full_path_outputfile + '"'
        _logger.debug("Running command '%s'" % command)
        call(command, shell=True)

    def ffmepg_convert_file(self, dirname, filename_without_extension, input_file_extension):
        # See: https://aaron.cc/ffmpeg-hevc-apple-devices/
        #   ffmpeg -i input.avi -c:v libx265 -crf 28 -c:a aac -b:a 128k -tag:v hvc1 output.mp4
        from subprocess import call
        input_filename = filename_without_extension + '.' + input_file_extension
        output_filename = filename_without_extension + '.' + self.OUTPUTFILE_EXTENSION
        full_path_imputfile = dirname + os.sep + input_filename
        full_path_outputfile = dirname + os.sep + self.OUTPUT_DIR_NAME + os.sep + output_filename
        pretty_print("Converting file '%s' to file '%s'" % (input_filename,output_filename))        
        command = "ffmpeg -i '{full_path_imputfile}' -qscale 0 -c:v libx265 -crf 22 -c:a aac -b:a 192k -tag:v hvc1 '{full_path_outputfile}'".format(
            full_path_imputfile=full_path_imputfile, full_path_outputfile=full_path_outputfile)
        _logger.debug("Running comamnd '%s'" % command)
        call(command, shell=True)
        return full_path_outputfile

    def convert_file_from_dir(self, dir, input_file_extension, filename_without_extension, creation_date_str):
        input_filename = filename_without_extension + "." + input_file_extension, 
        _logger.debug("Converting file '{input_file}' and setting '{creation_date_str}' as creation date".format(
            input_file=input_filename, creation_date_str=creation_date_str))
        new_creation_datetime = self.datetime_str_to_datetime(
            creation_date_str)
        _logger.debug("New Date time %s" % new_creation_datetime)        
        full_path_outputfile = self.ffmepg_convert_file(dir, filename_without_extension, input_file_extension)
        self.change_creation_date_on_macos( full_path_outputfile, new_creation_datetime)
    
    def create_output_dir (self, current_dir, output_dirname):
        pretty_print ("Creating directory '%s' on current dir '%s'" % (self.OUTPUT_DIR_NAME,current_dir))        
        pathlib.Path(current_dir + os.sep + output_dirname).mkdir(parents=True, exist_ok=True)

    def convert_dir(self, dir):
        os.chdir(dir)
        self.create_output_dir ( dir, self.OUTPUT_DIR_NAME)
        for xmp_file in glob.glob("*." + self.XMP_EXTENSION):
            print("------------------------------------")
            filename_without_extension, extension = os.path.splitext(xmp_file)
            creation_date_str       = self.extract_creation_date_from_xmp_file(xmp_file)
            input_file_extension    = self.detect_input_file_extension(filename_without_extension)            
            self.convert_file_from_dir(dir,
                                       input_file_extension,
                                       filename_without_extension, 
                                       creation_date_str)
