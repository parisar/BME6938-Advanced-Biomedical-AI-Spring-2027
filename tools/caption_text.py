"""Turn a narration line into caption text.

The narration is written to be read aloud: names are respelled so the voice says them
correctly ("co-sine", "A U C") and numbers are spelled out ("zero point six three").
Captions are read, not heard, so both go back to normal spelling.

Anything the parser cannot know from the words alone (a token ID read out as digit
pairs, a model version, an ambiguous unit) is listed in OVERRIDES and applied first.
"""
import re

# ---------------------------------------------------------------- 1. exact overrides
# Applied before anything else, longest key first. These are cases where the spoken
# form is ambiguous or the number parser would get it wrong.
OVERRIDES = {
    # identifiers and codes: digit-by-digit speech, not one number
    "thirty-one forty-seven": "3147",                 # a token ID
    "P zero zero one": "P001",                        # synthetic patient ID
    "A forty-one point nine": "A41.9",                # ICD-10 sepsis code
    "then Q ten": "then Q10",                         # quantile token
    # named things whose spoken form the glossary cannot reach
    "Chat G P T four seven percent": "ChatGPT-4 7%",
    "Chat G P T four": "ChatGPT-4",
    "R one Zero": "R1-Zero",
    "Med Palm two": "Med-PaLM 2",
    "Med Q A": "MedQA",
    "leads two, three, and a V F": "leads II, III, and aVF",
    "P D L one": "PD-L1",
    "R F diffusion": "RFdiffusion",
    "R F joint": "RFjoint",
    "R one first": "R1 first",
    "cryo E M": "cryo-EM",
    "Chest X ray fourteen": "ChestX-ray14",
    "info N C E": "InfoNCE",
    "MIMIC four": "MIMIC-IV",
    "seventy B model": "70B model",
    "H and E": "H&E",
    "C alpha": "C-alpha",
    "Compare A one": "Compare A1",
    "partner, A two": "partner, A2",
}

# ---------------------------------------------------------------- 2. names and terms
# Spoken form -> written form. Longest first at substitution time.
GLOSS = {
    # single-letter spellouts
    "A U Cs": "AUCs", "A U C": "AUC", "E C G": "ECG", "Q R S": "QRS", "A F": "AF",
    "V F": "VF", "S T": "ST", "C L S": "CLS", "K V": "KV", "I C U": "ICU",
    "G P T": "GPT", "R L H F": "RLHF", "D P O": "DPO", "P P O": "PPO", "G R P O": "GRPO",
    "N C E": "NCE", "E M": "EM", "R M S": "RMS", "P D L": "PD-L1", "R F": "RF",
    "M P N N": "MPNN", "B I M C V": "BIMCV", "Q A": "QA",
    # products and papers
    "Chat GPT": "ChatGPT", "Modern BERT": "ModernBERT", "Med Gemma": "MedGemma",
    "Med Palm M": "Med-PaLM M", "Med Palm": "Med-PaLM", "Palm E": "PaLM-E",
    "Med QA": "MedQA", "Biomed CLIP": "BiomedCLIP", "Pad Chest": "PadChest",
    "Alpha Fold": "AlphaFold", "Rosetta Fold": "RoseTTAFold", "Protein MPNN": "ProteinMPNN",
    "Res Net": "ResNet", "Pub Med": "PubMed", "GitHub COVID": "GitHub-COVID",
    "De Grave": "DeGrave", "Hotpot QA": "HotpotQA", "ALF World": "ALFWorld",
    "Chest X ray": "Chest X-ray", "Lora": "LoRA", "Q Lora": "QLoRA",
    # pronunciation respellings
    "co-sine": "cosine", "Co-sine": "Cosine", "rope": "RoPE", "Rope": "RoPE",
    "Alibi": "ALiBi", "Kwen": "Qwen", "Mamba": "Mamba",
}

# versions spoken as words: "DeepSeek V three" -> "DeepSeek-V3"
VERSION = [
    (r"\bDeepSeek V (three)\b", "DeepSeek-V3"), (r"\bDeepSeek R (one)\b", "DeepSeek-R1"),
    (r"\bGPT four o\b", "GPT-4o"), (r"\bGPT four\b", "GPT-4"), (r"\bGPT three\b", "GPT-3"),
    (r"\bGPT two\b", "GPT-2"), (r"\bLlama three\b", "Llama 3"), (r"\bLlama two\b", "Llama 2"),
    (r"\bGemma three\b", "Gemma 3"), (r"\bGemma two\b", "Gemma 2"),
    (r"\bAlphaFold (two)\b", "AlphaFold 2"), (r"\bAlphaFold (three)\b", "AlphaFold 3"),
    (r"\bResNet fifty\b", "ResNet-50"), (r"\bResNet 50\b", "ResNet-50"),
    (r"\bQwen three\b", "Qwen3"), (r"\bQwen two\b", "Qwen2"),
    (r"\bBERT base\b", "BERT base"), (r"\beight B\b", "8B"),
]

# ---------------------------------------------------------------- 3. numbers
ONES = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
        "seventy": 70, "eighty": 80, "ninety": 90}
SCALE = {"hundred": 100, "thousand": 1000, "million": 10 ** 6, "billion": 10 ** 9}
WORD = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)?")


def _val(w):
    """Value of one number word, including hyphenated compounds like 'twenty-four'."""
    lw = w.lower()
    if lw in ONES: return ONES[lw]
    if lw in TENS: return TENS[lw]
    if lw in SCALE: return SCALE[lw]
    if "-" in lw:
        a, b = lw.split("-", 1)
        if a in TENS and b in ONES and ONES[b] < 10: return TENS[a] + ONES[b]
    return None


def _to_int(words):
    """Standard spoken-number accumulation: 'thirty-eight thousand four hundred fifty-five'."""
    total, cur = 0, 0
    for w in words:
        v = _val(w)
        if v == 100:
            cur = (cur or 1) * 100
        elif v in (1000, 10 ** 6, 10 ** 9):
            total += (cur or 1) * v; cur = 0
        else:
            cur += v
    return total + cur


def _fmt(n):
    return f"{n:,}" if n >= 1000 else str(n)


BIG = {"million": "million", "billion": "billion"}
FRACTION = {"half", "third", "thirds", "quarter", "quarters"}
# after a bare "one", these words mean it was a value ("sum to one."), not a determiner
# ("one row per token"), so only then is it written as a digit
ONE_IS_VALUE = {"to", "and", "or", "is", "in", "", ",", ".", ";", ":"}


def _numbers(text):
    """Replace spoken numbers with digits.

    Pass 1 converts what a reader always expects in digits: decimals, percentages,
    years, anything spelled with more than one word, and single words from eleven up.
    Pass 2 then levels each sentence: once a sentence shows one number in digits, the
    small ones in it follow, so a caption never reads "seventeen of the 23".
    """
    toks = list(WORD.finditer(text))

    def joined(a, b):
        """True only if a single space separates the two words. A comma normally ends a
        number phrase ('zero point five, zero point two' is two numbers), except inside
        a long spoken number, which _block handles."""
        return text[toks[a].end():toks[b].start()] == " "

    def word(k):
        return toks[k].group().lower() if 0 <= k < len(toks) else ""

    def after(k):
        """The punctuation or word that follows token k, for the context tests."""
        if k + 1 >= len(toks):
            return text[toks[k].end():].strip()[:1]
        gap = text[toks[k].end():toks[k + 1].start()]
        return gap.strip()[:1] or word(k + 1)

    def block(i):
        """The contiguous run of number words starting at i, as (words, end_index)."""
        j = i
        while j + 1 < len(toks) and _val(word(j + 1)) is not None and joined(j, j + 1):
            j += 1
        return [word(k) for k in range(i, j + 1)], j + 1

    edits = []           # (start, end, replacement, kind)
    i = 0
    while i < len(toks):
        if _val(word(i)) is None:
            i += 1; continue
        words, j = block(i)

        # -- a year read as "twenty seventeen" / "twenty twenty-six"
        if len(words) == 2 and words[0] == "twenty" and 10 <= (_val(words[1]) or 0) <= 99:
            edits.append((toks[i].start(), toks[j - 1].end(), str(2000 + _val(words[1])), "hard"))
            i = j; continue

        # -- a decimal: NUM 'point' DIGIT DIGIT ...
        if j < len(toks) and word(j) == "point" and joined(j - 1, j):
            k, digits = j + 1, []
            while (k < len(toks) and word(k) in ONES and ONES[word(k)] < 10 and joined(k - 1, k)):
                digits.append(ONES[word(k)]); k += 1
            if digits:
                s = str(_to_int(words)) + "." + "".join(map(str, digits))
                end = toks[k - 1].end()
                if k < len(toks) and word(k) in BIG and joined(k - 1, k):   # "4.4 million"
                    s += " " + BIG[word(k)]; end = toks[k].end()
                edits.append((toks[i].start(), end, s, "hard"))
                i = k + (1 if end > toks[k - 1].end() else 0); continue

        # -- "a hundred" / "a thousand" stay idiomatic
        if len(words) == 1 and words[0] in ("hundred", "thousand") and word(i - 1) == "a":
            i = j; continue

        # -- a long spoken number may carry commas or "and": "two million, two hundred
        #    ninety-three thousand, seven hundred sixty". Only continue when the run so
        #    far has a scale word and the next block is smaller than it.
        end_tok = j - 1
        while True:
            scales = [SCALE[w] for w in words if w in SCALE and SCALE[w] >= 1000]
            if not scales: break
            nxt = end_tok + 1
            while nxt < len(toks) and _val(word(nxt)) is None and word(nxt) == "and":
                nxt += 1                      # "and" is a token of its own, so step over it
            if nxt >= len(toks) or _val(word(nxt)) is None: break
            gap = text[toks[end_tok].end():toks[nxt].start()]
            if gap not in (", ", " and ", ", and "): break
            nwords, nend = block(nxt)
            if _to_int(nwords) >= min(scales): break
            if word(nend) in ("percent", "per"): break
            words += nwords; end_tok = nend - 1

        n = _to_int(words)
        # -- keep the scale word: "400 million", not "400,000,000"
        if words[-1] in BIG:
            pre = _to_int(words[:-1]) or 1
            edits.append((toks[i].start(), toks[end_tok].end(), f"{_fmt(pre)} {BIG[words[-1]]}", "hard"))
            i = end_tok + 1; continue

        single = len(words) == 1
        nxt = word(end_tok + 1)
        pct = nxt in ("percent", "per")
        # "three and a half hours" and "two thirds" stay in words
        half = nxt == "and" and word(end_tok + 2) == "a" and word(end_tok + 3) in FRACTION
        span = (toks[i].start(), toks[end_tok].end())
        if not single or n >= 11 or pct:
            edits.append((*span, _fmt(n), "hard"))
        elif nxt not in FRACTION and not half:
            if words[0] != "one" or after(end_tok) in ONE_IS_VALUE:
                edits.append((*span, _fmt(n), "soft"))
        i = end_tok + 1

    # ---- pass 2: a soft edit is applied only in a sentence that already shows digits
    hard_spans = [(a, b) for a, b, _, k in edits if k == "hard"]
    keep = []
    for a, b, rep, kind in edits:
        if kind == "hard":
            keep.append((a, b, rep)); continue
        s0 = max([m.end() for m in re.finditer(r"[.!?] ", text[:a])] or [0])
        m = re.search(r"[.!?] ", text[b:])
        s1 = b + m.start() if m else len(text)
        if any(s0 <= x < s1 for x, _ in hard_spans):
            keep.append((a, b, rep))

    out, pos = [], 0
    for a, b, rep in keep:
        out.append(text[pos:a]); out.append(rep); pos = b
    out.append(text[pos:])
    s = "".join(out)
    s = re.sub(r"(\d(?:\.\d+)?) percent", r"\1%", s)
    return s


def _gloss(s):
    for k in sorted(GLOSS, key=len, reverse=True):
        s = re.sub(r"\b" + re.escape(k) + r"\b", GLOSS[k].replace("\\", "\\\\"), s)
    return s


def _version(s):
    for pat, rep in VERSION:
        s = re.sub(pat, rep, s)
    return s


def convert(text):
    s = text
    for k in sorted(OVERRIDES, key=len, reverse=True):
        s = s.replace(k, OVERRIDES[k])
    s = _version(_gloss(_version(s)))
    s = _numbers(s)
    s = _gloss(_version(s))        # names whose digit only appeared in the number pass
    return re.sub(r"\s+", " ", s).strip()
