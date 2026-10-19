# Attention for one token

Week 2, clip 2 of 5. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week02-clip2-attention-one-token-narrated.mp4); the [silent
version](../silent/week02-clip2-attention-one-token.mp4) shows the same steps with on-screen
captions only.

Let's follow the token cold. Its query vector, in red, is compared with the key vector of every
token in the sentence, in green.

Each score is the query for cold dotted with a key, then divided by the square root of d. The scaled
scores are minus 0.5, 0.2, 1.3, 0.6, and 1.6.

The highest scores go to cold itself, at 1.6, and to has, at 1.3. These are the tokens that matter
most here.

A softmax turns the five scores into attention weights. They are all between zero and one, and
together they sum to one.

The new vector for cold is the weighted sum of the five value vectors, in blue. The values of has
and cold contribute the most.

Now the vector for cold carries its context. In the phrase has a cold, the model can represent cold
as an infection, not a temperature.
