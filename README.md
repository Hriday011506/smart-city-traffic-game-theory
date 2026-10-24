# Game-Theoretic Modeling of Traffic Route Selection in Smart Cities

A Python simulation and interactive dashboard exploring congestion games: drivers choose routes to minimize personal travel time, while routes become slower as more drivers use them.

## Features
- Sequential best-response dynamics
- Three illustrative alternative routes
- Route distribution and average-travel-time charts
- CSV exports for assignments and simulation history
- Streamlit dashboard with adjustable simulation settings

## Mathematical model
Estimated route travel time is `C_r(n_r) = a_r + b_r * n_r`, where `n_r` is the number of drivers on route `r`, `a_r` is base travel time, and `b_r` is the congestion factor.

| Route | Base time | Congestion factor |
|---|---:|---:|
| Route A | 10.0 | 0.18 |
| Route B | 13.0 | 0.10 |
| Route C | 16.0 | 0.04 |

**These parameters are illustrative assumptions, not measured real-world traffic data.**

Drivers switch only when another route offers a strictly lower estimated travel time. When a complete sweep produces no switches, the assignment is stable under the update rule. For this parallel-route congestion game, a stable assignment corresponds to a pure-strategy Nash equilibrium.

## Project structure
```text
smart-city-traffic-game-theory/
├── traffic_game_theory.py
├── app.py
├── requirements.txt
├── README.md
├── results/   # generated locally
└── plots/     # generated locally
```

## Installation
Python 3.10 or newer is recommended.

```bash
git clone https://github.com/Hriday011506/smart-city-traffic-game-theory.git
cd smart-city-traffic-game-theory
python -m venv .venv
```

Activate the virtual environment:

**macOS/Linux**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Run the simulation
```bash
python traffic_game_theory.py
```
The script creates `results/simulation_history.csv`, `results/final_route_summary.csv`, and PNG files under `plots/` automatically.

## Launch the dashboard
```bash
streamlit run app.py
```
Use the sidebar to set the number of drivers, random seed, and maximum sweeps. The dashboard provides downloadable CSVs.

## Research questions
- How does route distribution change as the number of drivers increases?
- What happens when one route has a larger congestion factor?
- Does selfish route selection minimize total travel time?
- How does equilibrium compare with a system-optimal assignment?

## Limitations and future work
This model uses three parallel routes with linear congestion costs. It does not incorporate a real road graph, intersections, traffic lights, stochastic travel times, weather, or time-varying demand. Possible extensions include comparing Nash equilibrium with a centrally optimized assignment and using real traffic observations.

## Technologies
Python, pandas, Matplotlib, Streamlit.

## Academic use
Clearly distinguish model assumptions and simulated results from real-world traffic observations in reports and presentations.