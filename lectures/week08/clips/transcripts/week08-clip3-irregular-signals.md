# Irregular sampling and physiological signals

Week 8, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week08-clip3-irregular-signals-narrated.mp4); the [silent
version](../silent/week08-clip3-irregular-signals.mp4) shows the same steps with on-screen captions
only.

In the ICU, measurements arrive at irregular times. Heart rate is charted about every hour, with a
long gap overnight, and lactate is drawn only three times in the whole day.

The first option is to put everything on an hourly grid. Empty hours are filled with the last
measured value, and a mask of ones and zeros records which values were actually measured.

The mask matters, because missing values carry information. Nobody draws a lactate at two in the
morning without a reason. The mask lets the model use when a test was ordered, not just its result.

The second option is the one from clip one: interval tokens between events. The overnight gap is no
longer missing data. It becomes a token, two to six hours, that the model can read.

The third option is a time embedding, like the sine and cosine position waves from week two, but
measured in real hours. At two and a half hours, the eight-hour wave gives 0.92 and minus 0.38, and
the 24-hour wave gives 0.61 and 0.79.

Dense signals such as the ECG are cut into patches, exactly as in week six. A ten-second ECG at 500
samples per second becomes 10 one-second patches of 500 samples each.

So every clinical data type can become tokens: codes, lab values, time, missing values, and signals.
Each choice decides what the model can see, and what it cannot.
