#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, addDatasetTag

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.monojet.monojetpost import monojetPost, jet_pt_names
from PhysicsTools.NanoAODTools.postprocessing.modules.monojet.triggerselector import triggerSelector

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018

# Loop over input arguments
options = {}
prefixes = ['dataset', 'ismc', 'year','nofilter','test']
for argument in sys.argv:
    for prefix in prefixes:
        if argument.startswith(prefix):
            value = argument.split('=')[-1]
            options[prefix] = value
for p in prefixes:
    if p not in options.keys():
        options[p] = ''

options['ismc'] = options['ismc'].lower() == "true"
options['nofilter'] = options['nofilter'].lower() == "true"
options['test'] = options['test'].lower() == "true"

if options['test']:
    files = ['./GJets_HT-400To600_2018.root']
    options['dataset'] = 'GJets_HT-400To600_2018'
    maxEntries = 1000
else:
    files = inputFiles()
    maxEntries = 0
branchsel = "keep_and_drop_monojet.txt"


def jetptcut(jet, value):
    for name in jet_pt_names:
        if hasattr(jet, name):
            if getattr(jet, name) > value:
                return True
    return False

def filter_electrons(electron):
    return (electron.pt>9.9) and (electron.cutBased > 0)

def filter_photons(photon):
    if hasattr(photon, 'cutBasedBitmap'):
        return photon.cutBasedBitmap > 0
    if hasattr(photon, 'cutBased17Bitmap'):
        return photon.cutBased17Bitmap > 0
    return False

def filter_genpart(genpart):
    good = False
    good |= genpart.status in [1,2,62]
    good |= (abs(genpart.pdgId) in [11,12,13,14,15,16,22,23,24])
    return good


def filter_muons(muon):
    return (muon.pt>9.9) and (muon.looseId) and (muon.pfRelIso04_all < 0.4)

if options['nofilter']:
    common_modules = []
    selectors = []
    mc_selectors = []
    trigger_selector = []
else:
    triggerfile = 'triggers_nano_v5.txt'
    trigger_selector = [triggerSelector(triggerfile)]
    common_modules = [monojetPost()]
    selectors = [
        collectionMerger(input=["Jet"],output="Jet", selector={"Jet" : lambda x : jetptcut(x,19.9)}),
        collectionMerger(input=["FatJet"],output="FatJet", selector={"FatJet" : lambda x : jetptcut(x,75.0)}),
        collectionMerger(input=["Muon"],output="Muon", selector={"Muon" : filter_muons}),
        collectionMerger(input=["Electron"],output="Electron", selector={"Electron" : filter_electrons}),
        collectionMerger(input=["Photon"],output="Photon", selector={"Photon" : filter_photons}),
    ]

    mc_selectors = [
        collectionMerger(input=["GenPart"],output="GenPart", selector={"GenPart" : filter_genpart}),
        collectionMerger(input=["GenJet"],output="GenJet", selector={"GenJet" : lambda x : x.pt>20}),
        collectionMerger(input=["GenJetAK8"],output="GenJetAK8", selector={"GenJetAK8" : lambda x : x.pt>20})
    ]

if options['ismc']:
    if options['year'] == '2016':
        modules = trigger_selector + [
            jetmetUncertainties2016(),
            jetmetUncertainties2016AK8Puppi()
            ] + common_modules + [
            puAutoWeight_2016(),
            PrefCorr(jetroot="L1prefiring_jetpt_2016BtoH.root",
                     jetmapname="L1prefiring_jetpt_2016BtoH",
                     photonroot="L1prefiring_photonpt_2016BtoH.root",
                     photonmapname="L1prefiring_photonpt_2016BtoH"),
            ] + selectors + mc_selectors
    if options['year'] == '2017':
        modules = trigger_selector + [
            jetmetUncertainties2017(),
            jetmetUncertainties2017AK8Puppi()
            ] + common_modules + [
            puAutoWeight_2017(),
            PrefCorr(jetroot="L1prefiring_jetpt_2017BtoF.root",
                     jetmapname="L1prefiring_jetpt_2017BtoF",
                     photonroot="L1prefiring_photonpt_2017BtoF.root",
                     photonmapname="L1prefiring_photonpt_2017BtoF"),
            ] + selectors + mc_selectors
    elif options['year'] == '2018':
        modules = trigger_selector + [
            jetmetUncertaintiesProducer("2018", "Autumn18_V19_MC", [ "Total" ], redoJEC=True, jerTag="Autumn18_V7_MC"),
            jetmetUncertaintiesProducer("2018", "Autumn18_V19_MC", [ "Total" ], jetType="AK8PFPuppi", redoJEC=True, jerTag="Autumn18_V7_MC"),
            ] + common_modules + [
                puAutoWeight_2018()
            ] + selectors + mc_selectors

    p = PostProcessor(
        outputDir=".",
        inputFiles=files,
        outputbranchsel=branchsel,
        modules=modules,
        provenance=True,
        maxEntries=maxEntries,
        fwkJobReport=True)
else:
    modules = trigger_selector + common_modules + selectors
    if options['year'] == '2016':
        json = "Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
    elif options['year'] == '2017':
        json = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
    elif options['year'] == '2018':
        json = "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
        if '2018A' in options['dataset']:
            modules.append(jetRecalib2018A())
        elif '2018B' in options['dataset']:
            modules.append(jetRecalib2018B())
        elif '2018C' in options['dataset']:
            modules.append(jetRecalib2018C())
        elif '2018D' in options['dataset']:
            modules.append(jetRecalib2018D())
    p=PostProcessor(outputDir=".",
        inputFiles=files,
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

