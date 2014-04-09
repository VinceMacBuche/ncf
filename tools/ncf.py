# -*- coding: utf-8 -*-
# This is a Python module containing functions to parse and analyze ncf components

# This module is designed to run on the latest major versions of the most popular
# server OSes (Debian, Red Hat/CentOS, Ubuntu, SLES, ...)
# At the time of writing (November 2013) these are Debian 7, Red Hat/CentOS 6,
# Ubuntu 12.04 LTS, SLES 11, ...
# The version of Python in all of these is >= 2.6, which is therefore what this
# module must support

import re
import subprocess
import json
import os.path

# Verbose output
VERBOSE = 0

dirs = [ "10_ncf_internals", "20_cfe_basics", "30_generic_methods", "40_it_ops_knowledge", "50_techniques", "60_services" ]

tags = {}
tags["common"] = ["bundle_name", "bundle_args"]
tags["generic_method"] = ["name", "description", "parameter", "class_prefix", "class_parameter", "class_parameter_id"]
tags["technique"] = ["name", "description", "version"]

def get_root_dir():
  return os.path.realpath(os.path.dirname(__file__) + "/../")

# This method emulates the behavior of subprocess check_output method.
# We aim to be compatible with Python 2.6, thus this method does not exist
# yet in subprocess.
def check_output(command):
    if VERBOSE == 1:
        print "VERBOSE: About to run command '" + " ".join(command) + "'"
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output = process.communicate()
    retcode = process.poll()
    if retcode != 0:
        if VERBOSE == 1:
            print "VERBOSE: Exception triggered, Command returned error code " + retcode
        raise subprocess.CalledProcessError(retcode, command, output=output[0])
    if VERBOSE == 1:
        print "VERBOSE: Command output: '" + output[0] + "'"
    return output[0]

def get_all_generic_methods_filenames(alt_path = ''):
  result = []
  filelist1 = get_all_generic_methods_filenames_in_dir(get_root_dir() + "/tree/30_generic_methods")
  filelist2 = []
  if alt_path == '':
    filelist2 = []
  else:
    filelist2 = get_all_generic_methods_filenames_in_dir(alt_path + "/30_generic_methods")
  result = filelist1 + filelist2

  return result

def get_all_generic_methods_filenames_in_dir(dir):
  return get_all_cf_filenames_under_dir(dir)

def get_all_techniques_filenames(alt_path = ''):
  result = []
  filelist1 = get_all_cf_filenames_under_dir(get_root_dir() + "/tree/50_techniques")
  filelist2 = []
  if alt_path == '':
    filelist2 = []
  else:
    filelist2 = get_all_cf_filenames_under_dir(alt_path + "/50_techniques")
  result = filelist1 + filelist2

  return result

def get_all_cf_filenames_under_dir(dir):
  filenames = []
  filenames_add = filenames.append
  for root, dirs, files in os.walk(dir):
    for file in files:
      if not file.startswith("_") and file.endswith(".cf"):
        filenames_add(os.path.join(root, file))
  return filenames

def parse_technique_metadata(technique_content):
  return parse_bundlefile_metadata(technique_content, "technique")

def parse_generic_method_metadata(technique_content):
  return parse_bundlefile_metadata(technique_content, "generic_method")

def parse_bundlefile_metadata(content, bundle_type):
  res = {}
  parameters = []

  for line in content.splitlines():
    for tag in tags[bundle_type]:
      unicodeLine = unicode(line,"UTF-8") #line.decode('unicode-escape')
      match = re.match("^\s*#\s*@" + tag + "\s(([a-zA-Z_]+)\s+(.*)|.*)$", unicodeLine, re.UNICODE)
      if match :
        # tag "parameter" may be multi-valued
        if tag == "parameter":
          parameters.append({'name': match.group(2), 'description': match.group(3)})
        else:
          res[tag] = match.group(1)

    match = re.match("[^#]*bundle\s+agent\s+([^(]+)\(?([^)]*)\)?.*$", line)
    if match:
      res['bundle_name'] = match.group(1)
      res['bundle_args'] = []

      if len(match.group(2)):
        res['bundle_args'] += [x.strip() for x in match.group(2).split(',')]

      # Any tags should come before the "bundle agent" declaration
      break
      
  # The tag "class_parameter_id" is a magic tag, it's value is built from class_parameter and the list of args
  if "class_parameter_id" in tags[bundle_type]:
    try:
      res['class_parameter_id'] = res['bundle_args'].index(res['class_parameter'])+1
    except:
      res['class_parameter_id'] = 0
      raise Exception("The class_parameter name \"" + res['class_parameter'] + "\" does not seem to match any of the bundle's parameters")

  # If we found any parameters, store them in the res object
  if len(parameters) > 0:
    res['parameter'] = parameters

  expected_tags = tags[bundle_type] + tags["common"]
  if sorted(res.keys()) != sorted(expected_tags):
    missing_keys = [mkey for mkey in expected_tags if mkey not in set(res.keys())]
    raise Exception("One or more metadata tags not found before the bundle agent declaration (" + ", ".join(missing_keys) + ")")

  return res

def parse_technique_methods(technique_file):
  res = []

  # Check file exists
  if not os.path.exists(technique_file):
    raise Exception("No such file: " + technique_file)

  out = check_output(["cf-promises", "-pjson", "-f", technique_file])
  promises = json.loads(out)

  # Sanity check: if more than one bundle, this is a weird file and I'm quitting
  bundle_count = 0
  for bundle in promises['bundles']:
    if bundle['bundleType'] == "agent":
      bundle_count += 1

  if bundle_count > 1:
    raise Exception("There is not exactly one bundle in this file, aborting")

  # Sanity check: the bundle must be of type agent
  if promises['bundles'][0]['bundleType'] != 'agent':
    raise Exception("This bundle if not a bundle agent, aborting")

  methods_promises = [promiseType for promiseType in promises['bundles'][0]['promiseTypes'] if promiseType['name']=="methods"]
  methods = []
  if len(methods_promises) >= 1:
    methods = methods_promises[0]['contexts']

  for context in methods:
    class_context = context['name']

    for method in context['promises']:
      method_name = None
      args = None

      promiser = method['promiser']

      for attribute in method['attributes']:
        if attribute['lval'] == 'usebundle':
          if attribute['rval']['type'] == 'functionCall':
            method_name = attribute['rval']['name']
            args = [ arg['value'] for arg in attribute['rval']['arguments']]
          if attribute['rval']['type'] == 'string':
            method_name = attribute['rval']['value']

      if args:
        res.append({'class_context': class_context, 'method_name': method_name, 'args': args})
      else:
        res.append({'class_context': class_context, 'method_name': method_name})

  return res

def get_all_generic_methods_metadata(alt_path = ''):
  all_metadata = {}

  filenames = get_all_generic_methods_filenames(alt_path)

  for file in filenames:
    content = open(file).read()
    try:
      metadata = parse_generic_method_metadata(content)
      all_metadata[metadata['bundle_name']] = metadata
    except Exception:
      continue # skip this file, it doesn't have the right tags in - yuk!

  return all_metadata

def get_all_techniques_metadata(include_methods_calls = True, alt_path = ''):
  all_metadata = {}

  if alt_path != '': print "INFO: Alternative source path added: %s" % alt_path

  filenames = get_all_techniques_filenames(alt_path)

  for file in filenames:
    content = open(file).read()
    try:
      metadata = parse_technique_metadata(content)
      all_metadata[metadata['bundle_name']] = metadata

      if include_methods_calls:
        method_calls = parse_technique_methods(file)
        all_metadata[metadata['bundle_name']]['method_calls'] = method_calls
    except Exception as e:
      print "ERROR: Exception triggered, Unable to parse file " + file
      print e
      continue # skip this file, it doesn't have the right tags in - yuk!

  return all_metadata

