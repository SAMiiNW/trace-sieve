from pathlib import Path
import hashlib,json,re,subprocess
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
R=Path(__file__).parents[1];ROOT=R.parents[3]
def env(name):
 text=(ROOT/'accounts.env').read_text();m=re.search(r'^'+re.escape(name)+r'\s*=\s*"?([^"\r\n]+)',text,re.M)
 if not m:raise RuntimeError(name+' missing')
 return m.group(1).strip()
assert env('ACCOUNT_1_GITHUB_USERNAME')=='SAMiiNW'
code=(R/'contracts'/'contract.py').read_text();client=create_client(chain=studionet,account=create_account(account_private_key=env('ACCOUNT_1_GENLAYER_PRIVATE_KEY')));tx=client.deploy_contract(code=code,args=[]);receipt=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);full=client.get_transaction(transaction_hash=tx);leaders=full.get('consensus_data',{}).get('leader_receipt') or [];leaders=[leaders] if isinstance(leaders,dict) else leaders;address=(full.get('data')or{}).get('contract_address') or full.get('to_address') or (receipt.get('data')or{}).get('contract_address');assert full.get('result_name')=='MAJORITY_AGREE' and any(x.get('execution_result')=='SUCCESS' for x in leaders) and address;out={'account':'SAMiiNW','network':'StudioNet','contractAddress':address,'deploymentTransaction':str(tx),'deploymentConsensus':'MAJORITY_AGREE','deploymentExecution':'SUCCESS','sourceSha256':hashlib.sha256(code.encode()).hexdigest(),'sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'repository':'https://github.com/SAMiiNW/trace-sieve','publicSite':'https://trace-sieve.pages.dev/'};(R/'deployment.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
