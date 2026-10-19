# A patient timeline as tokens

Week 8, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week08-clip1-timeline-tokens-narrated.mp4); the [silent
version](../silent/week08-clip1-timeline-tokens.mp4) shows the same steps with on-screen captions
only.

A hospital record is a timeline of events at irregular times. Our synthetic patient arrives in the
emergency department, has a lactate of 4.1, gets norepinephrine, is diagnosed with sepsis, and moves
to the ICU three and a half hours later.

Codes become tokens. Ethos splits each code into parts: the sepsis code A41.9 becomes two tokens,
and the drug code for norepinephrine becomes three, from the broad group down to the drug.

Numbers become quantile tokens. The lactate values in the training data are cut into ten bins with
equal counts. A lactate of 4.1 falls in the top bin, so it becomes lactate, then Q10.

Time gaps become interval tokens. Ethos uses 13 of them, and adds none for gaps under 5 minutes. Our
3 gaps of under an hour become 15 minutes to one hour, and the last gap becomes 1 to 2 hours.

Six static tokens come first, such as sex and age in five-year bins. Then the events follow in time
order, so the whole record becomes one sequence of 19 tokens.

A decoder transformer then learns to predict the next token, exactly as in weeks three to five.
Ethos was trained on 241,000 patients from MIMIC-IV, and it sees the most recent 2,048 tokens of
each timeline.
