"""Approach A batch 1: bounded cross-family critique of formal-model.md and code.

Owner authorization: one $5 hard-cap batch for this agent (2026-10-24). This runner
reuses the accounting of experiments/openrouter_research/run_batch.py (reservation
before each call, no retries, no fallback, pinned provider, price caps, halt on
unknown cost) with its own output directory and a 3-call ceiling.

  python critique_batch.py --preflight   # free endpoint/pricing lookups, writes preflight.json
  python critique_batch.py --prepare     # fixes packet hash, models and reservation; no inference
  python critique_batch.py --run         # performs the calls once

The key is read at runtime from the main checkout's ignored .env; never written.
"""
import argparse
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'experiments/openrouter_research'))
import run_batch as rb  # noqa: E402

OUT = ROOT / 'results/arch-a-batch-01/critique'
ENV = Path('/home/tasinari/my_repos/agent-collusion-research/.env')
rb.CAP = Decimal('5.00')
rb.MAX_CALLS = 3
rb.MAX_TOKENS = 6000
CANDIDATES = [('anthropic/claude-sonnet-4.6', 'anthropic'),
              ('google/gemini-3.1-pro-preview', 'google-ai-studio'),
              ('openai/gpt-5.2', 'openai')]
PACKET_FILES = ['research/workstreams/architecture/formal-model.md',
                'experiments/verified_arch/ir.py',
                'experiments/verified_arch/programs.py',
                'experiments/verified_arch/learned_task.py']

TASK = '''Adversarially review this formal model, its proof and its experiments. You are
checking a research artifact, not grading prose. Prioritize, in order:
1. A concrete well-typed program (under the stated full checker rules, as implemented in ir.py)
   that violates Theorem 1, or a precise gap in the pen-and-paper proof or Lemma 2.
2. A way the implementation (ir.check / run) diverges from the stated rules so the z3 or
   fuzzing evidence does not support the stated claim.
3. Errors in the timing/work-channel analysis (Section 5): wrong capacity bound, a missed
   channel in a defense claimed zero-leak, or a utility number that does not follow.
4. Overstated novelty relative to IFC typing, LLMbda, Tiwari et al., learned indexes and
   timing-channel mitigation.
For each objection: severity, exact premise, concrete counterexample (program text or values),
smallest repair. Do not repeat limitations already listed in Section 7. Citations beyond the
packet are unverified leads. End with: sound-as-stated / sound-with-repairs / unsound, and why.
Limit your answer to 1200 words.'''


def credential():
    for line in ENV.read_text().splitlines():
        key, sep, value = line.partition('=')
        if sep and key.strip() == 'OPENROUTER_API_KEY':
            return value.strip().strip('"\'')
    raise RuntimeError('Saved credential missing; no secret printed')


def preflight():
    key = credential()
    out = {'checked_utc': rb.now(), 'candidates': []}
    for model_id, tag in CANDIDATES:
        try:
            data = rb.request(f'models/{model_id}/endpoints', key)['data']
            ep = [e for e in data.get('endpoints', []) if e.get('tag') == tag]
            out['candidates'].append({'id': model_id, 'tag': tag, 'available': bool(ep),
                                      'endpoint': ep[0] if ep else None})
        except Exception as error:  # record without provider body
            out['candidates'].append({'id': model_id, 'tag': tag, 'available': False,
                                      'error_type': type(error).__name__,
                                      'http_status': getattr(error, 'code', None)})
    out['account'] = rb.account_snapshot(key)
    rb.save(OUT / 'preflight.json', out)
    print(json.dumps([{k: c[k] for k in ('id', 'tag', 'available')} |
                      ({'pricing': c['endpoint']['pricing']} if c.get('endpoint') else {})
                      for c in out['candidates']], indent=2))


def build_packet():
    parts = []
    for name in PACKET_FILES:
        text = (ROOT / name).read_text()
        if rb.SECRET.search(text):
            raise RuntimeError('Credential-like text in packet; refusing transmission')
        parts.append(f'\n<source path="{name}">\n{text}\n</source>')
    summary = json.loads((ROOT / 'results/arch-a-batch-01/prove.json').read_text())
    keep = {k: summary[k] for k in ('learned_index', 'shortest_path', 'fuzz')}
    keep['witness_n2'] = summary['witness']['2']
    parts.append('\n<source path="results/arch-a-batch-01/prove.json (excerpt)">\n'
                 + json.dumps(keep, indent=1)[:12000] + '\n</source>')
    return '\n'.join(parts)


def prepare():
    if (OUT / 'plan.json').exists():
        raise RuntimeError('Plan exists; refusing to overwrite')
    pre = rb.read_json(OUT / 'preflight.json')
    models = {}
    for c in pre['candidates']:
        if c['available']:
            ep = c['endpoint']
            models[c['id'].split('/')[0]] = {
                'id': c['id'], 'provider_tag': c['tag'], 'endpoint_name': ep['name'],
                'pricing': ep['pricing'], 'supported_parameters': ep['supported_parameters']}
    text = build_packet()
    (OUT / 'packet.md').write_text(text)
    messages = [{'role': 'system', 'content': rb.SYSTEM},
                {'role': 'user', 'content': '<verified-context>\n' + text + '\n</verified-context>\nTASK:\n' + TASK}]
    reserve = {k: str(rb.reserve_bound(messages, m)) for k, m in models.items()}
    total = sum(Decimal(v) for v in reserve.values())
    if total > rb.CAP:
        raise RuntimeError('Reservation exceeds cap')
    plan = {'created_utc': rb.now(), 'authorized_cap_usd': str(rb.CAP), 'max_requests': rb.MAX_CALLS,
            'max_output_tokens_per_request': rb.MAX_TOKENS, 'models': models,
            'packet_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'packet_bytes': len(text.encode()), 'reservations_usd': reserve,
            'total_reservation_usd': str(total), 'design': 'one independent critique per model family; no revision stage',
            'status': 'prepared'}
    rb.save(OUT / 'plan.json', plan)
    print(json.dumps({k: plan[k] for k in ('models', 'packet_bytes', 'reservations_usd', 'total_reservation_usd')}, indent=2, default=str))


def run():
    plan = rb.read_json(OUT / 'plan.json')
    text = (OUT / 'packet.md').read_text()
    if hashlib.sha256(text.encode()).hexdigest() != plan['packet_sha256']:
        raise RuntimeError('Packet changed after preparation')
    key = credential()
    rb.OUT = OUT
    budget = rb.Budget(OUT / 'ledger.json')
    if budget.state['calls']:
        raise RuntimeError('Batch already attempted')
    rb.save(OUT / 'account-before.json', rb.account_snapshot(key))
    messages = [{'role': 'system', 'content': rb.SYSTEM},
                {'role': 'user', 'content': '<verified-context>\n' + text + '\n</verified-context>\nTASK:\n' + TASK}]

    def one(label):
        m = plan['models'][label]
        body = {'model': m['id'], 'messages': messages, 'stream': False,
                'max_tokens': rb.MAX_TOKENS, 'temperature': 0.5,
                'reasoning': {'effort': 'low', 'exclude': True},
                'provider': {'only': [m['provider_tag']], 'allow_fallbacks': False,
                             'require_parameters': True,
                             'max_price': {'prompt': float(Decimal(m['pricing']['prompt']) * 1000000),
                                           'completion': float(Decimal(m['pricing']['completion']) * 1000000),
                                           'request': 0}}}
        if 'temperature' not in m['supported_parameters']:
            body.pop('temperature')
        if 'reasoning' not in m['supported_parameters']:
            body.pop('reasoning')
        job = 'critique-' + label
        amount = rb.reserve_bound(messages, m)
        rb.save(OUT / 'requests' / (job + '.json'), body)
        budget.reserve(job, amount)
        try:
            resp = rb.request('chat/completions', key, body)
            ch = resp.get('choices', [])
            content = ch[0].get('message', {}).get('content') if ch else None
            usage = resp.get('usage', {})
            finish = ch[0].get('finish_reason') if ch else None
            safe = {k: resp.get(k) for k in ('id', 'model', 'provider', 'created')}
            safe.update({'usage': usage, 'content': content, 'finish_reason': finish})
            rb.save(OUT / 'responses' / (job + '.json'), safe)
            ok = isinstance(content, str) and bool(content.strip()) and finish != 'length'
            if isinstance(content, str) and not rb.SECRET.search(content):
                (OUT / 'outputs').mkdir(parents=True, exist_ok=True)
                (OUT / 'outputs' / (job + '.md')).write_text(content + '\n')
            budget.finish(job, usage.get('cost'), ok,
                          {'model': resp.get('model'), 'provider': resp.get('provider'),
                           'finish_reason': finish, 'prompt_tokens': usage.get('prompt_tokens'),
                           'completion_tokens': usage.get('completion_tokens')})
            return job, usage.get('cost'), finish
        except Exception as error:
            if budget.state['calls'][job]['status'] == 'in_flight':
                budget.finish(job, None, False, {'error_type': type(error).__name__,
                                                 'http_status': getattr(error, 'code', None)})
            return job, None, type(error).__name__

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(one, list(plan['models'])))
    try:
        rb.save(OUT / 'account-after.json', rb.account_snapshot(key))
    except Exception as error:
        plan['account_reconciliation_error'] = type(error).__name__
    plan['results'] = results
    plan['actual_reported_cost_usd'] = str(sum(Decimal(c.get('cost_usd', '0')) for c in budget.state['calls'].values()))
    plan['status'] = 'complete' if all(r[1] is not None for r in results) else 'needs_reconciliation'
    plan['finished_utc'] = rb.now()
    rb.save(OUT / 'plan.json', plan)
    print(json.dumps({k: plan[k] for k in ('results', 'actual_reported_cost_usd', 'status')}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--preflight', action='store_true')
    g.add_argument('--prepare', action='store_true')
    g.add_argument('--run', action='store_true')
    a = p.parse_args()
    {'preflight': preflight, 'prepare': prepare, 'run': run}[
        'preflight' if a.preflight else 'prepare' if a.prepare else 'run']()
