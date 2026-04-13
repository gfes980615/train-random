#!/usr/bin/env python3
"""
讀取 taiwan_railway_stations.csv，結合車站座標，
產出一個包含地圖 + 抽籤動畫的 HTML 網頁應用。
"""

import csv, json, os
from station_quotes import STATION_QUOTES

CSV_PATH = os.path.join(os.path.dirname(__file__), "taiwan_railway_stations.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "draw_station.html")

# ---------------------------------------------------------------------------
# 所有 241 站的近似座標 (lat, lng)
# ---------------------------------------------------------------------------
COORDS = {
    # ===== 縱貫線北段 =====
    "基隆": (25.1316, 121.7390), "三坑": (25.1220, 121.7360),
    "八堵": (25.1084, 121.7326), "七堵": (25.0930, 121.7133),
    "百福": (25.0830, 121.7000), "暖暖": (25.0980, 121.7440),
    "五堵": (25.0730, 121.6720), "汐止": (25.0630, 121.6400),
    "汐科": (25.0580, 121.6230), "南港": (25.0530, 121.6064),
    "松山": (25.0496, 121.5780), "臺北": (25.0478, 121.5170),
    "萬華": (25.0340, 121.5000), "板橋": (25.0145, 121.4629),
    "浮洲": (25.0030, 121.4430), "樹林": (24.9913, 121.4200),
    "南樹林": (24.9840, 121.4100), "山佳": (24.9740, 121.3950),
    "鶯歌": (24.9545, 121.3530), "鳳鳴": (24.9490, 121.3400),
    "桃園": (24.9893, 121.3133), "內壢": (24.9700, 121.2660),
    "中壢": (24.9536, 121.2257), "埔心": (24.9270, 121.1820),
    "楊梅": (24.9120, 121.1500), "富岡": (24.8980, 121.1200),
    "新富": (24.8900, 121.1050), "北湖": (24.8800, 121.0850),
    "湖口": (24.8700, 121.0600), "新豐": (24.8450, 121.0050),
    "竹北": (24.8310, 120.9930), "新竹": (24.8017, 120.9715),
    "三姓橋": (24.7840, 120.9570), "香山": (24.7620, 120.9300),
    "崎頂": (24.7250, 120.9050), "竹南": (24.6850, 120.8780),
    # ===== 海岸線 =====
    "談文": (24.6660, 120.8620), "大山": (24.6450, 120.8420),
    "後龍": (24.6170, 120.7930), "龍港": (24.6010, 120.7700),
    "白沙屯": (24.5750, 120.7360), "新埔": (24.5570, 120.7150),
    "通霄": (24.5300, 120.6960), "苑裡": (24.4780, 120.6770),
    "日南": (24.4200, 120.6600), "大甲": (24.3840, 120.6300),
    "臺中港": (24.3530, 120.6120), "清水": (24.3200, 120.5880),
    "沙鹿": (24.2850, 120.5720), "龍井": (24.2480, 120.5650),
    "大肚": (24.2100, 120.5580), "追分": (24.1720, 120.5530),
    # ===== 臺中線 (山線) =====
    "造橋": (24.6430, 120.8700), "豐富": (24.6080, 120.8400),
    "苗栗": (24.5704, 120.8236), "南勢": (24.5450, 120.8100),
    "銅鑼": (24.4860, 120.7880), "三義": (24.4200, 120.7620),
    "泰安": (24.3550, 120.7430), "后里": (24.3080, 120.7260),
    "豐原": (24.2542, 120.7230), "栗林": (24.2340, 120.7120),
    "潭子": (24.2140, 120.7030), "頭家厝": (24.1950, 120.6970),
    "松竹": (24.1810, 120.6930), "太原": (24.1680, 120.6900),
    "精武": (24.1530, 120.6880), "臺中": (24.1368, 120.6869),
    "五權": (24.1230, 120.6790), "大慶": (24.1100, 120.6650),
    "烏日": (24.0980, 120.6230), "新烏日": (24.0930, 120.6130),
    "成功": (24.0880, 120.5800),
    # ===== 縱貫線南段 =====
    "彰化": (24.0809, 120.5387), "花壇": (24.0400, 120.5520),
    "大村": (24.0070, 120.5630), "員林": (23.9573, 120.5696),
    "永靖": (23.9250, 120.5650), "社頭": (23.8950, 120.5600),
    "田中": (23.8630, 120.5820), "二水": (23.8170, 120.6180),
    "林內": (23.7670, 120.6110), "石榴": (23.7430, 120.5880),
    "斗六": (23.7076, 120.5431), "斗南": (23.6630, 120.4820),
    "石龜": (23.6350, 120.4700), "大林": (23.6030, 120.4630),
    "民雄": (23.5530, 120.4450), "嘉北": (23.4980, 120.4390),
    "嘉義": (23.4792, 120.4410), "水上": (23.4330, 120.3980),
    "南靖": (23.4040, 120.3830), "後壁": (23.3650, 120.3590),
    "新營": (23.3074, 120.3166), "柳營": (23.2780, 120.3080),
    "林鳳營": (23.2540, 120.3020), "隆田": (23.2150, 120.2950),
    "拔林": (23.1930, 120.2800), "善化": (23.1650, 120.2720),
    "南科": (23.1200, 120.2700), "新市": (23.0900, 120.2660),
    "永康": (23.0450, 120.2470), "大橋": (23.0200, 120.2320),
    "臺南": (22.9971, 120.2129), "保安": (22.9650, 120.2100),
    "仁德": (22.9400, 120.2250), "中洲": (22.9180, 120.2330),
    "大湖": (22.8830, 120.2620), "路竹": (22.8570, 120.2750),
    "岡山": (22.7956, 120.2954), "橋頭": (22.7550, 120.2980),
    "楠梓": (22.7270, 120.3000), "新左營": (22.6880, 120.3080),
    "左營(舊城)": (22.6720, 120.3080), "內惟": (22.6590, 120.3040),
    "美術館": (22.6510, 120.3020), "鼓山": (22.6450, 120.3000),
    "三塊厝": (22.6420, 120.3020), "高雄": (22.6395, 120.3025),
    "民族": (22.6370, 120.3080), "科工館": (22.6350, 120.3160),
    "正義": (22.6310, 120.3250),
    # ===== 屏東線 =====
    "鳳山": (22.6266, 120.3440), "後庄": (22.6230, 120.3620),
    "九曲堂": (22.6180, 120.3810), "六塊厝": (22.6370, 120.4400),
    "屏東": (22.6694, 120.4862), "歸來": (22.6600, 120.4980),
    "麟洛": (22.6430, 120.5150), "西勢": (22.6230, 120.5250),
    "竹田": (22.5970, 120.5300), "潮州": (22.5515, 120.5322),
    "崁頂": (22.5150, 120.5400), "南州": (22.4880, 120.5450),
    "鎮安": (22.4650, 120.5480), "林邊": (22.4400, 120.5520),
    "佳冬": (22.4180, 120.5620), "東海": (22.3980, 120.5730),
    "枋寮": (22.3734, 120.5938),
    # ===== 南迴線 =====
    "加祿": (22.3530, 120.6080), "內獅": (22.3220, 120.6280),
    "枋山": (22.2640, 120.6520),
    "大武": (22.3540, 120.8911), "瀧溪": (22.4230, 120.9450),
    "金崙": (22.5080, 120.9800), "太麻里": (22.6151, 121.0053),
    "知本": (22.7120, 121.0570), "康樂": (22.7580, 121.0900),
    "臺東": (22.7930, 121.1234),
    # ===== 臺東線 =====
    "山里": (22.8320, 121.1180), "鹿野": (22.9130, 121.1350),
    "瑞源": (22.9450, 121.1520), "瑞和": (22.9750, 121.1670),
    "關山": (23.0500, 121.1860), "海端": (23.0700, 121.1950),
    "池上": (23.0970, 121.2190), "富里": (23.1770, 121.2480),
    "東竹": (23.2150, 121.2650), "東里": (23.2700, 121.2830),
    "玉里": (23.3349, 121.3135), "三民": (23.4020, 121.3230),
    "瑞穗": (23.4970, 121.3680), "富源": (23.5600, 121.3830),
    "大富": (23.6080, 121.3950), "光復": (23.6450, 121.4180),
    "萬榮": (23.6880, 121.4300), "鳳林": (23.7430, 121.4550),
    "南平": (23.7780, 121.4730), "林榮新光": (23.8000, 121.4850),
    "豐田": (23.8370, 121.5050), "壽豐": (23.8700, 121.5250),
    "平和": (23.8950, 121.5380), "志學": (23.9150, 121.5530),
    "吉安": (23.9550, 121.5800), "花蓮": (23.9936, 121.6013),
    # ===== 北迴線 =====
    "北埔": (24.0130, 121.6070), "景美": (24.0680, 121.6120),
    "新城(太魯閣)": (24.1276, 121.6216), "崇德": (24.1730, 121.6330),
    "和仁": (24.2280, 121.6780), "和平": (24.2980, 121.7510),
    "漢本": (24.3580, 121.7680), "武塔": (24.4130, 121.7830),
    "南澳": (24.4580, 121.8000), "東澳": (24.5080, 121.8270),
    "永樂": (24.5280, 121.8400), "蘇澳": (24.5780, 121.8550),
    "蘇澳新": (24.5960, 121.8580),
    # ===== 宜蘭線 =====
    "新馬": (24.6180, 121.8600), "冬山": (24.6350, 121.7920),
    "羅東": (24.6764, 121.7705), "中里": (24.7000, 121.7650),
    "二結": (24.7140, 121.7630), "宜蘭": (24.7579, 121.7583),
    "四城": (24.7820, 121.7550), "礁溪": (24.8070, 121.7670),
    "頂埔": (24.8280, 121.7780), "頭城": (24.8593, 121.8230),
    "外澳": (24.8800, 121.8430), "龜山": (24.9030, 121.8610),
    "大溪": (24.9300, 121.8660), "大里": (24.9600, 121.8710),
    "石城": (24.9850, 121.8780),
    "四腳亭": (25.0750, 121.7680), "瑞芳": (25.1086, 121.8068),
    "猴硐": (25.0870, 121.8280), "三貂嶺": (25.0650, 121.8400),
    "牡丹": (25.0450, 121.8450), "雙溪": (25.0330, 121.8670),
    "貢寮": (25.0230, 121.9040), "福隆": (25.0170, 121.9440),
    # ===== 平溪線 =====
    "大華": (25.0500, 121.8370), "十分": (25.0420, 121.7760),
    "望古": (25.0380, 121.7610), "嶺腳": (25.0350, 121.7490),
    "平溪": (25.0260, 121.7380), "菁桐": (25.0240, 121.7250),
    # ===== 深澳線 =====
    "海科館": (25.1370, 121.7890), "八斗子": (25.1380, 121.8010),
    # ===== 內灣線 =====
    "北新竹": (24.8060, 120.9830), "千甲": (24.8000, 120.9980),
    "新莊": (24.7950, 121.0120), "竹中": (24.7810, 121.0280),
    "上員": (24.7650, 121.0550), "榮華": (24.7480, 121.0780),
    "竹東": (24.7330, 121.0950), "橫山": (24.7200, 121.1150),
    "九讚頭": (24.7100, 121.1330), "合興": (24.7020, 121.1480),
    "富貴": (24.6950, 121.1630), "內灣": (24.6930, 121.1760),
    # ===== 六家線 =====
    "六家": (24.7870, 121.0360),
    # ===== 集集線 =====
    "源泉": (23.8120, 120.6350), "濁水": (23.8290, 120.6800),
    "龍泉": (23.8330, 120.7230), "集集": (23.8270, 120.7490),
    "水里": (23.8220, 120.8040), "車埕": (23.8330, 120.8370),
    # ===== 沙崙線 =====
    "長榮大學": (22.9320, 120.2560), "沙崙": (22.9220, 120.2770),
    # ===== 花蓮臨港線 =====
    "花蓮港": (23.9790, 121.6150),
}

def main():
    # 普悠瑪號停靠站（排除這些大站，保留秘境小站）
    PUYUMA_STOPS = {
        "基隆", "八堵", "七堵", "汐止", "南港", "松山", "臺北", "板橋",
        "樹林", "桃園", "中壢", "楊梅", "湖口", "新竹", "竹南",
        "後龍", "通霄", "苑裡", "大甲", "清水", "沙鹿",
        "造橋", "苗栗", "銅鑼", "三義",
        "后里", "豐原", "臺中", "新烏日", "彰化",
        "員林", "田中", "二水",
        "斗六", "大林", "民雄", "嘉義", "新營",
        "善化", "臺南", "保安", "新左營", "左營(舊城)",
        "高雄", "鳳山", "屏東", "潮州", "枋寮",
        "大武", "金崙", "太麻里", "知本", "臺東",
        "鹿野", "關山", "池上", "富里", "玉里",
        "瑞穗", "光復", "鳳林", "壽豐", "志學", "吉安", "花蓮",
        "新城(太魯閣)", "和平", "南澳", "蘇澳新",
        "羅東", "宜蘭", "礁溪", "頭城",
        "瑞芳", "四腳亭", "雙溪", "貢寮", "福隆",
        "岡山", "橋頭", "楠梓", "九曲堂",
        "林榮新光",
    }

    # 讀取 CSV
    stations = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["車站名稱"]
            lat, lng = COORDS.get(name, (23.5, 121.0))
            stations.append({
                "id": int(row["編號"]),
                "name": name,
                "city": row["縣市"],
                "line": row["路線"],
                "puyuma": name in PUYUMA_STOPS,
                "lat": lat,
                "lng": lng,
            })

    candidates = [s for s in stations if not s["puyuma"]]
    data_json = json.dumps(stations, ensure_ascii=False)
    candidates_json = json.dumps(candidates, ensure_ascii=False)
    quotes_json = json.dumps(STATION_QUOTES, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>台鐵車站抽籤機</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>
/* ---------- reset & base ---------- */
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Noto Sans TC','PingFang TC','Microsoft JhengHei',sans-serif;
  background:#1f1a14;color:#f0e6d6;overflow:hidden;height:100vh}}

/* ---------- layout ---------- */
#app{{display:flex;height:100vh}}
#panel{{width:420px;min-width:360px;display:flex;flex-direction:column;
  background:linear-gradient(180deg,#2a2118 0%,#1f1a14 100%);
  background-image:
    linear-gradient(180deg,#2a2118 0%,#1f1a14 100%),
    repeating-linear-gradient(90deg,transparent,transparent 40px,rgba(255,255,255,.01) 40px,rgba(255,255,255,.01) 41px),
    repeating-linear-gradient(0deg,transparent,transparent 80px,rgba(255,255,255,.008) 80px,rgba(255,255,255,.008) 81px);
  border-right:1px solid #4a3d2e;z-index:1000;position:relative;overflow:hidden}}
#map-wrap{{flex:1;position:relative}}
#map{{height:100%;width:100%;filter:sepia(.25) saturate(.9) brightness(.95) hue-rotate(5deg)}}

/* ---------- panel elements ---------- */
.panel-header{{text-align:center;padding:28px 20px 12px}}
.panel-header h1{{font-size:1.6rem;font-weight:700;
  background:linear-gradient(135deg,#e0a84c,#d47a4a);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.panel-header p{{font-size:.85rem;color:#b8a88e;margin-top:6px}}

/* stats bar */
.stats{{display:flex;justify-content:center;gap:16px;padding:10px;font-size:.78rem;color:#9a8a70}}
.stats span{{background:#2e2519;border:1px solid #4a3d2e;border-radius:8px;padding:4px 12px}}
.stats em{{color:#e0a84c;font-style:normal;font-weight:600}}

/* slot machine */
.slot-wrap{{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:10px 24px;gap:12px;overflow-y:auto;min-height:0}}
.slot-window{{width:100%;height:200px;border-radius:16px;overflow:hidden;position:relative;
  background:#1f1a14;border:2px solid #4a3d2e;
  box-shadow:inset 0 0 40px rgba(224,168,76,.06)}}
.slot-window.spinning{{border-color:#e0a84c;
  box-shadow:inset 0 0 40px rgba(224,168,76,.15),0 0 30px rgba(224,168,76,.1)}}
.slot-window.landed{{border-color:#d47a4a;
  box-shadow:inset 0 0 40px rgba(212,122,74,.2),0 0 40px rgba(212,122,74,.15)}}

/* mask gradients at top/bottom of slot */
.slot-window::before,.slot-window::after{{content:'';position:absolute;left:0;right:0;
  height:50px;z-index:2;pointer-events:none}}
.slot-window::before{{top:0;background:linear-gradient(#1f1a14,transparent)}}
.slot-window::after{{bottom:0;background:linear-gradient(transparent,#1f1a14)}}

.slot-track{{position:absolute;left:0;right:0;transition:none;will-change:transform}}
.slot-item{{height:50px;display:flex;align-items:center;justify-content:center;
  font-size:1.25rem;color:#7d6e58;white-space:nowrap}}
.slot-item.highlight{{color:#f1f5f9;font-size:1.6rem;font-weight:700;
  text-shadow:0 0 20px rgba(212,122,74,.5)}}

/* result card */
.result-card{{width:100%;background:linear-gradient(135deg,#2e2519,#261f16);
  border-radius:16px;padding:20px;text-align:center;
  border:1px solid #4a3d2e;min-height:110px;
  display:flex;flex-direction:column;align-items:center;justify-content:center}}
.result-card.has-result{{border-color:#d47a4a;
  box-shadow:0 0 30px rgba(212,122,74,.1)}}
.result-card .station-name{{font-size:2rem;font-weight:800;
  background:linear-gradient(135deg,#e0a84c,#d47a4a);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.result-card .station-meta{{font-size:.9rem;color:#b8a88e;margin-top:6px}}
.result-card .placeholder{{color:#7d6e58;font-size:.95rem}}
.result-card .station-quote{{font-size:.82rem;color:#b8a88e;margin-top:10px;
  font-style:italic;line-height:1.5;opacity:0;animation:quoteFade 1s .3s ease forwards}}
@keyframes quoteFade{{0%{{opacity:0;transform:translateY(6px)}}
  100%{{opacity:1;transform:translateY(0)}}}}

/* ---------- floating reveal overlay ---------- */
.reveal-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:9500;
  display:flex;align-items:center;justify-content:center;
  background:rgba(31,26,20,.7);backdrop-filter:blur(6px);
  opacity:0;pointer-events:none;transition:opacity .4s}}
.reveal-overlay.active{{opacity:1;pointer-events:auto}}
.reveal-card{{max-width:360px;width:90%;padding:32px 28px;border-radius:20px;
  background:linear-gradient(145deg,#2e2519 0%,#261f16 100%);
  border:1px solid rgba(212,122,74,.3);text-align:center;
  box-shadow:0 0 60px rgba(224,168,76,.1),0 20px 60px rgba(0,0,0,.4);
  transform:scale(0.85) translateY(20px);opacity:0;
  transition:all .5s cubic-bezier(.34,1.56,.64,1)}}
.reveal-overlay.active .reveal-card{{transform:scale(1) translateY(0);opacity:1}}
.reveal-card .rv-line{{font-size:.7rem;color:#7d6e58;text-transform:uppercase;
  letter-spacing:3px;margin-bottom:12px}}
.reveal-card .rv-name{{font-size:2.4rem;font-weight:900;
  background:linear-gradient(135deg,#e0a84c,#d47a4a,#c46a3a);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1.2}}
.reveal-card .rv-meta{{font-size:.85rem;color:#b8a88e;margin-top:8px}}
.reveal-card .rv-divider{{width:40px;height:2px;margin:16px auto;
  background:linear-gradient(90deg,transparent,#d47a4a,transparent);border-radius:1px}}
.reveal-card .rv-quote{{font-size:.88rem;color:#d4c8b0;font-style:italic;
  line-height:1.6;opacity:0;animation:quoteFade .8s .5s ease forwards}}
.reveal-card .rv-tap{{font-size:.65rem;color:#7d6e58;margin-top:20px;
  letter-spacing:1px}}

/* button */
.btn-draw{{width:100%;padding:16px;border:none;border-radius:14px;cursor:pointer;
  font-size:1.15rem;font-weight:700;letter-spacing:2px;
  background:linear-gradient(135deg,#c4882a,#e0a84c);color:#fff;
  box-shadow:0 4px 20px rgba(224,168,76,.35);transition:all .2s}}
.btn-draw:hover{{transform:translateY(-2px);box-shadow:0 6px 28px rgba(224,168,76,.45)}}
.btn-draw:active{{transform:translateY(0)}}
.btn-draw:disabled{{opacity:.5;cursor:not-allowed;transform:none}}

/* bottom controls */
.controls{{padding:16px 24px 24px;display:flex;flex-direction:column;gap:12px}}
.count-row{{display:flex;align-items:center;justify-content:center;gap:12px}}
.count-row label{{font-size:.85rem;color:#b8a88e}}
.count-row select{{background:#2e2519;border:1px solid #4a3d2e;color:#f0e6d6;
  border-radius:8px;padding:6px 14px;font-size:.95rem}}

/* filter tags */
.filter-group{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}
.filter-group-label{{width:100%;text-align:center;font-size:.7rem;color:#7d6e58;
  text-transform:uppercase;letter-spacing:1px;margin-bottom:2px}}
.filter-tag{{padding:4px 12px;border-radius:8px;font-size:.75rem;cursor:pointer;
  border:1px solid #4a3d2e;background:#2e2519;color:#7d6e58;
  transition:all .2s;user-select:none}}
.filter-tag.active{{background:linear-gradient(135deg,#c4882a,#e0a84c);
  color:#fff;border-color:#e0a84c;box-shadow:0 2px 8px rgba(224,168,76,.3)}}
.filter-tag:hover{{border-color:#e0a84c}}

/* progress bar */
.progress-wrap{{width:100%;padding:0 24px;margin-top:2px}}
.progress-bar{{width:100%;height:4px;background:#2e2519;border-radius:2px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:2px;transition:width .5s ease;
  background:linear-gradient(90deg,#c4882a,#d47a4a)}}
.progress-label{{display:flex;justify-content:center;align-items:center;gap:8px;
  font-size:.72rem;color:#7d6e58;margin-top:4px}}
.progress-label em{{color:#e0a84c;font-style:normal;font-weight:600}}
.btn-reset{{background:none;border:1px solid #4a3d2e;color:#7d6e58;
  padding:2px 8px;border-radius:4px;font-size:.65rem;cursor:pointer;transition:all .2s}}
.btn-reset:hover{{border-color:#c97a5a;color:#c97a5a}}

/* conquer overlay */
.conquer-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:rgba(31,26,20,.92);opacity:0;transition:opacity .5s;pointer-events:none}}
.conquer-overlay.active{{opacity:1;pointer-events:auto}}
.conquer-title{{font-size:3rem;font-weight:900;
  background:linear-gradient(135deg,#d47a4a,#e0a84c,#f0cc7a);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-shadow:0 0 80px rgba(212,122,74,.4)}}
.conquer-sub{{font-size:1.2rem;color:#b8a88e;margin-top:12px}}

/* history */
.history{{padding:0 24px 16px;max-height:90px;overflow-y:auto}}
.history h3{{font-size:.78rem;color:#7d6e58;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px}}
.history-list{{display:flex;flex-wrap:wrap;gap:6px}}
.history-tag{{background:#2e2519;border:1px solid #4a3d2e;border-radius:6px;
  padding:2px 10px;font-size:.75rem;color:#b8a88e}}

/* ---------- map custom ---------- */
.leaflet-popup-content-wrapper{{background:#2e2519;color:#f0e6d6;border:1px solid #4a3d2e;
  border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.5)}}
.leaflet-popup-tip{{background:#2e2519}}
.leaflet-popup-content{{font-family:inherit;font-size:.9rem;margin:12px 16px}}
.popup-name{{font-size:1.1rem;font-weight:700;color:#e0a84c}}
.popup-meta{{color:#b8a88e;font-size:.8rem;margin-top:4px}}

/* pulse marker */
@keyframes pulse{{
  0%{{transform:scale(1);opacity:.9}}
  50%{{transform:scale(1.8);opacity:.3}}
  100%{{transform:scale(2.4);opacity:0}}
}}
.marker-pulse{{position:absolute;width:24px;height:24px;border-radius:50%;
  background:rgba(212,122,74,.5);animation:pulse 1.5s ease-out infinite}}

/* sparkles (warm floating) */
@keyframes sparkle-drift{{
  0%{{transform:translateY(0) scale(0);opacity:0}}
  15%{{opacity:1;transform:translateY(-20px) scale(1.2)}}
  40%{{opacity:.8;transform:translateY(-50px) scale(1)}}
  100%{{transform:translateY(-140px) scale(0.2);opacity:0}}
}}
.sparkle{{position:absolute;border-radius:50%;
  box-shadow:0 0 6px currentColor;
  animation:sparkle-drift 2.5s ease-out forwards;pointer-events:none;z-index:3}}

/* ---------- countdown overlay ---------- */
.countdown-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:9999;display:flex;align-items:center;justify-content:center;
  background:rgba(31,26,20,.88);pointer-events:none;opacity:0;transition:opacity .3s}}
.countdown-overlay.active{{opacity:1}}
.countdown-num{{font-size:8rem;font-weight:900;color:transparent;
  background:linear-gradient(135deg,#e0a84c,#d47a4a,#c46a3a);
  -webkit-background-clip:text;text-shadow:0 0 80px rgba(224,168,76,.5);
  animation:countPop .6s ease-out forwards}}
.countdown-num.go{{font-size:5rem;letter-spacing:8px;
  background:linear-gradient(135deg,#d47a4a,#c46a3a,#e0a84c);
  -webkit-background-clip:text}}
@keyframes countPop{{
  0%{{transform:scale(0.3);opacity:0}}
  50%{{transform:scale(1.2);opacity:1}}
  100%{{transform:scale(1);opacity:1}}
}}

/* ---------- suspense text ---------- */
.suspense-text{{position:absolute;bottom:12px;left:0;right:0;text-align:center;
  font-size:.82rem;color:#e0a84c;z-index:4;opacity:0;
  transition:opacity .4s;pointer-events:none;font-style:italic}}
.suspense-text.visible{{opacity:1}}

/* ---------- screen flash (warm bloom) ---------- */
.screen-flash{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:9998;pointer-events:none;opacity:0;
  background:radial-gradient(circle,rgba(212,122,74,.25),rgba(224,168,76,.08) 60%,transparent 80%)}}
.screen-flash.flash{{animation:warmBloom 1.2s ease-out forwards}}
@keyframes warmBloom{{
  0%{{opacity:0}}
  15%{{opacity:1}}
  100%{{opacity:0}}
}}

/* ---------- result reveal ---------- */
@keyframes revealFadeUp{{
  0%{{opacity:0;transform:translateY(12px)}}
  100%{{opacity:1;transform:translateY(0)}}
}}
@keyframes revealWarmGlow{{
  0%{{box-shadow:0 0 0 rgba(212,122,74,0)}}
  40%{{box-shadow:0 0 40px rgba(212,122,74,.15),0 0 80px rgba(224,168,76,.08)}}
  100%{{box-shadow:0 0 20px rgba(212,122,74,.06)}}
}}
.result-card.reveal-anim{{
  animation:revealFadeUp .6s ease-out,revealWarmGlow 1.5s ease-out}}

/* ---------- falling leaves ---------- */
.leaves-container{{position:fixed;top:0;left:0;width:100%;height:100%;
  pointer-events:none;z-index:2;overflow:hidden}}
.leaf{{position:fixed;top:-50px;opacity:0;
  font-size:1.4rem;will-change:transform;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.15));
  animation:leafFall linear infinite}}
@keyframes leafFall{{
  0%{{opacity:0;transform:translateY(0) rotate(0deg) translateX(0)}}
  5%{{opacity:.8}}
  25%{{opacity:.65;transform:translateY(25vh) rotate(90deg) translateX(40px)}}
  50%{{opacity:.5;transform:translateY(50vh) rotate(180deg) translateX(-30px)}}
  75%{{opacity:.35;transform:translateY(75vh) rotate(270deg) translateX(20px)}}
  100%{{opacity:0;transform:translateY(110vh) rotate(360deg) translateX(-10px)}}
}}

/* panel nature deco */
.panel-deco{{position:absolute;pointer-events:none;opacity:.2;z-index:1;font-size:2.5rem}}
.panel-deco.top-left{{top:8px;left:8px;transform:rotate(-30deg)}}
.panel-deco.top-right{{top:8px;right:8px;transform:rotate(20deg) scaleX(-1)}}
.panel-deco.bot-left{{bottom:60px;left:8px;transform:rotate(15deg)}}
.panel-deco.bot-right{{bottom:60px;right:8px;transform:rotate(-25deg) scaleX(-1)}}

/* ---------- floating motes (ambient reveal) ---------- */
@keyframes mote-rise{{
  0%{{transform:translateY(0) scale(0);opacity:0}}
  20%{{opacity:.7;transform:translateY(-10vh) scale(1.1)}}
  50%{{opacity:.5}}
  100%{{transform:translateY(-70vh) scale(0.15);opacity:0}}
}}
.mote{{position:fixed;z-index:9997;pointer-events:none;border-radius:50%;
  box-shadow:0 0 8px currentColor;
  animation:mote-rise 4s ease-out forwards}}

/* responsive */
@media(max-width:800px){{
  html,body{{overflow:auto !important;height:auto !important}}
  #app{{flex-direction:column;height:auto;min-height:auto}}
  #panel{{width:100%;min-width:0;height:auto;max-height:none;
    border-right:none;border-bottom:1px solid #4a3d2e;overflow:visible}}
  #map-wrap{{width:100%;height:50vh;min-height:300px;position:relative;flex-shrink:0}}
  #map{{height:100% !important;width:100% !important;min-height:300px}}

  #map-wrap.map-expanded{{position:fixed;top:0;left:0;width:100vw;height:100vh;
    z-index:9000;min-height:100vh}}
  #map-wrap.map-expanded #map{{height:100vh !important;min-height:100vh}}
  .map-close-btn{{display:none;position:fixed;top:16px;right:16px;z-index:9001;
    background:rgba(31,26,20,.85);color:#f0e6d6;border:1px solid #7d6e58;
    border-radius:50%;width:40px;height:40px;font-size:1.2rem;cursor:pointer;
    backdrop-filter:blur(4px);transition:all .2s}}
  .map-close-btn:hover{{background:rgba(201,122,90,.7);border-color:#c46a3a}}
  #map-wrap.map-expanded ~ .map-close-btn,
  .map-close-btn.visible{{display:flex;align-items:center;justify-content:center}}

  .panel-header{{padding:16px 16px 6px}}
  .panel-header h1{{font-size:1.3rem}}
  .panel-header p{{font-size:.75rem;margin-top:3px}}

  .stats{{gap:8px;padding:6px 12px;font-size:.7rem}}
  .stats span{{padding:3px 8px}}

  .slot-wrap{{padding:8px 16px;gap:10px}}
  .slot-window{{height:140px}}
  .slot-item{{height:35px;font-size:1rem}}
  .slot-item.highlight{{font-size:1.3rem}}

  .result-card{{padding:14px;min-height:80px}}
  .result-card .station-name{{font-size:1.5rem}}
  .result-card .station-meta{{font-size:.8rem}}

  .info-card{{padding:8px 12px;gap:10px}}
  .info-card .card-emoji{{font-size:1.3rem;width:32px;height:32px;border-radius:8px}}
  .info-card .card-text{{font-size:.78rem}}
  .info-section-title{{font-size:.72rem}}

  .controls{{padding:10px 16px 16px;gap:8px}}
  .btn-draw{{padding:14px;font-size:1rem;letter-spacing:1px}}
  .count-row label{{font-size:.8rem}}
  .count-row select{{padding:5px 10px;font-size:.85rem}}

  .reveal-card{{padding:24px 20px;max-width:300px}}
  .reveal-card .rv-name{{font-size:2rem}}
  .reveal-card .rv-quote{{font-size:.82rem}}

  .filter-tag{{padding:3px 8px;font-size:.65rem}}
  .filter-group-label{{font-size:.6rem}}
  .progress-wrap{{padding:0 16px}}
  .progress-label{{font-size:.65rem}}

  .history{{padding:0 16px 12px;max-height:70px}}
  .history-tag{{font-size:.7rem;padding:2px 8px}}

  .countdown-num{{font-size:5rem}}
  .countdown-num.go{{font-size:3.5rem}}
}}
</style>
</head>
<body>
<!-- falling leaves -->
<div class="leaves-container" id="leavesContainer"></div>
<!-- countdown overlay -->
<div class="countdown-overlay" id="countdownOverlay"></div>
<!-- screen flash -->
<div class="screen-flash" id="screenFlash"></div>
<!-- reveal overlay -->
<div class="reveal-overlay" id="revealOverlay" onclick="dismissReveal()">
  <div class="reveal-card" id="revealCard"></div>
</div>
<!-- conquer overlay -->
<div class="conquer-overlay" id="conquerOverlay">
  <div class="conquer-title">&#127942; 恭喜全制霸！</div>
  <div class="conquer-sub">你已經抽過所有 {len(candidates)} 個秘境小站！</div>
</div>

<div id="app">
  <!-- ===== 左側面板 ===== -->
  <div id="panel">
    <span class="panel-deco top-left">🌿</span>
    <span class="panel-deco top-right">🍂</span>
    <span class="panel-deco bot-left">🍁</span>
    <span class="panel-deco bot-right">🌾</span>
    <div class="panel-header">
      <h1>台鐵車站抽籤機</h1>
      <p>排除普悠瑪號停靠站，探索秘境小站</p>
    </div>
    <div class="stats">
      <span>全部 <em>{len(stations)}</em> 站</span>
      <span>候選 <em id="statCandidateCount">{len(candidates)}</em> 站</span>
      <span>制霸 <em id="statProgress">0</em>/{len(candidates)}</span>
    </div>
    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
      <div class="progress-label">
        <span>已抽 <em id="progressText">0</em>/{len(candidates)} 站</span>
        <button class="btn-reset" id="btnReset" onclick="resetProgress()">重置</button>
      </div>
    </div>

    <div class="slot-wrap">
      <div class="slot-window" id="slotWindow">
        <div class="slot-track" id="slotTrack"></div>
        <div class="suspense-text" id="suspenseText"></div>
      </div>
      <div class="result-card" id="resultCard">
        <span class="placeholder">點擊下方按鈕開始抽籤</span>
      </div>

    </div>

    <div class="controls">
      <div class="filter-group" id="filterRegion">
        <span class="filter-group-label">區域</span>
      </div>
      <div class="count-row">
        <label for="drawCount">抽籤數量</label>
        <select id="drawCount">
          <option value="1" selected>1 站</option>
          <option value="2">2 站</option>
          <option value="3">3 站</option>
          <option value="5">5 站</option>
        </select>
      </div>
      <button class="btn-draw" id="btnDraw" onclick="startDraw()">開始抽籤</button>
    </div>

    <div class="history" id="historyWrap">
      <h3>抽籤記錄</h3>
      <div class="history-list" id="historyList">
        <span class="history-tag" style="color:#7d6e58">尚無記錄</span>
      </div>
    </div>
  </div>

  <!-- ===== 右側地圖 ===== -->
  <div id="map-wrap"><div id="map"></div></div>
  <button class="map-close-btn" id="mapCloseBtn" onclick="collapseMap()">&#10005;</button>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
// ============================================================
// Data
// ============================================================
const allStations  = {data_json};
const candidates   = {candidates_json};
const expressStations = allStations.filter(s => s.express);
const stationQuotes = {quotes_json};

// ============================================================
// Filter & Progress State
// ============================================================
const TOTAL_CANDIDATES = candidates.length;

const REGION_MAP = {{
  '北部': ['基隆市','新北市','臺北市','桃園市','新竹縣','新竹市'],
  '中部': ['苗栗縣','臺中市','彰化縣','南投縣','雲林縣'],
  '南部': ['嘉義縣','嘉義市','臺南市','高雄市','屏東縣'],
  '東部': ['宜蘭縣','花蓮縣','臺東縣'],
}};
const REGION_COLORS = {{
  '北部': {{ fill: '#7ca8c4', border: '#5a8aaa' }},
  '中部': {{ fill: '#e0a84c', border: '#c4882a' }},
  '南部': {{ fill: '#d47a4a', border: '#b86030' }},
  '東部': {{ fill: '#b07898', border: '#966080' }},
}};
const CITY_TO_REGION = {{}};
Object.entries(REGION_MAP).forEach(([region, cities]) => {{
  cities.forEach(c => {{ CITY_TO_REGION[c] = region; }});
}});

const activeRegions = new Set(Object.keys(REGION_MAP));

// localStorage persistence
let drawnStations = new Set(JSON.parse(localStorage.getItem('train-random-drawn') || '[]'));
let historyData = JSON.parse(localStorage.getItem('train-random-history') || '[]');

function saveDrawn() {{
  localStorage.setItem('train-random-drawn', JSON.stringify([...drawnStations]));
}}
function saveHistory() {{
  localStorage.setItem('train-random-history', JSON.stringify(historyData));
}}

function getFilteredCandidates() {{
  const allowedCities = new Set();
  activeRegions.forEach(r => REGION_MAP[r].forEach(c => allowedCities.add(c)));
  return candidates.filter(s =>
    allowedCities.has(s.city) && !drawnStations.has(s.name)
  );
}}

function updateFilteredCount() {{
  const pool = getFilteredCandidates();
  document.getElementById('statCandidateCount').textContent = pool.length;
  const btn = document.getElementById('btnDraw');
  if (pool.length === 0 && !isSpinning) {{
    btn.disabled = true;
    btn.textContent = drawnStations.size >= TOTAL_CANDIDATES
      ? '已全制霸！' : '無可用車站';
  }} else if (!isSpinning) {{
    btn.disabled = false;
    btn.textContent = '開始抽籤';
  }}
}}

function updateProgress() {{
  const count = drawnStations.size;
  const pct = (count / TOTAL_CANDIDATES * 100).toFixed(1);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressText').textContent = count;
  document.getElementById('statProgress').textContent = count;
}}

// ============================================================
// Web Audio API — Sound Effects
// ============================================================
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
function ensureAudio() {{ if (!audioCtx) audioCtx = new AudioCtx(); }}

function playTick(pitch) {{
  ensureAudio();
  // wooden percussion tick — warm, organic feel
  const t = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const osc2 = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const filter = audioCtx.createBiquadFilter();
  filter.type = 'bandpass';
  filter.frequency.value = 800 + pitch * 600;
  filter.Q.value = 8;
  osc.type = 'triangle';
  osc.frequency.value = 280 + pitch * 200;
  osc2.type = 'sine';
  osc2.frequency.value = 1200 + pitch * 800;
  gain.gain.setValueAtTime(0.06, t);
  gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
  osc.connect(filter);
  osc2.connect(gain);
  filter.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(t); osc.stop(t + 0.08);
  osc2.start(t); osc2.stop(t + 0.04);
}}

function playCountdownBeep(isGo) {{
  ensureAudio();
  const t = audioCtx.currentTime;
  // bell-like countdown tone
  const osc = audioCtx.createOscillator();
  const osc2 = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc2.type = 'sine';
  if (isGo) {{
    // rising two-tone chime for "go"
    osc.frequency.value = 659;
    osc2.frequency.value = 988;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.12, t + 0.02);
    gain.gain.setValueAtTime(0.12, t + 0.15);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
    osc.connect(gain); osc2.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(t); osc.stop(t + 0.25);
    osc2.start(t + 0.15); osc2.stop(t + 0.5);
  }} else {{
    // soft bell tap
    osc.frequency.value = 523;
    osc2.frequency.value = 1047;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.08, t + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
    osc.connect(gain); osc2.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(t); osc.stop(t + 0.3);
    osc2.start(t); osc2.stop(t + 0.15);
  }}
}}

function playArrivalChime() {{
  ensureAudio();
  // wind chime arrival melody — layered harmonics for warmth
  const t = audioCtx.currentTime;
  const melody = [
    {{ freq: 392, delay: 0,    dur: 0.9 }},  // G4
    {{ freq: 523, delay: 0.2,  dur: 0.8 }},  // C5
    {{ freq: 659, delay: 0.45, dur: 0.7 }},  // E5
    {{ freq: 784, delay: 0.7,  dur: 1.2 }},  // G5
    {{ freq: 1047, delay: 1.0, dur: 1.5 }},  // C6 (shimmer)
  ];
  // reverb via delay feedback
  const convolver = audioCtx.createGain();
  const delay = audioCtx.createDelay(0.5);
  const feedback = audioCtx.createGain();
  delay.delayTime.value = 0.12;
  feedback.gain.value = 0.2;
  convolver.connect(audioCtx.destination);
  convolver.connect(delay);
  delay.connect(feedback);
  feedback.connect(delay);
  delay.connect(audioCtx.destination);

  melody.forEach(n => {{
    const osc = audioCtx.createOscillator();
    const overtone = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    overtone.type = 'sine';
    osc.frequency.value = n.freq;
    overtone.frequency.value = n.freq * 2.01; // slight detune for shimmer
    const start = t + n.delay;
    gain.gain.setValueAtTime(0, start);
    gain.gain.linearRampToValueAtTime(0.07, start + 0.03);
    gain.gain.setValueAtTime(0.07, start + n.dur * 0.3);
    gain.gain.exponentialRampToValueAtTime(0.001, start + n.dur);
    osc.connect(gain);
    overtone.connect(gain);
    gain.connect(convolver);
    osc.start(start); osc.stop(start + n.dur);
    overtone.start(start); overtone.stop(start + n.dur);
  }});
}}

function playDrumRoll() {{
  ensureAudio();
  // soft taiko-inspired suspense roll — filtered low rumble
  const t = audioCtx.currentTime;
  const filter = audioCtx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 300;
  filter.Q.value = 2;
  filter.connect(audioCtx.destination);
  for (let i = 0; i < 16; i++) {{
    const hitT = t + i * 0.05;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.value = 80 + Math.random() * 30;
    const vol = 0.04 + i * 0.003;
    gain.gain.setValueAtTime(vol, hitT);
    gain.gain.exponentialRampToValueAtTime(0.001, hitT + 0.06);
    osc.connect(gain);
    gain.connect(filter);
    osc.start(hitT);
    osc.stop(hitT + 0.06);
  }}
}}

// ============================================================
// Floating Particles (ambient)
// ============================================================
(function initLeaves() {{
  const container = document.getElementById('leavesContainer');
  const leaves = ['🍂','🍁','🍃','🌿','🍂','🍁','🍃','🍂'];
  for (let i = 0; i < 18; i++) {{
    const l = document.createElement('div');
    l.className = 'leaf';
    l.textContent = leaves[Math.floor(Math.random() * leaves.length)];
    l.style.left = Math.random() * 100 + '%';
    l.style.fontSize = (0.8 + Math.random() * 1.0) + 'rem';
    l.style.animationDuration = (12 + Math.random() * 18) + 's';
    l.style.animationDelay = (Math.random() * 20) + 's';
    container.appendChild(l);
  }}
}})();

// ============================================================
// Map
// ============================================================
const map = L.map('map', {{
  center: [23.7, 121.0],
  zoom: 8,
  zoomControl: false,
  attributionControl: false,
}});

L.control.zoom({{ position: 'bottomright' }}).addTo(map);
L.control.attribution({{ position: 'bottomleft' }}).addTo(map);

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}@2x.png', {{
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19,
}}).addTo(map);

// 手機版：確保地圖正確渲染
if (window.matchMedia('(max-width:800px)').matches) {{
  setTimeout(() => {{ map.invalidateSize(); }}, 100);
  setTimeout(() => {{ map.invalidateSize(); }}, 500);
  setTimeout(() => {{ map.invalidateSize(); }}, 1500);
  window.addEventListener('resize', () => {{ map.invalidateSize(); }});
}}

const markerLayers = {{}};

expressStations.forEach(s => {{
  const m = L.circleMarker([s.lat, s.lng], {{
    radius: 3, fillColor: '#9a8a70', color: '#7d6e58',
    weight: 1, fillOpacity: 0.5,
  }}).addTo(map);
  m.bindTooltip(s.name, {{ className: 'dark-tooltip', direction: 'top', offset: [0,-5] }});
  markerLayers[s.name] = m;
}});

candidates.forEach(s => {{
  const region = CITY_TO_REGION[s.city] || '北部';
  const rc = REGION_COLORS[region];
  const m = L.circleMarker([s.lat, s.lng], {{
    radius: 5, fillColor: rc.fill, color: rc.border,
    weight: 1.5, fillOpacity: 0.7,
  }}).addTo(map);
  m.bindTooltip(s.name, {{ className: 'dark-tooltip', direction: 'top', offset: [0,-5] }});
  m._region = region;
  markerLayers[s.name] = m;
}});

let resultMarkers = [];

function clearResultMarkers() {{
  resultMarkers.forEach(m => map.removeLayer(m));
  resultMarkers = [];
}}

// ============================================================
// Mobile Map Expand / Collapse
// ============================================================
function expandMap() {{
  if (!isMobile) return;
  const wrap = document.getElementById('map-wrap');
  const btn = document.getElementById('mapCloseBtn');
  wrap.classList.add('map-expanded');
  btn.classList.add('visible');
  document.body.style.overflow = 'hidden';
  setTimeout(() => {{ map.invalidateSize(); }}, 100);
  setTimeout(() => {{ map.invalidateSize(); }}, 400);
}}

function collapseMap() {{
  const wrap = document.getElementById('map-wrap');
  const btn = document.getElementById('mapCloseBtn');
  wrap.classList.remove('map-expanded');
  btn.classList.remove('visible');
  document.body.style.overflow = '';
  setTimeout(() => {{ map.invalidateSize(); }}, 100);
}}

function addResultMarker(station) {{
  const pulse = L.divIcon({{
    className: '',
    html: '<div class="marker-pulse"></div>',
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  }});
  const pm = L.marker([station.lat, station.lng], {{ icon: pulse }}).addTo(map);
  resultMarkers.push(pm);

  const cm = L.circleMarker([station.lat, station.lng], {{
    radius: 10, fillColor: '#d47a4a', color: '#fff',
    weight: 2, fillOpacity: 0.9,
  }}).addTo(map);
  cm.bindPopup(
    '<div class="popup-name">' + station.name + '</div>' +
    '<div class="popup-meta">' + station.city + ' · ' + station.line + '</div>',
    {{ closeButton: false, autoClose: false }}
  ).openPopup();
  resultMarkers.push(cm);
}}

// ============================================================
// Map Flicker Effect (during spin)
// ============================================================
let flickerInterval = null;
let flickerHighlighted = [];

function restoreMarkerStyle(name) {{
  const m = markerLayers[name];
  if (!m) return;
  const s = candidates.find(c => c.name === name);
  if (!s) return;
  const region = CITY_TO_REGION[s.city] || '北部';
  const rc = REGION_COLORS[region];
  const active = activeRegions.has(region);
  m.setStyle({{ fillColor: active ? rc.fill : '#7d6e58', color: active ? rc.border : '#4a3d2e',
    fillOpacity: active ? 0.7 : 0.15 }});
  m.setRadius(active ? 5 : 3);
}}

function startMapFlicker() {{
  flickerInterval = setInterval(() => {{
    flickerHighlighted.forEach(name => restoreMarkerStyle(name));
    flickerHighlighted = [];
    for (let i = 0; i < 3; i++) {{
      const s = candidates[Math.floor(Math.random() * candidates.length)];
      const m = markerLayers[s.name];
      if (m) {{
        m.setStyle({{ fillColor: '#d47a4a', color: '#c46a3a', fillOpacity: 1 }});
        m.setRadius(9);
        flickerHighlighted.push(s.name);
      }}
    }}
  }}, 150);
}}

function stopMapFlicker() {{
  if (flickerInterval) clearInterval(flickerInterval);
  flickerInterval = null;
  flickerHighlighted.forEach(name => restoreMarkerStyle(name));
  flickerHighlighted = [];
}}

// ============================================================
// Suspense Text
// ============================================================
const suspenseMessages = [
  '列車正駛向未知的風景...',
  '窗外的光影正在變換...',
  '下一站，是專屬於你的故事...',
  '鐵軌的那一端，有風在等你...',
  '旅途的驚喜正在醞釀...',
  '慢慢來，好風景不會跑走...',
  '車輪轉動，帶你去一個溫柔的地方...',
  '這班列車，只為你停靠...',
];
let suspenseTimer = null;
const suspenseEl = document.getElementById('suspenseText');

function startSuspenseText() {{
  let idx = 0;
  suspenseEl.classList.add('visible');
  suspenseEl.textContent = suspenseMessages[0];
  suspenseTimer = setInterval(() => {{
    idx = (idx + 1) % suspenseMessages.length;
    suspenseEl.style.opacity = '0';
    setTimeout(() => {{
      suspenseEl.textContent = suspenseMessages[idx];
      suspenseEl.style.opacity = '1';
    }}, 300);
  }}, 1200);
}}

function stopSuspenseText() {{
  if (suspenseTimer) clearInterval(suspenseTimer);
  suspenseTimer = null;
  suspenseEl.classList.remove('visible');
}}

// ============================================================
// Countdown
// ============================================================
function runCountdown() {{
  return new Promise(resolve => {{
    const overlay = document.getElementById('countdownOverlay');
    overlay.classList.add('active');
    const steps = ['3', '2', '1', '出發'];
    let i = 0;

    function showStep() {{
      if (i >= steps.length) {{
        overlay.classList.remove('active');
        overlay.innerHTML = '';
        resolve();
        return;
      }}
      const isGo = steps[i] === 'GO!';
      playCountdownBeep(isGo);
      overlay.innerHTML = '<div class="countdown-num ' + (isGo ? 'go' : '') + '">' + steps[i] + '</div>';
      i++;
      setTimeout(showStep, isGo ? 500 : 700);
    }}

    showStep();
  }});
}}

// ============================================================
// Enhanced Confetti
// ============================================================
function spawnSparkles() {{
  const wrap = slotWindow;
  const colors = ['#e0a84c','#f0cc7a','#f5e0b0','#d47a4a','#c4882a','#c46a3a'];
  for (let i = 0; i < 25; i++) {{
    const s = document.createElement('div');
    s.className = 'sparkle';
    s.style.left = (10 + Math.random() * 80) + '%';
    s.style.bottom = (5 + Math.random() * 40) + '%';
    s.style.background = colors[Math.floor(Math.random() * colors.length)];
    s.style.animationDelay = (Math.random() * 1.2) + 's';
    s.style.animationDuration = (2 + Math.random() * 1.5) + 's';
    const size = 3 + Math.random() * 6;
    s.style.width = size + 'px';
    s.style.height = size + 'px';
    wrap.appendChild(s);
    setTimeout(() => s.remove(), 5000);
  }}
}}

function spawnMotes() {{
  const colors = ['#e0a84c','#f0cc7a','#d47a4a','#c4882a','#f5e0b0','#c46a3a','#e8c878'];
  for (let i = 0; i < 35; i++) {{
    const m = document.createElement('div');
    m.className = 'mote';
    const size = 3 + Math.random() * 8;
    m.style.width = size + 'px';
    m.style.height = size + 'px';
    m.style.left = (5 + Math.random() * 90) + 'vw';
    m.style.bottom = (Math.random() * 20) + 'vh';
    m.style.background = colors[Math.floor(Math.random() * colors.length)];
    m.style.animationDelay = (Math.random() * 2) + 's';
    m.style.animationDuration = (2.5 + Math.random() * 2.5) + 's';
    document.body.appendChild(m);
    setTimeout(() => m.remove(), 7000);
  }}
}}

// screen flash
function triggerScreenFlash() {{
  const flash = document.getElementById('screenFlash');
  flash.classList.remove('flash');
  void flash.offsetWidth; // reflow
  flash.classList.add('flash');
}}

// ============================================================
// Slot Machine
// ============================================================
const slotWindow = document.getElementById('slotWindow');
const slotTrack  = document.getElementById('slotTrack');
const resultCard = document.getElementById('resultCard');
const btnDraw    = document.getElementById('btnDraw');
const isMobile = window.matchMedia('(max-width:800px)').matches;
const ITEM_H = isMobile ? 35 : 50;

let isSpinning = false;

function buildTrack(filteredPool) {{
  slotTrack.innerHTML = '';
  const source = filteredPool || candidates;
  const pool = [];
  for (let i = 0; i < 80; i++) {{
    pool.push(source[Math.floor(Math.random() * source.length)]);
  }}
  pool.forEach((s, i) => {{
    const div = document.createElement('div');
    div.className = 'slot-item';
    div.textContent = s.name + '\uff08' + s.city + '\uff09';
    div.dataset.index = i;
    slotTrack.appendChild(div);
  }});
  const initOffset = isMobile ? 52 : 75;
  slotTrack.style.transform = 'translateY(' + initOffset + 'px)';
  return pool;
}}

// main draw — now with countdown + suspense + flicker + sound
async function startDraw() {{
  if (isSpinning) return;
  const pool = getFilteredCandidates();
  if (pool.length === 0) return;

  isSpinning = true;
  btnDraw.disabled = true;
  ensureAudio();

  const count = Math.min(parseInt(document.getElementById('drawCount').value), pool.length);
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  const winners = shuffled.slice(0, count);

  clearResultMarkers();
  map.flyTo([23.7, 121.0], 8, {{ duration: 1.0 }});
  resultCard.classList.remove('has-result', 'reveal-anim');
  resultCard.innerHTML = '<span class="placeholder">準備中...</span>';

  // ---- COUNTDOWN ----
  await runCountdown();

  // expand map on mobile for better animation view
  expandMap();

  // ---- SEQUENTIAL ANIMATION ----
  let seq = 0;
  function animateOne() {{
    const winner = winners[seq];
    const filteredPool = getFilteredCandidates();
    const displayPool = filteredPool.length > 0 ? filteredPool : candidates;
    const pool = buildTrack(displayPool);

    const landIndex = 60 + Math.floor(Math.random() * 5);
    const landItem = slotTrack.children[landIndex];
    landItem.textContent = winner.name + '\uff08' + winner.city + '\uff09';

    slotWindow.classList.add('spinning');
    slotWindow.classList.remove('landed');

    // start effects
    startSuspenseText();
    startMapFlicker();
    playDrumRoll();

    const baseOffset = isMobile ? 52 : 75;
    const targetY = baseOffset - landIndex * ITEM_H;
    const duration = 3500 + Math.random() * 500;
    const startTime = performance.now();
    const startY = baseOffset;
    let lastTickItem = -1;

    function easeOutQuint(t) {{ return 1 - Math.pow(1 - t, 5); }}

    function tick(now) {{
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutQuint(progress);
      const currentY = startY + (targetY - startY) * eased;
      slotTrack.style.transform = 'translateY(' + currentY + 'px)';

      // tick sound — play a click for each item passed
      const currentItem = Math.floor(Math.abs(currentY - 75) / ITEM_H);
      if (currentItem !== lastTickItem) {{
        lastTickItem = currentItem;
        if (progress < 0.85) playTick(progress);
      }}

      if (progress < 1) {{
        requestAnimationFrame(tick);
      }} else {{
        // ===== LANDED! =====
        slotWindow.classList.remove('spinning');
        slotWindow.classList.add('landed');
        landItem.classList.add('highlight');

        // stop effects
        stopSuspenseText();
        stopMapFlicker();

        // reveal effects
        playArrivalChime();
        triggerScreenFlash();
        spawnSparkles();
        spawnMotes();

        // show floating reveal card
        showRevealOverlay(winner);

        // show on map (behind the overlay)
        addResultMarker(winner);
        map.flyTo([winner.lat, winner.lng], 13, {{ duration: 1.8 }});

        // update result card (visible after overlay dismisses)
        showResult(winners.slice(0, seq + 1));
        resultCard.classList.remove('reveal-anim');
        void resultCard.offsetWidth;
        resultCard.classList.add('reveal-anim');

        // add to history & track drawn
        drawnStations.add(winner.name);
        saveDrawn();
        historyData.unshift({{ name: winner.name, city: winner.city, line: winner.line, time: new Date().toISOString() }});
        saveHistory();
        updateProgress();
        renderHistory();

        seq++;
        if (seq < winners.length) {{
          setTimeout(animateOne, 3500);
        }} else {{
          // mobile: map is already expanded, invalidate after flyTo
          if (isMobile) {{
            setTimeout(() => {{ map.invalidateSize(); }}, 600);
          }}
          isSpinning = false;
          btnDraw.disabled = false;
          updateFilteredCount();
          checkConquer();
        }}
      }}
    }}
    requestAnimationFrame(tick);
  }}

  animateOne();
}}

// ============================================================
// Floating Reveal Overlay
// ============================================================
let revealTimeout = null;

function showRevealOverlay(winner) {{
  const overlay = document.getElementById('revealOverlay');
  const card = document.getElementById('revealCard');
  const quote = stationQuotes[winner.name] || '';
  const region = CITY_TO_REGION[winner.city] || '北部';
  const rc = REGION_COLORS[region];

  card.innerHTML =
    '<div class="rv-line">下一站</div>' +
    '<div class="rv-name">' + winner.name + '</div>' +
    '<div class="rv-meta">' + winner.city + ' \u00b7 ' + winner.line + '</div>' +
    (quote ? '<div class="rv-divider"></div><div class="rv-quote">\u300c' + quote + '\u300d</div>' : '') +
    '<div class="rv-tap">點擊任意處繼續</div>';

  card.style.borderColor = rc.fill;
  card.style.boxShadow = '0 0 60px ' + rc.fill + '20,0 20px 60px rgba(0,0,0,.4)';
  overlay.classList.add('active');

  if (revealTimeout) clearTimeout(revealTimeout);
  revealTimeout = setTimeout(dismissReveal, 5000);
}}

function dismissReveal() {{
  if (revealTimeout) {{ clearTimeout(revealTimeout); revealTimeout = null; }}
  document.getElementById('revealOverlay').classList.remove('active');
}}

function showResult(winners) {{
  resultCard.classList.add('has-result');
  if (winners.length === 1) {{
    const w = winners[0];
    const quote = stationQuotes[w.name] || '';
    resultCard.innerHTML =
      '<div class="station-name">' + w.name + '</div>' +
      '<div class="station-meta">' + w.city + ' \u00b7 ' + w.line + '</div>' +
      (quote ? '<div class="station-quote">\u300c' + quote + '\u300d</div>' : '');
  }} else {{
    const lastWinner = winners[winners.length - 1];
    const quote = stationQuotes[lastWinner.name] || '';
    resultCard.innerHTML = winners.map((w, i) =>
      '<div style="margin-bottom:4px">' +
      '<span class="station-name" style="font-size:1.3rem">[' + (i+1) + '] ' + w.name + '</span>' +
      ' <span class="station-meta" style="font-size:.78rem">' + w.city + '</span></div>'
    ).join('') + (quote ? '<div class="station-quote">\u300c' + quote + '\u300d</div>' : '');
  }}
}}

// ============================================================
// Filter Tags — render & toggle
// ============================================================
function updateMapRegions() {{
  candidates.forEach(s => {{
    restoreMarkerStyle(s.name);
  }});
}}

function renderFilterTags() {{
  const regionWrap = document.getElementById('filterRegion');
  regionWrap.innerHTML = '<span class="filter-group-label">區域</span>';

  Object.keys(REGION_MAP).forEach(name => {{
    const rc = REGION_COLORS[name];
    const tag = document.createElement('span');
    tag.className = 'filter-tag' + (activeRegions.has(name) ? ' active' : '');
    tag.textContent = name;
    if (activeRegions.has(name)) {{
      tag.style.background = 'linear-gradient(135deg,' + rc.fill + ',' + rc.border + ')';
      tag.style.borderColor = rc.border;
    }}
    tag.onclick = () => {{
      if (activeRegions.has(name)) activeRegions.delete(name);
      else activeRegions.add(name);
      renderFilterTags();
      updateFilteredCount();
      updateMapRegions();
    }};
    regionWrap.appendChild(tag);
  }});
}}

// ============================================================
// Reset progress
// ============================================================
function resetProgress() {{
  if (!confirm('確定要重置制霸進度嗎？所有抽籤記錄將被清除')) return;
  drawnStations.clear();
  historyData = [];
  saveDrawn();
  saveHistory();
  updateProgress();
  updateFilteredCount();
  renderHistory();
}}

// ============================================================
// History — render with timestamps
// ============================================================
function renderHistory() {{
  const list = document.getElementById('historyList');
  if (historyData.length === 0) {{
    list.innerHTML = '<span class="history-tag" style="color:#7d6e58">尚無記錄</span>';
    return;
  }}
  list.innerHTML = historyData.slice(0, 50).map(h => {{
    const d = new Date(h.time);
    const label = (d.getMonth() + 1) + '/' + d.getDate() + ' ' + h.name;
    return '<span class="history-tag">' + label + '</span>';
  }}).join('');
}}

// ============================================================
// Conquer-all celebration
// ============================================================
function checkConquer() {{
  if (drawnStations.size >= TOTAL_CANDIDATES) {{
    const overlay = document.getElementById('conquerOverlay');
    overlay.classList.add('active');
    spawnMotes();
    spawnMotes();
    setTimeout(() => overlay.classList.remove('active'), 4000);
  }}
}}

// ============================================================
// Init
// ============================================================
renderFilterTags();
renderHistory();
updateProgress();
updateFilteredCount();
updateMapRegions();
buildTrack();
</script>
</body>
</html>"""

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已產出: {OUT_PATH}")
    print(f"  全部車站: {len(stations)} 站")
    print(f"  候選車站: {len(candidates)} 站 (排除普悠瑪號)")
    print(f"  請用瀏覽器開啟 draw_station.html")


if __name__ == "__main__":
    main()
