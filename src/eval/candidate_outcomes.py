"""Create a responsible, generalized portfolio of high-value follow-up outcomes."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def main()->None:
 blind=pd.read_csv(ROOT/'results/tables/survey_blind_spots.csv'); score=pd.read_csv(ROOT/'results/tables/public_coarse_scores.csv'); forecast=pd.read_csv(ROOT/'results/tables/site_damage_forecast_cells.csv')
 opportunity=blind.merge(score[['state','cell_id_10km','threat_proxy','risk_score']],on=['state','cell_id_10km'],how='left')
 opportunity['evidence_level']=1; opportunity['outcome_type']='candidate for field verification'; opportunity['independent_evidence_layers']=1
 opportunity['why_prioritized']='high lower-bound archaeological score + low modeled documentation propensity'
 opportunity['required_next_evidence']='independent historical feature or expert chip review, then permitted field verification'
 opportunity.sort_values(['state','blind_spot_score'],ascending=[True,False]).groupby('state').head(10).to_csv(ROOT/'results/tables/high_value_candidate_portfolio.csv',index=False)
 protection=forecast.copy(); protection['outcome_type']='known-site construction-pressure screening'; protection['evidence_level']='not applicable: known inventory site'; protection['why_prioritized']='highest robust-trend projected built-pressure growth within 2 km'; protection['required_next_evidence']='planning/quarry records, high-resolution change review and field condition assessment'
 protection.sort_values(['state','forecast_pressure_score'],ascending=[True,False]).groupby('state').head(10).to_csv(ROOT/'results/tables/high_value_conservation_portfolio.csv',index=False)
 pd.DataFrame([{'claim':'new archaeological discovery','supported':False,'reason':'no expert or field verification and no independent historical convergence layer'},{'claim':'lost city or empire identified','supported':False,'reason':'coarse susceptibility cells cannot establish settlement identity, chronology, scale or political affiliation'},{'claim':'retrospective recovery of dense withheld clusters','supported':True,'reason':'twelve known clusters were excluded with spatial buffers and compared with random and proximity baselines'},{'claim':'field-verification candidates ranked','supported':True,'reason':'generalized ranking is traceable to model, uncertainty and documentation-propensity outputs'},{'claim':'known-site construction-pressure screen','supported':True,'reason':'annual 2016-2025 built-probability histories were backtested; ranking skill is weak and explicitly reported'}]).to_csv(ROOT/'results/tables/candidate_claims_register.csv',index=False)
if __name__=='__main__': main()
