import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DATA_DIR = r"C:\Users\ahmed\AppData\Roaming\SlayTheSpire2\steam\76561197960287930\profile1\saves\history"
OUTPUT_CSV = "runs.csv"


# --- reuse your parser functions ---
from parser import load_run_file, parse_run  # or same file


def append_to_csv(new_rows):
    new_df = pd.DataFrame(new_rows)

    if os.path.exists(OUTPUT_CSV):
        existing_df = pd.read_csv(OUTPUT_CSV)

        # Avoid duplicate runs
        existing_runs = set(existing_df["run_id"].unique())
        new_df = new_df[~new_df["run_id"].isin(existing_runs)]

        combined = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined = new_df

    combined.to_csv(OUTPUT_CSV, index=False)
    print(f"Updated CSV with {len(new_df)} new rows")


class RunFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".run"):
            print(f"New run detected: {event.src_path}")

            try:
                run_data = load_run_file(event.src_path)
                run_id = os.path.basename(event.src_path).replace(".run", "")

                rows = parse_run(run_data, run_id)
                append_to_csv(rows)

            except Exception as e:
                print(f"Error processing {event.src_path}: {e}")


if __name__ == "__main__":
    event_handler = RunFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DATA_DIR, recursive=False)

    observer.start()
    print("Watching for new .run files...")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()