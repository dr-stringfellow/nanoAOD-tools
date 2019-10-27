#!/usr/bin/env python
import os
import sys
import re
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger


modules = [
    createJMECorrector(
                        isMC=True,
                        dataYear='2017',
                        jesUncert="Total",
                        redojec=False,
                        jetType='AK4PFchs',
                        metBranchName='MET'
                        )(),
    collectionMerger(input=["Jet"],output="Jet2", selector={"Jet" : lambda x: x.pt > 20})
]

p=PostProcessor(outputDir=".",
    inputFiles=['GJets_HT-400To600_2017.root'],
    outputbranchsel='keep_drop_test.txt',
    modules=modules,
    provenance=True,
    fwkJobReport=True,
    maxEntries=10)
p.run()
