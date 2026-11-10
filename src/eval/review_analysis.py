"""Analyse completed expert-review sheets; never generates reviewer labels."""
from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=ROOT/'results/candidate_review/review_sheet.csv'; d=pd.read_csv(p)
 d=d[d.rating.fillna('').ne('')]
 if d.empty: raise SystemExit('No reviewer ratings present; results were not simulated.')
 key=pd.read_csv(ROOT/'data/private/review_key_private.csv'); d=d.merge(key,on='review_id',validate='many_to_one')
 summary=d.groupby('hidden_stratum').rating.value_counts().rename('count').reset_index()
 summary.to_csv(ROOT/'results/tables/expert_review_results.csv',index=False)
 if d.reviewer.nunique()==2:
  w=d.pivot(index='review_id',columns='reviewer',values='rating').dropna()
  pd.DataFrame([{'reviewers':2,'shared_items':len(w),'cohen_kappa':cohen_kappa_score(w.iloc[:,0],w.iloc[:,1])}]).to_csv(ROOT/'results/tables/interrater_agreement.csv',index=False)
if __name__=='__main__': main()
