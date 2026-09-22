#!/usr/bin/env python3
"""Populate datasets.json and benchmarks.json from the survey PDF (Tables 3-6)."""
import json, os

ROOT = "/home/claude/site"

# ---------- Table 3: Datasets ----------
# name, year, domain, total_frames, categories, temporal, spatial, semantic, group
detection = "Detection-Oriented"
category  = "Category-Oriented"
understanding = "Anomaly-Understanding"

DATASETS = [
 # Detection-oriented (semantic = None)
 ("Subway Entrance",2008,"Streetscape","86,535",5,"Frame","None","None",detection),
 ("Subway Exit",2008,"Streetscape","38,940",3,"Frame","None","None",detection),
 ("UMN",2009,"Crowd behavior","3,855",1,"Frame","None","None",detection),
 ("UCSD Ped1",2013,"Streetscape","14,000",5,"Frame","Bounding box","None",detection),
 ("UCSD Ped2",2013,"Streetscape","4,560",5,"Frame","Bounding box","None",detection),
 ("CUHK Avenue",2013,"Streetscape","30,652",5,"Frame","Bounding box","None",detection),
 ("NWPU Campus",2023,"Streetscape","1,466,073",28,"Frame","None","None",detection),
 ("ShanghaiTech",2017,"Streetscape","317,398",13,"Frame","Bounding box","None",detection),
 ("Street Scene",2020,"Streetscape","203,257",17,"Track","Bounding box","None",detection),
 ("ComplexVAD",2025,"Streetscape","3,681,438",40,"Track","Bounding box","None",detection),
 # Category-oriented (semantic = Category labels)
 ("UCF-Crime",2018,"Crime","13,741,393",13,"Video","None","Category labels",category),
 ("UCF-Crime Extension",2021,"Crime","14,475,793",15,"Video","None","Category labels",category),
 ("XD-Violence",2020,"Violence","114,096",6,"Video","None","Category labels",category),
 ("TAD",2024,"Traffic","721,280",4,"Frame","Bounding box","Category labels",category),
 ("BOSS",2017,"Multiple","48,624",11,"Video","None","Category labels",category),
 ("CamNuvem",2022,"Robbery","6,151,788",1,"Video","None","Category labels",category),
 ("Ubnormal",2022,"Multiple","236,902",22,"Frame","Pixel","Category labels",category),
 ("SENSE-VAD",2026,"Autonomous driving","540,888",15,"Frame","Bounding box","Category labels",category),
 ("MSAD",2024,"Multiple","447,236",55,"Frame","None","Category labels",category),
 # Anomaly-understanding
 ("CUVA",2024,"Multiple","3,345,097",11,"Time duration","None","Video QA",understanding),
 ("ECVA",2024,"Multiple","19,042,560",21,"Time duration","None","Video QA",understanding),
 ("VANE-Bench",2025,"Multiple","951,482",19,"Video","None","Conversational QA",understanding),
 ("VAGU",2025,"Multiple","20,400,000",21,"Period","None","Grounding + QA",understanding),
 ("FineVAU",2026,"Surveillance","Not reported",13,"None","None","Fine-grained QA",understanding),
 ("SVTA",2025,"Multiple","1,360,000",68,"Video-level","None","Retrieval text pairs",understanding),
 ("CVACBench",2025,"Surveillance","60,160",13,"Frame","None","Captioning",understanding),
 ("HVAU-70K",2025,"Multiple","13,855,489",15,"Frame","None","Video QA",understanding),
 ("UCA",2024,"Crime","11,817,597",13,"Frame","None","Video QA",understanding),
]

def slugify(s):
    out = "".join(c.lower() if c.isalnum() else "-" for c in s)
    while "--" in out: out = out.replace("--","-")
    return out.strip("-")

def tasks_for(group, semantic):
    if group == understanding:
        base = ["Explanation","Question answering"]
        if "Grounding" in semantic: base.append("Grounding")
        if "Retrieval" in semantic: base = ["Retrieval","Explanation"]
        if "Captioning" in semantic: base = ["Captioning","Explanation"]
        return base
    if group == category:
        return ["Detection","Classification"]
    return ["Detection","Localization"]

datasets_json = []
for (name,year,domain,frames,cats,temporal,spatial,semantic,group) in DATASETS:
    datasets_json.append({
        "slug": slugify(name),
        "name": name,
        "year": year,
        "group": group,
        "domain": domain,
        "scale": f"{frames} frames" if frames not in ("Not reported",) else "Not reported",
        "categories": cats,
        "temporal": temporal,
        "spatial": spatial,
        "semantic": semantic,
        "tasks": tasks_for(group, semantic),
        "access": "See original paper",
        "verified": "Sourced from survey PDF, Table 3",
    })

with open(os.path.join(ROOT,"data/datasets.json"),"w") as f:
    json.dump(datasets_json, f, indent=1, ensure_ascii=False)
print(f"datasets.json: {len(datasets_json)} records")

# ---------- Tables 4,5,6: Benchmarks ----------
# Each entry: (method, dataset, metric, value). Empty cells skipped.
bench = []

def add(group, method, cells, protocol, comparable, reliability="Author Reported"):
    for dataset, metric, value in cells:
        if value in (None, "-", ""): continue
        bench.append({
            "group": group, "dataset": dataset, "method": method,
            "metric": metric, "value": value,
            "protocol": protocol, "source": "Survey PDF",
            "reliability": reliability, "comparable": comparable,
        })

# Table 4 — Semi-supervised VAD (Frame AUC)
G4 = "Semi-supervised VAD"
P4 = "Author-reported (survey Table 4)"
def m4(name, ped2, ave, sht, ub, cvad):
    add(G4, name, [("Ped2","AUC",ped2),("CUHK Avenue","AUC",ave),
                   ("ShanghaiTech","AUC",sht),("UBnormal","AUC",ub),
                   ("ComplexVAD","AUC",cvad)], P4, True)
m4("FutureFrame","95.4","85.1","72.8",None,None)
m4("MemAE","94.1","83.3","71.2",None,None)
m4("HyCoVAD",None,None,None,None,"72.5")
m4("MLLM-EVAD",None,"88.4",None,None,"71.0")
m4("SlowFastVAD","99.1","89.6","85.0","72.2",None)
m4("SFN-VAD","98.4","91.6","83.0",None,None)
m4("VLAVAD",None,"87.2",None,None,None)
m4("Follow the Rules","97.9","89.7","85.2","71.90",None)

# Table 5 — Weakly supervised VAD (UCF AUC, XD AP, SHTech AUC)
G5 = "Weakly supervised VAD"
P5 = "Author-reported (survey Table 5)"
def m5(name, ucf, xd, sht):
    add(G5, name, [("UCF-Crime","AUC",ucf),("XD-Violence","AP",xd),
                   ("ShanghaiTech","AUC",sht)], P5, True)
m5("MSL","85.62","78.59","97.32")
m5("MIST","82.30",None,"94.83")
m5("GCN","82.12",None,"84.44")
m5("DeepMIL","75.40",None,None)
m5("DAKD","88.34","85.61","98.10")
m5("LEC-VAD","89.97","86.56",None)
m5("Ex-VAD","88.29","86.52",None)
m5("Federated-WVAD","84.03","75.99",None)
m5("LOP-VAD","88.07","86.18",None)
m5("TCRFL","87.31","82.63","98.12")
m5("FSA-VAD",None,None,"97.66")
m5("VadCLIP++","88.12","85.03",None)
m5("RelVid","87.71","80.76",None)
m5("AVadCLIP",None,"86.04",None)
m5("Multimodal-VAD","87.96","86.32",None)
m5("PEMIL","86.76","85.59","98.14")
m5("VadCLIP","88.02","84.51",None)
m5("CLIP-TSA","87.58","82.19","98.32")
m5("ReFLIP-VAD","89.14","86.29",None)
m5("IELD-WVAD","89.67","85.92",None)
m5("DWFF-VAD","88.58","85.58",None)
m5("CMSIL","87.57","86.06",None)
m5("WSVAD-LLMKE","86.88","87.05","98.25")
m5("TEVAD","85.30",None,None)

# Table 6 — Training-free / open-world / instruction (UCF AUC, XD AP, UB AUC)
G6 = "Training-free & open-world LM-based VAD"
P6 = "Author-reported (survey Table 6)"
def m6(name, ucf, xd, ub):
    add(G6, name, [("UCF-Crime","AUC",ucf),("XD-Violence","AP",xd),
                   ("UBnormal","AUC",ub)], P6, True)
m6("OVVAD","86.40","66.53","62.94")
m6("Anomize","84.89","69.31",None)
m6("PLOVAD","87.06",None,None)
m6("Holmes-VAU","88.96","87.68",None)
m6("Holmes-VAD","89.51","90.67",None)
m6("QVAD","84.28","68.53","79.60")
m6("Flashback","87.30","75.10",None)
m6("TFPLG","87.52","85.08",None)
m6("MoniTor","82.57","55.01",None)
m6("EventVAD","82.03","64.04",None)
m6("PANDA","84.89","70.16","75.78")
m6("VADTree","84.74","68.85",None)
m6("VERA","86.55","70.11",None)
m6("SUVAD","83.90","70.10",None)
m6("MCANet","82.47","69.72","62.94")
m6("LAVAD","80.28","62.01","64.23")

with open(os.path.join(ROOT,"data/benchmarks.json"),"w") as f:
    json.dump(bench, f, indent=1, ensure_ascii=False)
print(f"benchmarks.json: {len(bench)} rows")
