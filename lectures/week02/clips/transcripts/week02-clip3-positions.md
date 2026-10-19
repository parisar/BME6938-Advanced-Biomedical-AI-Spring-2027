# Giving tokens a position

Week 2, clip 3 of 5. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week02-clip3-positions-narrated.mp4); the [silent
version](../silent/week02-clip3-positions.mp4) shows the same steps with on-screen captions only.

Word order matters: chest pain and pain chest are not the same. But attention gives each word the
same output vector in both orders, only swapped, so on its own it cannot tell them apart.

The fix is to give each position its own vector and add it to the token vector. The sum, the input
vector, now carries both the word and its position.

The simplest option is to learn a table with one vector per position. BERT learns 512 rows. The
patient has a cold uses rows one to five, but a longer input has no row to look up.

The original transformer computes position vectors instead of learning them. It uses waves: a sine
and a cosine wave at a fast speed, and another sine and cosine pair at a slow speed.

To build the vector for position one, read the height of each wave at position one. The 4 heights,
0.84, 0.54, 0.25, and 0.97, are the position vector.

Move to position two and the fast waves change a lot, while the slow waves barely move, like the
second hand and the hour hand of a clock. Together, they give every position its own pattern.

Learned or computed, these absolute positions are added once, at the input, and every later layer
has to carry that information forward. Newer models handle position differently, inside attention
itself.
