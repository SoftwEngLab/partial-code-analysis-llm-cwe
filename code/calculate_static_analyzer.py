import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def read_files_from_directory(directory_path):

    try:
        return {f for f in os.listdir(directory_path) if not f.startswith('.')}
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return set()

def read_json_results(json_file):

    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
 
        return {finding['vulnerability']['filePath']['path'] for finding in data.get('findings', [])}
    except FileNotFoundError:
        print(f"File not found: {json_file}")
        return set()
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return set()

def compute_metrics(before_files, after_files, predicted_paths):

    tp = sum('func_src_before' in path for path in predicted_paths)
    fp = sum('func_src_after' in path for path in predicted_paths)
    fn = len(before_files) - tp
    tn = len(after_files) - fp

    total = tp + fp + fn + tn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return accuracy, precision, recall, f1, tp, fp, tn, fn

def compute_pairwise_accuracy(before_files, after_files):

    if not before_files:
        return 0
    correct_pairs = sum(1 for filename in before_files if filename not in after_files)
    return correct_pairs / len(before_files)

 
base_path = "/Users/ic/Desktop/LLM-as-Static-Proxy-Test"
cwe_dir = os.path.join(base_path, "raw_data_static_analyzer")
scan_dir = os.path.join(base_path, "static_analyzer_scans")

results = {}
 
cwe_directories = [d for d in os.listdir(cwe_dir) if os.path.isdir(os.path.join(cwe_dir, d))]

for cwe in cwe_directories:
    print(f"Processing CWE {cwe}")

 
    path_before = os.path.join(cwe_dir, cwe, 'func_src_before')
    path_after = os.path.join(cwe_dir, cwe, 'func_src_after')

    before_files = read_files_from_directory(path_before)
    after_files = read_files_from_directory(path_after)

 
    print(f"  Number of files in func_src_before: {len(before_files)}")
    print(f"  Number of files in func_src_after: {len(after_files)}")

 
    json_files = [os.path.join(scan_dir, f) for f in os.listdir(scan_dir)
                  if f.startswith(cwe) and f.endswith('.json')]
    predicted_paths = set()
    for json_file in json_files:
        predicted_paths.update(read_json_results(json_file))

 
    accuracy, precision, recall, f1, tp, fp, tn, fn = compute_metrics(before_files, after_files, predicted_paths)
    pairwise_accuracy = compute_pairwise_accuracy(before_files, after_files)

 
    results[cwe] = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1,
        'True Positives': tp,
        'False Positives': fp,
        'True Negatives': tn,
        'False Negatives': fn,
        'Pairwise Accuracy': pairwise_accuracy,
        'Total Files in func_src_before': len(before_files),
        'Total Files in func_src_after': len(after_files)
    }

print("\nResults Summary:")
for cwe, metrics in results.items():
    print(f"CWE {cwe}:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    print() 
