#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Usage: ./ncf_json.py 
#
# This is a Python module to generate json data from ncf generic methods and techniques
#
# This module is designed to run on the latest major versions of the most popular
# server OSes (Debian, Red Hat/CentOS, Ubuntu, SLES, ...)
# At the time of writing (November 2013) these are Debian 7, Red Hat/CentOS 6,
# Ubuntu 12.04 LTS, SLES 11, ...
# The version of Python in all of these is >= 2.6, which is therefore what this
# module must support

import ncf 
import sys
import json


if __name__ == '__main__':


  generic_methods = ncf.get_all_generic_methods_metadata()
  
  myJson = json.dumps(generic_methods,indent=4, separators=(',', ': '))
  
  dest = open("generic_methods.json","w")
   
  dest.write(myJson)

  techniques = ncf.get_all_techniques_metadata()
  myJson2 = json.dumps(techniques,indent=4, separators=(',', ': '))
  dest2 = open("techniques.json","w")
  dest2.write(myJson2)
