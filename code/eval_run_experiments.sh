#!/bin/bash

 
BASE_DIR="/Users/ic/Desktop/LLM-as-Static-Proxy-Test/experiments_latest"

 
MODELS=("deepseek-ai/DeepSeek-R1-Distill-Qwen-32B" "o1" "deepseek-ai/DeepSeek-R1" "bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0")
 

extract_trial_number() {
  local FILENAME=$1
  local TRIAL_NUM=""

  if [[ "$FILENAME" =~ trial_([0-9]+)\.json$ ]]; then
    TRIAL_NUM="${BASH_REMATCH[1]}"
  fi

  echo "$TRIAL_NUM"
}


sanitize_model_name() {
  local MODEL=$1
  case "$MODEL" in
    "deepseek-ai/DeepSeek-R1")
      echo "deepseek-ai_DeepSeek-R1"
      ;;
    "bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0")
      echo "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0"
      ;;
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
      echo "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B"
      ;;
    "o1")
      echo "o1"
      ;;
    *)
 
 
 
      ;;
  esac
}

run_experiment() {
  local DIR=$1
  for MODEL in "${MODELS[@]}"; do
    CLEAN_MODEL=$(sanitize_model_name "$MODEL")
    echo "Evaluating $DIR with model $CLEAN_MODEL"

 
    EXISTING_FILES=( $(ls "$DIR" | grep -E "output_responses_${CLEAN_MODEL}_temp[0-9.]+_[0-9]+_trial_[0-9]+\.json") )

 
    if [ ${#EXISTING_FILES[@]} -eq 0 ]; then
      EXISTING_FILES=( $(ls "$DIR" | grep -E "output_responses_${CLEAN_MODEL}_temp[0-9.]+_[0-9]+\.json") )
    fi

    if [ ${#EXISTING_FILES[@]} -eq 0 ]; then
      echo "No existing file found for model $CLEAN_MODEL in directory $DIR"
      continue
    fi

    for EXISTING_FILE in "${EXISTING_FILES[@]}"; do
      echo "Processing file: $EXISTING_FILE"

 
      TEMPERATURE=$(echo "$EXISTING_FILE" | sed -n 's/.*_temp\([0-9.]*\)_.*\.json/\1/p')
      TIMESTAMP=$(echo "$EXISTING_FILE" | sed -n 's/.*_\([0-9]*\)\.json/\1/p')
      TRIAL_NUM=$(extract_trial_number "$EXISTING_FILE")

 
      if [[ -n "$TRIAL_NUM" ]]; then
        NEW_FILE_NAME="eval_${CLEAN_MODEL}_temp${TEMPERATURE}_${TIMESTAMP}_trial_${TRIAL_NUM}.json"
      else
        NEW_FILE_NAME="eval_${CLEAN_MODEL}_temp${TEMPERATURE}_${TIMESTAMP}.json"
      fi

 
      if [ -f "$DIR/$NEW_FILE_NAME" ]; then
        echo "Evaluation file $NEW_FILE_NAME already exists. Skipping evaluation."
        continue
      fi

 
      echo "RUNNING eval_api_results.py $DIR/$EXISTING_FILE $DIR/$NEW_FILE_NAME"
      python eval_api_results.py "$DIR/$EXISTING_FILE" "$DIR/$NEW_FILE_NAME"
    done
  done
}

 
for CWE_FOLDER in "$BASE_DIR"/cwe-*; do
 
  if [ -d "$CWE_FOLDER" ]; then
    echo "Entering CWE folder: $CWE_FOLDER"
 
    for EXPERIMENT_FOLDER in "$CWE_FOLDER"/*; do
 
      if [ -d "$EXPERIMENT_FOLDER" ]; then
        echo "Entering experiment folder: $EXPERIMENT_FOLDER"
 
        FUNC_SRC_BEFORE_DIR="$EXPERIMENT_FOLDER/func_src_before"
        FUNC_SRC_AFTER_DIR="$EXPERIMENT_FOLDER/func_src_after"

 
        if [ -d "$FUNC_SRC_BEFORE_DIR" ]; then
          echo "Found func_src_before directory: $FUNC_SRC_BEFORE_DIR"
          run_experiment "$FUNC_SRC_BEFORE_DIR"
        else
          echo "func_src_before directory not found: $FUNC_SRC_BEFORE_DIR"
        fi

 
        if [ -d "$FUNC_SRC_AFTER_DIR" ]; then
          echo "Found func_src_after directory: $FUNC_SRC_AFTER_DIR"
          run_experiment "$FUNC_SRC_AFTER_DIR"
        else
          echo "func_src_after directory not found: $FUNC_SRC_AFTER_DIR"
        fi
      else
        echo "Experiment folder not found or is not a directory: $EXPERIMENT_FOLDER"
      fi
    done
  else
    echo "CWE folder not found or is not a directory: $CWE_FOLDER"
  fi
done
