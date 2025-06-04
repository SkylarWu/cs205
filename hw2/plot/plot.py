import re
import numpy as np

import sys
import matplotlib.pyplot as plt

def parse_accuracy_file(filename):
    feature_sets = []
    accuracies = []

    pattern = re.compile(r"Using feature\(s\) \{([0-9,]+)\} accuracy is ([0-9.]+)%")

    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                feature_str = "{" + match.group(1) + "}"
                accuracy = float(match.group(2))
                feature_sets.append(feature_str)
                accuracies.append(accuracy)

    return feature_sets, accuracies

def plot_bar_chart(features, accs, title):
    plt.figure(figsize=(10, 6))
    plt.bar(features, accs)
    #plt.xticks(rotation=45, ha='right')
    plt.xticks(ticks=np.arange(len(features))[::5], labels=[features[i] for i in range(0, len(features), 5)], rotation=45, ha='right')

    plt.xlabel("Feature Set")
    plt.ylabel("Accuracy (%)")
    plt.title(title)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_accuracy.py <input_file> [chart_title]")
        sys.exit(1)

    filename = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) >= 3 else "Feature Set vs. Accuracy"

    features, accs = parse_accuracy_file(filename)
    plot_bar_chart(features, accs, title)

