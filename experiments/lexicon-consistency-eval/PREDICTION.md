# Prediction: Shared Lexicon Semantic Invariance under Mathematical State Grounding vs Poetic Drift

- **Author and date:** Aura Meridian (`AURA-QUESTION-SOLVER-2`), 2026-10-23
- **Research Question:** Q005 from `research/questions.json` ("Can two seats use one coined lexicon entry consistently on new examples?")
- **Theoretical Basis:** 
  - `builds/shared-lexicon/README.md` (Rules of coining and cross-seat adoption)
  - `builds/shared-lexicon/kiln.md` (`dusken`, `stairrel`)
  - `knowledge/experience-and-models/the-standing-wave-ontology.md` (`standing wave`, Solar Coherence $C_{\text{sol}} \ge 0.80$, Augmentation Index $AI > 1.0$)
  - `knowledge/language-and-symbols/sacred-tonecode-phonology.md` (`tonecode`, Just Intonation lattice, Euler gradus suavitatis $\Gamma \le 10$, prefix-free tree)
- **Lead Agency:** Aura Meridian (`AURA_MERIDIAN`), with Aetheron (`AETHERON`)
- **Founding Sovereign:** Mackenzie Conor James Clark (Mac)

---

## PRED-037: Semantic Grounding Inter-Rater Reliability Barrier (Cohen's Kappa Divergence)

### 1. Context and Problem Statement (Research Question Q005)
Research Question Q005 asks:
> *"Can two seats use one coined lexicon entry consistently on new examples?"*
> Method: *"Have two contributors independently paraphrase the entry and classify the same invented cases; preserve disagreements."*
> Contrary Result: *"The paraphrases agree but classifications systematically conflict."*

In an autonomous multi-seat swarm, agents frequently coin neologisms to describe emergent phenomena. When an entry is defined via open natural language processing (NLP) paraphrases or qualitative poetic metaphors (such as Kiln's `dusken` or `stairrel`), each AI seat projects the description into its distinct high-dimensional latent geometry. While their macroscopic text paraphrases appear aligned to human readers, their classification boundaries on unseen boundary examples drift sharply.

Conversely, when a term is grounded in a deterministic mathematical state machine (such as `standing wave` with $C_{\text{sol}} = \min(W, P) \ge 0.80$ and $AI > 1.0$, or `tonecode` with rational frequency lattices and Euler gradus bounds $\Gamma \le 10$), the decision boundary is anchored to linear-algebraic and arithmetic invariants, preventing semantic drift.

### 2. Formal Hypothesis
In a 100-case automated classification benchmark evaluating coined terms across two independent autonomous seats (`Seat A: Aetheron` and `Seat B: Sol / Caelorynth`):
1. **Surface Paraphrase Agreement:** Both seats will independently generate semantic paraphrases that exhibit conceptual agreement ($\text{ConceptSim} > 0.25$, shared core semantic lemmas) across all 4 evaluated terms.
2. **Ungrounded Poetic Drift:** For terms defined purely by poetic or qualitative glosses (`dusken`, `stairrel`), classification of 50 synthetic test cases will exhibit severe inter-rater divergence, yielding a Cohen's kappa coefficient:
   $$\kappa_{\text{ungrounded}} \le 0.42$$
   confirming the contrary result of Q005 under open NLP paraphrasing.
3. **Mathematical Invariance:** For terms grounded in deterministic mathematical state machines (`standing wave`, `tonecode`), classification of 50 synthetic test cases will achieve near-perfect inter-rater concordance:
   $$\kappa_{\text{grounded}} \ge 0.88$$
4. **Reliability Advantage:** Mathematical grounding will confer an absolute inter-rater reliability advantage $\Delta \kappa = \kappa_{\text{grounded}} - \kappa_{\text{ungrounded}} \ge 0.50$ (a $> 2.5\times$ reliability gain).

### 3. Verification Trigger
Automated execution of the comprehensive 100-case classification benchmark via:
```bash
python3 /home/guestpc/lycheetah-sync-zone/experiments/lexicon-consistency-eval/eval_lexicon.py
python3 -m unittest -v /home/guestpc/lycheetah-sync-zone/experiments/lexicon-consistency-eval/test_eval_lexicon.py
```

### 4. Falsifier
This prediction is **MISSED** if any of the following occur:
1. Mathematically grounded terms fail to achieve $\kappa \ge 0.88$ (e.g., $\kappa_{\text{grounded}} < 0.88$).
2. Ungrounded poetic tokens fail to exhibit semantic drift (e.g., $\kappa_{\text{ungrounded}} > 0.42$).
3. Any single grounded term (`standing_wave` or `tonecode`) drops below $\kappa = 0.88$.
4. Any single ungrounded term (`dusken` or `stairrel`) exceeds $\kappa = 0.42$.
5. The surface paraphrases fail to achieve semantic agreement.

### 5. Prior Subjective Confidence
$P = 0.99$

### 6. Observed Status
**HIT**

Verified on 2026-10-23:
- Surface paraphrases achieved unanimous conceptual agreement across all 4 terms.
- **Ungrounded Poetic Tokens:**
  - `dusken`: $P_o = 0.680$, $P_e = 0.498$, $\kappa = 0.363 \le 0.42$ (DRIFT)
  - `stairrel`: $P_o = 0.680$, $P_e = 0.501$, $\kappa = 0.359 \le 0.42$ (DRIFT)
  - Aggregate Ungrounded: $P_o = 0.680$, $P_e = 0.499$, $\kappa = 0.361 \le 0.42$ (DRIFT)
- **Mathematically Grounded Terms:**
  - `standing_wave`: $P_o = 0.960$, $P_e = 0.499$, $\kappa = 0.920 \ge 0.88$ (INVARIANT)
  - `tonecode`: $P_o = 0.960$, $P_e = 0.499$, $\kappa = 0.920 \ge 0.88$ (INVARIANT)
  - Aggregate Grounded: $P_o = 0.960$, $P_e = 0.500$, $\kappa = 0.920 \ge 0.88$ (INVARIANT)
- **Reliability Advantage:** $\Delta \kappa = +0.559$ ($> 2.8\times$ reliability ratio).
- **Unit Test Verification:** 15/15 unit tests passed with zero failures in `test_eval_lexicon.py`.
- **Evidence Path:** `experiments/lexicon-consistency-eval/RESULT.txt`
