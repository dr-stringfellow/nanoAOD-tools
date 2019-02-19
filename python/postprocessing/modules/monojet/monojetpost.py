import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os

jet_pt_names = ['pt','pt_jesTotalDown','pt_jesTotalUp','pt_jerDown','pt_jerUp','pt_nom','pt_raw']
met_pt_names = ['pt','pt_jesTotalDown','pt_jesTotalUp','pt_jerDown','pt_jerUp','pt_nom','pt_unclustEnUp','pt_unclustEnDown']
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
    def has_jets(self, jets, fatjets):
        for name in jet_pt_names:
            for j in jets:
                if hasattr(j, name):
                    if getattr(j, name) > 75:
                        return True
            for fj in fatjets:
                if hasattr(fj, name):
                    if (getattr(fj, name) > 75):
                            return True
            return False
    def has_met(self, event):
        for name in met_pt_names:
            branch = 'MET_'+name
            if hasattr(event, branch):
                if getattr(event, 'MET_'+name) > 75:
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
            if e.pt > 20 and e.cutBased > 0:
                return True
        return False
    def has_photons(self, event):
        photons = Collection(event,"Photon")
        for p in photons:
            if p.pt > 150 and p.electronVeto:
                if hasattr(p,'cutBasedBitmap') and (getattr(p,'cutBasedBitmap') > 0):
                    return True
                if hasattr(p,'cutBased17Bitmap') and (getattr(p,'cutBased17Bitmap') > 0):
                    return True
        return False

    def has_b_jet(self, jets):
        for j in jets:
            # tighter than tight WP for both years
            if j.cleanmask and j.pt > 20 and abs(j.eta) < 2.5 and  j.btagDeepB > 0.81:
                return False

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        jets = Collection(event,"Jet")
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
        if self.has_met(event):
            return True
        if event.PuppiMET_pt > 75:
            return True

        return False