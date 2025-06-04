from util import loocv


def forward_selection(data, total_feature):
    selected = []
    left = list(range(total_feature))
    best_accuracy = 0.0
    history = []

    while left:
        level_history = []
        best_feature = None
        best_feature_acc = 0.0

        for feature in left:
            test_feature = selected + [feature] # adding this feature
            acc = loocv(data, test_feature)  # Evaluate using LOOCV

            level_history.append((test_feature[:], acc))

            if acc > best_feature_acc:
                best_feature = feature
                best_feature_acc = acc

        history.append(level_history)  # Save this level's test results

        # if a better feature was found, keep it and continue
        if best_feature is not None and best_feature_acc > best_accuracy:
            selected.append(best_feature)
            left.remove(best_feature)
            best_accuracy = best_feature_acc
        else:
            break

    return selected, best_accuracy, history


def backward_elimination(data, total_features):
    selected = list(range(total_features))
    best_accuracy = loocv(data, selected)
    history = [[(selected[:], best_accuracy)]]

    while len(selected) > 1:
        level_history = [] # stores all feature combinations tested at this level
        worst_feature = None
        best_feature_acc = 0.0

        for feature in selected:
            test_feature = [f for f in selected if f != feature] # removing this feature
            acc = loocv(data, test_feature)

            level_history.append((test_feature[:], acc))

            if acc > best_feature_acc:
                worst_feature = feature
                best_feature_acc = acc

        history.append(level_history)

        # if accuracy improves, remove the feature
        if best_feature_acc > best_accuracy:
            selected.remove(worst_feature)
            best_accuracy = best_feature_acc
        else:
            break

    return selected, best_accuracy, history

