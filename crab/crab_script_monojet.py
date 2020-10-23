#!/usr/bin/env python
import os
import sys
import re
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

jsons = {
        '2016': "Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt",
        '2017': "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt",
        '2018': "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
}

def main():
    # Get 1000 events for testing
    maxEntries = 1000
    files = ['root://cmsxrootd.fnal.gov//store/data/Run2017B/SingleElectron/NANOAOD/02Apr2020-v1/230000/1D3BEA1E-34E5-F04D-B470-5527915AC028.root']
    branchsel = "keep_and_drop_monojet.txt"
    dataset = '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD'
    # Run period for data
    run_period = 'B'
    jet_type = 'AK8PFPuppi'

    # Define the collection merger module for fat jets
    selectors = [
        collectionMerger(input=["FatJet"],output="FatJet",sortkey=lambda x: x.pt_nom),
    ]

    # Define the jetMET module for fat jets
    jme_modules = [
                    createJMECorrector(
                                        isMC=False,
                                        dataYear='2017',
                                        jesUncert="Total",
                                        runPeriod=run_period,
                                        jetType=jet_type,
                                        metBranchName='METFixEE2017'
                                        )()
                    ]
                    
    modules = jme_modules + selectors

    p=PostProcessor(outputDir=".",
        inputFiles=files,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        fwkJobReport=True,
        maxEntries=maxEntries,
        jsonInput=jsons['2017'])

    p.run()

    print "DONE"

if __name__ == "__main__":
    main()

