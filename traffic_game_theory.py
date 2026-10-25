"""Game-theoretic traffic route selection using a congestion game."""
from pathlib import Path
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
PLOTS_DIR = BASE_DIR / "plots"
ROUTES = {
    "MUJ → C-Scheme": {"base_time": 35.0, "congestion_factor": 0.18},
    "MUJ → Malviya Nagar": {"base_time": 37.0, "congestion_factor": 0.10},
    "MUJ → Pacific Mall (Mansarovar)": {"base_time": 40.0, "congestion_factor": 0.04},
}

def route_cost(route, load):
    """Illustrative travel time at a specified route load."""
    p = ROUTES[route]
    return p["base_time"] + p["congestion_factor"] * load

def simulate(number_of_drivers=100, seed=42, max_sweeps=500):
    """Run sequential best-response updates until a sweep makes no switches."""
    if number_of_drivers < 1 or max_sweeps < 1:
        raise ValueError("Drivers and max_sweeps must be positive.")
    rng = random.Random(seed)
    names = list(ROUTES)
    choices = [rng.choice(names) for _ in range(number_of_drivers)]
    history = []
    updates = 0
    def counts():
        return {r: choices.count(r) for r in names}
    def record(sweep, changed=False):
        c = counts()
        total = sum(route_cost(r, c[r]) * c[r] for r in names)
        history.append({"update": updates, "sweep": sweep,
            "route_a_drivers": c[names[0]], "route_b_drivers": c[names[1]],
            "route_c_drivers": c[names[2]],
            "average_travel_time": total / number_of_drivers,
            "total_driver_minutes": total, "changed_in_update": changed})
    record(0)
    converged = False
    for sweep in range(1, max_sweeps + 1):
        changed = False
        order = list(range(number_of_drivers))
        rng.shuffle(order)
        for i in order:
            current = choices[i]
            c = counts()
            current_cost = route_cost(current, c[current])
            improving = []
            best_cost = current_cost
            for route in names:
                load = c[route] if route == current else c[route] + 1
                cost = route_cost(route, load)
                if cost < best_cost - 1e-12:
                    best_cost = cost
                    improving = [route]
                elif cost < current_cost - 1e-12 and abs(cost - best_cost) <= 1e-12:
                    improving.append(route)
            if improving:
                choices[i] = rng.choice(improving)
                updates += 1
                changed = True
                record(sweep, True)
        if not changed:
            converged = True
            break
    c = counts()
    assignments = pd.DataFrame([{"driver_id": i + 1, "selected_route": r,
        "drivers_on_route": c[r], "estimated_travel_time": route_cost(r, c[r])}
        for i, r in enumerate(choices)])
    return pd.DataFrame(history), assignments, converged

def make_plots(history, assignments):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    last = history.iloc[-1]
    labels = list(ROUTES)
    counts = [int(last["route_a_drivers"]), int(last["route_b_drivers"]), int(last["route_c_drivers"])]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, counts)
    ax.set(title="Final Driver Distribution Across Jaipur Destinations", xlabel="Destination route", ylabel="Drivers")
    ax.grid(axis="y", alpha=0.25); fig.tight_layout()
    fig.savefig(PLOTS_DIR / "final_route_distribution.png", dpi=160); plt.close(fig)
    series = history.drop_duplicates("update")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(series["update"], series["average_travel_time"])
    ax.set(title="Average Travel Time During Best-Response Updates", xlabel="Driver updates", ylabel="Average travel time (illustrative minutes)")
    ax.grid(alpha=0.25); fig.tight_layout()
    fig.savefig(PLOTS_DIR / "average_travel_time.png", dpi=160); plt.close(fig)
    used = assignments.groupby("selected_route").agg(estimated_travel_time=("estimated_travel_time", "first")).reindex(labels)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(used.index, used["estimated_travel_time"])
    ax.set(title="Estimated Travel Time by Used Route", xlabel="Destination route", ylabel="Estimated minutes")
    ax.grid(axis="y", alpha=0.25); fig.tight_layout()
    fig.savefig(PLOTS_DIR / "final_route_travel_times.png", dpi=160); plt.close(fig)

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    history, assignments, converged = simulate()
    history.to_csv(RESULTS_DIR / "simulation_history.csv", index=False)
    assignments.to_csv(RESULTS_DIR / "final_route_summary.csv", index=False)
    make_plots(history, assignments)
    summary = assignments.groupby("selected_route").agg(drivers=("driver_id", "count"), estimated_travel_time=("estimated_travel_time", "first")).reindex(ROUTES.keys(), fill_value=0)
    print("\nTraffic Route Selection — Simulation Summary")
    print("=" * 48)
    print("Drivers simulated:", len(assignments))
    print("Converged:", "Yes" if converged else "No (maximum sweeps reached)")
    print(summary.to_string())
    print("Average travel time: %.2f illustrative minutes" % history.iloc[-1]["average_travel_time"])
    print("Results saved to:", RESULTS_DIR)
    print("Plots saved to:", PLOTS_DIR)

if __name__ == "__main__":
    main()