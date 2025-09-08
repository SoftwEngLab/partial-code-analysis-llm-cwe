import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid") 

def read_metrics(file_path):
    metrics = {}
    with open(file_path, 'r') as file:
        for line in file:
            if 'Overall Accuracy:' in line:
                metrics['Overall Accuracy'] = float(line.split(':')[1].strip().strip('%'))
            elif 'Pairwise Accuracy:' in line:
                metrics['Pairwise Accuracy'] = float(line.split(':')[1].strip().strip('%'))
            elif 'F1 Score:' in line:
                metrics['F1 Score'] = float(line.split(':')[1].strip()) * 100 
    return metrics

def add_value_labels(ax, rects, offset=5, color='black', fontweight='normal', fontsize=11, highlight=False):
    for rect in rects:
        height = rect.get_height()
        x_pos = rect.get_x() + rect.get_width() / 2
        if highlight:
            ax.annotate(f'{height:.1f}%',
                        xy=(x_pos, height),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', fontsize=fontsize, fontweight=fontweight,
                        color=color,
                        bbox=dict(facecolor='white', edgecolor='none', pad=2, alpha=0.9))
        else:
            ax.annotate(f'{height:.1f}%',
                        xy=(x_pos, height),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', fontsize=fontsize, fontweight=fontweight,
                        color=color)

def plot_average_performance(results, output_dir):
    experiment_labels = {
        'exp_0_1': 'B1', 'exp_0_2': 'B2', 'exp_15': 'NL(S1)', 'exp_15_2': 'NL(S2)',
        'exp_16': 'NL(S3)', 'exp_17_inherent': 'NL+CoT(S1)', 'exp_17': 'NL+CoT(S2)',
        'exp_18': 'NL+CoT(S3)'
    }
    avg_results = {exp: {'Overall Accuracy': [], 'Pairwise Accuracy': [], 'F1 Score': []} for exp in experiment_labels.keys()}
    for cwe in results.values():
        for exp, metrics in cwe.items():
            if exp in avg_results:
                avg_results[exp]['Overall Accuracy'].append(np.mean(metrics['Overall Accuracy']))
                avg_results[exp]['Pairwise Accuracy'].append(np.mean(metrics['Pairwise Accuracy']))
                avg_results[exp]['F1 Score'].append(np.mean(metrics['F1 Score']))
    avg_overall_acc = [np.mean(avg_results[exp]['Overall Accuracy']) for exp in experiment_labels]
    avg_pairwise_acc = [np.mean(avg_results[exp]['Pairwise Accuracy']) for exp in experiment_labels]
    avg_f1_scores = [np.mean(avg_results[exp]['F1 Score']) for exp in experiment_labels]
    labels = [experiment_labels[exp] for exp in experiment_labels]
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.25
    x = np.arange(len(experiment_labels))
    rects1 = ax.bar(x - width, avg_overall_acc, width, label='Overall Acc.', color='blue', alpha=0.7)
    rects2 = ax.bar(x, avg_pairwise_acc, width, label='Pairwise Acc.', color='darkorange', alpha=0.7)
    rects3 = ax.bar(x + width, avg_f1_scores, width, label='F1 Score', color='green', alpha=0.7)
    add_value_labels(ax, rects1, offset=5, color='black')
    add_value_labels(ax, rects2, offset=10, color='#D35400', fontweight='bold', fontsize=12, highlight=True)
    add_value_labels(ax, rects3, offset=5, color='green')
    ax.axhline(y=50, color='gray', linestyle='--', linewidth=1)
    ax.set_ylabel('Scores (%)', fontsize=12)
    ax.set_title('Average Performance Across All CWEs and Models', fontsize=14, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)
    ax.legend(fontsize=11, loc='upper left', bbox_to_anchor=(1, 1), frameon=True)
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plot_path = os.path.join(output_dir, 'average_performance.png')
    plt.savefig(plot_path, bbox_inches='tight', dpi=300)
    plt.close()

def main(directory, model_names):
    output_dir = os.path.join(directory, 'plots')
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    for model_name in model_names:
        pattern = re.compile(
            f"cwe-(\\d+)_exp_(0_1|0_2|15|15_2|16|17|17_inherent|18)_{re.escape(model_name)}_.*_metrics\\.txt$"
        )
        seen_trials = set()
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt') and (match := pattern.search(file)):
                    cwe, exp = f'cwe-{match.group(1)}', f'exp_{match.group(2)}'
                    trial_id = f"{cwe}_{exp}_{model_name}"
                    if trial_id not in seen_trials:
                        seen_trials.add(trial_id)
                        results.setdefault(cwe, {}).setdefault(exp, {'Overall Accuracy': [], 'Pairwise Accuracy': [], 'F1 Score': []})
                        metrics = read_metrics(os.path.join(root, file))
                        for key in metrics:
                            results[cwe][exp][key].append(metrics[key])
    plot_average_performance(results, output_dir)
    print("Average performance plot generated.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python plot_average_performance.py <results_directory> <model_name1> <model_name2> ...")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2:])
