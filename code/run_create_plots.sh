#!/bin/bash

# Usage: ./run_create_plots.sh <results_dir> <plot_script_path>
# Example: ./run_create_plots.sh "/Users/ic/Desktop/LLM-as-Static-Proxy-Test/trial_results" ./plot_results.py

RESULTS_DIR=$1
PLOT_SCRIPT=$2

 
mkdir -p "$RESULTS_DIR"

 
PLOTS_DIR="${RESULTS_DIR}/plots"
mkdir -p "$PLOTS_DIR"

 
sanitize_model_name() {
  case "$1" in
    "deepseek-ai/DeepSeek-R1")
      echo "deepseek-ai_DeepSeek-R1"
      ;;
    "bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0")
      echo "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0"
      ;;
    "o1")
      echo "o1"
      ;;
    *)
 
      echo "${1//[^a-zA-Z0-9_]/_}" 
      ;;
  esac
}

 
MODELS=("o1" "deepseek-ai/DeepSeek-R1" "bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0")

 
if [[ -d "$RESULTS_DIR" ]]; then
    echo "Generating plots using results from: $RESULTS_DIR"
    for MODEL in "${MODELS[@]}"; do
        MODEL_NAME=$(sanitize_model_name "$MODEL")
        echo "Processing model: $MODEL_NAME"
 
        python $PLOT_SCRIPT $RESULTS_DIR $MODEL_NAME
    done
    echo "Plots have been generated in $PLOTS_DIR."
else
    echo "Results directory does not exist: $RESULTS_DIR"
fi
