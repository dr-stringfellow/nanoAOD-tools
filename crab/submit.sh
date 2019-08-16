SUBMITFILE="./wdir/10Aug19/submitted.txt"

submit_dataset_list(){
    LIST=${1}
    touch $SUBMITFILE
    while read DS; do
        echo $DS
        if [[ $DS = \#* ]]; then
            continue
        elif [ -z "${DS}" ]; then
            continue
        fi

        if [ $(grep -c "$DS" $SUBMITFILE) -gt 0 ]; then
            # echo "Dataset was already submitted. Skipping $DS."
            continue
        fi
        crab submit crab_cfg.py Data.inputDataset=${DS}
        code=$?
        if [ $code -eq 0 ]; then
            echo $DS >> $SUBMITFILE
        fi
        # break
    done < $LIST
}

submit_dataset_list "datasets_2017.txt"
submit_dataset_list "datasets_2018.txt"
