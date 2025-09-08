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

def plot_metrics(results, cwe, model_type, output_dir):
    experiment_labels = {
        'exp_0_1': 'B', 'exp_0_2': 'NL (S0)', 'exp_15': 'NL(S1)', 'exp_15_2': 'NL(S2)',
        'exp_16': 'NL(S3)', 'exp_25': 'NL+CoT(S0)', 'exp_17_inherent': 'NL+CoT(S1)', 'exp_17': 'NL+CoT(S2)',
        'exp_18': 'NL+CoT(S3)'
    }

    experiments = sorted(results.keys(), key=lambda x: experiment_labels[x])
    labels = [experiment_labels[exp] for exp in experiments]
    overall_acc = [np.mean(results[exp]['Overall Accuracy']) for exp in experiments]
    pairwise_acc = [np.mean(results[exp]['Pairwise Accuracy']) for exp in experiments]
    f1_scores = [np.mean(results[exp]['F1 Score']) for exp in experiments]

 
    fig_width = max(12, len(experiments) * 1.5)
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    width = 0.25 
    x = np.arange(len(experiments))

    rects1 = ax.bar(x - width, overall_acc, width, label='Overall Acc.', color='blue', alpha=0.7)
    rects2 = ax.bar(x, pairwise_acc, width, label='Pairwise Acc.', color='darkorange', alpha=0.7)
    rects3 = ax.bar(x + width, f1_scores, width, label='F1 Score', color='green', alpha=0.7)

 
    add_value_labels(ax, rects1, offset=5, color='black') 
    add_value_labels(ax, rects2, offset=10, color='#D35400', fontweight='bold', fontsize=12, highlight=True) 
    add_value_labels(ax, rects3, offset=5, color='green') 

    ax.axhline(y=50, color='gray', linestyle='--', linewidth=1)
    ax.set_ylabel('Scores (%)', fontsize=12)
    ax.set_title(f'Metrics Comparison for {cwe} Using {model_type}', fontsize=14, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)

 
    ax.legend(fontsize=11, loc='upper left', bbox_to_anchor=(1, 1), frameon=True)

 
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plot_path = os.path.join(output_dir, f'{cwe}_{model_type}_metrics_comparison.png')
    plt.savefig(plot_path, bbox_inches='tight', dpi=300) 
    plt.close()

def main(directory, model_name):
    """ Reads metric files and generates plots. """
    output_dir = os.path.join(directory, 'plots')
    os.makedirs(output_dir, exist_ok=True)

    pattern = re.compile(
        f"cwe-(\\d+)_exp_(0_1|0_2|15|15_2|16|17|17_inherent|18|25)_{re.escape(model_name)}_.*_metrics\\.txt$"
    )
    results = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt') and (match := pattern.search(file)):
                cwe, exp = f'cwe-{match.group(1)}', f'exp_{match.group(2)}'
                results.setdefault(cwe, {}).setdefault(exp, {'Overall Accuracy': [], 'Pairwise Accuracy': [], 'F1 Score': []})
                metrics = read_metrics(os.path.join(root, file))
                for key in metrics:
                    results[cwe][exp][key].append(metrics[key])

    for cwe, exp_data in results.items():
        plot_metrics(exp_data, cwe, model_name, output_dir)
        print(f"Plot generated for {cwe} using model {model_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plot_results.py <results_directory> <model_name>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

