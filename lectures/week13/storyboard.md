# Week 13 storyboard: deployment, human-AI teaming, and ambient intelligence

Lecture Tue Apr 6; papers Thu Apr 8: Wong et al. (Epic Sepsis Model external validation) and Haque et al.
(ambient intelligence). Paper numbers below were checked against Wong et al. (JAMA Intern Med 2021, PMC8218233);
Haque et al. is a review, so no performance numbers are quoted from it. Anything marked illustrative is invented.
Show the storyboard first.

## Clip 1: What external validation found

1. A sepsis model deployed in hundreds of hospitals was validated at Michigan Medicine: 38,455 hospitalizations,
   about 7% with sepsis.
2. AUC 0.63, against 0.76 to 0.83 reported by the vendor.
3. At the vendor's recommended threshold: sensitivity 33% (two thirds of sepsis cases missed), positive predictive
   value 12%, and alerts on 18% of all hospitalizations.
4. Only 7% of sepsis cases were flagged before clinicians had already given timely antibiotics.
5. Lesson: validate locally before deployment, and measure what the alert adds to what clinicians already do.

## Clip 2: Thresholds, alert burden, and drift

1. One model, three thresholds, prevalence 7% (illustrative): sensitivity 80% with PPV 10% gives 56 alerts per 100
   admissions; 50% with PPV 20% gives 17.5; 25% with PPV 35% gives 5.
2. Choosing a threshold is choosing how many alerts clinicians will see for each true case.
3. Inputs drift: a new lab assay, a coding change, a new patient population. A monitoring chart of monthly AUC
   drifts below its control limit (illustrative).
4. Monitoring plan: track inputs, outputs, and outcomes; set limits; decide in advance who acts when a limit is crossed.

## Clip 3: Humans and models together

1. Clinician sensitivity 0.80, model sensitivity 0.75 (illustrative). If their errors were independent:
   flag when either flags gives 1 - 0.20 x 0.25 = 0.95 sensitivity (with more false alarms); flag only when both
   flag gives 0.80 x 0.75 = 0.60.
2. Real errors are correlated, and people over-trust or ignore alerts (automation bias, alert fatigue), so the
   combination must be measured, not assumed (Week 12, Goh et al.).
3. Ambient intelligence: passive sensors (for example depth sensors) observe care spaces, such as hand hygiene or
   patient mobility in the ICU, without anyone entering data.
4. Privacy and consent come first: depth sensing can avoid identifiable images, but monitoring staff and patients
   raises consent and governance questions.

## Notebook (week13_deployment.ipynb, CPU)

Threshold sweeps on a synthetic risk score at 7% prevalence (sensitivity, PPV, alerts per 100 admissions); a
simulated drift with a monitoring chart and control limits; combining a simulated clinician and model with OR and
AND rules, with and without correlated errors. All examples biomedical; commit and push after each clip.
