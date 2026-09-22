# Problem Settings and Supervision in Video Anomaly Detection

Video Anomaly Detection (VAD) can be formulated under several supervision settings depending on the type and granularity of annotations available during training. These settings differ not only in annotation requirements, but also in their underlying assumptions regarding normality, anomaly distributions, and temporal localization. Classical VAD research has primarily focused on unsupervised, semi-supervised, and weakly supervised formulations, while recent advances in Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) have further introduced paradigms such as open-vocabulary and training-free VAD. In the following, we formalize these different settings.

Let a video be represented as an ordered sequence of visual units

$$V = \{x_t\}_{t=1}^{T} \qquad (1)$$

where each unit $x_t$ may denote either an individual frame $x_t \in \mathbb{R}^{H\times W\times C}$ or a short video clip $x_t \in \mathbb{R}^{L\times H\times W\times C}$ consisting of $L$ consecutive frames. Here, $H$, $W$, and $C$ denote the height, width, and number of channels, respectively, while $L$ denotes the temporal length of a clip. Thus, the index $t$ represents the temporal ordering of the video, whereas the spatial or spatio-temporal structure of each observation is contained within $x_t$. Depending on the method, $x_t$ may correspond to a frame, a fixed-length clip, or a temporal segment extracted from the original video.

A VAD model generally aims to estimate anomaly-related outputs for a video at one or more levels of granularity. In the most common temporal detection setting, the model assigns an anomaly score to each frame, clip, or temporal segment,

$$s_t = g(x_t) \qquad (2)$$

where larger values indicate a higher likelihood of anomalous behavior at the corresponding time step or temporal unit. A binary temporal prediction can then be obtained as

$$\hat{y}_t = \begin{cases} 1, & s_t > \tau, \\ 0, & \text{otherwise,} \end{cases} \qquad (3)$$

where $\tau$ denotes a predefined anomaly threshold.

Beyond temporal detection, VAD systems may also produce spatial localization outputs. For example, a model may estimate an anomalous region, bounding box, or object track associated with each temporal unit,

$$\hat{r}_t = h(x_t) \qquad (4)$$

where $\hat{r}_t$ denotes the predicted spatial region or localized anomalous entity at time $t$. In object-centric settings, this output may correspond to a bounding box, segmentation mask, or track-level prediction.

Recent language-model-based VAD systems may further generate semantic outputs, such as anomaly categories, textual explanations, question-answer responses, or temporal grounding results. This can be written generally as

$$\hat{o}_t = F(x_t, p) \qquad (5)$$

where $p$ denotes a natural-language prompt or query and $\hat{o}_t$ denotes the generated semantic output. Depending on the task, $\hat{o}_t$ may represent an anomaly label, a natural-language explanation, an answer to an anomaly-related question, or a grounded temporal segment.

More generally, modern VAD systems often operate on learned visual or multimodal representations

$$z_t = \phi(x_t) \qquad (6)$$

where $\phi(\cdot)$ denotes a feature extraction backbone, vision-language encoder, or multimodal foundation model. Different supervision settings primarily vary in how these representations are learned, constrained, queried, localized, or decoded during training and inference. In the following subsections, we review the major supervision and deployment paradigms used in contemporary VAD research.

## A. Unsupervised and Semi-Supervised

Unsupervised and semi-supervised VAD are closely related paradigms and are often used interchangeably in the literature. Both settings aim to detect anomalous events by learning the distribution of normal or mostly normal video patterns and assigning high anomaly scores to observations that deviate from this learned behavior. The main distinction lies in the assumptions made about the training data. In the strict unsupervised setting, the training set is fully unlabeled and may contain both normal and anomalous videos, with anomalies assumed to be rare relative to normal events. In the semi-supervised, or one-class, setting, the training data are assumed to contain only normal videos. These formulations are closely related to classical one-class anomaly detection, where the objective is to estimate the support or compact description of normal data and identify observations outside this region as anomalous [37]-[39].

Formally, in the unsupervised case, the model is given a collection of unlabeled videos

$$\mathcal{D}_{\text{train}} = \{V_i\}_{i=1}^{N} \qquad (7)$$

where $V_i$ denotes the $i$-th video (that may contain both normal and anomalous activity) and $N$ is the total number of training videos, and aims to learn the underlying distribution of the observed data,

$$p(V) \text{ or } p(z) \qquad (8)$$

where $z$ denotes a learned latent representation of the video content. Since labels are unavailable, anomalous events are expected to appear as low-density, irregular, or poorly reconstructed samples within the learned distribution. In semi-supervised VAD, the training set $\mathcal{D}_{\text{train}}$ is assumed to consist of only normal videos. The objective is therefore to learn a representation of normality and identify deviations from this representation during inference.

A common formulation in both settings relies on reconstruction-based or prediction-based learning. Reconstruction based methods train an encoder-decoder model to reproduce normal frames, clips, or temporal units, while prediction-based methods learn to forecast future frames or motion patterns. The anomaly score can be defined as

$$s_t = \|x_t - \hat{x}_t\|_2 \qquad (9)$$

where $x_t$ denotes the input visual unit and $\hat{x}_t$ denotes its reconstruction or prediction and $\|x\|_2$ represents $L_2$ or Euclidean distance. A large reconstruction or prediction error suggests that the observed event cannot be well represented by the learned normal data manifold. Other approaches estimate likelihood directly using probabilistic generative models such as normalizing flows, where low likelihood indicates anomalous behavior:

$$s_t = -\log p(z_t) \qquad (10)$$

where $z_t$ is a learned representation given by Equation 6. More generally an anomaly score can be computed as the distance from the learned normal manifold,

$$s_t = d(z_t, \mathcal{M}_{\text{normal}}) \qquad (11)$$

where $\mathcal{M}_{\text{normal}}$ denotes the learned representation of normal behavior and $d(\cdot,\cdot)$ denotes a distance or dissimilarity function. Larger distances indicate a higher likelihood of anomaly. Recent methods also employ memory modules, contrastive learning, masked modeling, transformer-based architectures, and density estimation to improve representation quality and temporal modeling.

These paradigms are attractive for real-world surveillance applications because anomalous events are rare, diverse, and difficult to enumerate exhaustively. Collecting representative anomalous samples is often impractical, and normal-only or unlabeled training data are substantially easier to obtain. However, the central assumption that anomalies deviate strongly from normal patterns does not always hold in practice. Subtle anomalies may closely resemble normal activities at the visual level, while normal behavior may vary significantly across scenes and contexts. Moreover, purely statistical deviations do not necessarily correspond to semantically meaningful anomalies: an event may appear visually unusual while remaining contextually normal, whereas a semantically abnormal event may exhibit only subtle low-level differences. These limitations have motivated recent research toward semantic reasoning and multimodal understanding through language-guided and MLLM-based frameworks.

## B. Weakly Supervised

In the weakly supervised setting, the training set contains both normal and anomalous videos, but supervision is provided only at the video level. Formally, the training data can be represented as

$$\mathcal{D}_{\text{train}} = \{(V_i, Y_i)\}_{i=1}^{N} \qquad (12)$$

where $Y_i \in \{0,1\}$ indicates whether video $V_i$ contains any anomalous event. Unlike fully supervised VAD, no temporal annotations are provided regarding the exact location or duration of anomalies within the video. This coarse supervision substantially reduces annotation cost while still providing stronger training signal than the semi-supervised setting.

Multiple Instance Learning (MIL) is the dominant framework for weakly supervised VAD [19]. This follows the classical multiple-instance learning assumption, where labels are observed at the bag level while instance-level labels remain latent [40], [41]. In MIL-based formulations, each video is treated as a bag of temporal visual units,

$$B_i = \{x_{i1}, x_{i2}, \ldots, x_{iK}\} \qquad (13)$$

where $x_{ij}$ denotes the $j$-th temporal unit of video $V_i$. The central assumption is that a positive bag contains at least one anomalous instance:

$$Y_i = 1 \iff \exists\, j \in \{1,\ldots,K\} : y_{ij} = 1 \qquad (14)$$

The model predicts anomaly scores for individual temporal units,

$$s_{ij} = f_\theta(x_{ij}) \qquad (15)$$

where $f_\theta$ denotes a parameterized anomaly scoring model and $s_{ij}$ is the predicted anomaly score for the temporal unit $x_{ij}$. A common formulation uses max pooling,

$$S_i = \max_{j \in \{1,\ldots,K\}} s_{ij} \qquad (16)$$

which encourages the model to identify the most suspicious temporal regions in anomalous videos while suppressing scores in normal videos.

Subsequent research has extended the MIL framework through graph-based temporal reasoning, attention mechanisms, self-training, memory augmentation, feature enhancement, and transformer-based architectures. These methods aim to improve temporal localization accuracy and reduce the ambiguity introduced by coarse supervision. Compared with semi-supervised approaches, weakly supervised methods generally achieve stronger anomaly localization performance because they are exposed to anomalous examples during training.

The weakly supervised setting is also particularly compatible with language model-based approaches. Video-level descriptions, anomaly categories, or textual metadata can naturally be converted into language supervision. This allows MLLMs to leverage semantic priors and world knowledge about anomalous activities, enabling reasoning beyond low-level motion and appearance statistics. As a result, weakly supervised VAD has become one of the primary settings for integrating multimodal foundation models into anomaly detection pipelines.

## C. Open-Set and Open-Vocabulary

Conventional weakly supervised VAD benchmarks commonly assume a closed-set protocol, in which the anomaly categories encountered during testing are also observed during training. Formally, this assumption can be expressed as

$$\mathcal{Y}_{\text{test}} \subseteq \mathcal{Y}_{\text{train}} \qquad (17)$$

where $\mathcal{Y}_{\text{train}}$ and $\mathcal{Y}_{\text{test}}$ denote the anomaly categories present in the training and testing sets, respectively. This relaxation is related to the broader open-set recognition problem, where models must handle samples outside the training label space rather than assuming a closed-world classification protocol [42], [43]. While this setting simplifies evaluation, it does not accurately reflect real-world surveillance environments, where anomalous events are often unpredictable and continuously evolving.

Open-set VAD relaxes this assumption by requiring models to detect anomalies belonging to previously unseen categories,

$$\exists\, y^{*} \in \mathcal{Y}_{\text{test}} \text{ such that } y^{*} \notin \mathcal{Y}_{\text{train}} \qquad (18)$$

where $y^{*}$ denotes an anomaly category that appears during testing but is absent from the training category set. In this setting, the objective is not necessarily to classify the anomaly into a predefined category, but rather to recognize that the observed event deviates from known patterns. Open-set VAD therefore places stronger emphasis on generalization and semantic understanding than conventional closed-set evaluation.

Closely related to this paradigm is open-vocabulary VAD, which leverages language supervision to define anomaly concepts through natural language descriptions rather than fixed category labels. Instead of restricting prediction to a predefined taxonomy, models can reason about arbitrary textual queries or prompts. Given a visual representation $\phi_v(x_t)$ of a frame, clip, temporal segment, or video-level unit, and a text representation $\phi_t(p)$ derived from a prompt $p$, anomaly relevance can be estimated through cross-modal similarity:

$$s(x_t, p) = \frac{\phi_v(x_t)^{T}\phi_t(p)}{\|\phi_v(x_t)\|\,\|\phi_t(p)\|} \qquad (19)$$

This formulation enables flexible anomaly querying using descriptions such as "person carrying a weapon" or "vehicle moving against traffic," even when such events were not explicitly annotated during training.

The emergence of vision-language models and MLLMs has substantially accelerated research in open-set and open-vocabulary VAD. Large-scale multimodal pretraining provides semantic priors and world knowledge that improve generalization to unseen anomaly types. In contrast to traditional VAD systems that primarily rely on low-level appearance and motion statistics, open-vocabulary approaches enable anomaly detection through contextual and semantic reasoning. However, these methods also introduce new challenges, including prompt sensitivity, semantic ambiguity, hallucination, and difficulties in evaluating open-ended anomaly definitions consistently across datasets.

## D. Training-Free

Training-free VAD refers to approaches that leverage pretrained foundation models, including vision-language models and Multimodal Large Language Models (MLLMs), without performing task-specific optimization or fine-tuning. Unlike conventional supervised learning frameworks, the model parameters remain fixed during deployment,

$$\theta_{\text{deploy}} = \theta_{\text{pretrained}} \qquad (20)$$

and anomaly detection is performed directly through prompting, similarity estimation, or zero-shot reasoning.

Given a visual unit $x_t$ and a textual prompt $p$, a training-free framework estimates anomaly relevance using the pretrained multimodal model,

$$s(x_t, p) = f_{\theta_{\text{pretrained}}}(x_t, p) \qquad (21)$$

where $s(x_t, p)$ denotes the anomaly score or semantic relevance between the observed frame, clip, temporal segment, or video-level unit and the textual description. In many methods, prompts describe either normal behavior or candidate anomalous events, and anomaly detection is formulated as a semantic comparison problem in a shared multimodal embedding space.

The training-free paradigm has emerged rapidly following the availability of capable foundation models pretrained on large-scale web data. Because these models already encode substantial semantic and contextual knowledge, they can often generalize to unseen anomaly categories and environments without requiring annotated VAD datasets. Prompt engineering and in-context learning therefore play a central role. Carefully designed prompts can guide an MLLM to reason about whether an observed activity is abnormal relative to the surrounding scene context, even without gradient-based adaptation.

Training-free methods offer several practical advantages. They eliminate the need for expensive VAD training pipelines, reduce deployment overhead, and provide immediate transferability across domains and anomaly categories. In addition, they naturally support open-vocabulary reasoning through natural language interaction. These properties make training-free VAD particularly attractive for rapidly evolving or low-resource surveillance environments where collecting representative anomaly annotations is impractical.

Despite these advantages, training-free approaches also face important limitations. Their performance is fundamentally constrained by the capabilities and biases of the underlying foundation model, which may not adequately represent specialized surveillance domains or rare anomaly types encountered during deployment. In addition, training-free pipelines are often substantially slower than conventional VAD systems because they rely on large multimodal architectures that require computationally expensive inference. Sequential reasoning, multi-step prompting, and repeated query evaluation can further increase latency and memory consumption, limiting practicality for real-time or large-scale surveillance applications.

Nevertheless, training-free VAD has become a major research direction in modern anomaly detection. Recent studies demonstrate that large multimodal models can achieve competitive performance on several VAD benchmarks despite requiring no task-specific optimization or annotated anomaly data. As a result, training-free methods increasingly serve both as practical deployment frameworks and as strong baselines for measuring the benefits of fine-tuning and specialized adaptation strategies.

## E. Instruction-Tuned

Instruction-tuned VAD can be viewed as an extension of training-free VAD, where pretrained vision-language or multimodal large language models are adapted to anomaly-related tasks through instruction tuning. Unlike training-free methods, which keep all model parameters fixed, instruction-tuned approaches perform task-specific adaptation using curated video-instruction pairs, anomaly question-answer data, or explanation-oriented supervision. In many cases, parameter-efficient fine-tuning strategies such as LoRA are used to adapt large multimodal models without updating all parameters.

Formally, given a pretrained multimodal model with parameters $\theta_{\text{pretrained}}$, instruction-tuned VAD learns adapted parameters

$$\theta^{*} = \theta_{\text{pretrained}} + \Delta\theta \qquad (22)$$

where $\Delta\theta$ denotes the task-specific adaptation introduced through fine-tuning. Given a visual unit $x_t$ and an instruction prompt $p$, the model estimates anomaly relevance or generates an anomaly-related response as

$$\hat{y}_t = f_{\theta^{*}}(x_t, p) \qquad (23)$$

Depending on the task formulation, $\hat{y}_t$ may represent an anomaly score, a binary decision, a category prediction, a temporal grounding result, or a natural-language explanation.

Instruction-tuned methods are particularly important for anomaly understanding, since they can align pretrained multimodal models with VAD-specific reasoning patterns, domain terminology, and output formats. Compared with training-free methods, they often provide better task alignment and more controllable responses. However, they require task-specific instruction data and may inherit dataset biases or overfit to limited anomaly types. As a result, instruction-tuned VAD occupies an intermediate position between fully training-free reasoning and conventional supervised adaptation.

## F. Other Paradigms: Fully Supervised and Online VAD

Beyond the major settings discussed above, fully supervised and online VAD represent two additional paradigms. Fully supervised VAD assumes access to dense temporal annotations, and in some cases anomaly category labels or spatial annotations. Formally, each training video may be associated with anomaly intervals

$$A_i = \{(t_s^{(k)}, t_e^{(k)}, c_k)\}_{k=1}^{N_i} \qquad (24)$$

where $t_s^{(k)}$ and $t_e^{(k)}$ denote the start and end times of the $k$-th anomalous event, and $c_k$ denotes its category label. This setting provides strong supervision for temporal localization, but it is often impractical for large-scale VAD because dense annotation of rare and ambiguous anomalous events is expensive and difficult to scale. Consequently, fully supervised formulations are less common in VAD than semi-supervised, weakly supervised, training-free, or open-vocabulary settings. Within language-model-based VAD, fully supervised methods are especially rare, since most LM-based approaches aim to reduce annotation requirements or exploit language supervision instead of relying on dense frame-level labels.

Online and streaming VAD considers scenarios in which video frames or clips arrive sequentially and predictions must be generated without access to future observations. Given a partial video stream

$$V_{\leq t} = \{x_1, x_2, \ldots, x_t\} \qquad (25)$$

the prediction at time step $t$ is restricted to information available up to the current time,

$$\hat{y}_t = g(V_{\leq t}) \qquad (26)$$

This setting is important for real-time surveillance, where delayed detection can reduce practical utility. However, online deployment is challenging for language-model-based VAD because MLLMs often require computationally expensive inference, prompt processing, multi-step reasoning, and long-context video understanding. These factors introduce latency and memory overhead, making real-time LM-based VAD substantially more difficult than offline analysis. As a result, efficient and streaming-compatible adaptation of foundation models remains an important but relatively underexplored direction.
