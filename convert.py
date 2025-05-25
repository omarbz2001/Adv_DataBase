import json
import ijson
from decimal import Decimal

# Custom serializer function for Decimal type
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")

input_file = "dblp_v14.json"
output_file = "dblp_v14.jsonl"

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    objects = ijson.items(f_in, "item")
    count = 0

    for obj in objects:
        
        f_out.write(json.dumps(obj, default=decimal_serializer) + "\n")
        count += 1
        if count % 1000 == 0:
            print(f"Written {count} objects...")
        
        
        if count >= 20000:
            break

print(f"Conversion complete. Total objects written: {count}")
