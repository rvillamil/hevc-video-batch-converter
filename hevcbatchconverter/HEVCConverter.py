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


    #def from subprocess import call
    def change_creation_date_on_macos(self, filepath, new_creation_datetime):
        from subprocess import call
        command = 'SetFile -d ' + new_creation_datetime + ' ' + filepath
        call(command, shell=True)

    def datetime_str_to_datetime(self, my_date_time_str):
        my_datetime_object=ciso8601.parse_datetime(my_date_time_str)
        return my_datetime_object.strftime("%m/%d/%Y %H:%M:%S")

    def convert_file (self,file, creation_date_str):
        print ("Convirtiendo fichero '{file}' y estableciendo '{creation_date_str}' como fecha de creacion".format(file=file,creation_date_str=creation_date_str))
        new_creation_datetime=self.datetime_str_to_datetime (creation_date_str)
        print ("New Date time %s" % new_creation_datetime)

        # Set fecha de creacion
        self.change_creation_date_on_macos (file, new_creation_datetime)
        
        
    def convert_dir (self, dir):
        os.chdir(dir)
        for file in glob.glob("*."+ self.XMP_EXTENSION):
            print ("------------------------------------")
            creation_date_str = self.extract_creation_date_from_xmp_file (file)
            filename, extension = os.path.splitext(file) 
            self.convert_file(filename + "." + self.VIDEO_EXTENSION, creation_date_str)
