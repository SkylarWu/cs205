import argparse
from util import load_labeled_txt, loocv
from search_algor import forward_selection, backward_elimination


# find best in every level
def best_in_level(level_history):
    return max(level_history, key=lambda x: x[1])  # (features, acc)

# find best among all level
def best_overall(history):
    return max((item for level in history for item in level), key=lambda x: x[1])


def print_history(total_feature, data, history, final_features, final_acc):
    print(f"Dataset info: {total_feature} features, {len(data)} instances.")
    
    all_features_acc = loocv(data, list(range(total_feature)))
    print(f"  - Without any search algorithm, the baseline is {all_features_acc * 100:.2f}%\n")

    for level, level_history in enumerate(history, start=1):
        level_selection = best_in_level(level_history)
        print(f"On level {level} of the search tree, {level_selection} is best")
        for features, acc in level_history:
            feature_str = ','.join(str(f + 1) for f in features)
            print(f"    Using feature(s) {{{feature_str}}} accuracy is {acc * 100:.2f}%")

    best_global = best_overall(history)
    print(f"\nBest feature(s): {{{','.join(str(f+1) for f in best_global[0])}}} with accuracy {best_global[1] * 100:.2f}%\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CS205 Feature Selection using 1-NN + LOOCV")
    parser.add_argument('--file', type=str, required=True, help='Path to input data file')
    parser.add_argument('--method', type=str, choices=['forward', 'backward'], default='forward', help='Search method to use')
    args = parser.parse_args()

    # Load data
    data = load_labeled_txt(args.file)
    total_feature = len(data[0][0])

    # Run search
    if args.method == 'forward':
        selected, acc, history = forward_selection(data, total_feature)
    else:
        selected, acc, history = backward_elimination(data, total_feature)

    # Print result
    print_history(total_feature, data, history, selected, acc)
