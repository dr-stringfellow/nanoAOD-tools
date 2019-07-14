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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger

# Loop over input arguments
options = {}
prefixes = ['dataset', 'ismc', 'year']
for argument in sys.argv:
    for prefix in prefixes:
        if argument.startswith(prefix):
            value = argument.split('=')[-1]
            options[prefix] = value
options['ismc'] = options['ismc'].lower() == "true"

test = False
if test:
    files = ['299516D6-8D79-F542-B7F6-C7C041A2E1D0.root']
    maxEntries = 1000
else:
    files = inputFiles()
    maxEntries = 0
branchsel = "keep_and_drop_monojet.txt"

selectors = [
    collectionMerger(input=["Jet"],output="Jet", selector=dict([("Jet",lambda x : x.pt>20)])),
    collectionMerger(input=["Muon"],output="Muon", selector=dict([("Muon",lambda x : x.pt>10 and x.looseId and x.pfRelIso04_all < 0.4)])),
    collectionMerger(input=["Electron"],output="Electron", selector=dict([("Electron",lambda x : x.pt>10 and x.cutBased > 1)])),
    collectionMerger(input=["Photon"],output="Photon", selector=dict([("Photon",lambda x : x.cutBasedBitmap>0)])),
]
mc_selectors = [
    collectionMerger(input=["GenPart"],output="GenPart", selector=dict([("GenPart",lambda x : x.status==1)])),
    collectionMerger(input=["GenJet"],output="GenJet", selector=dict([("GenJet",lambda x : x.pt>20)]))
]

triggerfile = 'triggers_nano_v5.txt'
if options['ismc']:
    if options['year'] == '2017':
        modules = [
            monojetPost(triggerfile),
            jetmetUncertainties2017(),
            jetmetUncertainties2017AK8Puppi(),
            PrefCorr(jetroot="L1prefiring_jetpt_2017BtoF.root",
                     jetmapname="L1prefiring_jetpt_2017BtoF",
                     photonroot="L1prefiring_photonpt_2017BtoF.root",
                     photonmapname="L1prefiring_photonpt_2017BtoF")
            ] + selectors + mc_selectors
    elif options['year'] == '2018':
        modules = [
            monojetPost(triggerfile),
            jetmetUncertainties2018(),
            jetmetUncertainties2018AK8Puppi(),
            ] + selectors + mc_selectors

    p = PostProcessor(
        outputDir=".",
        inputFiles=files,
        branchsel=branchsel,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        maxEntries=maxEntries,
        fwkJobReport=True)
else:
    if options['year'] == '2017':
        json = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
    elif options['year'] == '2018':
        json = "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
    modules = [monojetPost(triggerfile)] + selectors
    p=PostProcessor(outputDir=".",
        inputFiles=files,
        branchsel=branchsel,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        fwkJobReport=True,
        maxEntries=maxEntries,
        jsonInput=json)
p.run()

addDatasetTag()

print "DONE"
# os.system("ls -lR")

