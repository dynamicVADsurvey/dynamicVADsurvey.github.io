# Evaluation Metrics

The evaluation of VAD systems has evolved alongside the development of the field itself. Early VAD benchmarks primarily focused on measuring anomaly detection performance, emphasizing whether a model could successfully distinguish anomalous events from normal observations. As datasets began providing spatial and temporal annotations, localization-oriented metrics were introduced to assess the ability of models to accurately identify where anomalies occur. More recently, the emergence of video anomaly understanding benchmarks has motivated the adoption of semantic evaluation metrics that assess explanation quality, question answering performance, grounding accuracy, and language-based reasoning capabilities.

Consequently, modern VAD evaluation can be broadly categorized into three groups: detection metrics, localization metrics, and semantic understanding metrics. Detection metrics assess whether anomalous events can be reliably distinguished from normal activities. Localization metrics evaluate the accuracy of spatial and temporal anomaly localization. Semantic understanding metrics measure the ability of models to interpret, explain, and reason about anomalous events through natural language. In the following subsections, we review the most commonly used metrics within each category and discuss their relevance to both conventional VAD systems and emerging MLLM-based approaches.

## A. Detection Metrics

Detection metrics evaluate a model's ability to distinguish anomalous events from normal observations. Given a set of predictions and corresponding ground-truth labels, these metrics assess the quality of anomaly classification at either the frame, clip, or video level. Because anomalous events are typically rare relative to normal activities, VAD datasets often exhibit significant class imbalance. Consequently, metrics that consider performance across multiple decision thresholds are generally preferred over threshold-dependent measures.

**Area Under the ROC Curve (AUC).** Threshold-independent metrics such as ROC-AUC and precision-recall analysis are widely used for imbalanced detection problems because they summarize model behavior across operating points [66], [67]. AUC is the most widely used evaluation metric in VAD. It measures the area under the Receiver Operating Characteristic (ROC) curve, which plots the True Positive Rate (TPR) against the False Positive Rate (FPR) across different decision thresholds. These quantities are defined as

$$TPR = \frac{TP}{TP+FN}, \qquad FPR = \frac{FP}{FP+TN} \qquad (27)$$

where $TP$, $TN$, $FP$, and $FN$ denote the numbers of true positive, true negative, false positive, and false negative frames, respectively. The AUC score is then computed as

$$AUC = \int_0^1 TPR(FPR)\, d(FPR) \qquad (28)$$

An AUC value of 1 indicates perfect frame-level anomaly discrimination, whereas a value of 0.5 corresponds to random guessing. Since AUC evaluates performance across all possible thresholds, it is particularly suitable for highly imbalanced VAD datasets and remains the dominant metric in most benchmark evaluations.

**Average Precision (AP).** AP summarizes the precision-recall curve and is commonly employed when anomalous samples constitute only a small fraction of the dataset [67], [68]. Given anomaly scores for all evaluated frames, clips, or videos, samples are ranked from highest to lowest anomaly confidence. Precision and recall are then computed at each rank position as progressively more samples are treated as positive:

$$Precision_n = \frac{TP_n}{TP_n+FP_n}, \qquad Recall_n = \frac{TP_n}{TP_n+FN_n} \qquad (29)$$

where $TP_n$, $FP_n$, and $FN_n$ are computed after considering the top-$n$ ranked predictions. The AP score is computed as

$$AP = \sum_n (R_n - R_{n-1})P_n \qquad (30)$$

where $P_n$ and $R_n$ denote precision and recall at the $n$-th ranked operating point. Compared with AUC, AP places greater emphasis on correctly retrieving anomalous events and is therefore particularly informative when the positive class is extremely sparse.

**Accuracy.** Accuracy measures the proportion of correctly classified samples after anomaly scores are converted into binary predictions using a fixed decision threshold. Given a threshold $\tau$, the predicted label is defined as

$$\hat{y}_t = \begin{cases} 1, & s_t > \tau, \\ 0, & \text{otherwise.} \end{cases} \qquad (31)$$

Accuracy is then computed as

$$Accuracy = \frac{TP+TN}{TP+TN+FP+FN} \qquad (32)$$

Although accuracy is intuitive and easy to interpret, it is less frequently reported in VAD because it depends strongly on the selected threshold and is prone to manipulation through threshold tuning. This issue is further amplified by the severe class imbalance present in many anomaly detection datasets. A model may achieve high accuracy simply by predicting most samples as normal while failing to detect anomalous events. For this reason, threshold-independent metrics such as AUC and ranking-based metrics such as AP are generally preferred.

**Equal Error Rate (EER).** EER is defined as the operating point on the ROC curve where the false positive rate equals the false negative rate. It is obtained by varying the decision threshold over anomaly scores and identifying the threshold at which

$$FPR = FNR \qquad (33)$$

where

$$FNR = \frac{FN}{TP+FN} \qquad (34)$$

Lower EER values indicate better detection performance. Unlike accuracy, EER does not depend on a manually selected fixed threshold, but it still summarizes performance at a single operating point. It is occasionally used in VAD benchmarks to compare the balance between missed detections and false alarms.

**Equal Detected Rate (EDR).** EDR measures the proportion of anomalous events successfully detected under a predefined operating condition, such as a fixed false alarm rate, false positive rate, or dataset-specific evaluation protocol. While definitions may vary across benchmarks, EDR generally quantifies detection completeness at a specified operating point. Since it depends on the chosen operating condition, it should be interpreted together with the corresponding threshold or false-alarm constraint. In surveillance applications, where missing a true anomaly may have serious consequences, EDR provides additional insight into the practical effectiveness of a detection system and is often reported alongside EER.

## B. Localization Metrics

While detection metrics evaluate whether a model can distinguish anomalous events from normal activities, they do not assess the accuracy of spatial localization of anomalies. In many practical applications, identifying the spatial and temporal extent of an anomaly is equally important as detecting its presence. Consequently, several localization-oriented metrics have been proposed to evaluate how accurately models identify anomalous regions and trajectories [47]. The Street Scene evaluation protocol introduced region-based and track-based criteria to better account for spatial localization and false-positive regions, rather than only evaluating whether anomalous frames are detected.

**Region-Based Detection Criterion (RBDC).** RBDC evaluates anomaly localization at the level of anomalous regions. Under this criterion, a ground-truth anomalous region is considered detected if its intersection-over-union (IoU) with at least one detected anomalous region is greater than or equal to a predefined threshold $\beta$. Formally, the IoU between a ground-truth region $R_{gt}$ and a detected region $R_{det}$ is defined as

$$IoU(R_{gt}, R_{det}) = \frac{|R_{gt} \cap R_{det}|}{|R_{gt} \cup R_{det}|} \qquad (35)$$

A ground-truth region is counted as detected if

$$IoU(R_{gt}, R_{det}) \geq \beta \qquad (36)$$

The corresponding region-based detection rate (RBDR) is then computed as

$$RBDR = \frac{\text{number of anomalous regions detected}}{\text{total number of anomalous regions}} \qquad (37)$$

RBDR is computed over all ground-truth anomalous regions in all frames of the test set. Unlike frame-level evaluation, this criterion requires spatial overlap between predicted and ground-truth anomalous regions, making it more appropriate for datasets with bounding-box or pixel-level annotations.

**Track-Based Detection Criterion (TBDC).** TBDC evaluates anomaly localization at the object-track or event-track level rather than requiring successful region detection in every frame. Under this criterion, a ground-truth anomalous track is considered detected if at least a fraction $\alpha$ of its ground-truth regions are detected. Each ground-truth region within the track is considered detected when its IoU with a detected region is at least $\beta$.

Formally, let $\mathcal{T}_{gt}$ denote the set of ground-truth anomalous tracks and let $\mathcal{T}_{det}$ denote the subset of ground-truth tracks that satisfy the track-level detection criterion. The track-based detection rate (TBDR) is defined as

$$TBDR = \frac{|\mathcal{T}_{det}|}{|\mathcal{T}_{gt}|} \qquad (38)$$

This criterion reflects the practical observation that an anomaly occurring over many frames does not necessarily need to be localized in every frame to be useful. Instead, the anomalous track should be detected in a sufficient fraction of its temporal extent.

**False Positive Regions per Frame.** Both RBDC and TBDC are evaluated together with the number of false positive regions per frame (FPR) to obtain the Area Under RBDR/TBDR–FPR Curve (AUC). A detected region in a frame is counted as a false positive if its IoU with every ground-truth anomalous region in that frame is less than $\beta$. The false-positive rate is defined as

$$FPR = \frac{\text{total false positive regions}}{\text{total frames}} \qquad (39)$$

This differs from traditional frame-level false-positive counting because multiple false positive regions can occur in a single frame, and false positives can also be counted in frames that contain true anomalies. This provides a more realistic estimate of how many incorrect anomalous regions a human operator would need to inspect.

Localization metrics have become increasingly important as recent datasets provide richer spatial and temporal annotations. For example, Street Scene [47] provides bounding-box annotations with track identifiers, enabling both region-based and track-based evaluation. ComplexVAD similarly provides object-centric annotations that support evaluation through metrics such as RBDC and TBDC. Such metrics are particularly valuable for complex interaction anomalies, where identifying the anomalous object or interaction at the region or track level can be as important as frame-level anomaly scoring.

## C. Semantic Understanding Metrics

The emergence of vision-language models (VLMs) and Multimodal Large Language Models (MLLMs) has expanded the scope of VAD beyond anomaly detection toward anomaly understanding. Modern systems are increasingly expected not only to identify anomalous events, but also to explain why they are anomalous, answer questions about their causes, localize relevant evidence, and generate natural language descriptions. Consequently, evaluation protocols have adopted metrics from natural language processing and multimodal reasoning to assess semantic understanding capabilities. For generated anomaly descriptions and explanations, early automatic evaluation commonly relies on lexical-overlap metrics originally developed for machine translation and summarization [69]-[71].

**BLEU.** BLEU evaluates the similarity between a generated response and one or more reference annotations based on n-gram precision. The BLEU score is computed as

$$BLEU = BP \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right) \qquad (40)$$

where $p_n$ denotes the modified n-gram precision, $w_n$ represents the weight assigned to each n-gram order, and $BP$ is a brevity penalty that penalizes overly short outputs. Higher BLEU scores indicate greater lexical overlap between generated and reference descriptions.

**ROUGE.** ROUGE measures the overlap between generated and reference text from a recall-oriented perspective. For example, ROUGE-N is defined as

$$ROUGE\text{-}N = \frac{\sum \text{N-gram}\ Count_{match}}{\sum \text{N-gram}\ Count_{reference}} \qquad (41)$$

Unlike BLEU, which emphasizes precision, ROUGE focuses on how much of the reference content is successfully recovered by the generated output.

**METEOR.** METEOR evaluates semantic similarity using word matching, stemming, and synonym relationships. It is computed as

$$METEOR = \frac{10PR}{R+9P} \qquad (42)$$

where $P$ and $R$ denote precision and recall, respectively. Compared with BLEU and ROUGE, METEOR often exhibits stronger correlation with human judgments because it accounts for linguistic variations beyond exact word matching.

While lexical metrics are useful for evaluating anomaly descriptions and captions, they often fail to capture semantic correctness and reasoning quality. Two responses may convey the same meaning while exhibiting little lexical overlap, resulting in artificially low scores.

**LLM-Based Evaluation.** To address the limitations of lexical metrics, several recent works employ large language models as evaluators. Given a generated response $\hat{y}$, a reference annotation $r$, and an evaluation prompt $p$, the evaluation score can be expressed as

$$Score_{LLM} = f_{LLM}(\hat{y}, r, p) \qquad (43)$$

Such evaluators can assess semantic consistency, factual correctness, and reasoning quality beyond surface-level text similarity.

**MLLM-Based Evaluation.** Multimodal evaluation further incorporates the original video into the assessment process. Given a video $V$, generated response $\hat{y}$, reference annotation $r$, and evaluation prompt $p$, the evaluation score can be expressed as

$$Score_{MLLM} = f_{MLLM}(V, \hat{y}, r, p) \qquad (44)$$

Because the evaluator has direct access to both visual and textual information, MLLM-based evaluation can better assess grounding accuracy, contextual understanding, and anomaly reasoning. Such evaluation protocols are becoming increasingly important for benchmarks such as CUVA [56], ECVA [57], VANE-Bench [58], VAGU [59], FineVAU [60], HVAU-70K [61], and UCA [62], which explicitly focus on anomaly understanding and language-guided reasoning.
