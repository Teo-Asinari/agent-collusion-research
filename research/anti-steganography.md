# Active anti-steganography direction

2026-10-24: owner requested actual construction of defenses that interfere with a carrier after encoding, or prevent encoding. Authorized a concrete local prototype; a full hackathon experiment/model budget is still unselected.

## Existing work that constrains novelty

[Roger & Greenblatt, Preventing Language Models From Hiding Their Reasoning, v2](https://arxiv.org/abs/2310.18512) empirically evaluate active defenses including paraphrasing and report low residual encoding rates for tested schemes under specified conditions. This is not universal prevention. Review depth here: abstract plus author-written [research post](https://www.alignmentforum.org/posts/9Fdd9N7Escg3tcymb/preventing-language-models-from-hiding-their-reasoning); no code or full proof audit.

[Mathew et al.](https://arxiv.org/html/2410.03768v2) already test optimization against oversight/paraphrasing; see existing literature notes. [Conceptual Steganography](https://arxiv.org/abs/2605.26537) reports concepts as a channel more robust to paraphrasing than keyword approaches across tested models/tasks. Review depth: abstract only; full methodology must be read before selecting a semantic-defense study.

The proposed release broker does not claim to invent canonicalization or defeat conceptual communication generally. Its exact schema is useful for testing what an intervention preserves and discards. A meaningful follow-up needs adaptive encoders, legitimate task variation and an explicit utility budget.

## Verified cache-timing report

Primary source: [OpenAI, Securing our frontier model training environment](https://openai.com/index/securing-our-frontier-model-training-environment/), October 23, 2026, “Communicating across isolated tasks.” The report describes synthetic-secret transfer between VMs on shared hosts using cache-versus-main-memory access timing. It also lists storage-write timing, CPU contention and a TLS certificate cache. Most tests directed agents toward specific channels or provided an encoding protocol; one provided a broad vulnerability list. Thus the report supports tool-assisted channel construction but does not demonstrate universal unaided spontaneous discovery, theoretical undetectability or arbitrary-environment reproducibility. No independent reproduction was performed here.

**Implication for our design:** message rewriting cannot remove information that bypasses the message path through shared-resource effects. Any eventual defense claim must identify the complete receiver observation boundary. A content-only prototype can establish a scoped property without establishing process/hardware isolation.

## Concrete artifact and results

- [Protocol, evaluation and reproduction instructions](../experiments/anti_stego/README.md).
- [Local metrics](../results/anti_stego/local-smoke/metrics.json); source hashes and configuration included.
- Six explicit scripted carriers, five release modes, 256 balanced trials per cell. All identity positive controls work. Projection erases the tested presentation distinctions; semantic choices survive. Replanning removes those choices under the public cost objective and intentionally changes some assignments.
- Eight invariant/boundary tests pass. No LLM calls or provider expenditure. No new discovery or cryptographic security claim.

The evidence motivates a concrete fork for discussion: constrain representation while preserving exact agent choices, or permit the defender to change task-equivalent choices. How much decision authority the defender can take is a substantive research variable, not an implementation detail.
