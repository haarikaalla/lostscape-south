from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def test_forecast_is_generalized_and_benchmarked():
 cells=pd.read_csv(ROOT/'results/tables/site_damage_forecast_cells.csv')
 assert {'state','cell_id_10km','model_selected','change_low_90','change_high_90'}.issubset(cells)
 assert not {'latitude','longitude','lat','lon','site_key'}.intersection(cells.columns)
 comparison=pd.read_csv(ROOT/'results/tables/site_damage_forecast_model_comparison.csv')
 assert {'persistence','linear_trend','robust_theil_sen','hgb_temporal_context'}.issubset(set(comparison.model))

def test_discovery_claims_are_not_promoted():
 claims=pd.read_csv(ROOT/'results/tables/candidate_claims_register.csv')
 unsupported={'new archaeological discovery','lost city or empire identified'}
 rows=claims[claims.claim.isin(unsupported)]
 assert len(rows)==2
 assert not rows.supported.astype(bool).any()

def test_blind_spots_have_propensity_and_no_coordinates():
 blind=pd.read_csv(ROOT/'results/tables/survey_blind_spots.csv')
 assert {'documentation_propensity','documentation_propensity_sd','probability_lower_90'}.issubset(blind)
 assert not {'latitude','longitude','lat','lon'}.intersection(blind.columns)

def test_pseudo_discovery_is_retrospective_and_generalized():
    result=pd.read_csv(ROOT/'results/tables/pseudo_discovery_cluster_tests.csv')
    assert {'full_hgb','random','distance_to_remaining_known'}.issubset(set(result.method))
    assert result.state.nunique()==4
    assert not {'latitude','longitude','lat','lon','name'}.intersection(result.columns)
    scope=pd.read_csv(ROOT/'results/tables/pseudo_discovery_scope.csv')
    prospective=scope[scope.interpretation.eq('prospective archaeological discovery')]
    assert len(prospective)==1 and not prospective.supported.astype(bool).iloc[0]
