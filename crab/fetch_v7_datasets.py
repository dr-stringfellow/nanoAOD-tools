import subprocess
import os
import re
import sys
from pprint import pprint

def dump_v7_datasets(v5file, year):
    outputfile = './datasets_v7_{}.txt'.format(year)
    lines_for_v7 = []
    campaign = 'Fall17' if int(year) == 2017 else 'Autumn18'
    with open(v5file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            if not line.startswith('/'):
                lines_for_v7.append(line)
            else:
                dataset_name_to_search = line.split('/')[1]
                if re.match('MET|Single(Photon|Electron|Muon).*', dataset_name_to_search):
                    cmd = ['dasgoclient', '-query', 'dataset=/{}*/Run{}*02Apr2020*/NANOAOD'.format(dataset_name_to_search, year)]
                else:
                    cmd = ['dasgoclient', '-query', 'dataset=/{}*/*RunII{}NanoAODv7*/NANOAODSIM'.format(dataset_name_to_search, campaign)]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stdout, stderr = proc.communicate()
                lines_for_v7.append(stdout)
    
    # Dump the v7 datasets to new file
    with open(outputfile, 'w+') as f:
        f.write('\n'.join(lines_for_v7))

def main():
    year = sys.argv[1]
    v5file = './datasets_{}.txt'.format(year)

    dump_v7_datasets(v5file, year)

if __name__ == '__main__':
    main()

