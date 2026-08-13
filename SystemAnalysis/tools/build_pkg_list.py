# -*- coding: utf-8 -*-
"""트로피컬 바캉스 전체 아이템을 받아 경매장 거래분만 골라 JSON으로 굳힌다."""
import json, io, time
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError

KEY = open(r"C:\Users\MBC-501-08\Desktop\GameDesignStudy\SystemAnalysis\tools\apikey.txt",
           encoding="utf-8").read().strip()
BASE = "https://api.neople.co.kr/df"


def call(path, params):
    qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    try:
        with urlopen(Request(f"{BASE}{path}?{qs}&apikey={KEY}",
                             headers={"User-Agent": "probe/1.0"}), timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        return {"__err__": f"HTTP {e.code}"}


# limit 상한 확인
for lim in (100, 200, 400):
    d = call("/items", {"itemName": "트로피컬 바캉스", "wordType": "front", "limit": lim})
    n = len(d.get("rows", [])) if "__err__" not in d else -1
    print(f"limit={lim:>4} -> {n}건")

rows = call("/items", {"itemName": "트로피컬 바캉스", "wordType": "front",
                       "limit": 400}).get("rows", [])
print(f"\n전체 {len(rows)}건")

# 거래되는 것만 남긴다
keep = []
for r in rows:
    live = call("/auction", {"itemId": r["itemId"], "limit": 1, "sort": "unitPrice:asc"})
    sold = call("/auction-sold", {"itemId": r["itemId"], "limit": 1})
    nl = len(live.get("rows", [])) if "__err__" not in live else 0
    ns = len(sold.get("rows", [])) if "__err__" not in sold else 0
    if nl or ns:
        keep.append({
            "itemName": r["itemName"],
            "itemId": r["itemId"],
            "rarity": r.get("itemRarity"),
            "slot": r.get("itemTypeDetail"),
        })
    time.sleep(0.25)

print(f"거래되는 것 {len(keep)}종")

# 같은 이름이 여러 개면 뒤에 순번을 붙여 구분한다
seen = {}
for k in keep:
    n = k["itemName"]
    seen[n] = seen.get(n, 0) + 1
    k["label"] = n if seen[n] == 1 else f"{n}#{seen[n]}"

with io.open("pkg_items.json", "w", encoding="utf-8") as f:
    json.dump(keep, f, ensure_ascii=False, indent=1)

dups = {n: c for n, c in seen.items() if c > 1}
print(f"\n이름 중복 {len(dups)}종:")
for n, c in dups.items():
    print(f"  {n} x{c}")
print("\n-> pkg_items.json")
