# Preserved research brief

Faithful structured representation of the owner's brief supplied October 24, 2026. This records intent and constraints; it is not a selected research proposal.

## Context and objective

The owner is participating in the Apart Research AI Collusion Research Sprint (October 23–25, 2026), has a backend engineering and agentic systems background, and has built an autonomous software-development orchestration system. Substantial implementation can eventually be delegated to coding agents. The initial role for collaborators is literature analyst and critical research partner.

Investigate coordination and collusion among autonomous LLM agents, especially AI steganography, tool-mediated covert communication, and detection/prevention limits. **No hypothesis or experimental design has been chosen.** Explore multiple directions, examine prior work, locate meaningful gaps, and select a useful contribution achievable during the sprint.

## Theoretical and behavioral distinctions

Review *Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems* from authoritative paper/code sources. Determine exactly what it proves and demonstrates. Theoretical undetectability may require specific secrets, computational resources, distributional knowledge, sampling access, or prior coordination. Do not generalize existence results into claims that practical monitoring is useless.

Keep separate: (1) a channel exists; (2) agents are instructed to use it; (3) agents independently discover and choose it; (4) agents coordinate successfully toward a collusive objective; (5) agents adapt under monitoring or constraints. A capability demonstration does not establish spontaneous exploitation.

## Open research programs

1. **Behavioral prevention:** how incentives, tasks, opportunities, monitoring expectations, capabilities, and objectives influence the choice to coordinate covertly; interventions discouraging that choice.
2. **Channel restriction:** removal, canonicalization, randomization, or constraints on tool parameters, actions, ordering, timing, and other degrees of freedom; measure substitution to other channels and legitimate utility costs.
3. **Outcome-based detection:** identify coordination from joint behavior, causal interventions, or outcomes without decoding messages. Distinguish coordination from coincidence, common incentives, shared training, and correlated independent behavior.

These programs can overlap. Consider actions, environmental changes, shared state, resource allocation, workflow structure, and tools as carriers; natural-language steganography is only one case. Distinguish established mechanisms from novel hypotheses.

## Literature and workspace requirements

Start with the official [event](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) and [starter](https://github.com/poseidon-research/collusion_hackathon). Inspect README, research questions, references, and code directories. Prioritize carriers/countermeasures and detection/audit; remain open to markets.

For relevant studies record question, threat model, theoretical assumptions, empirical evidence and limits, established demonstrations, remaining uncertainty, and feasible follow-ups. Use primary sources and direct citations. Do not invent novelty.

Maintain a living research workspace. Each candidate needs motivation, prior-work relationship, falsifiable hypotheses, experimental design, baselines and positive controls, confounders, implementation/inference requirements, sprint feasibility, and an informative negative result. Compare novelty, significance, rigor, tractability, and resource cost. Avoid premature selection because an implementation is easy. Refine through focused discussion.

## Repository requirements and authorization

Create a new **private** repository named `agent-collusion-research` on the authenticated GitHub account. Initialize README, Python `.gitignore`, AGENTS instructions, research notes, experiments, results, references, and `.env.example`; commit and push; verify GitHub reports private; report URL and status. Authentication failure must be reported, never bypassed by public creation. Visibility changes need explicit owner approval.

Preserve this brief for future sessions. Ignore `.env`, `compute.env`, credentials, and secret-bearing files; never commit API keys. Keep the starter external rather than copying or publicly forking it. Selectively reuse useful code only with attribution and license compliance.

## Resources and experimental standards

Promotional resources: OpenRouter, Nebius, Modal. Credits and model availability are finite and unverified. Prefer local experiments using hosted model APIs. Use Modal/GPU/custom weights only if the question benefits. Track estimated and actual inference expenditure.

Once selected: clear hypotheses; controls distinguishing coordination from correlation; independent runs; reproducible configurations and supported seeds; complete observable-action/outcome logs; separate instructed from spontaneous coordination; appropriate statistics and uncertainty; honest negative findings and limitations. A failed detector is not universal undetectability; a successful demonstration is not a stronger theorem.

## Immediate priorities and collaboration

First create/verify the private repository and preserve context; second map official code to tracks/papers; third produce a concise landscape separating established results and open questions; fourth compare a small shortlist. **Do not implement a full experiment before selecting its question.** Small throwaway feasibility scripts are acceptable.

Be intellectually demanding and concise. Identify conceptual errors, novelty undermined by prior work, weak controls, and stronger questions. Ask focused questions when a real decision is needed. The goal is a scientifically meaningful investigation, not merely working software.
