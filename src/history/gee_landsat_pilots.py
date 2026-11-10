"""Submit approved Landsat Collection-2 pilot pressure time series to private Drive."""
from pathlib import Path
from datetime import datetime,timezone
import json,yaml,ee
ROOT=Path(__file__).resolve().parents[2]
PILOTS={'chennai_south':[79.90,12.60,80.25,13.00],'tirupati_srikalahasti':[79.75,13.30,80.10,13.70],'thrissur_belt':[75.85,10.40,76.40,10.85]}
def prep(img):
 qa=img.select('QA_PIXEL'); clear=qa.bitwiseAnd(1<<3).eq(0).And(qa.bitwiseAnd(1<<4).eq(0))
 sensor=ee.String(img.get('SPACECRAFT_ID')); modern=sensor.match('LANDSAT_8|LANDSAT_9').length().gt(0)
 blue=ee.Image(ee.Algorithms.If(modern,img.select('SR_B2'),img.select('SR_B1'))).multiply(.0000275).add(-.2)
 red=ee.Image(ee.Algorithms.If(modern,img.select('SR_B4'),img.select('SR_B3'))).multiply(.0000275).add(-.2)
 nir=ee.Image(ee.Algorithms.If(modern,img.select('SR_B5'),img.select('SR_B4'))).multiply(.0000275).add(-.2)
 swir=ee.Image(ee.Algorithms.If(modern,img.select('SR_B6'),img.select('SR_B5'))).multiply(.0000275).add(-.2)
 ndvi=nir.subtract(red).divide(nir.add(red)).rename('ndvi'); ndbi=swir.subtract(nir).divide(swir.add(nir)).rename('ndbi')
 bare=swir.add(red).subtract(nir.add(blue)).divide(swir.add(red).add(nir).add(blue)).rename('bsi')
 return ee.Image.cat([ndvi,ndbi,bare]).updateMask(clear)
def collection(geom,start,end):
 ids=['LANDSAT/LT05/C02/T1_L2','LANDSAT/LE07/C02/T1_L2','LANDSAT/LC08/C02/T1_L2','LANDSAT/LC09/C02/T1_L2']
 c=ee.ImageCollection(ids[0])
 for x in ids[1:]: c=c.merge(ee.ImageCollection(x))
 return c.filterBounds(geom).filterDate(start,end).filter(ee.Filter.calendarRange(1,4,'month')).map(prep)
def main():
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text()); ee.Initialize(project=cfg['gee']['project']); tasks=[]
 for name,bounds in PILOTS.items():
  geom=ee.Geometry.Rectangle(bounds)
  feats=[]
  for year in range(1985,2026,5):
   c=collection(geom,f'{year}-01-01',f'{min(year+5,2026)}-01-01'); im=c.median()
   vals=im.reduceRegion(ee.Reducer.mean().combine(ee.Reducer.stdDev(),sharedInputs=True),geom,1000,maxPixels=1e8)
   feats.append(ee.Feature(None,vals.combine({'pilot':name,'period_start':year,'period_end':min(year+4,2025),'image_count':c.size()})))
  task=ee.batch.Export.table.toDrive(collection=ee.FeatureCollection(feats),description=f'lostscape_history_{name}',folder='lostscape_south_private',fileNamePrefix=f'landsat_history_{name}',fileFormat='CSV'); task.start(); tasks.append({'pilot':name,'task_id':task.id})
 out=ROOT/'results/tasks'; out.mkdir(exist_ok=True); stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); (out/f'history_tasks_{stamp}.json').write_text(json.dumps(tasks,indent=2)); print(json.dumps(tasks,indent=2))
if __name__=='__main__': main()
