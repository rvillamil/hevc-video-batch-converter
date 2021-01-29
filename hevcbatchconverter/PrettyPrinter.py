#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Metadata
__author__      = "Rodrigo Villamil Pérez"
__copyright__   = "RVP"
__license__     = "MIT License"

def pretty_print(text):
    # Monkey
    print("\U0001F412 {text}".format(text=text))

def pretty_warn(text):
    # Fire
    print("\U0001F525 Warn! {text}".format(text=text))

def pretty_error(text):
    # Skull
    print("\U0001F480 ERROR! {text}".format(text=text))
