"""Interactive dashboard for the traffic congestion game."""
import pandas as pd
import streamlit as st
from traffic_game_theory import ROUTES, simulate

st.set_page_config(page_title="Traffic Route Game Theory", page_icon="🚦", layout="wide")
st.title("🚦 Game-Theoretic Traffic Route Selection")
st.write("Explore how self-interested drivers distribute across routes as congestion changes travel time.")
with st.sidebar:
    st.header("Simulation settings")
    drivers = st.slider("Number of drivers", 10, 300, 100, 10)
    seed = st.number_input("Random seed", min_value=0, max_value=100000, value=42, step=1)
    sweeps = st.slider("Maximum sweeps", 10, 1000, 500, 10)
    run = st.button("Run simulation", type="primary")
if "simulation" not in st.session_state or run:
    with st.spinner("Simulating route choices..."):
        st.session_state.simulation = simulate(int(drivers), int(seed), int(sweeps))
history, assignments, converged = st.session_state.simulation
counts = assignments["selected_route"].value_counts()
last = history.iloc[-1]
a, b, c = st.columns(3)
a.metric("Drivers", len(assignments))
b.metric("Average travel time", "%.2f min" % last["average_travel_time"])
c.metric("Convergence", "Reached" if converged else "Sweep limit")
left, right = st.columns(2)
with left:
    st.subheader("Final route distribution")
    st.bar_chart(pd.DataFrame({"Drivers": [int(counts.get(r, 0)) for r in ROUTES]}, index=list(ROUTES)))
with right:
    st.subheader("Average travel time over updates")
    st.line_chart(history.drop_duplicates("update").set_index("update")[["average_travel_time"]])
st.subheader("Route cost model")
rows = []
for route, params in ROUTES.items():
    n = int(counts.get(route, 0))
    rows.append({"Route": route, "Base time": params["base_time"], "Congestion factor": params["congestion_factor"], "Drivers assigned": n, "Estimated travel time": round(params["base_time"] + params["congestion_factor"] * n, 2)})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
st.subheader("Driver assignments")
st.dataframe(assignments, use_container_width=True, hide_index=True)
st.download_button("Download driver assignments CSV", assignments.to_csv(index=False).encode("utf-8"), "final_route_summary.csv", "text/csv")
st.download_button("Download simulation history CSV", history.to_csv(index=False).encode("utf-8"), "simulation_history.csv", "text/csv")
with st.expander("Model assumptions"):
    st.markdown("- Each driver minimizes their own estimated travel time.\n- Route cost is `base_time + congestion_factor × drivers_on_route`.\n- Drivers switch only when a move strictly improves their cost.\n- Route parameters are illustrative, not measured traffic data.\n- A stable assignment is a pure-strategy Nash equilibrium when no single driver can lower their travel time by changing routes alone.")