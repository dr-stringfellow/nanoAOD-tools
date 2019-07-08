#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, addDatasetTag

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.monojet.monojetpost import monojetPost

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr

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
branchsel = "keep_and_drop_monojet.txt"

modules = []
if options['ismc']:
    if options['year'] == '2017':
        modules = [
            monojetPost(),
            jetmetUncertainties2017(),
            jetmetUncertainties2017AK8Puppi(),
            PrefCorr(jetroot="L1prefiring_jetpt_2017BtoF.root",
                     jetmapname="L1prefiring_jetpt_2017BtoF",
                     photonroot="L1prefiring_photonpt_2017BtoF.root",
                     photonmapname="L1prefiring_photonpt_2017BtoF")
            ]
    elif options['year'] == '2018':
        modules = [
            monojetPost(),
            jetmetUncertainties2018(),
            jetmetUncertainties2018AK8Puppi(),
            ]

    p = PostProcessor(
        outputDir=".",
        inputFiles=files,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        fwkJobReport=True)
else:
    if options['year'] == '2017':
        json = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
    elif options['year'] == '2018':
        json = "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
    modules = [monojetPost()]
    p=PostProcessor(outputDir=".",
        inputFiles=files,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        fwkJobReport=True,
        jsonInput=json)
p.run()

addDatasetTag()

print "DONE"
# os.system("ls -lR")

