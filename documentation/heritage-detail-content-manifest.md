# HeritageAI — Heritage Detail Content Manifest

## Purpose

This document defines the historical timeline and related-heritage content that will be populated through the existing HeritageAI admin APIs.

No database records are created by this document.

---

# Historical Timeline Content

## Angkor Wat

1. **9th century** — Angkor develops as the centre of the Khmer Kingdom.
2. **12th century** — Angkor Wat emerges as one of the major monumental temples of the Khmer capital.
3. **12th–13th centuries** — Successive Khmer rulers expand the monumental and hydraulic landscape, including Angkor Thom and Bayon.
4. **15th century** — Angkor's period as the principal Khmer political centre comes to an end.

## Petra

1. **Prehistoric period** — The Petra region is inhabited before the rise of the Nabataean city.
2. **Hellenistic period** — Petra develops into the rock-cut capital and caravan centre of the Nabataeans.
3. **106 CE** — Petra and the Nabataean kingdom come under Roman control.
4. **19th century** — Petra becomes known internationally after its rediscovery by European travellers.

## Konark Sun Temple

1. **1238–1264 CE** — Reign of Narasimha Deva I, under whom the Sun Temple belongs.
2. **13th century** — The monumental Sun Temple is established as a major expression of Kalingan architecture.
3. **19th century** — The principal sanctuary's great tower/shikhara is already lost by this period.
4. **1984** — Konark is inscribed on the UNESCO World Heritage List.

## Brihadeeswarar Temple

1. **1003–1004 CE** — Construction of the Brihadisvara Temple is inaugurated under Rajaraja I.
2. **1009–1010 CE** — The temple is consecrated.
3. **c. 13th century** — The separate Amman shrine is added later than the principal temple.
4. **1987** — Brihadisvara becomes part of the UNESCO World Heritage listing for the Great Living Chola Temples.

## Hampi

1. **14th century** — Vijayanagara develops Hampi as its capital.
2. **14th–16th centuries** — Hampi develops into a major urban, royal, sacred and defensive complex.
3. **16th century** — The Vijayanagara capital reaches its historic mature form and monumental landscape.
4. **1986** — Hampi is inscribed on the UNESCO World Heritage List.

## Acropolis of Athens

1. **5th century BCE** — Athens enters the period associated with the great classical rebuilding of the Acropolis.
2. **5th century BCE** — The Parthenon is constructed.
3. **5th century BCE** — The Erechtheon, Propylaea and Temple of Athena Nike form part of the major monument group.
4. **1987** — The Acropolis is inscribed on the UNESCO World Heritage List.

## Ellora Caves

1. **5th–8th centuries CE** — The earliest Buddhist caves are excavated.
2. **7th–10th centuries** — The Brahmanical cave group develops, including Kailasa Cave 16.
3. **9th–12th centuries** — The Jain caves form the final major excavation phase.
4. **1983** — Ellora is inscribed on the UNESCO World Heritage List.

## Ajanta Caves

1. **2nd century BCE** — The first major phase of Buddhist excavation begins.
2. **1st century BCE** — The early Satavahana phase continues.
3. **5th–6th centuries CE** — A second major phase produces richly decorated caves during the Vakataka period.
4. **1983** — Ajanta is inscribed on the UNESCO World Heritage List.

## Machu Picchu

1. **Mid-15th century** — Machu Picchu is established as an Inca highland urban complex.
2. **15th century** — Its terraces, stone architecture and water-management systems develop.
3. **1911** — The site enters modern international archaeological attention.
4. **1983** — Machu Picchu is inscribed as a UNESCO World Heritage property.

## Taj Mahal

1. **1632** — Construction begins under Shah Jahan.
2. **1648** — The principal Taj Mahal complex is completed.
3. **1653** — Additional architectural works are completed subsequently.
4. **1983** — The Taj Mahal is inscribed on the UNESCO World Heritage List.

---

# Related Heritage Relationships

| Source | Target | Relation Type | Description |
|---|---|---|---|
| Angkor Wat | Hampi | RELATED_TO | Both preserve extensive sacred, urban and monumental landscapes shaped by major South Asian cultural traditions. |
| Angkor Wat | Konark Sun Temple | RELATED_TO | Both are monumental temple complexes whose architecture expresses religious cosmology. |
| Petra | Acropolis of Athens | RELATED_TO | Petra combines local traditions with Hellenistic architectural influence; the Acropolis represents the classical Greek architectural tradition. |
| Petra | Taj Mahal | RELATED_TO | Both are major monumental heritage sites whose architecture combines local traditions with wider cultural influences. |
| Konark Sun Temple | Brihadeeswarar Temple | RELATED_TO | Both are major medieval Indian temple complexes representing highly developed regional architectural traditions. |
| Konark Sun Temple | Hampi | RELATED_TO | Both are major surviving expressions of India's medieval temple and urban heritage. |
| Brihadeeswarar Temple | Konark Sun Temple | RELATED_TO | Shared importance as monumental Hindu temple architecture. |
| Brihadeeswarar Temple | Hampi | RELATED_TO | Both preserve major South Indian temple and cultural landscapes. |
| Hampi | Brihadeeswarar Temple | RELATED_TO | Both reflect major developments in South Indian monumental architecture. |
| Hampi | Machu Picchu | RELATED_TO | Both preserve sophisticated historic highland urban environments. |
| Acropolis of Athens | Petra | RELATED_TO | Both demonstrate interaction between regional architectural traditions and the wider Hellenistic world. |
| Acropolis of Athens | Angkor Wat | RELATED_TO | Both are major monumental complexes with strong religious and symbolic architectural programmes. |
| Ellora Caves | Ajanta Caves | RELATED_TO | Both are major rock-cut Buddhist heritage complexes in Maharashtra. |
| Ellora Caves | Konark Sun Temple | RELATED_TO | Both demonstrate exceptional Indian monumental and sculptural traditions. |
| Ajanta Caves | Ellora Caves | RELATED_TO | Both are major rock-cut heritage complexes in Maharashtra. |
| Ajanta Caves | Brihadeeswarar Temple | RELATED_TO | Both represent major achievements in Indian religious art and architecture. |
| Machu Picchu | Hampi | RELATED_TO | Both preserve complex historic urban landscapes integrated with difficult terrain. |
| Machu Picchu | Angkor Wat | RELATED_TO | Both are major archaeological landscapes associated with sophisticated historic civilizations. |
| Taj Mahal | Red Fort | ASSOCIATED_WITH | Both are major Mughal monuments associated with imperial architecture in northern India. |
| Taj Mahal | Brihadeeswarar Temple | RELATED_TO | Both are landmark Indian monuments representing exceptional architectural and artistic achievement. |

---

# Implementation Rules

1. All timeline records must be created through the existing `/heritage-sites/{site_id}/historical-events` admin endpoint.
2. All relation records must be created through the existing `/heritage-sites/{site_id}/relations` admin endpoint.
3. All inserted records must use `is_active = true`.
4. Timeline records should use ordered `display_order` values beginning at `0`.
5. Timeline records should use the appropriate `date_precision` rather than inventing exact dates.
6. Relations must not point a site to itself.
7. Existing records must be checked before insertion to prevent duplicates.
8. No frontend source changes are part of this data-population task.

---

# Existing Data

Red Fort currently contains:
- 6 historical timeline events
- 1 related heritage-site relation

The remaining 10 sites require timeline and relation population.

---

# Approval Gate

This manifest must be reviewed before database insertion.

No database records are created by this document.
