import pandas as pd
import streamlit as st
from traffic_game_theory import ROUTES, simulate

st.set_page_config(page_title="UrbanFlow | Traffic Game Theory", page_icon="🚦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap");
:root { --bg:#07111d; --panel:#101f30; --line:#20364b; --muted:#9ab0c4; --text:#eef6ff; --cyan:#55d6d0; --blue:#65aaff; --amber:#ffbf69; }
.stApp { background: radial-gradient(ellipse at 70% 0%, #142c42 0%, #07111d 48%); color:var(--text); font-family:"Manrope",sans-serif; }
[data-testid="stSidebar"] { background:#0b1725; border-right:1px solid #20364b; }
[data-testid="stSidebar"] * { font-family:"Manrope",sans-serif; }
h1,h2,h3,p,label { font-family:"Manrope",sans-serif; }
h1 { letter-spacing:-1.8px; font-weight:800; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#12273a,#0d1b2a); border:1px solid #244158; padding:18px 20px; border-radius:16px; }
[data-testid="stMetricLabel"] { color:#9ab0c4 !important; }
[data-testid="stMetricValue"] { color:#f1f8ff !important; font-weight:800; }
.eyebrow { color:#55d6d0; text-transform:uppercase; letter-spacing:2.5px; font-size:11px; font-weight:800; }
.hero { padding:26px 28px; border:1px solid #244158; border-radius:22px; background:linear-gradient(115deg,rgba(19,45,65,.98),rgba(10,24,38,.96)); margin:0 0 22px 0; position:relative; overflow:hidden; }
.hero h1 { font-size:clamp(30px,4vw,46px); line-height:1.08; margin:8px 0 12px; }
.hero p { color:#afc3d5; max-width:700px; font-size:15px; line-height:1.7; margin-bottom:0; }
.signal { display:inline-block; padding:6px 10px; border-radius:99px; border:1px solid #2a5b64; color:#79e5d8; background:#10333a; font-size:11px; font-weight:800; letter-spacing:1px; }
.section-label { color:#dceaf6; font-size:20px; font-weight:800; letter-spacing:-.4px; margin:12px 0 4px; }
.section-sub { color:#8da6bb; font-size:13px; margin-bottom:14px; }
.route-card { border:1px solid #243d53; background:linear-gradient(145deg,#102237,#0b1928); border-radius:16px; padding:17px 18px; min-height:150px; }
.route-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:15px; }
.route-name { color:#f2f8ff; font-size:15px; font-weight:800; }
.route-dot { width:9px; height:9px; display:inline-block; border-radius:50%; margin-right:7px; }
.route-value { color:#f5faff; font-size:28px; font-weight:800; letter-spacing:-1px; }
.route-caption { color:#8da6bb; font-size:12px; margin-top:3px; }
.mini-bar { height:5px; background:#23384a; border-radius:8px; margin-top:14px; overflow:hidden; }
.mini-fill { height:5px; border-radius:8px; }
.info-box { background:#0d2030; border:1px solid #244158; border-radius:14px; padding:16px 18px; color:#b5c9da; font-size:13px; line-height:1.65; }
.mono { font-family:"DM Mono",monospace; color:#75ddd7; }
div[data-testid="stDataFrame"] { border:1px solid #20364b; border-radius:12px; overflow:hidden; }
div.stButton > button { border-radius:10px; border:1px solid #55d6d0; background:#55d6d0; color:#06141d; font-weight:800; padding:10px 16px; }
div.stButton > button:hover { background:#83eee5; border-color:#83eee5; color:#06141d; }
div[data-testid="stDownloadButton"] button { border-radius:9px; border:1px solid #35536b; background:#12273a; color:#eaf5ff; }
hr { border-color:#20364b; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class=\"eyebrow\">URBANFLOW / CONTROL ROOM</div>", unsafe_allow_html=True)
    st.markdown("## Simulation controls")
    st.caption("Tune the traffic scenario, then run the model.")
    drivers = st.slider("Driver population", 10, 300, 100, 10)
    seed = st.number_input("Random seed", min_value=0, max_value=100000, value=42, step=1)
    sweeps = st.slider("Maximum sweeps", 10, 1000, 500, 10)
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
    <h1 style="margin:0;">UrbanFlow</h1><span class="signal">● SIMULATION ACTIVE</span>
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
    st.bar_chart(distribution, color="#65aaff", height=300)
with right:
    st.markdown("<div class=\"section-label\">03 / System travel-time trend</div>", unsafe_allow_html=True)
    st.markdown("<div class=\"section-sub\">Average estimated travel time recorded during driver updates.</div>", unsafe_allow_html=True)
    trend = history.drop_duplicates("update").set_index("update")[["average_travel_time"]]
    st.line_chart(trend, color="#55d6d0", height=300)

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