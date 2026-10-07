# Advanced Biomedical AI (BME 6938)

University of Florida, J. Crayton Pruitt Family Department of Biomedical Engineering, Spring 2027

**Instructor:** Dr. Parisa Rashidi

**Meetings:** Tuesdays 1:55-2:45 PM (Period 7) and Thursdays 1:55-3:50 PM (Periods 7-8), Black Hall BLK 0315

A graduate course on current research in biomedical AI: self-supervised representation learning, foundation models for imaging, EHR, and physiological time series, vision-language and multimodal models, LLM adaptation, agentic systems, generative models, clinical evaluation, robustness and fairness, and deployment.

## How the course works

| Session | What happens |
|---|---|
| Tuesday lecture | Instructor mini-lecture on the core concept of the week, a curated video, and a preview of the papers for Thursday |
| Thursday paper sessions | Two papers, one per period. Each has a presentation group (20 min), a critique group (15 min), and class discussion (15 min) |
| Reading responses | One paragraph and one discussion question per paper, due before the Thursday class |
| Term project | Teams of three write a research paper on an open problem in biomedical AI |
| Final two weeks | Reserved for project presentations: no lectures or paper sessions |

## Where things are

| Folder | Contents |
|---|---|
| [syllabus/](syllabus/) | Course syllabus |
| [papers/](papers/) | Reading list with links to every assigned paper |
| [presentations/](presentations/) | Paper presentation and critique rubric, reading response guidelines |
| [project/](project/) | Term project guidelines, milestones, rubric, suggested problems, templates |
| [lectures/](lectures/) | Tuesday slides and video links, posted weekly |

Submissions, grades, and announcements are on Canvas.

## Schedule

| Week | Tue | Thu | Topic | Thursday papers | Project |
|---|---|---|---|---|---|
| 1 | Jan 12 | Jan 14 | From task-specific models to foundation models; transformer refresher | Transformer refresher; Instructor-led model paper session: [Moor et al., Foundation models for generalist medical artificial intelligence](https://doi.org/10.1038/s41586-023-05881-4). Group sign-ups. | Start data-access training (MIMIC credentialing) |
| 2 | Jan 19 | Jan 21 | Self-supervised representation learning | [He et al., Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)<br>[Zhou et al., A foundation model for generalizable disease detection from retinal images (RETFound)](https://doi.org/10.1038/s41586-023-06555-x) |  |
| 3 | Jan 26 | Jan 28 | Foundation models for medical imaging | [Oquab et al., DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)<br>[Chen et al., Towards a general-purpose foundation model for computational pathology (UNI)](https://doi.org/10.1038/s41591-024-02857-3) | Teams formed (Thu Jan 28) |
| 4 | Feb 2 | Feb 4 | Vision-language models | [Radford et al., Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://proceedings.mlr.press/v139/radford21a.html)<br>[Li et al., LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day](https://arxiv.org/abs/2306.00890) |  |
| 5 | Feb 9 | Feb 11 | Foundation models for EHR and physiological time series | [Wornow et al., The shaky foundations of large language models and foundation models for electronic health records](https://doi.org/10.1038/s41746-023-00879-8)<br>[Renc et al., Zero shot health trajectory prediction using transformer (ETHOS)](https://doi.org/10.1038/s41746-024-01235-0) |  |
| 6 | Feb 16 | Feb 18 | Multimodal fusion and generalist medical AI | [Acosta et al., Multimodal biomedical AI](https://doi.org/10.1038/s41591-022-01981-2)<br>[Tu et al., Towards Generalist Biomedical AI (Med-PaLM M)](https://doi.org/10.1056/AIoa2300138) | Proposal due Fri Feb 19 |
| 7 | Feb 23 | Feb 25 | Adapting LLMs: retrieval and parameter-efficient fine-tuning | [Hu et al., LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)<br>[Zakka et al., Almanac: Retrieval-Augmented Language Models for Clinical Medicine](https://doi.org/10.1056/AIoa2300068) | 2-min pitches in class Tue Feb 23; peer reviews assigned |
| 8 | Mar 2 | Mar 4 | Agentic systems and tool use | [Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)<br>[Tu et al., Towards conversational diagnostic artificial intelligence (AMIE)](https://doi.org/10.1038/s41586-025-08866-7) | Peer reviews due |
| 9 | Mar 9 | Mar 11 | Generative models and AI for science | [Watson et al., De novo design of protein structure and function with RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8)<br>[Abramson et al., Accurate structure prediction of biomolecular interactions with AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) |  |
| 10 | Mar 16 | Mar 18 | Spring break | No class |  |
| 11 | Mar 23 | Mar 25 | Evaluation: benchmarks versus clinical trials | [Goh et al., Large Language Model Influence on Diagnostic Reasoning: A Randomized Clinical Trial](https://doi.org/10.1001/jamanetworkopen.2024.40969)<br>[Lång et al., Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI)](https://doi.org/10.1016/S1470-2045(23)00298-X) | Progress report due Fri Mar 26 |
| 12 | Mar 30 | Apr 1 | Robustness, shortcut learning, and fairness | [DeGrave et al., AI for radiographic COVID-19 detection selects shortcuts over signal](https://doi.org/10.1038/s42256-021-00338-7)<br>[Gichoya et al., AI recognition of patient race in medical imaging: a modelling study](https://doi.org/10.1016/S2589-7500(22)00063-2) |  |
| 13 | Apr 6 | Apr 8 | Deployment, human-AI teaming, and ambient intelligence | [Wong et al., External Validation of a Widely Implemented Proprietary Sepsis Prediction Model in Hospitalized Patients](https://doi.org/10.1001/jamainternmed.2021.2626)<br>[Haque et al., Illuminating the dark spaces of healthcare with ambient intelligence](https://doi.org/10.1038/s41586-020-2669-y) |  |
| 14 | Apr 13 | Apr 15 | Final project presentations | Final project presentations (Tuesday and Thursday) | Final presentations Tue Apr 13 (3 teams) and Thu Apr 15 (5 teams); all slides due before Tue Apr 13 |
| 15 | Apr 20 |  | Final project presentations and wrap-up | Final project presentations (Tuesday) | Final presentations Tue Apr 20 (2 teams); paper and repository due Wed Apr 21 |

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

BME 6938 Medical Artificial Intelligence (Fundamentals of Biomedical AI) or an equivalent machine learning or deep learning course, and proficiency in Python. A transformer refresher is provided in Week 1.
