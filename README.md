# Partial Code Analysis with LLM-Based CWE-Specific Rules

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_16,exp_17" "mistral-large@2407" ./analyze_results.py


bash run_main.sh

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_16,exp_17" "us.meta.llama3-1-70b-instruct-v1:0" ./analyze_results.py

(nlp) partial-code-analysis-llm-cwe/code % bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "mistral-large@2407" ./analyze_results.py


bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "mistral-large@2407" ./analyze_results.py

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "us.meta.llama3-1-70b-instruct-v1:0" ./analyze_results.py

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py


bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0


bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0


bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py 2


bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py 2

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py 2

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1-Distill-Qwen-32B" ./analyze_results.py 3

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 1


bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 1


# 190
bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 3

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 5


bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 4
---^ seed = 567

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

#190 retry
bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 2

#190 claude
bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-190" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 2

# 78

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 4
---^ seed = 567

-- claude
bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 2

--- o1
bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-078" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 2


# 416 
bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 4
---^ seed = 567
bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 5

-- o1
bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 2


bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-416" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 1


# 476  
--- deepseek-r1


bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 2
^ not sure if i passed the temperature parameter here


bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 3

^ trying with 0.6 temp passed

(nlp) partial-code-analysis-llm-cwe/code % bash run_eval_analysis.sh "cwe-476" "exp_17" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 6 

(nlp) partial-code-analysis-llm-cwe/code % bash run_eval_analysis.sh "cwe-476" "exp_17" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 7

---- claude

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 2

---- o1
bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 1

bash run_eval_analysis.sh "cwe-476" "exp_0_1,exp_0_2,exp_15,exp_15_2,exp_16,exp_17,exp_17_inherent,exp_18" "o1" ./analyze_results.py 2



# So You've Made a Mistake!

Remember to set OpenAI API key:
(nlp) partial-code-analysis-llm-cwe/code % export OPENAI_API_KEY=sk-proj-

Delete the mistakes "ERROR" eval files:
(nlp) partial-code-analysis-llm-cwe/code % find experiments_latest/cwe-416 -type f -name "eval_bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0_temp0.5_1_trial_1.json" -delete

find experiments_latest/cwe-078 -type f -name "eval_bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0_temp0.5_2_trial_2.json" -delete

# Create eval_ files
(nlp) partial-code-analysis-llm-cwe/code % bash eval_run_experiments.sh --> this is what goes through all the output responses and creates eval files

# Create Plots

# Example:

bash run_create_plots.sh "partial-code-analysis-llm-cwe/data/trial_results" ./plot_average_performance_all.py

# indiviudal model plot
(nlp) partial-code-analysis-llm-cwe/code % bash run_create_plots.sh "partial-code-analysis-llm-cwe/data/trial_results" ./plot_results.py 


# for Generic CoT 
bash run_eval_analysis.sh "cwe-078" "exp_25" "bedrock_us.anthropic.claude-3-5-sonnet-20241022-v2:0" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-416" "exp_25" "o1" ./analyze_results.py 0

bash run_eval_analysis.sh "cwe-078" "exp_25" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 5

bash run_eval_analysis.sh "cwe-476" "exp_25" "deepseek-ai_DeepSeek-R1" ./analyze_results.py 7