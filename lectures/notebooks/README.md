# Reference notebooks

Ungraded code companions to the lectures. Each notebook follows its lecture step by step, uses the same running example and the same numbers as the slides, and runs on Google Colab or HiPerGator (CPU is enough).

| Week | Notebook | Run | Lecture |
|---|---|---|---|
| 2 | [week02_transformer_review_part1.ipynb](week02_transformer_review_part1.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/parisar/BME6938-Advanced-Biomedical-AI-Spring-2027/blob/main/lectures/notebooks/week02_transformer_review_part1.ipynb) | Transformer Review, Part 1: tokens, embeddings, attention, the encoder block |
| 3 | [week03_transformer_review_part2.ipynb](week03_transformer_review_part2.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/parisar/BME6938-Advanced-Biomedical-AI-Spring-2027/blob/main/lectures/notebooks/week03_transformer_review_part2.ipynb) | Transformer Review, Part 2: next-token prediction, masking, the decoder, cross-attention, ViT patches |
| 6 | [week06_self_supervised_learning.ipynb](week06_self_supervised_learning.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/parisar/BME6938-Advanced-Biomedical-AI-Spring-2027/blob/main/lectures/notebooks/week06_self_supervised_learning.ipynb) | Self-supervised learning on PathMNIST pathology tiles: masked autoencoder, contrastive learning, linear probes, DINOv2 features |

## How to open the notebooks

1. **Google Colab (recommended).** Click **Open in Colab** in the table above or at the top of a notebook. Then choose *File > Save a copy in Drive*; otherwise your changes are lost when you close the tab. Run everything with *Runtime > Run all*. Nothing to install.
2. **Read on GitHub.** Click the notebook name to see the code, outputs, and figures without running anything. If GitHub shows "Unable to render", click *Reload*.
3. **HiPerGator.** Open JupyterLab through Open OnDemand (ood.rc.ufl.edu), clone this repository into your `/blue` folder, and pick a PyTorch kernel. Use HiPerGator for project work with real or credentialed data (for example MIMIC); never upload credentialed data to Colab or other outside services.
