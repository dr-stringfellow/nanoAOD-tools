import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os

class triggerSelector(Module):
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

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        return self.has_trigger(event)