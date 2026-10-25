import pandas as pd
import streamlit as st
from traffic_game_theory import ROUTES, simulate

st.set_page_config(page_title="Game-Theoretic Modeling of Traffic Route Selection in Smart Cities", page_icon="🚦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap");
:root { --bg:#ffffff; --panel:#ffffff; --line:#e2e8f0; --muted:#64748b; --text:#172033; --cyan:#0891b2; --blue:#2563eb; --amber:#d97706; }
.stApp { background:linear-gradient(180deg,#ffffff 0%,#f7fafc 100%); color:var(--text); font-family:"Manrope",sans-serif; }
[data-testid="stSidebar"] { background:#f1f5f9; border-right:1px solid #dbe4ee; }
[data-testid="stSidebar"] * { font-family:"Manrope",sans-serif; color:#111827 !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  color:#111827 !important;
  opacity:1 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stMarkdownContainer"] * {
  color:#111827 !important;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] [data-baseweb="input"] * {
  color:#111827 !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
  color:#111827 !important;
}
h1,h2,h3,p,label { font-family:"Manrope",sans-serif; }
h1 { letter-spacing:-1.8px; font-weight:800; }
[data-testid="stMetric"] { background:#ffffff; border:1px solid #e2e8f0; box-shadow:0 5px 20px rgba(15,23,42,.045); padding:18px 20px; border-radius:16px; }
[data-testid="stMetricLabel"] { color:#64748b !important; }
[data-testid="stMetricValue"] { color:#172033 !important; font-weight:800; }
.eyebrow { color:#0891b2; text-transform:uppercase; letter-spacing:2.5px; font-size:11px; font-weight:800; }
.hero { padding:26px 28px; border:1px solid #dbeafe; border-radius:22px; background:linear-gradient(115deg,#effaff,#ffffff 72%); box-shadow:0 10px 35px rgba(15,23,42,.06); margin:0 0 22px 0; position:relative; overflow:hidden; }
.hero h1 { font-size:clamp(25px,3vw,38px); line-height:1.12; margin:8px 0 12px; }
.hero p { color:#526477; max-width:700px; font-size:15px; line-height:1.7; margin-bottom:0; }
.signal { display:inline-block; padding:6px 10px; border-radius:99px; border:1px solid #a7f3d0; color:#047857; background:#ecfdf5; font-size:11px; font-weight:800; letter-spacing:1px; }
.section-label { color:#172033; font-size:20px; font-weight:800; letter-spacing:-.4px; margin:12px 0 4px; }
.section-sub { color:#64748b; font-size:13px; margin-bottom:14px; }
.route-card { border:1px solid #e2e8f0; background:linear-gradient(145deg,#ffffff,#f8fafc); box-shadow:0 6px 22px rgba(15,23,42,.04); border-radius:16px; padding:17px 18px; min-height:150px; }
.route-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:15px; }
.route-name { color:#172033; font-size:15px; font-weight:800; }
.route-dot { width:9px; height:9px; display:inline-block; border-radius:50%; margin-right:7px; }
.route-value { color:#172033; font-size:28px; font-weight:800; letter-spacing:-1px; }
.route-caption { color:#64748b; font-size:12px; margin-top:3px; }
.mini-bar { height:5px; background:#e2e8f0; border-radius:8px; margin-top:14px; overflow:hidden; }
.mini-fill { height:5px; border-radius:8px; }
.info-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:16px 18px; color:#475569; font-size:13px; line-height:1.65; }
.mono { font-family:"DM Mono",monospace; color:#0891b2; }
div[data-testid="stDataFrame"] { border:1px solid #20364b; border-radius:12px; overflow:hidden; }
div.stButton > button { border-radius:10px; border:1px solid #0891b2; background:#0891b2; color:#ffffff; font-weight:800; padding:10px 16px; }
div.stButton > button:hover { background:#0e7490; border-color:#0e7490; color:#ffffff; }
div[data-testid="stDownloadButton"] button { border-radius:9px; border:1px solid #cbd5e1; background:#ffffff; color:#172033; }
hr { border-color:#e2e8f0; }\n@keyframes trafficPulse { 0%,100% { box-shadow:0 0 0 0 rgba(8,145,178,.0); } 50% { box-shadow:0 0 0 7px rgba(8,145,178,.12); } }\n.signal { animation:trafficPulse 2.8s ease-in-out infinite; }\n.route-card { transition:transform .22s ease, box-shadow .22s ease; }\n.route-card:hover { transform:translateY(-4px); box-shadow:0 14px 30px rgba(15,23,42,.09); }\n.stApp, [data-testid="stSidebar"] { cursor: auto; }\n/* PNG cursor is more widely supported than SVG data cursors in Chromium. */
.stApp, .stApp * {
  cursor: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAwCAYAAABwrHhvAAABmUlEQVR4nO2YoW7DQAyG/00FCyobDh0NyBMUjxUHFLRSwZQq0qQ8QKRJVaeCSisoGC4r7l4gIM8QPFbUkWlDkab27JydRFmk/PDk8/+d787AQMu6kW64Wx9+ymK+nh6t81oH2hhrQEoDLo3v315KjT9nz9YgLMBfcxtjDoSCuLVJpDG33UdWoDg9lSR/f71ac4PQGFtUwlSFQSkiYX6KY+M6BUHJeAXc6SlzADjFsbEyRR7TT7J6AzbmZRCURABNqAfoFoAbhBgmCRszTBLRVxRXgIOQmgPKRuQGoagT1g4AAHj4Vm+tDJCnS5z3I8P6Ea4fiXKJ3wBlDgDn/Qh5umwOgDPXQnSrD/QArQO4fgRnfGRjnLHsK8pbMQMhNQe0rdiPkKfXEFJzNQAAfAwc7dbqALtsg2m2Mq5PvLkol/gNUOYAMM1W2GWb5gA4cy1Et/pAD9A6wMSbY+st2JittxB9RXEFOAipOVBhPmD6apR57fMBzkwq8goK2suBk1Tc6VkAUxKtOaf/PabjQGxUy6BSAyIZ1fZqXb9qE7U+u7/Y4AAAAABJRU5ErkJggg==") 16 4, auto !important;
}
.stApp button, .stApp a, .stApp input, .stApp [role="slider"] {
  cursor: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAwCAYAAABwrHhvAAABmUlEQVR4nO2YoW7DQAyG/00FCyobDh0NyBMUjxUHFLRSwZQq0qQ8QKRJVaeCSisoGC4r7l4gIM8QPFbUkWlDkab27JydRFmk/PDk8/+d787AQMu6kW64Wx9+ymK+nh6t81oH2hhrQEoDLo3v315KjT9nz9YgLMBfcxtjDoSCuLVJpDG33UdWoDg9lSR/f71ac4PQGFtUwlSFQSkiYX6KY+M6BUHJeAXc6SlzADjFsbEyRR7TT7J6AzbmZRCURABNqAfoFoAbhBgmCRszTBLRVxRXgIOQmgPKRuQGoagT1g4AAHj4Vm+tDJCnS5z3I8P6Ea4fiXKJ3wBlDgDn/Qh5umwOgDPXQnSrD/QArQO4fgRnfGRjnLHsK8pbMQMhNQe0rdiPkKfXEFJzNQAAfAwc7dbqALtsg2m2Mq5PvLkol/gNUOYAMM1W2GWb5gA4cy1Et/pAD9A6wMSbY+st2JittxB9RXEFOAipOVBhPmD6apR57fMBzkwq8goK2suBk1Tc6VkAUxKtOaf/PabjQGxUy6BSAyIZ1fZqXb9qE7U+u7/Y4AAAAABJRU5ErkJggg==") 16 4, pointer !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class=\"eyebrow\">🚦 TRAFFIC GAME THEORY / CONTROL ROOM</div>", unsafe_allow_html=True)
    st.markdown("## Simulation controls")
    st.caption("Tune the traffic scenario, then run the model.")
    drivers = st.slider("Number of drivers (traffic participants)", 10, 300, 100, 10)
    seed = st.number_input("Random seed (repeatable simulation)", min_value=0, max_value=100000, value=42, step=1)
    sweeps = st.slider("Maximum driver-update rounds", 10, 1000, 500, 10)
    run = st.button("▶  Run simulation", use_container_width=True)
    st.markdown("---")
    st.markdown("**MODEL**")
    st.markdown("<div class=\"info-box\">Sequential best-response dynamics<br>3 parallel routes<br>Linear congestion cost</div>", unsafe_allow_html=True)
    st.caption("All route parameters are illustrative, not live traffic data.")

if "simulation" not in st.session_state or "sim_settings" not in st.session_state:
    st.session_state.simulation = simulate(int(drivers), int(seed), int(sweeps))
    st.session_state.sim_settings = (int(drivers), int(seed), int(sweeps))
if run:
    with st.spinner("Updating the city traffic model..."):
        st.session_state.simulation = simulate(int(drivers), int(seed), int(sweeps))
        st.session_state.sim_settings = (int(drivers), int(seed), int(sweeps))

history, assignments, converged = st.session_state.simulation
counts = assignments["selected_route"].value_counts()
last = history.iloc[-1]
avg_time = float(last["average_travel_time"])
total_time = float(last["total_driver_minutes"])
used_settings = st.session_state.sim_settings

st.markdown("""
<div class="hero">
  <div class="eyebrow">SMART CITY SYSTEMS · GAME THEORY</div>
  <div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:10px;">
    <span style="font-size:34px;line-height:1;filter:drop-shadow(0 3px 4px rgba(15,23,42,.12));">🚦</span><h1 style="margin:0;">Game-Theoretic Modeling of Traffic Route Selection in Smart Cities</h1><span class="signal">● SIMULATION ACTIVE</span>
  </div>
  <p>Model how self-interested drivers distribute across a road network. As route load increases, travel time changes — creating a strategic game where every route choice affects the system.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Drivers in system", f"{len(assignments):,}")
m2.metric("Mean travel time", f"{avg_time:.2f} min")
m3.metric("Total driver-time", f"{total_time:.1f} min")
m4.metric("Stability check", "Reached" if converged else "Sweep limit")

st.markdown("<div class=\"section-label\">01 / Route network status</div>", unsafe_allow_html=True)
st.markdown("<div class=\"section-sub\">Final load and estimated travel time for each alternative route.</div>", unsafe_allow_html=True)
route_colors = {"Route A": "#55d6d0", "Route B": "#65aaff", "Route C": "#ffbf69"}
route_cards = st.columns(3)
for col, route in zip(route_cards, ROUTES):
    n = int(counts.get(route, 0))
    params = ROUTES[route]
    travel = params["base_time"] + params["congestion_factor"] * n
    share = n / max(len(assignments), 1) * 100
    color = route_colors[route]
    with col:
        st.markdown(f"""<div class="route-card">
          <div class="route-top"><span class="route-name"><span class="route-dot" style="background:{color}"></span>{route}</span><span style="color:#8da6bb;font-size:12px;">{share:.1f}% load</span></div>
          <div class="route-value">{travel:.2f}<span style="font-size:13px;color:#9ab0c4;font-weight:500;"> min</span></div>
          <div class="route-caption">{n} drivers assigned · base {params["base_time"]:.1f} min</div>
          <div class="mini-bar"><div class="mini-fill" style="width:{share:.1f}%;background:{color};"></div></div>
        </div>""", unsafe_allow_html=True)

left, right = st.columns([1, 1])
with left:
    st.markdown("<div class=\"section-label\">02 / Driver allocation</div>", unsafe_allow_html=True)
    st.markdown("<div class=\"section-sub\">How the population is distributed across routes.</div>", unsafe_allow_html=True)
    distribution = pd.DataFrame({"Drivers": [int(counts.get(r, 0)) for r in ROUTES]}, index=list(ROUTES))
    st.bar_chart(distribution, color="#2563eb", height=300)
with right:
    st.markdown("<div class=\"section-label\">03 / System travel-time trend</div>", unsafe_allow_html=True)
    st.markdown("<div class=\"section-sub\">Average estimated travel time recorded during driver updates.</div>", unsafe_allow_html=True)
    trend = history.drop_duplicates("update").set_index("update")[["average_travel_time"]]
    st.line_chart(trend, color="#0891b2", height=300)

st.markdown("<div class=\"section-label\">04 / Route cost model</div>", unsafe_allow_html=True)
st.markdown("<div class=\"section-sub\">Travel time = base time + congestion factor × drivers on route.</div>", unsafe_allow_html=True)
rows = []
for route, params in ROUTES.items():
    n = int(counts.get(route, 0))
    rows.append({"Route": route, "Base time (min)": params["base_time"], "Congestion factor": params["congestion_factor"], "Drivers": n, "Estimated time (min)": round(params["base_time"] + params["congestion_factor"] * n, 2)})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with st.expander("View driver-level assignments and export data"):
    st.dataframe(assignments, use_container_width=True, hide_index=True)
    d1, d2 = st.columns(2)
    d1.download_button("↓  Driver assignments CSV", assignments.to_csv(index=False).encode("utf-8"), "final_route_summary.csv", "text/csv", use_container_width=True)
    d2.download_button("↓  Simulation history CSV", history.to_csv(index=False).encode("utf-8"), "simulation_history.csv", "text/csv", use_container_width=True)

st.markdown("---")
st.markdown("""<div class="info-box"><span class="mono">GAME THEORY NOTE</span><br>A stable outcome means no driver switched routes during a full sweep. It is interpreted as a Nash equilibrium only if no individual driver can improve their own travel time by unilaterally changing routes. This simulation uses simplified illustrative route costs and does not represent live city traffic.</div>""", unsafe_allow_html=True)
st.caption(f"Run configuration: {used_settings[0]} drivers · seed {used_settings[1]} · max {used_settings[2]} sweeps")