#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

p=PostProcessor(".",inputFiles(),"",branchsel="keep_and_drop_vbf_hinv.txt",provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

