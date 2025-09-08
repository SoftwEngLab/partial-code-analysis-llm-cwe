#!/bin/bash

# Usage: ./run_create_plots.sh <results_dir> <plot_script_path>
# Example: ./run_create_plots.sh "/Users/ic/Desktop/LLM-as-Static-Proxy-Test/trial_results" ./plot_average_performance.py

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

 
SANITIZED_MODELS=()
for MODEL in "${MODELS[@]}"; do
    SANITIZED_MODELS+=("$(sanitize_model_name "$MODEL")")
done

 
SANITIZED_MODELS_STR="${SANITIZED_MODELS[*]}"

 
if [[ -d "$RESULTS_DIR" ]]; then
    echo "Generating plots using results from: $RESULTS_DIR"
    echo "Processing models: ${SANITIZED_MODELS_STR}"
    
 
    python "$PLOT_SCRIPT" "$RESULTS_DIR" ${SANITIZED_MODELS_STR}
    
    echo "Plots have been generated in $PLOTS_DIR."
else
    echo "Results directory does not exist: $RESULTS_DIR"
    exit 1
fi



 

 
 

 
 

 
 

 
 
 

 
 
 
 
 
 
 
 
 
