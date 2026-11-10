"""Export annual construction-pressure histories around known sites to private Drive."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,yaml,ee,pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def main():
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text()); ee.Initialize(project=cfg['gee']['project']); d=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon'])
 feats=[]
 for r in d.itertuples():
  key=hashlib.sha256(f'{r.source}:{r.source_id}'.encode()).hexdigest()[:16]
  feats.append(ee.Feature(ee.Geometry.Point([float(r.lon),float(r.lat)]),{'site_key':key,'state':r.state,'site_class':r._10}))
 sites=ee.FeatureCollection(feats); rows=[]
 for year in range(2016,2026):
  im=ee.ImageCollection(cfg['gee']['datasets']['dynamic_world']).filterDate(f'{year}-01-01',f'{year+1}-01-01').select('built').mean().focalMean(radius=2000,units='meters').rename('built_probability')
  fc=im.sampleRegions(collection=sites,properties=['site_key','state','site_class'],scale=1000,tileScale=8,geometries=False).map(lambda f:f.set('year',year))
  rows.append(fc)
 allrows=ee.FeatureCollection(rows).flatten(); task=ee.batch.Export.table.toDrive(collection=allrows,description='lostscape_site_damage_history',folder='lostscape_south_private',fileNamePrefix='site_damage_history_2016_2025',fileFormat='CSV'); task.start()
 rec={'task_id':task.id,'description':'lostscape_site_damage_history','sites':len(d),'years':'2016-2025','buffer_m':2000,'scale_m':1000,'pressure':'Dynamic World built probability only; quarry unavailable'}
 out=ROOT/'results/tasks'; stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); (out/f'site_damage_task_{stamp}.json').write_text(json.dumps(rec,indent=2)); print(json.dumps(rec,indent=2))
if __name__=='__main__': main()
