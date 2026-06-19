import json
import os
import pandas as pd

DATA_DIR = "C:\Users\ahmed\AppData\Roaming\SlayTheSpire2\steam\76561197960287930\profile1\saves\history"

def load_run_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_run(run_data, run_id):
    rows = []

    floors = run_data.get("floor_snapshots", [])

    
    victory = run_data.get("victory", False)

    for floor_data in floors:
        floor = floor_data.get("floor", None)

        base = {
            "run_id": run_id,
            "floor": floor,
            "hp": floor_data.get("current_hp"),
            "gold": floor_data.get("gold"),
            "victory": victory,  # ✅ added here
            "room_type": floor_data.get("map_point_type"),
        }

        # --- CARD CHOICES ---
        for choice in floor_data.get("card_choices", []):
            options = [c["card"]["id"] for c in choice.get("cards", [])]
            picked = next(
                (c["card"]["id"] for c in choice.get("cards", []) if c.get("was_picked")),
                None
            )

            rows.append({
                **base,
                "type": "card_choice",
                "options": options,
                "picked": picked,
            })

        # --- RELIC CHOICES ---
        for relic in floor_data.get("relic_choices", []):
            rows.append({
                **base,
                "type": "relic_choice",
                "options": [relic.get("choice")],
                "picked": relic.get("choice") if relic.get("was_picked") else None,
            })

        # --- EVENTS ---
        for event in floor_data.get("event_choices", []):
            rows.append({
                **base,
                "type": "event",
                "options": None,
                "picked": event.get("title", {}).get("key"),
            })

        # --- REST ---
        for rest in floor_data.get("rest_site_choices", []):
            rows.append({
                **base,
                "type": "rest",
                "options": None,
                "picked": rest,
            })

    return rows

def parse_all_runs(data_dir):
    all_rows = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".run"):
            path = os.path.join(data_dir, filename)
            try:
                run_data = load_run_file(path)
                run_id = filename.replace(".run", "")
                rows = parse_run(run_data, run_id)
                all_rows.extend(rows)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = parse_all_runs(DATA_DIR)
    print(df.head())

    # Save for analysis
    df.to_csv("slay_the_spire_runs.csv", index=False)