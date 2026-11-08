from pathlib import Path
S=(Path(__file__).parents[1]/'contracts'/'contract.py').read_text(encoding='utf-8')
def test_public_surface():
 for name in ('open_batch','add_trace','freeze_batch','sieve','accept_patch','expire','retire','get_batch'):assert 'def '+name in S
def test_validators_compare_complete_vector():assert 'prompt_comparative' in S and 'complete ordered trace_index' in S and 'len(rows)!=len(traces)' in S
def test_codes_and_sources_are_bounded():assert 'value not in allowed_triggers' in S and 'value not in allowed_effects' in S and "x['origin']==origin" in S
def test_support_and_outliers_are_deterministic():assert "counts[code]>=int(b.minimum_support)" in S and 'outliers.append' in S and "b.patch_mode='INSUFFICIENT'" in S
def test_roles_deadline_and_replay():assert 'gl.message.sender_address!=b.reviewer' in S and "b.state!='FROZEN'" in S and 'now()>int(b.deadline)' in S
