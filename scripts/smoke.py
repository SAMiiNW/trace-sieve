from pathlib import Path
import json,re,time
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as ca
R=Path(__file__).parents[1];ROOT=R.parents[3]
def env(name):
 text=(ROOT/'accounts.env').read_text();return re.search(r'^'+re.escape(name)+r'\s*=\s*"?([^"\r\n]+)',text,re.M).group(1).strip()
def calldata(method=None,args=None,kwargs=None):
 out={}
 if method is not None:out['method']=method
 if args:out['args']=args
 if kwargs:out['kwargs']=kwargs
 return out
ca.make_calldata_object=calldata
operator=create_account(account_private_key=env('ACCOUNT_1_GENLAYER_PRIVATE_KEY'));reviewer=create_account(account_private_key=env('ACCOUNT_2_GENLAYER_PRIVATE_KEY'));clients={'operator':create_client(chain=studionet,account=operator),'reviewer':create_client(chain=studionet,account=reviewer)};deployment=json.loads((R/'deployment.json').read_text());address=deployment['contractAddress'];sha=deployment['sourceCommit'];record_id='SIEVE-'+str(int(time.time()));raw='https://raw.githubusercontent.com/SAMiiNW/trace-sieve/'+sha+'/evidence/';cdn='https://cdn.jsdelivr.net/gh/SAMiiNW/trace-sieve@'+sha+'/evidence/';gack='https://raw.githack.com/SAMiiNW/trace-sieve/'+sha+'/evidence/';static='https://cdn.statically.io/gh/SAMiiNW/trace-sieve/'+sha+'/evidence/';txs={}
def send(who,method,args):
 tx=clients[who].write_contract(address=address,function_name=method,args=args);receipt=clients[who].wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);leaders=receipt.get('consensus_data',{}).get('leader_receipt') or [];leaders=[leaders] if isinstance(leaders,dict) else leaders;assert receipt.get('result_name')=='MAJORITY_AGREE' and any(x.get('execution_result')=='SUCCESS' for x in leaders),receipt;txs[method+'_'+str(len(txs))]=str(tx)
send('operator','open_batch',[record_id,reviewer.address,'API exception trigger batch',raw+'rulebook.md',json.dumps(['TIMEOUT','QUEUE_SATURATED','AUTH_EXPIRED','SCHEMA_DRIFT']),json.dumps(['RETRY','DELAY','DENY','DROP']),2,3600]);send('operator','add_trace',[record_id,'ALPHA','Timeout retry trace',cdn+'trace-alpha.md']);send('operator','add_trace',[record_id,'BETA','Queue timeout trace',gack+'trace-beta.md']);send('operator','add_trace',[record_id,'GAMMA','Expired credential trace',static+'trace-gamma.md']);send('operator','freeze_batch',[record_id]);send('reviewer','sieve',[record_id]);sieved=clients['operator'].read_contract(address=address,function_name='get_batch',args=[record_id]);assert sieved['state']=='SIEVED' and sieved['patch_mode']=='SPLIT' and 'TIMEOUT' in sieved['common_triggers'] and sieved['outlier_indexes']==[2],sieved;send('operator','accept_patch',[record_id]);final=clients['operator'].read_contract(address=address,function_name='get_batch',args=[record_id]);assert final['state']=='ACCEPTED';out={'recordType':'operator-controlled exception rehearsal','recordId':record_id,'contractAddress':address,'wallets':{'operator':operator.address,'reviewer':reviewer.address},'transactions':txs,'readback':final};(R/'network-run.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,indent=2,default=str),flush=True)
