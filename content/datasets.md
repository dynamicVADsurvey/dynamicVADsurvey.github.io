# Datasets

Table 3 summarizes representative VAD datasets and compares them according to their annotation granularity and semantic richness. While traditional VAD benchmarks primarily provide temporal and spatial anomaly annotations, recent datasets increasingly incorporate higher-level semantic supervision. To capture this distinction, we include a semantic annotation category that describes the richest form of semantic information available in each dataset.

**Semantic Annotation** refers to the highest level of semantic supervision provided by a dataset, ranging from anomaly category labels to question-answer pairs, grounding annotations, retrieval pairs, captioning supervision, and textual explanations.

Early VAD research was largely driven by scene-specific datasets designed to evaluate statistical anomaly detection methods. Representative benchmarks include Subway Entrance and Subway Exit [7], UMN [9], UCSD Ped1 and UCSD Ped2 [47], CUHK Avenue [20], ShanghaiTech [48], NWPU Campus [49], and Street Scene [50]. These datasets primarily provide frame-level anomaly labels and, in some cases, spatial annotations through bounding boxes. Their focus is on detecting deviations from learned normal patterns within relatively constrained environments. Among them, Street Scene [50] provides track-level temporal annotations that support object-centric anomaly localization and interaction analysis. ComplexVAD [51], a large-scale streetscape benchmark containing complex interaction anomalies with both track-level temporal annotations and bounding-box spatial annotations, enabling fine-grained object-centric anomaly localization and future research on anomaly explanation and understanding. Despite their importance for evaluating anomaly detection performance, these datasets generally lack semantic annotations and therefore provide limited support for language-based reasoning, explanation generation, or anomaly understanding.

To improve scalability and anomaly diversity, later benchmarks expanded beyond single-scene settings and introduced category-level semantic supervision. Representative examples include UCF-Crime [19], UCF-Crime Extension [52], XD-Violence [53], TAD [54], BOSS [55], CamNuvem [56], Ubnormal [57], and the dataset introduced by Zhu et al. [58]. Compared with earlier benchmarks, these datasets contain substantially larger numbers of videos and anomaly categories, enabling the development of weakly supervised and fully supervised VAD methods. However, semantic supervision remains relatively coarse, typically consisting of anomaly category labels rather than detailed descriptions, explanations, or reasoning-oriented annotations.

More recently, several benchmarks have been proposed to evaluate anomaly understanding rather than anomaly detection alone. Examples include CUVA [59], ECVA [60], VANE-Bench [61], VAGU [62], FineVAU [63], HVAU-70K [45], and UCA [64]. These datasets introduce richer semantic annotations, including question-answer pairs, conversational interactions, grounding annotations, and fine-grained reasoning tasks. Similarly, the retrieval benchmark proposed by Yang et al. [65] and the captioning benchmark introduced by Bao et al. [66] extend evaluation toward video-text retrieval and anomaly description generation. Such benchmarks enable the assessment of higher-level capabilities including anomaly explanation, contextual reasoning, temporal grounding, and language-guided understanding, making them particularly relevant for modern vision-language models and MLLMs.

Despite their importance for benchmarking, existing VAD datasets exhibit several limitations that should be considered when interpreting reported performance. Many conventional benchmarks contain data from a limited number of cameras, geographic locations, or environmental conditions, which can encourage scene-specific or background-dependent representations and limit conclusions about cross-scene generalization. Anomaly definitions may also be dataset-dependent and sometimes ambiguous, since the same behavior can be normal or abnormal depending on location, context, or local activity patterns. In addition, VAD datasets are typically highly imbalanced, with anomalous events occupying only a small fraction of the available video, while multi-scene datasets may still provide limited diversity relative to real deployment environments. Some recent benchmarks increase anomaly diversity through curated or synthetically generated content; for example, VANE-Bench includes both real-world surveillance videos and synthetically generated anomalous videos [61]. While such data can broaden anomaly coverage, synthetic or curated events may not fully capture the visual, temporal, and contextual variability of naturally occurring real-world anomalies. Closed-set category annotations can further encourage category recognition rather than scene-specific anomaly reasoning. These factors should therefore be considered when transferring benchmark results to operational settings, and future datasets would benefit from greater camera, scene, geographic, and contextual diversity together with richer annotations of ambiguous and location-dependent abnormality.

**TABLE 3. Comparison of representative VAD datasets in terms of annotation granularity and semantic richness. Datasets are grouped according to their dominant annotation and semantic characteristics.**

| Dataset | Year | Domain | Total Frames | Anomaly Categories | Temporal Annotation | Spatial Annotation | Semantic Annotation |
|---|---|---|---|---|---|---|---|
| Subway Entrance [7] | 2008 | Streetscape | 86,535 | 5 | Frame | – | None |
| Subway Exit [7] | 2008 | Streetscape | 38,940 | 3 | Frame | – | None |
| UMN [9] | 2009 | Crowd Behavior | 3,855 | 1 | Frame | – | None |
| UCSD Ped1 [47] | 2013 | Streetscape | 14,000 | 5 | Frame | Bounding Box | None |
| UCSD Ped2 [47] | 2013 | Streetscape | 4,560 | 5 | Frame | Bounding Box | None |
| CUHK Avenue [20] | 2013 | Streetscape | 30,652 | 5 | Frame | Bounding Box | None |
| NWPU Campus [49] | 2023 | Streetscape | 1,466,073 | 28 | Frame | – | None |
| ShanghaiTech [48] | 2017 | Streetscape | 317,398 | 13 | Frame | Bounding Box | None |
| Street Scene [50] | 2020 | Streetscape | 203,257 | 17 | Track | Bounding Box | None |
| ComplexVAD [51] | 2025 | Streetscape | 3,681,438 | 40 | Track | Bounding Box | None |
| UCF-Crime [19] | 2018 | Crime | 13,741,393 | 13 | Video | – | Category Labels |
| UCF-Crime Extension [52] | 2021 | Crime | 14,475,793 | 15 | Video | – | Category Labels |
| XD-Violence [53] | 2020 | Violence | 114,096 | 6 | Video | – | Category Labels |
| TAD [54] | 2024 | Traffic | 721,280 | 4 | Frame | Bounding Box | Category Labels |
| BOSS [55] | 2017 | Multiple | 48,624 | 11 | Video | – | Category Labels |
| CamNuvem [56] | 2022 | Robbery | 6,151,788 | 1 | Video | – | Category Labels |
| Ubnormal [57] | 2022 | Multiple | 236,902 | 22 | Frame | Pixel | Category Labels |
| SENSE-VAD [67] | 2026 | Autonomous Driving | 540,888 | 15 | Frame | Bounding Box | Category Labels |
| MSAD [58] | 2024 | Multiple | 447,236 | 55 | Frame | – | Category Labels |
| CUVA [59] | 2024 | Multiple | 3,345,097 | 11 | Time Duration | – | Video QA |
| ECVA [60] | 2024 | Multiple | 19,042,560 | 21 | Time Duration | – | Video QA |
| VANE-Bench [61] | 2025 | Multiple | 951,482 | 19 | Video | – | Conversational QA |
| VAGU [62] | 2025 | Multiple | 20,400,000 | 21 | Period | – | Grounding + QA |
| FineVAU [63] | 2026 | Surveillance | – | 13 | – | – | Fine-grained QA |
| SVTA [65] | 2025 | Multiple | 1,360,000 | 68 | Video-level | – | Retrieval text pairs |
| CVACBench [66] | 2025 | Surveillance | 60,160 | 13 | Frame | – | Captioning |
| HVAU-70K [45] | 2025 | Multiple | 13,855,489 | 15 | Frame | – | Video QA |
| UCA [64] | 2024 | Crime | 11,817,597 | 13 | Frame | – | Video QA |
