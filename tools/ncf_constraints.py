import re
import subprocess
import json
import os.path
import shutil
import sys
import os
import codecs


def from_list( parameter, accepted_result):
  return accepted_result.contains(parameter)

def not_from_list( parameter, not_accepted_result):
  return not from_list(parameter, not_accepted_result)

def max_length( parameter, max_size):
  return parameter.length <= max_size

def min_length( parameter, min_size):
  return parameter.length >= min_size

def match_regexp(parameter, regexp):
  match = re.match(regexp, parameter, re.S)
  return match is not None

def not_match_regexp(parameter, regexp):
  return not match_regexp(parameter, regexp)

string_constraints = {
    "default" : "^\S(.*\S)?$"
  , "allow_whitespace_string" : "^.+$"
  , "allow_empty_string" : "^(\S(.*\S)?)?$"
  , "all" : ".*"
}

def check(parameter, constraint):
  string_constraint = "default"
  empty_constraint = constraint.get("allow_empty_string", False)
  if constraint.get("allow_whitespace_string", False):
    if empty_constraint:
      string_constraint = "all"
    else:
      string_constraint = "allow_whitespace_string"
  elif empty_constraint:
    string_constraint = "allow_empty_string"
  string_regex = string_constraints[string_constraint]
  result = match_regexp(parameter, string_regex)
  print(result)
  return result
