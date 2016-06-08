import re
import subprocess
import json
import os.path
import shutil
import sys
import os
import codecs

if sys.version_info < (3,):
  string_type = unicode
else:
  string_type = str

### Constraint checking function

def from_list( parameter_value, accepted_result):
  return parameter_value in accepted_result

def max_length( parameter_value, max_size):
  return len(parameter_value) <= max_size

def min_length( parameter_value, min_size):
  return len(parameter_value) >= min_size

def match_regex(parameter_value, regex):
  match = re.match(regex, parameter_value, re.U)
  return match is not None

def not_match_regex(parameter_value, regex):
  return not match_regex(parameter_value, regex)

def allow_empty_string(parameter_value, allow):
  # If empty strings are not allowed, and we have one, this is an error
  return allow or min_length(parameter_value,1)

def allow_whitespace_string(parameter_value, allow):
  # If leading/trailing whitespace is not allowed, and we have some, this is an error
  return allow or ( not_match_regex(parameter_value, r'^\s') and not_match_regex(parameter_value, r'.*\s$') )


constraints = {
    "select" : {
        "check" : from_list
      , "type"  : list
    }
  , "allow_whitespace_string" : {
        "check" : allow_whitespace_string
      , "type"  : bool
    }
  , "allow_empty_string" : {
        "check" : allow_empty_string
      , "type"  : bool
    }
  # use unicode for regexs, since they will be parsed as unicode ...
  , "regex" :  {
        "check" : match_regex
      , "type"  : string_type
    }
  , "not_regex":  {
        "check" : not_match_regex
      , "type"  : string_type
    }
  , "max_length" :  {
        "check" : max_length
      , "type"  : int
    }
  , "min_length" :  {
        "check" : min_length
      , "type"  : int
    }
}

variable_constraints = {
  "max_length" : constraints["max_length"]
}

default_constraint = {
    "allow_whitespace_string" : False
  , "allow_empty_string" : False
}

def check_parameter(parameter_value, parameter_constraints):
  """Checks that a parameter value is ok with the constraint of the parameter"""

  result = True
  errors = []
  constraint_set = constraints

  # Check that our value contains a variable or not
  value_without_variables = re.sub(r'[\$@][\{\(][a-zA-Z0-9\[\]_.-]+[\}\)]', "", parameter_value)
  if parameter_value != value_without_variables:
    constraint_set = variable_constraints
    parameter_value = value_without_variables


  for (constraint_name, constraint_value) in parameter_constraints.iteritems():
    if constraint_name in constraint_set:
      constraint = constraint_set[constraint_name]
      if not constraint['check'](parameter_value,constraint_value):
        result = False
        errors.append(constraint_name)

  check = {'result': result, 'errors': errors}
  return check

def check_constraint_type(key, value):

  result = True
  errors = []

  if key in constraints:
    constraint = constraints[key]
    result = type(value) is constraint["type"]
    if not result:
      errors.append("expected a value of type '" + constraint["type"].__name__ + "', got '"+ str(value) +"' of type '"+ type(value).__name__  + "'")
  else:
    result = False
    errors.append("'"+ key +"' is an unknwown constraint")
  check = {'result': result, 'errors': errors}
  return check


