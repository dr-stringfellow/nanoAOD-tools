#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

modules = [ jetmetUncertainties2017(), jetmetUncertainties2017AK4Puppi(),btagSF2017(),puAutoWeight()]

files = inputFiles()
files = ["/user/albert/scratch/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/823D1180-A3F3-E811-9C4E-E0071B73C600.root"]
p=PostProcessor(".",files,"",modules=modules,provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

