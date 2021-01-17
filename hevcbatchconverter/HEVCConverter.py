#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import external libraries
import os
import glob
import logging

# Metadata
__author__ = "Rodrigo Villamil Pérez"
__copyright__ = "RVP"
__license__ = "MIT License"

import re
import time
from datetime import datetime
import ciso8601

_logger = logging.getLogger(__name__)

class HEVCConverter:
    """ API for HEVCConverter
    """
    XMP_EXTENSION = "xmp"
    VIDEO_EXTENSION = "avi"
    XML_NODE_REGEX = r"photoshop:DateCreated>(.*)</photoshop:DateCreated"
    
    def print_files(self):
        print ("Printing..")
    
    def print_all_convertible_files_in_dir(self, dir):
        os.chdir(dir)
        for file in glob.glob("*."+ self.XMP_EXTENSION):
            creation_date = self.extract_creation_date_from_xmp_file (file)
            print("Fichero '{file}' creado el dia '{creation_date}'".format(file=file,creation_date=creation_date))  

    def extract_creation_date_from_xmp_file (self, filepath):
        creation_date=None
        content_file = open(filepath, 'r').read()
        matches = re.finditer(self.XML_NODE_REGEX, content_file, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            _logger.debug ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1                
                _logger.debug ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                creation_date=match.group(groupNum)
        return creation_date


    def timestamp_to_datetime(self,ts):
        """ Example:
            For ts '1072362918.0' then returns datetime '2003-12-25T15:35:18+01:00'
        """
        TIME_FORMAT='%Y-%m-%d %H:%M:%S'
        dt = datetime.utcfromtimestamp(ts).strftime(TIME_FORMAT)
        print("Time as string : %s" % dt)        
        return dt

    def datetime_str_to_timestamp(self,my_date_time_str):
        """ Example:
            For my_date_time_str '2003-12-25T15:35:18+01:00' then returns timestamp '1072362918.0'
        """
        print ("Transformando la fecha de creacion: "+ my_date_time_str)
        my_datetime_object=ciso8601.parse_datetime(my_date_time_str)
        #print ("CISO" , my_datetime_object)
        ts = int(datetime.timestamp(my_datetime_object))
        
        #print("timestamp =", ts)
        return ts

    def datetime_str_to_datetime(self, my_date_time_str):
        my_datetime_object=ciso8601.parse_datetime(my_date_time_str)
        return my_datetime_object.strftime("%m/%d/%Y %H:%M:%S")


    def change_creation_date_on_macos(self, dirname, filename, new_creation_datetime):
        from subprocess import call
        full_path_file =dirname+ os.sep + filename
        print ("Modificando la fecha de cracion del fichero '%s'" % full_path_file)
        command = 'SetFile -d "' + new_creation_datetime + '" "' + full_path_file + '"'
        print ("Corriendo comando '%s'" % command)
        call(command, shell=True)

    def ffmep_convert_file(self, dirname, input_filename):
        # See: https://aaron.cc/ffmpeg-hevc-apple-devices/
        from subprocess import call
        output_filename = input_filename.replace('.avi','.mp4')
        full_path_imputfile = dirname + os.sep + input_filename
        full_path_outputfile = dirname + os.sep + output_filename
        # ffmpeg -i input.avi -c:v libx265 -crf 28 -c:a aac -b:a 128k -tag:v hvc1 output.mp4
        command = "ffmpeg -i '{full_path_imputfile}' -c:v libx265 -crf 0 -c:a aac -b:a 128k -tag:v hvc1 '{full_path_outputfile}'".format(full_path_imputfile=full_path_imputfile, full_path_outputfile=full_path_outputfile)
        print ("FFMPEG: Corriendo comando '%s'" % command)
        call(command, shell=True)
        return output_filename


    def process_file (self,dir, file, creation_date_str):
        print ("Convirtiendo fichero '{file}' y estableciendo '{creation_date_str}' como fecha de creacion".format(file=file,creation_date_str=creation_date_str))
        new_creation_datetime=self.datetime_str_to_datetime (creation_date_str)
        print ("New Date time %s" % new_creation_datetime)
        # Set fecha de creacion
        output_filename = self.ffmep_convert_file(dir,file)
        self.change_creation_date_on_macos (dir, output_filename, new_creation_datetime)  
        
    def convert_dir (self, dir):
        os.chdir(dir)
        for file in glob.glob("*."+ self.XMP_EXTENSION):
            print ("------------------------------------")
            creation_date_str = self.extract_creation_date_from_xmp_file (file)
            filename, extension = os.path.splitext(file) 
            self.process_file(dir, filename + "." + self.VIDEO_EXTENSION, creation_date_str)
