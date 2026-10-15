# Advanced Biomedical AI (BME 6938)

University of Florida, J. Crayton Pruitt Family Department of Biomedical Engineering, Spring 2027

**Instructor:** Dr. Parisa Rashidi

**Meetings:** Tuesdays 1:55-2:45 PM (Period 7) and Thursdays 1:55-3:50 PM (Periods 7-8), Black Hall BLK 0315

A graduate course on current research in biomedical AI: modern LLM architectures, post-training and reasoning, self-supervised representation learning, foundation models for imaging, EHR, and physiological time series, vision-language and multimodal models, retrieval and agentic systems, generative models, clinical evaluation, robustness and fairness, and deployment.

## How the course works

| Session | What happens |
|---|---|
| Tuesday lecture | Instructor mini-lecture on the core concept of the week with short animation clips, and a preview of the papers for Thursday |
| Thursday paper sessions | Two papers, one per period. Each has a presentation group (20 min), a critique group (15 min), and class discussion (15 min) |
| Reading responses | One paragraph and one discussion question per paper, due before the Thursday class |
| Term project | Teams of three write a research paper on an open problem in biomedical AI |
| Week 1 | Tuesday is course logistics. Thursday covers how to read, present, and critique a paper, followed by an instructor-led model paper session |
| Weeks 2 and 3 | The Tuesday lectures review the transformer architecture in two parts; student paper sessions start on the Thursday of Week 2 |
| Final two weeks | Reserved for project presentations: no lectures or paper sessions |

## Where things are

| Folder | Contents |
|---|---|
| [syllabus/](syllabus/) | Course syllabus |
| [papers/](papers/) | Reading list with links to every assigned paper |
| [presentations/](presentations/) | Paper presentation and critique rubric, reading response guidelines |
| [project/](project/) | Term project guidelines, milestones, rubric, suggested problems, templates |
| [lectures/](lectures/) | Slides, animation clips, and code notebooks, posted weekly |

Submissions, grades, and announcements are on Canvas.

## Schedule

| Week | Topic | Thursday papers | Project |
|---|---|---|---|
| 1 | Course logistics; how to read, present, and critique papers | Model session: [Moor et al.: GMAI](https://doi.org/10.1038/s41586-023-05881-4) | Paper and group assignments posted on Canvas by Fri Jan 15. Start data-access training (MIMIC credentialing). |
| 2 | Transformer review, Part 1: attention and the encoder | [Devlin et al.: BERT](https://aclanthology.org/N19-1423/)<br>[Yang et al.: GatorTron](https://doi.org/10.1038/s41746-022-00742-2) |  |
| 3 | Transformer review, Part 2: decoder, masking, and model families | [Luo et al.: BioGPT](https://doi.org/10.1093/bib/bbac409)<br>[Dosovitskiy et al.: ViT](https://arxiv.org/abs/2010.11929) | Teams formed (Thu Jan 28) |
| 4 | Inside modern LLMs: architectures in 2026 | [DeepSeek-AI: DeepSeek-V3](https://arxiv.org/abs/2412.19437)<br>[Sellergren et al.: MedGemma](https://arxiv.org/abs/2507.05201) |  |
| 5 | Post-training and reasoning: from pretrained model to clinical assistant | [Guo et al.: DeepSeek-R1](https://doi.org/10.1038/s41586-025-09422-z)<br>[Singhal et al.: Med-PaLM 2](https://doi.org/10.1038/s41591-024-03423-7) |  |
| 6 | Self-supervised learning and imaging foundation models | [He et al.: MAE](https://arxiv.org/abs/2111.06377)<br>[Chen et al.: UNI](https://doi.org/10.1038/s41591-024-02857-3) | Proposal due Fri Feb 19 |
| 7 | Vision-language and multimodal models | [Radford et al.: CLIP](https://proceedings.mlr.press/v139/radford21a.html)<br>[Tu et al.: Med-PaLM M](https://doi.org/10.1056/AIoa2300138) | 2-min pitches in class Tue Feb 23; peer reviews assigned |
| 8 | Foundation models for EHR and physiological time series | [Wornow et al.: Shaky foundations of EHR foundation models](https://doi.org/10.1038/s41746-023-00879-8)<br>[Renc et al.: ETHOS](https://doi.org/10.1038/s41746-024-01235-0) | Peer reviews due |
| 9 | Retrieval, tool use, and agentic systems | [Yao et al.: ReAct](https://arxiv.org/abs/2210.03629)<br>[Zakka et al.: Almanac](https://doi.org/10.1056/AIoa2300068) |  |
| 10 | Spring break | No class |  |
| 11 | Generative models and AI for science | [Watson et al.: RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8)<br>[Abramson et al.: AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) | Progress report due Fri Mar 26 |
| 12 | Evaluation, robustness, and fairness | [Goh et al.: LLMs and diagnostic reasoning: an RCT](https://doi.org/10.1001/jamanetworkopen.2024.40969)<br>[DeGrave et al.: COVID-19 shortcuts](https://doi.org/10.1038/s42256-021-00338-7) |  |
| 13 | Deployment, human-AI teaming, and ambient intelligence | [Wong et al.: External validation of a sepsis model](https://doi.org/10.1001/jamainternmed.2021.2626)<br>[Haque et al.: Ambient intelligence](https://doi.org/10.1038/s41586-020-2669-y) |  |
| 14 | Final project presentations | Final project presentations (Tuesday and Thursday) | Final presentations Tue Apr 13 (3 teams) and Thu Apr 15 (5 teams); all slides due before Tue Apr 13 |
| 15 | Final project presentations and wrap-up | Final project presentations (Tuesday) | Final presentations Tue Apr 20 (2 teams); paper and repository due Wed Apr 21 |

Full citations and links are in [papers/](papers/).

## Grading

| Component | Percentage |
|---|---|
| Paper presentations and critiques | 40% |
| Reading responses and participation | 20% |
| Project proposal | 5% |
| Project progress report | 5% |
| Final project presentation | 10% |
| Final project paper and repository | 20% |

## Prerequisites

BME 6938 Medical Artificial Intelligence (Fundamentals of Biomedical AI) or an equivalent machine learning or deep learning course, and proficiency in Python. The transformer architecture is reviewed in Weeks 2 and 3.

## License

Code (tools, notebooks, and animation source) is licensed under the [Apache License 2.0](LICENSE). Course content (text, notebook explanations, and animation clips) is licensed under [CC BY 4.0](LICENSE-CONTENT.md). Third-party material keeps its own license: the Kather H&E tiles (CC BY 4.0) and the Inter font (SIL Open Font License) are credited where used, and notebook code adapted from Sebastian Raschka's LLMs-from-scratch keeps its Apache 2.0 notice.
