# Appendix: Reproducibility Characteristics of LM-Based VAD Methods

To provide a controlled view of reproducibility across recent LM-based VAD literature, Table 8 summarizes representative methods published at the selected top-tier venues considered in this survey. We include methods that invoke a generative LLM or MLLM at inference time and report the corresponding foundation model together with whether key implementation details are fully specified, partially specified, or not reported.

The table focuses on six reproducibility characteristics: model version/checkpoint, decoding parameters, number of inference calls, hardware, code availability, and data availability. These characteristics are not consistently documented across the literature, making direct comparison of runtime, latency, or computational cost difficult. The table is therefore intended to provide a compact and controlled indication of reporting completeness and model dependence rather than a unified computational benchmark.

**TABLE 8. Reproducibility characteristics of representative LM-based VAD methods published at top-tier venues (CVPR, ICCV, ECCV, WACV, NeurIPS, ICML, ICLR). We include only methods that invoke a generative LLM or MLLM at inference time — i.e., when scoring or explaining a test video — and exclude methods that use an LLM/VLM solely offline to build training labels, a fixed prompt library, or a knowledge graph, after which a purely visual or CLIP-embedding classifier runs at test time (e.g., VadCLIP-family methods, MissionGNN, OVVAD, Anomize). Methods are grouped by training paradigm. ✓ indicates the item is fully specified in the paper, its appendix, or its official repository, with enough detail to reproduce it exactly; ∼ indicates it is partially specified (e.g., a component is named without a version/snapshot, or only some of the required parameters are given); ✗ indicates it is not reported anywhere in the source. Score is the count of ✓ (1 point) and ∼ (0.5 point) across the six checklist columns, out of 6. Exact quoted values underlying every symbol, along with prompt-template disclosure, context-window size, and runtime/cost — omitted here for space — are provided in the supplementary reproducibility table.**

| Method | Foundation Model (Inference-Time) | Year | Version/Checkpoint | Decoding Params | #Inference Calls | Hardware | Code | Data | Score (/6) |
|---|---|---|---|---|---|---|---|---|---|
| AnomalyRuler [85] | CogVLM + Mistral-7B | 2024 | ✓ | ∼ | ✓ | ∼ | ✓ | ✓ | 5.0 |
| HAWK [148] | Video-LLaMA + LLaMA-2-7B | 2024 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6.0 |
| LAVAD [126] | Llama-2-13b-chat + BLIP-2 | 2024 | ∼ | ✗ | ✓ | ✓ | ✓ | ✓ | 4.5 |
| Anomaly-OV [142] | LLaVA-OneVision 0.5B/7B | 2025 | ∼ | ✗ | ✓ | ∼ | ✓ | ∼ | 3.5 |
| Holmes-VAU [45] | InternVL2-2B | 2025 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6.0 |
| Vad-R1 [150] | Qwen2.5-VL-7B-Instruct | 2025 | ∼ | ✓ | ✓ | ∼ | ✓ | ✓ | 5.0 |
| Ex-VAD [94] | BLIP-2 + Llama-3.1 | 2025 | ✗ | ✗ | ∼ | ✓ | ✗ | ✓ | 2.5 |
| VERA [138] | InternVL2-8B | 2025 | ∼ | ✗ | ✓ | ∼ | ✓ | ✓ | 4.0 |
| PANDA [136] | Qwen2.5-VL-7B + Gemini 2.0 | 2025 | ✗ | ✗ | ∼ | ∼ | ∼ | ✓ | 2.5 |
| VADTree [137] | LLaVA-Video-7B + DeepSeek-R1-14B | 2025 | ∼ | ✗ | ∼ | ✗ | ✓ | ✓ | 3.0 |
| MoniTor [134] | BLIP-2 ×5 + GLM-4-Flash | 2025 | ∼ | ∼ | ✓ | ✓ | ✗ | ✓ | 4.0 |
| AnyAnomaly [141] | Chat-UniVi-7B / MiniCPM-8B | 2026 | ∼ | ✗ | ✓ | ✓ | ✓ | ✓ | 4.5 |
