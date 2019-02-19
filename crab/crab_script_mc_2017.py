#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, addDatasetTag

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

modules = [
    puWeight_2017,
    jetmetUncertainties2017(),
    ]

files = inputFiles()
p=PostProcessor(".",files,"",branchsel="keep_drop_monojet.txt",modules=modules,provenance=True,fwkJobReport=True)
p.run()

addDatasetTag()

print "DONE"
os.system("ls -lR")

