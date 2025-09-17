#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeroBrief Day 1 — Flight brief + baseline delay risk (rule-based)
Usage:
  python main.py --flight_no CA123 --dep ZBAA --arr ZSPD \
    --dep_time 2025-09-20T08:30:00 --arr_time 2025-09-20T10:45:00 \
    --dep_metar "ZBAA 200800Z 04005MPS 9999 FEW020 22/12 Q1015" \
    --arr_metar "ZSPD 200945Z 06010MPS 8000 RA BKN015 24/20 Q1009"
"""
from __future__ import annotations
import argparse, datetime as dt, re, json, math
from dataclasses import dataclass

# --- Simple airport catalog (extend later) ---
HUB_AIRPORTS = {"ZBAA","ZSPD","ZGGG","ZGSZ","RJTT","RJAA","VHHH","WSSS","KJFK","KLAX","KORD","KSFO","KATL","KBOS","KSEA"}

# --- Minimal METAR parsing (very rough) ---
def parse_metar_conditions(metar: str | None) -> dict:
    if not metar:
        return {"wx": None, "vis": None, "cloud": None, "cat": "VMC?"}
    wx = None
    if re.search(r"\bTS\b|\bTSRA\b|\bSQ\b", metar): wx = "TS"
    elif re.search(r"\bRA\b|\bSHRA\b", metar): wx = "RA"
    elif re.search(r"\bSN\b|\bSHSN\b", metar): wx = "SN"
    elif re.search(r"\bFG\b|\bBR\b|\bHZ\b", metar): wx = "FG"
    # crude vis: look for #### or 9999
    vis = None
    m = re.search(r"\b(\d{4})\b", metar)
    if m: 
        vis_m = int(m.group(1))
        vis = vis_m
    cloud = "CLR" if "SKC" in metar or "NSC" in metar else None
    # flight category heuristic
    cat = "VFR"
    if vis is not None:
        if vis < 5000: cat = "MVFR"
        if vis < 3000: cat = "IFR"
        if vis < 1600: cat = "LIFR"
    if wx in {"TS","RA","SN","FG"}:
        if cat == "VFR": cat = "MVFR"
    return {"wx": wx, "vis": vis, "cloud": cloud, "cat": cat}

def hour_from_iso(s: str) -> int:
    return dt.datetime.fromisoformat(s).hour

@dataclass
class Brief:
    flight_no: str
    dep: str
    arr: str
    dep_time: str
    arr_time: str
    dep_metar: str|None=None
    arr_metar: str|None=None

def baseline_delay_risk(dep_hour:int, arr_hour:int, dep:str, arr:str, dep_cat:str, arr_cat:str, wx_flags:set[str], distance_km: float|None=None) -> float:
    score = 0.0
    # time-of-day peaks
    for h in (dep_hour, arr_hour):
        if 6 <= h <= 9: score += 0.12
        if 17 <= h <= 21: score += 0.10
    # hub congestion
    if dep in HUB_AIRPORTS: score += 0.05
    if arr in HUB_AIRPORTS: score += 0.10
    # wx impact
    if "RA" in wx_flags: score += 0.18
    if "SN" in wx_flags: score += 0.25
    if "TS" in wx_flags: score += 0.35
    if "FG" in wx_flags: score += 0.22
    # flight category
    for cat in (dep_cat, arr_cat):
        if cat == "MVFR": score += 0.06
        elif cat == "IFR": score += 0.12
        elif cat == "LIFR": score += 0.20
    # short stage = tighter turns (if known)
    if distance_km is not None and distance_km < 800: 
        score += 0.05
    # squash into [0,1]
    score = max(0.0, min(1.0, score))
    return round(score, 2)

def risk_band(x:float)->str:
    if x <= 0.33: return "low"
    if x <= 0.66: return "medium"
    return "high"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--flight_no", required=True)
    ap.add_argument("--dep", required=True)
    ap.add_argument("--arr", required=True)
    ap.add_argument("--dep_time", required=True, help="ISO8601, e.g., 2025-09-20T08:30:00")
    ap.add_argument("--arr_time", required=True, help="ISO8601")
    ap.add_argument("--dep_metar", default=None)
    ap.add_argument("--arr_metar", default=None)
    ap.add_argument("--distance_km", type=float, default=None, help="Optional stage length")
    args = ap.parse_args()

    dep_cond = parse_metar_conditions(args.dep_metar)
    arr_cond = parse_metar_conditions(args.arr_metar)
    wx_flags = {w for w in [dep_cond.get("wx"), arr_cond.get("wx")] if w}

    dep_h = hour_from_iso(args.dep_time)
    arr_h = hour_from_iso(args.arr_time)

    risk = baseline_delay_risk(
        dep_hour=dep_h, arr_hour=arr_h,
        dep=args.dep, arr=args.arr,
        dep_cat=dep_cond["cat"], arr_cat=arr_cond["cat"],
        wx_flags=wx_flags, distance_km=args.distance_km
    )

    # Render brief
    print(f"[BRIEF] {args.flight_no} {args.dep} → {args.arr} ({args.dep_time} → {args.arr_time})")
    print(f"[WEATHER] DEP({dep_cond['cat']}{','+dep_cond['wx'] if dep_cond['wx'] else ''}), ARR({arr_cond['cat']}{','+arr_cond['wx'] if arr_cond['wx'] else ''})")
    print(f"[BASELINE DELAY RISK] {risk}  ({risk_band(risk)})")

if __name__ == "__main__":
    main()
