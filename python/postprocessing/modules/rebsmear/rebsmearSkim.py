import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os

class rebsmearSkim(Module):
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

    def has_muons(self, event):
        muons = Collection(event,"Muon")
        for m in muons:
            if m.pt > 20 and m.looseId and (m.pfRelIso04_all < 0.4):
                return True
        return False

    def has_electrons(self, event):
        electrons = Collection(event,"Electron")
        for e in electrons:
            if e.pt > 20 and e.cutBased > 0:
                return True
        return False

    def has_photons(self, event):
        photons = Collection(event,"Photon")
        for p in photons:
            if p.pt > 175:
                return True
        return False

    def has_jets(self, jets, pt_thresh=15, ht_thresh=50):
        jetpt = [j.pt for j in jets if j.pt > pt_thresh]
        if len(jetpt) < 2:
            return False

        # HT threshold: HT > 50 GeV
        ht = sum(jetpt)
        if jetpt < ht_thresh:
            return False
        
        return True

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # If there are well identified leptons in the event, veto the event
        if self.has_electrons(event):
            return False
        if self.has_muons(event):
            return False
        if self.has_photons(event):
            return False
        
        # Check for jets: 
        # At least two jets must be present with pt > 15 GeV
        jets = Collection(event,"Jet")
        
        if not self.has_jets(jets):
            return False

        return True
