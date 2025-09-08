import json
import os
import sys
from sklearn.metrics import f1_score

def analyze_eval_file(eval_file_path):
    """
    Analyze the evaluation JSON file and report results.
    """
    try:
        with open(eval_file_path, 'r') as f:
            eval_data = json.load(f)
    except Exception as e:
        print(f"Error reading file {eval_file_path}: {e}")
        return None
    
    return eval_data

def calculate_accuracy(eval_data_before, eval_data_after):
    """
    Calculate the overall accuracy.
    """
    vulnerable_before = sum(1 for result in eval_data_before.values() if result == "vulnerable")
    non_vulnerable_after = sum(1 for result in eval_data_after.values() if result == "non-vulnerable")
    total_samples = len(eval_data_before) + len(eval_data_after)
    accuracy = (non_vulnerable_after + vulnerable_before) / total_samples if total_samples > 0 else 0
    return accuracy, vulnerable_before, non_vulnerable_after, total_samples

def calculate_pairwise_accuracy(eval_data_before, eval_data_after):
    """
    Calculate the pairwise accuracy.
    """
    correct_pairs = 0
    total_pairs = 0

    for key in eval_data_before:
        if key in eval_data_after:
            total_pairs += 1
            if eval_data_before[key] == "vulnerable" and eval_data_after[key] == "non-vulnerable":
                correct_pairs += 1

    pairwise_accuracy = correct_pairs / total_pairs if total_pairs > 0 else 0
    return pairwise_accuracy, correct_pairs, total_pairs

def calculate_f1_scores(eval_data_before, eval_data_after):
    """
    Calculate F1 scores for vulnerable and non-vulnerable classifications.
    """
    y_true = [(result == "vulnerable") for result in eval_data_before.values()]
    y_pred = [(result == "vulnerable") for result in eval_data_after.values()]
    f1 = f1_score(y_true, y_pred, pos_label=True)
    return f1

def save_results(output_file, results):
    """
    Save the results to the specified output file.
    """
    with open(output_file, 'w') as file:
        file.write(results)

def main():
    if len(sys.argv) != 4:
        print("Usage: python analyze_results.py <before_eval_file> <after_eval_file> <output_file>")
        sys.exit(1)

    before_eval_file = sys.argv[1]
    after_eval_file = sys.argv[2]
    output_file = sys.argv[3]

    before_results = analyze_eval_file(before_eval_file)
    after_results = analyze_eval_file(after_eval_file)
    if before_results is None or after_results is None:
        print("Error analyzing files.")
        sys.exit(1)

    accuracy, vul_before, non_vul_after, total_samples = calculate_accuracy(before_results, after_results)
    pairwise_accuracy, correct_pairs, total_pairs = calculate_pairwise_accuracy(before_results, after_results)
    f1 = calculate_f1_scores(before_results, after_results)

    result_string = f"Results:\n"
    result_string += f"Overall Accuracy: {accuracy * 100:.2f}%\n"
    result_string += f"Pairwise Accuracy: {pairwise_accuracy * 100:.2f}%\n"
    result_string += f"F1 Score: {f1:.2f}\n"
    result_string += f"Vulnerable in Before: {vul_before}, Non-Vulnerable in After: {non_vul_after}\n"
    result_string += f"Total Samples Considered: {total_samples}\n"
    result_string += f"Correct Pairs: {correct_pairs}, Total Pairs: {total_pairs}\n"

    save_results(output_file, result_string)
    print("Results saved to:", output_file)

if __name__ == "__main__":
    main()
