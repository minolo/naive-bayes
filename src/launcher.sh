#!/bin/bash

DATA_DIR="../res/dsets"

TMP_DIR=$(mktemp -d)
EV_HAM="$TMP_DIR/ev_ham"
EV_SPAM="$TMP_DIR/ev_spam"
TR_HAM="$TMP_DIR/tr_ham"
TR_SPAM="$TMP_DIR/tr_spam"
TR_DATA="$TMP_DIR/tr_data"

PYTHON="python3"
SPLITTER="$PYTHON splitter.py"
TRAINER="$PYTHON trainer.py"
EVALUATOR="$PYTHON evaluator.py"

ev_perc=0.20
tr_perc=0.80
token="basic"
threshold=0.1

not_def_parms=()
while getopts "e:t:k:u:" opt; do
	case $opt in
	e)
		ev_perc=$OPTARG
		not_def_parms+=($ev_perc)
		;;
	t)
		tr_perc=$OPTARG
		not_def_parms+=($tr_perc)
		;;
	k)
		token=$OPTARG
		not_def_parms+=($token)
		;;
	u)
		threshold=$OPTARG
		not_def_parms+=($threshold)
		;;
	esac
done

mkfifo $EV_HAM
mkfifo $EV_SPAM
mkfifo $TR_HAM
mkfifo $TR_SPAM
mkfifo $TR_DATA

$SPLITTER -e$ev_perc -t$tr_perc -d$DATA_DIR $EV_HAM $EV_SPAM $TR_HAM $TR_SPAM &\
$TRAINER -a$TR_HAM -s$TR_SPAM -o$TR_DATA -t$token&\
cmat=$($EVALUATOR -a$EV_HAM -s$EV_SPAM -d$TR_DATA -m -u$threshold)

echo "${not_def_parms[@]};$cmat"

rm -fr $TMP_DIR >& /dev/null
