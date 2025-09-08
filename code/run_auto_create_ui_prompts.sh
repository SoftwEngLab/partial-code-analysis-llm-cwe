#!/bin/bash

BASE_DIR="/Users/ic/Desktop/LLM-as-Static-Proxy-Test"
CWEs=("cwe-078" "cwe-190" "cwe-416" "cwe-476")
#CWEs=("cwe-476")
#TEMPLATES=("exp_0_1.txt" "exp_0_2.txt" "exp_15.txt" "exp_15_2.txt" "exp_16.txt" "exp_17.txt" "exp_17_inherent.txt" "exp_18.txt")
TEMPLATES=("exp_25.txt")
FUNCTION_SOURCES=("func_src_before" "func_src_after")

for CWE in "${CWEs[@]}"; do
    for TEMPLATE in "${TEMPLATES[@]}"; do
        JSONL_FILE_PATH="${BASE_DIR}/raw_data/${CWE}.jsonl"
        TEMPLATE_FILE_PATH="${BASE_DIR}/templates/${CWE}/${TEMPLATE}"
        EXPERIMENT_FILE_PATH="${BASE_DIR}/testing_experiments/${CWE}/${TEMPLATE}"

        for FUNC_SRC in "${FUNCTION_SOURCES[@]}"; do
            python auto_create_ui_prompts.py "$JSONL_FILE_PATH" "$TEMPLATE_FILE_PATH" "$EXPERIMENT_FILE_PATH" "$FUNC_SRC"
        done
    done
done
