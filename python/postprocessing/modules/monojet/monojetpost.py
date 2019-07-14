import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os
class monojetPost(Module):
    def __init__(self):
        cmssw_base = os.getenv('CMSSW_BASE')
        triggerlist = cmssw_base + "/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/monojet/triggers_nano_v5.txt")

        with open(triggerlist "r") as f:
            self._triggers = filter(lambda x: len(x), map(lambda x: x.strip(), f.readlines()))

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

        # Check triggers
        has_trigger = False
        for trigger in self._triggerlist:
            if hasattr(event, trigger):
                has_trigger |= getattr(event, trigger)
                if has_trigger:
                    break
        if not has_trigger:
            return False

        # Logic:
        # All events need a minimum jet content
        # If that does not exist, return False, reject event
        if event.nJet + event.nFatJet == 0:
            return False

        # Check for jets
        jets = Collection(event,"Jet")
        fatjets = Collection(event,"FatJet")
        has_jets = False
        if len(jets):
            if (jets[0].pt > 75) and (abs(jets[0].eta) < 2.5 ):
                has_jets = True
        if len(fatjets):
            if (fatjets[0].pt > 75) and (abs(fatjets[0].eta) < 2.5 ):
                has_jets = True
        if not has_jets:
            return False

        # All events surviving this far have jets.
        # Now pass events if they have leptons, a photon or MET

        # Check for muons
        muons = Collection(event,"Muon")
        for m in muons:
            if m.pt > 20 and m.looseId and (m.pfRelIso04_all < 0.4):
                return True

        # Check for electrons
        electrons = Collection(event,"Electron")
        for e in electrons:
            if e.pt > 20 and e.cutBased > 1:
                return True

        # Check for photons
        photons = Collection(event,"Photon")
        for p in photons:
            if p.pt > 150 and p.electronVeto and (p.cutBasedBitmap > 1):
                return True

        # Check for MET
        if event.MET_pt > 75:
            return True
        if event.PuppiMET_pt > 75:
            return True

        return False