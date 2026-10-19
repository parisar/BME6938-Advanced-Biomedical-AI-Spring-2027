# Humans and models together

Week 13, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week13-clip3-teaming-narrated.mp4); the [silent
version](../silent/week13-clip3-teaming.mp4) shows the same steps with on-screen captions only.

Put a clinician and a model together and there are two obvious rules: flag if either flags, or flag
only if both do. Say the clinician catches 80% of cases and the model 75. Which rule is better
depends on something nobody measures.

Assume their errors are independent. Of a hundred real cases, both catch 60, the clinician alone 20,
the model alone 15, and 5 are missed by both. Either-flags reaches 0.95, and both-flags falls to
0.60.

Now assume the model misses whatever the clinician misses. Both catch 75, the clinician alone 5, and
20 are missed by both. Either-flags falls to 0.80, which is the clinician alone, so the model adds
nothing. Both-flags rises to 0.75. The same two sensitivities, opposite conclusions.

And people are not rules. A confident score can talk a clinician out of a correct judgement, and at
one true case in every eight alerts the rational response is to stop reading them. Goh and
colleagues measured exactly this: the model alone scored 92%, and the physicians using it scored 76,
against 74 without.

Ambient intelligence watches the room instead of waiting for someone to type. 16 depth sensors
detected hand hygiene at 92.1% sensitivity, better than the human observers at 85.2. But that came
from only 88 events, so read the interval. In an ICU, 7 sensors detected mobility at 87%, and
counted the staff involved correctly only 69% of the time.

Sensing a care space is a governance question first. Depth sensing keeps identifiable images out of
the room, which helps, but it does not settle who consents, who sees the data, or how long it is
kept, and the staff are being observed too. Validate locally, watch it after go-live, and measure
the team rather than the model.
