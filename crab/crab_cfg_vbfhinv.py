
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

import sys

def get_dataset():
    # Parse dataset from commandline
    # Stolen from https://gitlab.cern.ch/nsmith/monoZ/blob/master/crab/crab.py
    dataset = 'dummy'
    for arg in sys.argv:
        if 'Data.inputDataset=' in arg:
            dataset = arg.split('=')[1]
    if dataset == 'dummy':
        raise Exception("Must pass dataset argument as Data.inputDataset=...")
    return dataset


def base_configuration():
    config = Configuration()

    config.section_("General")
    config.General.transferLogs=True
    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe = 'crab_script.sh'
    config.JobType.inputFiles = ['crab_script.py','keep_and_drop_vbf_hinv.txt','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
    config.JobType.sendPythonFolder	 = True
    config.section_("Data")
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 2
    config.Data.totalUnits = 10

    config.Data.publication = False
    config.section_("Site")
    config.Site.storageSite = "T2_DE_RWTH"

    return config

tag = "test_v1"
dataset = get_dataset()

config = base_configuration()

dataset_simplified = dataset.split("/")[1]
config.General.requestName = "nano_post_{0}_{1}".format(tag, dataset_simplified)
config.Data.inputDataset = dataset
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10
config.Data.outputDatasetTag = tag
config.Data.outLFNDirBase = '/store/user/{0}/NanoPost/{1}/'.format(getUsernameFromSiteDB(), tag)


config.General.workArea = "./wdir/{}".format(tag)
config.JobType.allowUndistributedCMSSW = True