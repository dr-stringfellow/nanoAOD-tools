
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

import md5
import sys
import re

def get_dataset():
    # Parse dataset from commandline
    # Stolen from https://gitlab.cern.ch/nsmith/monoZ/blob/master/crab/crab.py
    dataset = 'dummy'
    for arg in sys.argv:
        if 'Data.inputDataset=' in arg:
            dataset = arg.split('=')[1]
    if dataset == 'dummy':
        raise Exception("Must pass dataset argument as Data.inputDataset=...")

    parts = dataset.split(":")
    assert(len(parts)==2)

    short, long = parts
    return short, long


def base_configuration():
    config = Configuration()

    config.section_("General")
    config.General.transferLogs=True
    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe = 'crab_script.sh'
    config.JobType.inputFiles = ['../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
    config.JobType.sendPythonFolder	 = True
    config.section_("Data")
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1
    # config.Data.totalUnits = 10

    config.Data.publication = False
    config.section_("Site")
    config.Site.storageSite = "T2_CH_CERNBOX"

    return config

# Ensure that the string is not longer than 100 characters
# To comply with the CRAB request name limit
def cut_string(string_in):
    l = len(string_in)
    if l < 100:
        return string_in

    partial_hash = md5.md5(string_in[90:]).hexdigest()
    ret = string_in[:90] + partial_hash[:10]
    return ret


tag = "test_v3"
name, dataset = get_dataset()

config = base_configuration()


### Determine what to do based on type of dataset
is_mc = dataset.endswith("SIM")
crab_script = "crab_script_monojet.py"


if ("Autumn18" in dataset) or ("Run2018" in dataset):
    year=2018
elif ("Run2017" in dataset) or ("Fall17" in dataset):
    year=2017

if not is_mc:
    if year==2017:
        config.JobType.inputFiles.append("input/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt")
    elif year==2018:
        config.JobType.inputFiles.append("input/json/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt")

config.JobType.inputFiles.append(crab_script)
config.JobType.inputFiles.append('keep_and_drop_monojet.txt')

# Pass the dataset name as an argument so that
# the script can write it into the output files.
config.JobType.scriptArgs = ["dataset={}".format(name),
                             "ismc={}".format(is_mc),
                             "year={}".format(year)]

config.General.requestName = cut_string("nano_post_{0}_{1}".format(tag, name))
config.Data.inputDataset = dataset
config.Data.unitsPerJob = 1

if "test" in tag:
    config.Data.totalUnits = 1
else:
    config.Data.totalUnits = -1

config.Data.outputDatasetTag = name
config.Data.outLFNDirBase = '/store/user/{0}/nanopost/{1}/{2}'.format(getUsernameFromSiteDB(),
                                                                          tag,
                                                                          "MC" if is_mc else "Data")


config.General.workArea = "./wdir/{}".format(tag)
config.JobType.allowUndistributedCMSSW = True
