import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class monojetPost(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event.nJet + event.nFatJet == 0:
            return False

        # Check for jets
        jets = Collection(event,"Jet")
        fatjets = Collection(event,"FatJet")
        has_jets = False
        if len(jets):
            if jets[0].pt > 50:
                has_jets = True
        if len(fatjets):
            if fatjets[0].pt > 50:
                has_jets = True


        # Check for leptons
        has_lep = event.nMuon + event.nElectron > 0

        # Check for photons
        photons = Collection(event,"Photon")
        has_photon = False
        if len(photons):
            if photons[0].pt > 100:
                has_photon = True

        # Check for MET
        has_met = event.MET_pt > 50

        # All together
        good = (has_lep or has_photon or has_met) and has_jets
        return good
