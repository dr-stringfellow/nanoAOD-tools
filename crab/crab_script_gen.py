#!/usr/bin/env python
import os
import sys
import re
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, addDatasetTag

def read_options():
    # Loop over input arguments
    options = {}
    prefixes = ['year','nofilter','test','file']
    for argument in sys.argv:
        for prefix in prefixes:
            if argument.startswith(prefix):
                value = argument.split('=')[-1]
                options[prefix] = value
    for p in prefixes:
        if p not in options.keys():
            options[p] = ''

    options['nofilter'] = options['nofilter'].lower() == "true"
    options['test'] = options['test'].lower() == "true"

    return options

def main():
    options = read_options()

    if options['test']:
        files = [options['file']]
        maxEntries = 1000
    else:
        files = inputFiles()
        maxEntries = 0
    branchsel = "keep_and_drop_gen.txt"

    p = PostProcessor(
        outputDir=".",
        inputFiles=files,
        outputbranchsel=branchsel,
        provenance=True,
        maxEntries=maxEntries,
        fwkJobReport=True)
    p.run()

    addDatasetTag()

    print "DONE"

if __name__ == "__main__":
    main()

