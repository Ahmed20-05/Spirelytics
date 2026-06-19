# 🗡️ Spirelytics

Spirelytics is a data parsing and analysis tool for *Slay the Spire* run history files. It converts raw `.run` JSON logs into structured tabular data for analysis using Pandas, SQL, or visualization tools.

The goal is to make it easy to analyze gameplay patterns such as:
- Card pick rates and deck evolution
- Relic acquisition impact
- Run progression (HP, gold, floors)
- Combat and event outcomes
- Win/loss behavior patterns

---


## ⚙️ Features

- Parses Slay the Spire `.run` files from local save data
- Extracts structured gameplay events:
  - Act and floor progression
  - HP and gold changes
  - Card choices and selections
  - Relic rewards and purchases
  - Events and rest site actions
- Converts nested JSON into a flat Pandas DataFrame
- Exports clean dataset to CSV for analysis

---

## 📊 Data Format

Each row represents a single gameplay decision or event.

| Column       | Description |
|--------------|-------------|
| run_id       | Unique run identifier |
| act          | Act number |
| floor_index  | Floor index within act |
| map_type     | Room type (monster, shop, event, etc.) |
| hp           | Player HP at that point |
| gold         | Player gold at that point |
| type         | Event type (card_choice, relic_choice, event, rest) |
| options      | Available choices |
| picked       | Selected choice |
| victory      | Whether the run was completed successfully |

---

## 🚀 Setup & Usage

### 1. Clone repository
```bash
git clone https://github.com/your-username/spirelytics.git
cd spirelytics