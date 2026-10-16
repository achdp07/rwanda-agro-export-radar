# 🌾 Rwanda Agro-Export & High-Value Processing Radar

> **NISR 2026 Big Data Hackathon Submission** | **Track 1: Agricultural Productivity**

An interactive decision-support platform fusing **National Institute of Statistics of Rwanda (NISR) Agricultural Household Survey (AHS 2024)** microdata with global **Product Complexity Indices (PCI)** and GIS spatial layers. The platform identifies optimal geographic hubs across Rwanda's 30 districts for high-value agro-processing investments, directly advancing the goals of **Vision 2050** and the **Rwanda Development Board (RDB) 2025–2030 Strategy**.

---

## 🌟 Key Features

- **Interactive Investment Map**: Multi-layer spatial visualization of Rwanda's 30 districts mapped against raw harvest availability and processing feasibility scores.
- **Agro-Processing Feasibility Index (APFI)**: A weighted multi-criteria decision model combining local NISR raw crop production volumes, economic complexity weights (PCI), and high-value export margins.
- **Investor & Policy Decision Cards**: Instant, actionable investment briefs for RDB officers, MINAGRI planners, and private investors detailing recommended facility types (e.g., specialty coffee roasting, essential oil extraction, organic fruit drying).
- **Dynamic Filtering**: Filter investment opportunities by target commodity, district, or minimum APFI feasibility threshold.

---

## 🎯 Strategic Alignment with National Priorities

1. **NISR Hackathon Track 1 (Agricultural Productivity)**: Leverages official NISR survey microdata to solve real-world agricultural productivity, post-harvest processing, and export market challenges.
2. **RDB 5-Year Strategy (2025–2030)**: Supports RDB's strategic mandate to double private investment to \$4.6B and increase export revenues to \$7.3B by transitioning from low-complexity raw commodity exports (unroasted coffee, raw tea) to high-complexity processed goods (specialty packaging, essential oils).
3. **Vision 2050**: Aligns with the *Agriculture for Wealth Creation* pillar, aiming to quadruple traditional export value and scale high-value niche produce for continental and global markets.

---

## 🛠️ Data Sources & Methodology

### 1. Primary Baseline Data (NISR)
- **Dataset**: NISR Agricultural Household Survey (AHS 2024) Section 3 & 4 Microdata (`.dta` Stata format).
- **Processing**: Melted multi-crop plot slots (`s3_q4_1` to `s3_q4_7`) and incorporated custom text entries (`s3q4_o1`) to capture 100% of harvested volumes across all inter-cropped plots.
- **Weighting**: Applied official household survey expansion weights (`weight`) to compute accurate district-level production totals in metric tonnes.

### 2. External & Open Datasets
- **Product Complexity Index (PCI)**: Integrated Harmonized System (HS 4-digit) economic complexity weights from the UN Comtrade / Atlas of Economic Complexity database.
- **Spatial GIS Boundaries**: Mapped using official Rwanda District GeoJSON polygons from open repositories (HDX / NISR Geoportal).

### 3. APFI Model Formula
\\[\text{APFI Score} = 0.50 \cdot (\text{NISR Yield Score}) + 0.35 \cdot (\text{Normalized PCI Weight}) + 0.15 \cdot (\text{Export Strategic Boost})\\]

---

## 🚀 Quickstart & Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/achdp07/rwanda-agro-export-radar
   cd rwanda-agro-export-radar