submit_dataset_list(){
    LIST=${1}
    touch submitted.txt
    while read DS; do
        if [[ $DS = \#* ]]; then
            continue
        elif [ -z "${DS}" ]; then
            continue
        fi

        if [ $(grep -c "$DS" submitted.txt) -gt 0 ]; then 
            # echo "Dataset was already submitted. Skipping $DS."
            continue
        fi
        crab submit crab_cfg.py Data.inputDataset=${DS}
        code=$?
        if [ $code -eq 0 ]; then
            echo $DS >> submitted.txt
        fi
    done < $LIST
}

submit_dataset_list "/afs/cern.ch/work/a/aalbert/public/2019-06-07_monojetcoffea/bucoffea/bucoffea/data/datasets/datasets_2018.txt"
submit_dataset_list "/afs/cern.ch/work/a/aalbert/public/2019-06-07_monojetcoffea/bucoffea/bucoffea/data/datasets/datasets_2017.txt"
