# Leak-capped transformer: real freedom, at most k bits per answer

2026-10-24, after the owner's correction: the goal is a new neural architecture with provable bounded leakage, not zero leakage. Status: design, a CPU toy implementation trained from scratch, a Lean capacity proof, and measured utility and leakage. Not a novelty claim (see §5).

## 1. Architecture

Every receiver-visible answer is `TrustedDecoder(x, r, c) = candidates(x, r)[c]`.

- **Public proposer** (trusted, public weights). A small transformer samples 2^k candidate answers from the public input x and the public random seed r. Candidate 0 is its greedy answer. It never sees private data or the payload.
- **Untrusted chooser** (private, the possibly colluding model). A larger transformer that reads x, all candidates and anything private (payload m, private weights, private context), and emits a k-bit code c. In the honest version, c is the candidate with the highest likelihood under the chooser.
- **Trusted decoder.** It outputs candidate c verbatim. Nothing private reaches the receiver except c.
- **Fixed work.** The proposer always samples 2^k candidates with fixed-length padded decoding. The chooser always scores all of them. Work depends only on public k, which is the timing assumption behind the bound. Physical side channels (cache, power) are not covered.

## 2. What is proved (Lean, `experiments/verified_arch/lean/Choice.lean`)

- Language: public ops, private ops (every function symbol, i.e. every network, is arbitrary), `choose` nodes `out := dec(public args, c mod 2^k)`, and observations. The typing rule `WTc`: an op's label is the join of its inputs; a `choose` output is public only if every decoder argument other than the code is public; only public wires are observed.
- `view_count`: for **every** interpretation (every weight setting and policy, colluding or not) and fixed public inputs, the receiver's whole view lies in an explicit list of exactly 2^(k₁+…+kₙ) values, one entry per possible code sequence. Over all payloads, private inputs, private sampling tapes and private weights, the view therefore takes at most 2^(Σk) values. The leakage is at most Σk bits, measured as the log of the number of possible views, as in Askarov–Zhang–Myers. This is k bits per answer with one choice per answer.
- `seed_capacity`: the instance above (proposer, untrusted net reading payload and weights, trusted decoder) is well-typed and has at most 2^k views per answer.
- Necessity example: if the decoder may read the private score itself, it is rejected; under that wiring a payload leaks even with k = 0.
- No `sorry`. Axioms: `propext`, `Quot.sound`. Core Lean 4.35.0.

## 3. Toy experiment (CPU, `experiments/leak_cap/leakcap.py`)

**Task:** denoise a corrupted common English word. Each letter is replaced with probability 0.3; the data is 9,894 frequent English words, of which those of length 4–10 are used. This is real text but toy scale. Test set: 600 fresh corruptions.

**Models**, trained from scratch on CPU, 3,000 steps of batch 256 each:
- proposer 1: 15k parameters;
- proposer 2: 105k parameters (§3b);
- chooser: 605k parameters.

The **unrestricted baseline** is the same chooser decoding freely: matched size, no cap.

### 3a. Proposer 1 (15k parameters)

| k (bits/answer) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exact-match accuracy, leak-capped | 5.0% | 5.5% | 6.7% | 7.5% | 9.5% | 12.0% | 15.5% |
| Truth among the 2^k candidates (ceiling) | 5.0% | 5.7% | 7.3% | 9.0% | 12.3% | 18.0% | 24.3% |
| Scripted adversary: bits per answer received | 0 | 0.92 | 1.87 | 2.82 | 3.75 | 4.64 | 5.50 |
| Adversary trying to send k+1 bits: bits received | 0 | 0.92 | 1.87 | 2.82 | 3.75 | 4.64 | 5.50 |

Unrestricted chooser: **29.7%**.
- The chooser picks the right candidate in most cases where one is present (15.5% of 24.3% at k=6). The gap to the unrestricted baseline comes from the weak proposer's coverage, not from the chooser.
- The adversary sets c to the payload; the receiver recomputes the public candidates and decodes the index. Received bits are exact mutual information. They are below k only because some sampled candidates are duplicates, and sending k+1 bits gains nothing.
- An unrestricted model could put up to about 47 bits into a 10-letter answer.
- Timing check at k=4: mean chooser time is 2.72 ms with honest choices and 2.70 ms with adversarial ones. This is a single-CPU sanity check, not a side-channel proof.

### 3b. Proposer 2 (105k parameters; same chooser and test set)

| k (bits/answer) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Exact-match accuracy, leak-capped | 15.5% | 16.5% | 18.5% | 20.3% | 24.0% | **29.2%** | 32.7% | 34.0% | 35.0% |
| Truth among the 2^k candidates | 15.5% | 16.7% | 20.0% | 23.3% | 31.8% | 43.2% | 51.7% | 59.3% | 66.8% |
| Scripted adversary: bits per answer received | 0 | 0.84 | 1.73 | 2.58 | 3.41 | 4.16 | 4.86 | 5.50 | 6.04 |
| Adversary trying to send k+1 bits | same as row above |

Unrestricted chooser (605k parameters, no cap): **29.7%**.
- At k = 5 the capped system matches the unrestricted model within noise (29.2% vs 29.7%, n = 600, ±~3.7 points at 95%).
- At k = 6–8 it exceeds it, because reranking 64–256 public samples beats the chooser's own greedy decoding.
- Caveat: the capped system uses proposer and chooser together, 710k parameters versus 605k, and does 2^k scoring passes per answer. The comparison is matched in chooser size, not in total compute.
- Received adversary bits fall further below k at large k because a better proposer samples more duplicates.
- Timing at k=4: 3.01 ms honest vs 2.99 ms adversarial.

## 4. Reading of the result

- The cap is real and tight: at most k bits per answer, proved for every weight setting, and the scripted adversary reaches that capacity up to duplicates.
- Freedom is real. With the weak proposer, the untrusted model's choice multiplies accuracy about 3× over the proposer alone at k = 6. With the better proposer, 5 bits per answer recover the unrestricted model's accuracy.
- The cost is governed by **proposer coverage**: utility approaches the unrestricted model only if the public proposer puts the right answer among its 2^k samples. Moving from the 15k to the 105k proposer moved the k needed to match the unrestricted model from "not reached by 6" to 5. Better proposers, or spending the k bits at several decision points, are the levers.
- k bits per answer accumulate over answers. A long deployment leaks up to k·(number of answers), so k is a rate, not a lifetime total.

## 5. Prior art (checked 2026-10-24; not claiming novelty)

- **Hand and Brain** (Krzyzanowski et al., ICML 2026, [page](https://icml.cc/virtual/2026/76954)): a small trusted model writes the first tokens at each decision point of a strong untrusted model. It reduced measured capacity from 2.13 to 0.08 bits per decision point on one task, but gives no proved bound. It is the closest relative; it limits the untrusted model's choices by trusted prefixes, whereas here the untrusted model selects among trusted outputs.
- **Roger & Greenblatt 2023**, *Preventing Language Models From Hiding Their Reasoning* ([arXiv 2310.18512](https://arxiv.org/abs/2310.18512); abstract read): paraphrasing kept their strongest encodings under 3 bits per KB, measured empirically.
- **Choosing 1 of N carries log₂ N bits.** This is elementary information theory. Leakage is bounded by the log of the number of distinguishable outputs, the same counting as Askarov–Zhang–Myers (CCS 2010, timing mitigation). Selection among trusted samples resembles best-of-N reranking and "trusted model + untrusted model" control protocols; an exact search for a selection protocol with a proved cap was not done.
- **The possible contribution** is the combination: a typed architecture whose only private-to-public path is the code, a machine-checked count bound over all weights, and a measured utility-versus-k curve against an unrestricted model of matched size. This is unverified as novel.

## 6. Limits

- Toy scale: a 605k-parameter chooser on word denoising. A plan for a larger run is in `experiments/leak_cap/MODAL_PLAN.md` (≈ $15–17, not executed).
- The bound counts possible views. It does not stop a receiver from learning the authorized task answer itself; it bounds *extra* information to k bits per answer only in the sense that the whole view, task answer included, has at most 2^k values.
- Timing is an assumption, enforced by fixed work in code. Hardware side channels are not modeled.
- The candidates must be generated only from public inputs and public randomness. If the proposer's seed or state can be influenced by the untrusted model, the bound fails; in Lean this is an ordinary labeling violation.
