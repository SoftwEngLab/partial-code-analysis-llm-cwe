#!/bin/bash

# Usage: ./run_eval_analysis.sh <cwe_list> <experiment_list> <model_name> <python_script_path> <trial_number>
# Example: ./run_eval_analysis.sh "cwe-078,cwe-190" "exp_16,exp_17" "gpt-4" ./analyze_results.py 1

CWE_LIST=$1
EXP_LIST=$2
MODEL_NAME=$3
PYTHON_SCRIPT=$4
TRIAL_NUMBER=$5

 
IFS=',' read -ra CWE_ARRAY <<< "$CWE_LIST"
IFS=',' read -ra EXP_ARRAY <<< "$EXP_LIST"

EXPERIMENTS_DIR="/Users/ic/Desktop/LLM-as-Static-Proxy-Test/experiments_latest"
RESULTS_DIR="/Users/ic/Desktop/LLM-as-Static-Proxy-Test/trial_results"

 
mkdir -p $RESULTS_DIR

for CWE in ${CWE_ARRAY[@]}; do
    for EXP in ${EXP_ARRAY[@]}; do
        FUNC_SRC_BEFORE_PATH="${EXPERIMENTS_DIR}/${CWE}/${EXP}/func_src_before/eval_${MODEL_NAME}_temp*_trial_${TRIAL_NUMBER}.json"
        FUNC_SRC_AFTER_PATH="${EXPERIMENTS_DIR}/${CWE}/${EXP}/func_src_after/eval_${MODEL_NAME}_temp*_trial_${TRIAL_NUMBER}.json"
        
 
        BEFORE_FILE=$(ls $FUNC_SRC_BEFORE_PATH 2>/dev/null | head -n 1)
        AFTER_FILE=$(ls $FUNC_SRC_AFTER_PATH 2>/dev/null | head -n 1)

        if [[ -f $BEFORE_FILE && -f $AFTER_FILE ]]; then
            echo "Processing: $CWE, $EXP"
            echo "Before file: $BEFORE_FILE"
            echo "After file: $AFTER_FILE"

 
            OUTPUT_FILE="${RESULTS_DIR}/${CWE}_${EXP}_${MODEL_NAME}_temp*_trial_${TRIAL_NUMBER}_metrics.txt"

 
            python $PYTHON_SCRIPT $BEFORE_FILE $AFTER_FILE $OUTPUT_FILE
            echo "Metrics saved to: $OUTPUT_FILE"
        else
            echo "Missing eval files for $CWE, $EXP"
        fi
    done
done
 