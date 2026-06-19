import json
import os
import pandas as pd

#ADD YOUR PATH HERE
DATA_DIR = "C:/Users/ahmed/AppData/Roaming/SlayTheSpire2/steam/76561197960287930/profile1/saves/history"

def load_run_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_run(run_data, run_id):
    rows = []

    acts = run_data.get("map_point_history", [])
    victory = run_data.get("win", False)

    for act_index, act in enumerate(acts):
        for floor_index, floor_data in enumerate(act):

            map_type = floor_data.get("map_point_type")

            for stat in floor_data.get("player_stats", []):

                base = {
                    "run_id": run_id,
                    "act": act_index,
                    "floor_index": floor_index,
                    "map_type": map_type,
                    "hp": stat.get("current_hp"),
                    "gold": stat.get("current_gold"),
                    "victory": victory,
                }

                # --- CARD CHOICES ---
                for choice in stat.get("card_choices", []):
                    rows.append({
                        **base,
                        "type": "card_choice",
                        "options": [c["card"]["id"] for c in stat.get("card_choices", [])],
                        "picked": next(
                            (c["card"]["id"] for c in stat.get("card_choices", []) if c.get("was_picked")),
                            None
                        )
                    })
                    break

                # --- RELICS ---
                for relic in stat.get("relic_choices", []):
                    rows.append({
                        **base,
                        "type": "relic_choice",
                        "options": [r["choice"] for r in stat.get("relic_choices", [])],
                        "picked": relic.get("choice") if relic.get("was_picked") else None,
                    })
                    break

                # --- EVENTS ---
                for event in stat.get("event_choices", []):
                    rows.append({
                        **base,
                        "type": "event",
                        "options": None,
                        "picked": event.get("title", {}).get("key"),
                    })

                # --- REST ---
                for rest in stat.get("rest_site_choices", []):
                    rows.append({
                        **base,
                        "type": "rest",
                        "options": None,
                        "picked": rest,
                    })

    return rows
def parse_all_runs(data_dir):
    all_rows = []

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"DATA_DIR does not exist: {data_dir}")

    files = os.listdir(data_dir)

    for filename in files:
        if not filename.endswith(".run"):
            continue

        path = os.path.join(data_dir, filename)

        try:
            run_data = load_run_file(path)
            run_id = filename.replace(".run", "")
            rows = parse_run(run_data, run_id)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")

    print("Total rows:", len(all_rows))
    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = parse_all_runs(DATA_DIR)
    print(df.head())

    # Save for analysis
    df.to_csv("runs.csv", index=False)