import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os

class monojetPost(Module):
    def __init__(self, triggerlist):
        with open(triggerlist, "r") as f:
            self._triggers = filter(lambda x: len(x), map(lambda x: x.strip(), f.readlines()))

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def has_trigger(self, event):
        # Check triggers
        for trigger in self._triggers:
            if hasattr(event, trigger):
                if getattr(event, trigger):
                    return True
        return False
    def has_jets(self, jets, fatjets):
        if len(jets):
            if (jets[0].pt > 75) and (abs(jets[0].eta) < 2.5 ):
                return True
        if len(fatjets):
            if (fatjets[0].pt > 75) and (abs(fatjets[0].eta) < 2.5 ):
                return True
        return False
    def has_muons(self, event):
        muons = Collection(event,"Muon")
        for m in muons:
            if m.pt > 20 and m.looseId and (m.pfRelIso04_all < 0.4):
                return True
        return False
    def has_electrons(self, event):
        electrons = Collection(event,"Electron")
        for e in electrons:
            if e.pt > 20 and e.cutBased > 1:
                return True
        return False
    def has_photons(self, event):
        photons = Collection(event,"Photon")
        for p in photons:
            if p.pt > 150 and p.electronVeto and (p.cutBasedBitmap > 1):
                return True
        return False
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ### Trigger
        if not self.has_trigger(event):
            return False
        ### Vetoes
        # B jet veto
        jets = Collection(event,"Jet")
        for j in jets:
            # tighter than tight WP for both years
            if j.pt > 20 and abs(j.eta) < 2.5 and  j.btagDeepB > 0.81:
                return False

        # All events need a minimum jet content
        # If that does not exist, return False, reject event
        if event.nJet + event.nFatJet == 0:
            return False

        # Check for jets
        fatjets = Collection(event,"FatJet")
        if not self.has_jets(jets, fatjets):
            return False

        # All events surviving this far have jets.
        # Now pass events if they have leptons, a photon or MET
        if self.has_muons(event):
            return True
        if self.has_electrons(event):
            return True
        if self.has_photons(event):
            return True

        # Check for MET
        if event.MET_pt > 75:
            return True
        if event.PuppiMET_pt > 75:
            return True

        return False