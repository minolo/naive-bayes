#!/bin/bash

LAUNCHER="./launcher.sh"

pb() {
	i=$1
	j=$2
	maxi=$3
	maxj=$4
	t=$(($j + $i * $maxj))
	maxt=$(($maxi * $maxj))

	echo -en "\033[k"
	echo -n "[$j/$maxj; $i/$maxi] ["
	for ((ii=0; ii < $maxt; ii++)); do
		if [ $ii -lt $t ]; then
			echo -n "="
		else
			echo -n "-"
		fi
	done
	echo -en "]\n"
}

usage() {
	echo "$1 -t <test_path> [-n <number of repetitions>" >&2
}

# Parse input parameters
while getopts ":t:n:" opt; do
	case $opt in
	t)
		test_path=$OPTARG
		if [ ! -f $test_path ]; then
			echo "ERROR: \"$test_path\" not found"
			exit -1
		fi
		;;
	n)
		nrep=$OPTARG
		;;
	h)
		usage $0
		exit 0
		;;
	\?)
		echo "ERROR: Illegal option -$OPTARG" >&2
		usage $0
		exit -1
		;;
	:)
		usage $0
		exit -1
		;;
	esac
done

if [ -z "$test_path" ]; then
	echo "ERROR: You must specify a test file" >&2
	usage $0
	exit -1
fi

# Outuput file is like input file but with extension ".out"
out_file="${test_path%.*}.out"

# Read test file
args_list=()
while read -r line; do
	args_list+=("$line")
done < $test_path

if [ -z "$nrep" ]; then
	nrep=${args_list[0]}
fi

# Execute tests
results=()
echo
pb 0 0 ${#args_list[@]} $nrep
for ((test = 1; test < ${#args_list[@]}; test++)); do
	for ((rep = 0; rep < nrep; rep++)); do
		results+=("$($LAUNCHER ${args_list[$test]})")
		pb $test $rep ${#args_list[@]} $nrep
	done
done

# Save results
> $out_file
for ((i = 0; i < ${#results[@]}; i++)); do
	echo ${results[$i]} >> $out_file
done
