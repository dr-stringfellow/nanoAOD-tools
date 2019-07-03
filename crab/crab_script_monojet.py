#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, addDatasetTag

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

# Loop over input arguments
options = {}
prefixes = ['dataset', 'ismc', 'year']
for argument in sys.argv:
    for prefix in prefixes:
        if argument.startswith(prefix):
            value = argument.split('=')[-1]
            options[prefix] = value
options['ismc'] = options['ismc'].lower() == "true"

files = inputFiles()
# files = ['file:/eos/user/a/aalbert/nanopost/nopost/2EC2FE2C-56B0-584D-9149-463719420BE5.root']
branchsel = "keep_and_drop_monojet.txt"
cut = ''

modules = []
if options['ismc']:
    if options['year'] == '2017':
        modules = [
            jetmetUncertainties2017(),
            jetmetUncertainties2017AK8Puppi(),
            ]
    elif options['year'] == '2018':
        modules = [
            jetmetUncertainties2018(),
            jetmetUncertainties2018AK8Puppi(),
            ]

    p = PostProcessor(
        outputDir=".",
        inputFiles=files,
        cut=cut,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        fwkJobReport=True)
else:
    if options['year'] == '2017':
        json = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
    elif options['year'] == '2018':
        json = "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
    p=PostProcessor(outputDir=".",
        inputFiles=files,
        cut=cut,
        outputbranchsel=branchsel,
        provenance=True,
        fwkJobReport=True,
        jsonInput=json)
p.run()

addDatasetTag()

print "DONE"
os.system("ls -lR")

