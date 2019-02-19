#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
# p=PostProcessor(".",inputFiles(),"",branchsel="keep_and_drop_vbf_hinv.txt",provenance=True,fwkJobReport=True)
# p=PostProcessor(".",inputFiles(),"",modules=[muonScaleRes2017(), puAutoWeight()],provenance=True,fwkJobReport=True)
p=PostProcessor(".",["/user/albert/scratch/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/823D1180-A3F3-E811-9C4E-E0071B73C600.root"],"",modules=[muonScaleRes2017(), puAutoWeight()],provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

