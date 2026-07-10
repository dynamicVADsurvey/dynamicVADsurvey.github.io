# Evaluation Metrics

Frame-level AUC remains common, but it compresses temporal behavior into one ranking statistic. Average precision, event-level measures, localization overlap, and language-generation metrics answer different questions.

## Protocol before score

Every benchmark value should identify its dataset, metric, evaluation protocol, source, verification status, and comparability. Values with different feature extraction, sampling, labels, or post-processing should not be treated as a single leaderboard.

## Language-aware evaluation

Explanation and question-answering systems require semantic evaluation alongside detection performance. Automated language metrics should be paired with human or task-grounded validation where possible.
