#!/bin/sh

TMP_DIR=$(mktemp)
EV_HAM="$TMP_DIR/ev_ham"
EV_SPAM="$TMP_DIR/ev_spam"
TR_HAM="$TMP_DIR/tr_ham"
TR_SPAM="$TMP_DIR/tr_spam"
TR_DATA="$TMP_DIR/tr_data"

PYTHON="python"
SPLITTER="$PYTHON splitter.py"
TRAINER="$PYTHON trainer.py"
EVALUATOR="$PYTHON evaluator.py"

ev_perc=0.25
tr_perc=0.75
token="basic"
umbral=0.9

while getopts "e:t:k:u:" opt; do
	case $opt in
	e)
		ev_perc=$OPTARG
		;;
	t)
		tr_perc=$OPTARG
		;;
	k)
		token=$OPTARG
		;;
	u)
		umbral=$OPTARG
		;;
	esac
done

mkfifo $EV_HAM
mkfifo $EV_SPAM
mkfifo $TR_HAM
mkfifo $TR_SPAM
mkfifo $TR_DATA

$SPLITTER -e$ev_perc -t$tr_perc -d$DATA_DIR $EV_HAM $EV_SPAM $TR_HAM $TR_SPAM &\
$TRAINER -a$TR_HAM -s$TR_SPAM -o$TR_DATA &\
$EVALUATOR -a$EV_HAM -s$EV_SPAM -t$TR_DATA -m

rm -fr $(TMP_DIR) >& /dev/null
