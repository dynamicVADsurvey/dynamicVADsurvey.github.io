# Problem Settings and Supervision

Let a video be divided into temporal units $x_t$. A detector produces an anomaly score:

$$s_t = g(x_t) \tag{2}$$

The form of $g$ depends on the available supervision and whether a language model supplies representations, prompts, retrieval, or reasoning.

## Unsupervised and semi-supervised settings

Normal-only training estimates regular patterns without labeled anomalies. Semi-supervised protocols may combine normal training data with limited auxiliary information.

## Weak supervision

Weakly supervised methods learn from video-level labels while producing finer temporal scores. Language-aligned features can improve semantic transfer, but evaluation must distinguish representation gains from supervision gains.

## Training-free and instruction-tuned settings

Training-free methods avoid task-specific optimization and instead compose pretrained models. Instruction-tuned approaches adapt multimodal models to detection, localization, question answering, or explanation.
