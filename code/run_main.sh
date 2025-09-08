
#!/bin/bash
 
BASE_DIR="/Users/ic/Desktop/LLM-as-Static-Proxy-Test/experiments_latest"

 
if [ "$#" -ge 3 ]; then
  MODEL_NAME="$3"
elif [ "$#" -eq 2 ]; then
  MODEL_NAME="o1" 
elif [ "$#" -eq 1 ]; then
  echo "Usage: $0 [CWE_FOLDER] [EXP_FOLDER] [MODEL_NAME]"
  echo "If no arguments are provided, it will process all CWE and experiment folders with default model 'o1'."
  exit 1
else
  MODEL_NAME="o1" 
fi

 
run_experiment() {
  local DIR=$1
  echo "Running model $MODEL_NAME for $DIR"

  if [[ "$MODEL_NAME" == deepseek-ai/* ]]; then
    python run_openai.py "$DIR" --model "$MODEL_NAME" --temperature 0.7 --trial 0
  elif [[ "$MODEL_NAME" == bedrock/* ]]; then
    python run_bedrock.py "$DIR" --model "$MODEL_NAME" --temperature 0.7 --trial 0
  else
    python run_openai.py "$DIR" --model "$MODEL_NAME" --temperature 0.7 --trial 0
  fi
}

 
process_experiment() {
  local CWE_FOLDER=$1
  local EXPERIMENT_FOLDER=$2

 
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
}

 
if [ "$#" -ge 2 ]; then
  CWE_FOLDER="$BASE_DIR/$1"
  EXP_FOLDER="$CWE_FOLDER/$2"
  process_experiment "$CWE_FOLDER" "$EXP_FOLDER"
else
 
  for CWE_FOLDER in "$BASE_DIR"/*; do
    if [ -d "$CWE_FOLDER" ]; then
      echo "Entering CWE folder: $CWE_FOLDER"

      for EXPERIMENT_FOLDER in "$CWE_FOLDER"/*; do
        if [ -d "$EXPERIMENT_FOLDER" ]; then
          process_experiment "$CWE_FOLDER" "$EXPERIMENT_FOLDER"
        else
          echo "Skipping non-directory: $EXPERIMENT_FOLDER"
        fi
      done
    else
      echo "Skipping non-directory: $CWE_FOLDER"
    fi
  done
fi
