#!/usr/bin/env python3
import json
import re
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

URL = "https://fev.se/atervinning/sophamtning.html?q=yttert%C3%A4nger%2083"

result = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "matavfall": None,
    "plast": None,
    "restavfall": None,
    "papper": None,
}

req = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0 HomeAssistant"}
)

html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

match = re.search(
    r"AppRegistry\.registerInitialState\('[^']+',(\{.*?\})\);</script>",
    html,
    re.DOTALL
)

if match:
    data = json.loads(match.group(1))

    mapping = {
        "Matavfall": "matavfall",
        "Plastförpackningar": "plast",
        "Restavfall": "restavfall",
        "Pappersförpackningar": "papper",
    }

    for container in data.get("containers", []):
        key = mapping.get(container.get("typeText"))
        if key:
            iso = container.get("pickupDateIso")
            if iso:
                dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                result[key] = dt.astimezone(ZoneInfo("Europe/Stockholm")).date().isoformat()
            else:
                result[key] = None

print(json.dumps(result, ensure_ascii=False))