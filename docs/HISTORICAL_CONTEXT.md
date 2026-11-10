# Documented historical context and claim boundary

This file separates documented historical places from LostScape-South model outputs. It is contextual documentation, not a manuscript and not evidence that the model discovered an empire, city, culture, or period.

## Authoritative reference cases

| State | Documented context | Authoritative source | Relationship to this project |
|---|---|---|---|
| Karnataka | Hampi preserves the remains of Vijayanagara, the former capital of the Vijayanagara empire. | UNESCO World Heritage Centre, *Group of Monuments at Hampi*, https://whc.unesco.org/en/list/241/ (accessed 2026-11-10) | A known-city spatial-withholding test. The model was denied the cluster and a 75-km training buffer. This is validation against a known landscape, not discovery. |
| Andhra Pradesh | Amaravati is an officially managed archaeological landscape associated in ASI documentation with the Amaravati monuments and museum. | Archaeological Survey of India, Amaravati Circle, https://asi.nic.in/pages/Amaravati-Circle (accessed 2026-11-10) | Inventory context only. No model output is assigned a Satavahana or other cultural identity. |
| Tamil Nadu | The Great Living Chola Temples document major royal centres and architectural achievements of the Chola empire. | UNESCO World Heritage Centre, *Great Living Chola Temples*, https://whc.unesco.org/en/list/250/ (accessed 2026-11-10) | Historical context only. These known monuments are not new model discoveries and do not label nearby candidates as Chola. |
| Kerala | The Government of Kerala's Muziris Heritage Project documents the North Paravur–Kodungallur heritage landscape and its association with long-distance trade and Chera history. | Kerala Tourism, *Muziris Heritage Conservation Project*, https://www.keralatourism.org/muziris/muziris-project (accessed 2026-11-10) | Historical context only. The project has not localized ancient Muziris, reconstructed its extent, or assigned candidate cells to the Chera polity. |

## What remote sensing and machine learning identify here

The system ranks coarse cells by similarity to the environmental and Earth-observation contexts of open-inventory records. Inputs include seasonal Sentinel-2 vegetation and water indices, Sentinel-1 backscatter, terrain, rainfall, land cover, built probability, and Landsat change summaries. Logistic regression, random forest, histogram gradient boosting, positive–unlabeled bagging, calibration, conformal diagnostics, and ensemble uncertainty are evaluated with spatial/state holdouts.

These methods can support:

- recovery tests for already documented sites withheld from training;
- prioritization of generalized cells for expert inspection and permitted survey;
- identification of documentation blind spots;
- screening of modern construction pressure near documented sites.

They cannot, without independent archaeological evidence:

- establish that a spectral or terrain signal is cultural rather than natural or modern;
- determine chronology, cultural affiliation, function, or legal status;
- distinguish a city, settlement, burial, tank, quarry, or field feature reliably at the current coarse scale;
- prove that an unverified feature belongs to Vijayanagara, Chola, Satavahana, Chera, or any other polity;
- support the phrase “lost empire discovered.”

## Required chain for a future discovery claim

1. A prospectively frozen candidate and model version.
2. Independent evidence not used by the model, such as a licensed historical map/CORONA feature or specialist image interpretation.
3. Blinded archaeological review with recorded agreement.
4. Permission from the relevant landowner and heritage authority.
5. Non-invasive field verification, followed where appropriate by authorized archaeological investigation.
6. Dating and culturally diagnostic evidence before assigning chronology or affiliation.

Until that chain is complete, public outputs remain “candidates for field verification.”
