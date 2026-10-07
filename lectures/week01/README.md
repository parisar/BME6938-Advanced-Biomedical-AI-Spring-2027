# Week 1: Logistics and transformer refresher

| Session | Content |
|---|---|
| Tue Jan 12 | Course logistics |
| Thu Jan 14, Period 7 | Transformer refresher with four animation clips |
| Thu Jan 14, Period 8 | Course overview, then an instructor-led model paper session on [Moor et al., Foundation models for generalist medical artificial intelligence](https://doi.org/10.1038/s41586-023-05881-4) |

## Animation clips

Silent, with on-screen captions, about one minute each.

| Clip | File |
|---|---|
| 1. Tokenization and embeddings | [clips/week01-clip1-tokenization-and-embeddings.mp4](clips/week01-clip1-tokenization-and-embeddings.mp4) |
| 2. Query, key, value: how attention works | [clips/week01-clip2-query-key-value-attention.mp4](clips/week01-clip2-query-key-value-attention.mp4) |
| 3. Inside an encoder block | [clips/week01-clip3-encoder-block.mp4](clips/week01-clip3-encoder-block.mp4) |
| 4. Encoder versus decoder, and masking | [clips/week01-clip4-encoder-vs-decoder-and-masking.mp4](clips/week01-clip4-encoder-vs-decoder-and-masking.mp4) |

The source code for the clips is in [animations/](animations/).

## Notebook: setup check and refresher

[week01_transformer_refresher.ipynb](week01_transformer_refresher.ipynb) confirms that your environment works and walks through the four clips in code. It runs in about 5 minutes on a GPU and needs no dataset.

- **Google Colab:** [open in Colab](https://colab.research.google.com/github/parisar/BME6938-Advanced-Biomedical-AI-Spring-2027/blob/main/lectures/week01/week01_transformer_refresher.ipynb), then choose *Runtime > Change runtime type > T4 GPU*.
- **HiPerGator:** open the notebook in a Jupyter session and set `CACHE_DIR` in the Settings cell to a folder on your group's `/blue` storage.

Submit the output of the setup-check cell and your answers to the three exercises on Canvas before Week 2.
