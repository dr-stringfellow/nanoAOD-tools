
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
    return dataset

def pretty_dataset_name(dataset, is_mc):
    ### Prettify data set name
    dataset_simplified, conditions = dataset.split("/")[1:3]

    if is_mc:
        # Attach short campaign identifier
        for campaign in ["RunIIFall17", "RunIIAutumn18"]:
            if campaign in conditions:
                dataset_simplified = "{}_{}".format(campaign, dataset_simplified)

        # Check if extension
        m = re.match(".*(ext\d+)", conditions);
        if m:
            groups = m.groups()
            assert len(groups) == 1
            dataset_simplified = "{}_{}".format(dataset_simplified, groups[0])
    else:
        m = re.match("(Run\d+[A-Z])", conditions)
        if m:
            groups = m.groups()
            assert len(groups) == 1
            dataset_simplified = "{}_{}".format(dataset_simplified, groups[0])

    return dataset_simplified

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
    config.Site.storageSite = "T2_DE_RWTH"

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
dataset = get_dataset()

config = base_configuration()


### Determine what to do based on type of dataset
is_mc = dataset.endswith("SIM")
if is_mc:
    crab_script = 'crab_script_vbfhinv.py'
elif "Run2017" in dataset:
    crab_script = 'crab_script_vbfhinv_data17.py'
    config.JobType.inputFiles.append("input/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt")
elif "Run2018" in dataset:
    crab_script = 'crab_script_vbfhinv_data18.py'
else:
    raise RuntimeError("Could not deduce what CRAB script to use for dataset: '{}'".format(dataset))

config.JobType.inputFiles.append(crab_script)

dataset_simplified = pretty_dataset_name(dataset, is_mc)

# Pass the dataset name as an argument so that
# the script can write it into the output files.
config.JobType.scriptArgs = ["dataset={}".format(dataset_simplified)]

config.General.requestName = cut_string("nano_post_{0}_{1}".format(tag, dataset_simplified))
config.Data.inputDataset = dataset
config.Data.unitsPerJob = 1

if "test" in tag:
    config.Data.totalUnits = 1
else:
    config.Data.totalUnits = -1

config.Data.outputDatasetTag = dataset_simplified
config.Data.outLFNDirBase = '/store/user/{0}/NanoPost/{1}/{2}'.format(getUsernameFromSiteDB(),
                                                                          tag,
                                                                          "MC" if is_mc else "Data")


config.General.workArea = "./wdir/{}".format(tag)
config.JobType.allowUndistributedCMSSW = True
