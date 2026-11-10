"""Analyse Landsat pilot indices without equating spectral trends to heritage loss."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress,t
ROOT=Path(__file__).resolve().parents[2]
def main():
 files=sorted((ROOT/'data/private').glob('landsat_history_*.csv')); rows=[]; frames=[]
 for p in files:
  d=pd.read_csv(p); d=d[d.period_start<2025].copy(); frames.append(d)
  for metric in ['ndvi_mean','ndbi_mean','bsi_mean']:
   r=linregress(d.period_start,d[metric]); crit=t.ppf(.975,len(d)-2); rows.append({'pilot':d.pilot.iloc[0],'metric':metric,'periods':len(d),'images':int(d.image_count.sum()),'start_year':int(d.period_start.min()),'end_year':int(d.period_end.max()),'slope_per_decade':r.slope*10,'ci95_low':(r.slope-crit*r.stderr)*10,'ci95_high':(r.slope+crit*r.stderr)*10,'p_value':r.pvalue})
 out=ROOT/'results/tables'; pd.DataFrame(rows).to_csv(out/'landsat_pilot_trends.csv',index=False)
 d=pd.concat(frames); fig,axs=plt.subplots(1,3,figsize=(12,3.7),sharex=True)
 for ax,(metric,label) in zip(axs,[('ndvi_mean','NDVI'),('ndbi_mean','NDBI'),('bsi_mean','BSI')]):
  for name,g in d.groupby('pilot'): ax.plot(g.period_start,g[metric],marker='o',label=name)
  ax.set_title(label); ax.set_xlabel('Five-year period start')
 axs[0].legend(fontsize=7); fig.tight_layout(); fig.savefig(ROOT/'results/figures/landsat_pilot_trends.png',dpi=300); fig.savefig(ROOT/'results/figures/landsat_pilot_trends.pdf'); plt.close(fig)
 pd.DataFrame([{'quantity':'share of earlier-visible heritage features lost/damaged','status':'not_estimable','reason':'no georeferenced historical feature inventory or completed manual before/after verification'},{'quantity':'heritage-loss rate by pressure type','status':'not_estimable','reason':'spectral pilot means cannot identify individual archaeological features or causal pressure'}]).to_csv(out/'heritage_loss_availability.csv',index=False)
if __name__=='__main__': main()
