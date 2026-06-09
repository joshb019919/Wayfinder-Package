import json
import pandas as pd

with open("Timeline.json") as jfp:
    data = json.load(jfp)

records = []

for seg in data["semanticSegments"]:
    if "activity" in seg:
        records.append({
            "type": "drive",
            "start": seg["startTime"],
            "end": seg["endTime"],
            "distance_m": seg["activity"]["distanceMeters"]
        })

    elif "visit" in seg:
        records.append({
            "type": "stop",
            "start": seg["startTime"],
            "end": seg["endTime"]
        })

df = pd.DataFrame(records)
df["miles"] = df["distance_m"] * 0.000621371
print(df)
