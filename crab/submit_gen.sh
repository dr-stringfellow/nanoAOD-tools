TAG=$(grep ^tag crab_cfg_gen.py | sed "s|.*= *||g;s|\"||g")
SUBMITFILE="./wdir/gen/${TAG}/submitted.txt"
mkdir -p $(dirname $SUBMITFILE)
submit_dataset_list(){
    LIST=${1}
    sed -i  -e '$a\' ${LIST}
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
        crab submit crab_cfg_gen.py Data.inputDataset=${DS}
        code=$?
        if [ $code -eq 0 ]; then
            echo $DS >> $SUBMITFILE
        fi
    done < $LIST
}

submit_dataset_list "datasets_gen.txt"
