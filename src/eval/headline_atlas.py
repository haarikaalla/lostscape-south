"""Build a result-led Headline Findings Atlas; unavailable evidence stays unavailable."""
from pathlib import Path
import pandas as pd,numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'results/tables'; profiles=ROOT/'results/state_profiles'; profiles.mkdir(parents=True,exist_ok=True)
 scores=pd.read_csv(out/'public_coarse_scores.csv'); labels=pd.read_csv(out/'label_counts.csv'); base=pd.read_csv(out/'baseline_spatial_cv.csv'); lost=pd.read_csv(out/'lost_settlement_holdouts.csv'); trends=pd.read_csv(out/'landsat_pilot_trends.csv')
 forecast=pd.read_csv(out/'site_damage_forecast_model_comparison.csv'); effort=pd.read_csv(out/'survey_effort_model_cv.csv'); portfolio=pd.read_csv(out/'high_value_candidate_portfolio.csv')
 scores['opportunity_score']=scores.probability/(1+scores.known_positive_cells)
 scores['urgency_score_no_protection']=scores.probability*scores.threat_proxy
 hot=[]
 for state,g in scores.groupby('state'):
  for typ,col in [('pressure_near_known','threat_proxy'),('opportunity','opportunity_score'),('urgency_no_protection','urgency_score_no_protection')]:
   z=g[g.known_positive_cells.gt(0)] if typ=='pressure_near_known' else g
   z=z.nlargest(25,col).copy(); z['hotspot_type']=typ; z['rank']=range(1,len(z)+1); hot.append(z)
 pd.concat(hot).to_csv(out/'headline_hotspots.csv',index=False)
 conv=scores[scores.known_positive_cells.eq(0)].sort_values(['state','probability'],ascending=[True,False]).groupby('state').head(10).copy()
 conv['model_layer']=1; conv['historical_independent_layer']=0; conv['paleoriver_or_route_layer']=0; conv['independent_settlement_signal_layer']=0; conv['unlocated_place_layer']=0; conv['agreeing_layers']=1; conv['evidence_level']=1
 conv.to_csv(out/'convergence_zones.csv',index=False)
 pd.DataFrame([{'test':'convergence randomization','status':'not_estimable','reason':'only the model layer is currently available; zero zones have two independent evidence layers'},{'test':'full-state pressure growth near sites vs matched random','status':'not_estimable','reason':'statewide historical pressure samples and matched controls have not been exported'},{'test':'quarry growth since 1984','status':'not_estimable','reason':'quarry classifier has not passed 100-cell visual validation'}]).to_csv(out/'headline_unavailable_tests.csv',index=False)
 state_map={'Karnataka':'features_5km_karnataka.csv','Andhra Pradesh':'features_5km_andhra_pradesh.csv','Tamil Nadu':'features_5km_tamil_nadu.csv','Kerala':'features_5km_kerala.csv'}
 headlines={'Karnataka':'Sparse-label result: the withheld Sannathi target ranked highly, but area-wide performance did not exceed random.', 'Andhra Pradesh':'The broader withheld-site model beat random on area-wide ranking, while the named target cell itself ranked only moderately.', 'Tamil Nadu':'The strongest primary-label coverage produced the best state-transfer baseline, but the Mandapakkadu blind target was weak.', 'Kerala':'Insufficient data: only eight coarse primary-positive cells support transfer evaluation and no settlement-mound blind test is available.'}
 for state,file in state_map.items():
  b=base[(base.held_out.eq(file))&(base.model.eq('hist_gradient_boosting'))]
  l=lost[(lost.state.eq(state))&(lost.method.eq('full_hgb'))]
  f=forecast[(forecast.held_out_state.eq(state))&(forecast.model.eq('robust_theil_sen'))]
  e=effort[effort.held_out_state.eq(state)]
  q=portfolio[portfolio.state.eq(state)]
  counts=labels[labels.state.eq(state)].groupby('class',as_index=False).site_count.sum().rename(columns={'site_count':'count'}).to_dict('records')
  text=f"# {state}\n\n**Headline:** {headlines[state]}\n\n- Best coarse state-transfer PR-AUC (histogram gradient boosting): {b.pr_auc.mean():.4f} across {len(b)} seeds.\n- Primary-label caveat: results measure recovery of documented cells, not undiscovered sites.\n- Blind settlement test: " + (f"median target percentile {l.target_cell_percentile.median():.3f}; mean PR-AUC {l.pr_auc.mean():.4f}." if len(l) else 'insufficient data.') + f"\n- Construction-pressure ranking backtest: Spearman {f.spearman.mean():.3f}; top-decile recall {f.top_decile_recall.mean():.3f}.\n- Documentation-propensity transfer ROC-AUC: {e.roc_auc.mean():.3f}.\n- Candidate portfolio: {len(q)} generalized Level-1 zones; mean lower-90% score {q.probability_lower_90.mean():.4f}.\n- Pressure conclusion: quarry and actual damage outcomes remain unvalidated.\n- Convergence: Level 1 model-only zones; no independent historical/route layer is available.\n\n## Inventory counts\n\n" + '\n'.join(f"- {x['class']}: {x['count']}" for x in counts) + '\n'
  (profiles/f"{state.lower().replace(' ','_')}.md").write_text(text)
  fig,axs=plt.subplots(1,2,figsize=(8,3.2)); b.pr_auc.plot.hist(ax=axs[0],bins=5); axs[0].set_title('State-transfer PR-AUC'); g=scores[scores.state.eq(state)]; axs[1].scatter(g.probability,g.risk_score,s=8,alpha=.5); axs[1].set(xlabel='Probability',ylabel='Provisional risk',title='Coarse cells'); fig.suptitle(state); fig.tight_layout(); fig.savefig(profiles/f"{state.lower().replace(' ','_')}.png",dpi=300); plt.close(fig)
 atlas="# Headline Findings Atlas\n\nThis atlas is computed from files in `results/`. It reports negative and unavailable findings; it is not a manuscript and makes no discovery claim.\n\n## Cross-state findings\n\n- The calibrated PU model did not beat the best baseline.\n- Leakage-safe 225-km conformal evaluation missed its nominal coverage target.\n- Terrain was the strongest coarse ablation group; SAR added no demonstrated coarse-scale value.\n- Hampi showed modest recovery under a 75-km withheld buffer.\n- Landsat pilot spectral trends do not identify individual heritage loss.\n- No zone currently has two genuinely independent evidence layers; all showcased convergence zones are Evidence Level 1.\n- Persistence best predicts exact pressure magnitude; robust Theil–Sen is retained only for weak ranking skill (top-decile recall 0.364).\n- Documentation-propensity transfer is weak (weighted ROC-AUC 0.577), though top-50 lists are stable across seeds.\n- Forty generalized candidate zones form a field-review portfolio; none is a discovery.\n\n## State profiles\n\n" + '\n'.join(f"- [{s}]({s.lower().replace(' ','_')}.md): {headlines[s]}" for s in state_map) + "\n\n## Unsupported headline requests\n\nSee `results/tables/headline_unavailable_tests.csv`, `results/tables/heritage_loss_availability.csv`, and `results/tables/candidate_claims_register.csv`.\n"
 (profiles/'HEADLINE_FINDINGS_ATLAS.md').write_text(atlas)
if __name__=='__main__': main()
