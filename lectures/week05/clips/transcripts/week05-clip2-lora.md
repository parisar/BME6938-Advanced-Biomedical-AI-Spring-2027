# LoRA: fine-tuning with a small fraction of the weights

Week 5, clip 2 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week05-clip2-lora-narrated.mp4); the [silent
version](../silent/week05-clip2-lora.mp4) shows the same steps with on-screen captions only.

Full fine-tuning with the Adam optimizer stores about 16 bytes for every parameter: the weight, its
gradient, and 2 optimizer states. That is about 5.8 gigabytes for this small model, and over a
thousand for a 70B model.

Look at one weight matrix in SmolLM2: a query projection with 960 rows and 960 columns, about
920,000 weights. With LoRA, it stays frozen.

LoRA adds two thin matrices beside it. A takes the token down to just eight numbers, and B brings it
back up. The output is W times x, plus B times A times x.

B and A together have 15,360 weights. That is about 1.7% of the frozen matrix, and only these are
trained.

B starts at zero, so at the first step B times A times x is zero, and the model gives exactly the
original output. Training then moves only B and A.

Add LoRA to the query, key, value, and output projections in all 32 layers, and it trains 1,638,400
weights. That is about 0.45% of the model.

Because the base model never changes, one copy can serve many tasks. Each task, such as discharge
summaries or radiology impressions, needs only its own small adapter, about 3.3 megabytes.
