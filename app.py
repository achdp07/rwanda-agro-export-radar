import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Rwanda Agro-Export Radar | NISR Hackathon",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for polished UI
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------
@st.cache_data
def load_radar_data():
  # Update this path if running locally or on Streamlit Cloud
  df = pd.read_csv("ranked_agro_radar.csv")
  return df


try:
  df_radar = load_radar_data()
except Exception as e:
  st.error("⚠️ `ranked_agro_radar.csv` not found. Please ensure the dataset is in the working directory.")
  st.stop()

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown(
    "<div class='main-header'>🌾 Rwanda Agro-Export & High-Value Processing"
    " Radar</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sub-header'>Fusing <b>NISR Agricultural Microdata</b> with"
    " Economic Complexity (PCI) models to identify optimal geographic hubs for"
    " high-value agro-processing investments. Grounded in <b>Vision 2050</b>"
    " & <b>RDB 2025–2030 Priorities</b>.</div>",
    unsafe_allow_html=True,
)
st.divider()

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Radar Investment Filters")

# Filter 1: Commodity Selection
crop_list = ["All Commodities"] + sorted(
    df_radar["crop_name"].dropna().unique().tolist()
)
selected_crop = st.sidebar.selectbox("Target Commodity", crop_list)

# Filter 2: District Selection
district_list = ["All Districts"] + sorted(
    df_radar["district_name"].dropna().unique().tolist()
)
selected_district = st.sidebar.selectbox("Target District", district_list)

# Filter 3: Minimum APFI Score Slider
min_apfi = st.sidebar.slider(
    "Minimum Feasibility Score (APFI)",
    min_value=0.0,
    max_value=float(df_radar["apfi_score"].max()),
    value=0.2,
    step=0.05,
)

# Apply Filters
filtered_df = df_radar.copy()
if selected_crop != "All Commodities":
  filtered_df = filtered_df[filtered_df["crop_name"] == selected_crop]
if selected_district != "All Districts":
  filtered_df = filtered_df[filtered_df["district_name"] == selected_district]
filtered_df = filtered_df[filtered_df["apfi_score"] >= min_apfi]

# ---------------------------------------------------------
# Key Performance Metrics (KPI Cards)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(
      label="Total Filtered Opportunities",
      value=f"{len(filtered_df)} Zones",
  )

with col2:
  top_district = (
      filtered_df.sort_values(by="apfi_score", ascending=False).iloc[
          "district_name"
      ]
      if not filtered_df.empty
      else "N/A"
  )
  st.metric(label="Top Recommended District", value=top_district)

with col3:
  max_score = (
      f"{filtered_df['apfi_score'].max():.3f}"
      if not filtered_df.empty
      else "0.0"
  )
  st.metric(label="Peak APFI Feasibility Score", value=max_score)

with col4:
  top_margin = (
      filtered_df.sort_values(by="apfi_score", ascending=False).iloc[
          "export_tier"
      ]
      if not filtered_df.empty
      else "N/A"
  )
  st.metric(label="Target Export Value Boost", value=top_margin)

st.divider()

# ---------------------------------------------------------
# Interactive Visualizations
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Feasibility Rankings",
    "🗺️ Spatial Harvest Distribution",
    "📋 Raw Radar Dataset",
])

with tab1:
  st.subheader("Top Agro-Processing Investment Hubs by District")
  if not filtered_df.empty:
    top_chart_df = filtered_df.sort_values(
        by="apfi_score", ascending=False
    ).head(15)

    fig_bar = px.bar(
        top_chart_df,
        x="apfi_score",
        y="district_name",
        color="crop_name",
        orientation="h",
        hover_data=[
            "production_tonnes",
            "processing_line",
            "export_tier",
        ],
        title="Agro-Processing Feasibility Index (APFI) by District & Crop",
        labels={
            "apfi_score": "Feasibility Index Score",
            "district_name": "District",
            "crop_name": "Commodity",
        },
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"}, height=500
    )
    st.plotly_chart(fig_bar, use_container_width=True)
  else:
    st.warning("No data available matching the selected filters.")

with tab2:
  st.subheader("Harvested Volume (Metric Tonnes) vs. Processing Score")
  if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x="production_tonnes",
        y="apfi_score",
        size="pci_weight",
        color="crop_name",
        hover_name="district_name",
        text="district_name",
        title="NISR Raw Volume vs. Value-Addition Potential",
        labels={
            "production_tonnes": "NISR Harvested Tonnes",
            "apfi_score": "Processing Feasibility Score",
        },
        log_x=True,
    )
    fig_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_scatter, use_container_width=True)
  else:
    st.warning("No data available matching the selected filters.")

with tab3:
  st.subheader("Complete Model Output Dataset")
  st.dataframe(filtered_df, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# Investment Recommendation Card
# ---------------------------------------------------------
st.subheader("💡 Strategic Investment Brief (RDB / MINAGRI Action Card)")

if not filtered_df.empty:
  best_match = filtered_df.sort_values(by="apfi_score", ascending=False).iloc

  st.success(f"""
    ### 🎯 Priority Investment Hub: **{best_match['district_name']} District**
    * **Target Commodity:** {best_match['crop_name']}
    * **NISR Raw Baseline Harvest:** `{best_match['production_tonnes']:,.1f} Metric Tonnes`
    * **Recommended Processing Line:** **{best_match['processing_line']}**
    * **Value-Addition Category:** {best_match['export_tier']}
    * **Model Feasibility Index Score:** `{best_match['apfi_score']}`
    
    ---
    **Strategic Alignment:** Shifting from exporting raw **{best_match['crop_name']}** to establishing a **{best_match['processing_line']}** in **{best_match['district_name']}** directly aligns with **RDB's 2025–2030 Strategy** to increase product complexity (PCI) and **Vision 2050** export goals.
    """)
else:
  st.info("Adjust your filters to display strategic recommendations.")

# Footer
st.caption(
    "NISR 2026 Big Data Hackathon | Track 1: Agricultural Productivity | Team"
    " Menace 2.0"
)