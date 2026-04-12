#!/usr/bin/env python3
"""
讀取 taiwan_railway_stations.csv，結合車站座標，
產出一個包含地圖 + 抽籤動畫的 HTML 網頁應用。
"""

import csv, json, os

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
                "express": row["自強號停靠"] == "Y",
                "lat": lat,
                "lng": lng,
            })

    candidates = [s for s in stations if not s["express"]]
    data_json = json.dumps(stations, ensure_ascii=False)
    candidates_json = json.dumps(candidates, ensure_ascii=False)

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
  background:#0f172a;color:#e2e8f0;overflow:hidden;height:100vh}}

/* ---------- layout ---------- */
#app{{display:flex;height:100vh}}
#panel{{width:420px;min-width:360px;display:flex;flex-direction:column;
  background:linear-gradient(180deg,#1e293b 0%,#0f172a 100%);
  border-right:1px solid #334155;z-index:1000;position:relative}}
#map-wrap{{flex:1;position:relative}}
#map{{height:100%;width:100%}}

/* ---------- panel elements ---------- */
.panel-header{{text-align:center;padding:28px 20px 12px}}
.panel-header h1{{font-size:1.6rem;font-weight:700;
  background:linear-gradient(135deg,#38bdf8,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.panel-header p{{font-size:.85rem;color:#94a3b8;margin-top:6px}}

/* stats bar */
.stats{{display:flex;justify-content:center;gap:16px;padding:10px;font-size:.78rem;color:#64748b}}
.stats span{{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:4px 12px}}
.stats em{{color:#38bdf8;font-style:normal;font-weight:600}}

/* slot machine */
.slot-wrap{{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:10px 24px;gap:16px}}
.slot-window{{width:100%;height:200px;border-radius:16px;overflow:hidden;position:relative;
  background:#0f172a;border:2px solid #334155;
  box-shadow:inset 0 0 40px rgba(56,189,248,.06)}}
.slot-window.spinning{{border-color:#818cf8;
  box-shadow:inset 0 0 40px rgba(129,140,248,.15),0 0 30px rgba(129,140,248,.1)}}
.slot-window.landed{{border-color:#38bdf8;
  box-shadow:inset 0 0 40px rgba(56,189,248,.2),0 0 40px rgba(56,189,248,.15)}}

/* mask gradients at top/bottom of slot */
.slot-window::before,.slot-window::after{{content:'';position:absolute;left:0;right:0;
  height:50px;z-index:2;pointer-events:none}}
.slot-window::before{{top:0;background:linear-gradient(#0f172a,transparent)}}
.slot-window::after{{bottom:0;background:linear-gradient(transparent,#0f172a)}}

.slot-track{{position:absolute;left:0;right:0;transition:none;will-change:transform}}
.slot-item{{height:50px;display:flex;align-items:center;justify-content:center;
  font-size:1.25rem;color:#64748b;white-space:nowrap}}
.slot-item.highlight{{color:#f1f5f9;font-size:1.6rem;font-weight:700;
  text-shadow:0 0 20px rgba(56,189,248,.5)}}

/* result card */
.result-card{{width:100%;background:linear-gradient(135deg,#1e293b,#1a1f35);
  border-radius:16px;padding:20px;text-align:center;
  border:1px solid #334155;min-height:110px;
  display:flex;flex-direction:column;align-items:center;justify-content:center}}
.result-card.has-result{{border-color:#38bdf8;
  box-shadow:0 0 30px rgba(56,189,248,.1)}}
.result-card .station-name{{font-size:2rem;font-weight:800;
  background:linear-gradient(135deg,#38bdf8,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.result-card .station-meta{{font-size:.9rem;color:#94a3b8;margin-top:6px}}
.result-card .placeholder{{color:#475569;font-size:.95rem}}

/* button */
.btn-draw{{width:100%;padding:16px;border:none;border-radius:14px;cursor:pointer;
  font-size:1.15rem;font-weight:700;letter-spacing:2px;
  background:linear-gradient(135deg,#6366f1,#818cf8);color:#fff;
  box-shadow:0 4px 20px rgba(99,102,241,.35);transition:all .2s}}
.btn-draw:hover{{transform:translateY(-2px);box-shadow:0 6px 28px rgba(99,102,241,.45)}}
.btn-draw:active{{transform:translateY(0)}}
.btn-draw:disabled{{opacity:.5;cursor:not-allowed;transform:none}}

/* bottom controls */
.controls{{padding:16px 24px 24px;display:flex;flex-direction:column;gap:12px}}
.count-row{{display:flex;align-items:center;justify-content:center;gap:12px}}
.count-row label{{font-size:.85rem;color:#94a3b8}}
.count-row select{{background:#1e293b;border:1px solid #334155;color:#e2e8f0;
  border-radius:8px;padding:6px 14px;font-size:.95rem}}

/* history */
.history{{padding:0 24px 16px;max-height:90px;overflow-y:auto}}
.history h3{{font-size:.78rem;color:#475569;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px}}
.history-list{{display:flex;flex-wrap:wrap;gap:6px}}
.history-tag{{background:#1e293b;border:1px solid #334155;border-radius:6px;
  padding:2px 10px;font-size:.75rem;color:#94a3b8}}

/* ---------- map custom ---------- */
.leaflet-popup-content-wrapper{{background:#1e293b;color:#e2e8f0;border:1px solid #334155;
  border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.5)}}
.leaflet-popup-tip{{background:#1e293b}}
.leaflet-popup-content{{font-family:inherit;font-size:.9rem;margin:12px 16px}}
.popup-name{{font-size:1.1rem;font-weight:700;color:#38bdf8}}
.popup-meta{{color:#94a3b8;font-size:.8rem;margin-top:4px}}

/* pulse marker */
@keyframes pulse{{
  0%{{transform:scale(1);opacity:.9}}
  50%{{transform:scale(1.8);opacity:.3}}
  100%{{transform:scale(2.4);opacity:0}}
}}
.marker-pulse{{position:absolute;width:24px;height:24px;border-radius:50%;
  background:rgba(56,189,248,.5);animation:pulse 1.5s ease-out infinite}}

/* confetti */
@keyframes confetti-fall{{
  0%{{transform:translateY(-10px) rotate(0deg) scale(1);opacity:1}}
  70%{{opacity:1}}
  100%{{transform:translateY(350px) rotate(1080deg) scale(0.3);opacity:0}}
}}
.confetti{{position:absolute;width:10px;height:10px;border-radius:2px;
  animation:confetti-fall 2.2s ease-in forwards;pointer-events:none;z-index:3}}

/* ---------- countdown overlay ---------- */
.countdown-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:9999;display:flex;align-items:center;justify-content:center;
  background:rgba(15,23,42,.85);pointer-events:none;opacity:0;transition:opacity .3s}}
.countdown-overlay.active{{opacity:1}}
.countdown-num{{font-size:8rem;font-weight:900;color:transparent;
  background:linear-gradient(135deg,#38bdf8,#818cf8,#f472b6);
  -webkit-background-clip:text;text-shadow:0 0 80px rgba(56,189,248,.5);
  animation:countPop .6s ease-out forwards}}
.countdown-num.go{{font-size:5rem;letter-spacing:8px;
  background:linear-gradient(135deg,#fbbf24,#fb923c,#f472b6);
  -webkit-background-clip:text}}
@keyframes countPop{{
  0%{{transform:scale(0.3);opacity:0}}
  50%{{transform:scale(1.2);opacity:1}}
  100%{{transform:scale(1);opacity:1}}
}}

/* ---------- suspense text ---------- */
.suspense-text{{position:absolute;bottom:12px;left:0;right:0;text-align:center;
  font-size:.82rem;color:#818cf8;z-index:4;opacity:0;
  transition:opacity .4s;pointer-events:none;font-style:italic}}
.suspense-text.visible{{opacity:1}}

/* ---------- screen flash ---------- */
.screen-flash{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:9998;pointer-events:none;opacity:0;
  background:radial-gradient(circle,rgba(56,189,248,.4),transparent 70%)}}
.screen-flash.flash{{animation:flashBang .5s ease-out forwards}}
@keyframes flashBang{{
  0%{{opacity:1}}
  100%{{opacity:0}}
}}

/* ---------- result reveal ---------- */
@keyframes revealShake{{
  0%,100%{{transform:translateX(0)}}
  10%,30%,50%,70%,90%{{transform:translateX(-4px)}}
  20%,40%,60%,80%{{transform:translateX(4px)}}
}}
@keyframes revealGlow{{
  0%{{box-shadow:0 0 0 rgba(56,189,248,0)}}
  50%{{box-shadow:0 0 60px rgba(56,189,248,.4),0 0 120px rgba(129,140,248,.2)}}
  100%{{box-shadow:0 0 30px rgba(56,189,248,.15)}}
}}
.result-card.reveal-anim{{
  animation:revealShake .5s ease-out,revealGlow 1.2s ease-out}}

/* ---------- floating particles ---------- */
.particles-container{{position:fixed;top:0;left:0;width:100%;height:100%;
  pointer-events:none;z-index:0;overflow:hidden}}
.particle{{position:absolute;border-radius:50%;opacity:0;
  animation:floatUp linear infinite}}
@keyframes floatUp{{
  0%{{opacity:0;transform:translateY(100vh) scale(0)}}
  10%{{opacity:.6}}
  90%{{opacity:.3}}
  100%{{opacity:0;transform:translateY(-10vh) scale(1)}}
}}

/* ---------- big confetti full screen ---------- */
@keyframes confetti-full{{
  0%{{transform:translateY(-20px) rotate(0deg) scale(1);opacity:1}}
  80%{{opacity:.8}}
  100%{{transform:translateY(100vh) rotate(1440deg) scale(0.2);opacity:0}}
}}
.confetti-big{{position:fixed;z-index:9997;pointer-events:none;
  animation:confetti-full 3s ease-in forwards}}

/* responsive */
@media(max-width:800px){{
  #app{{flex-direction:column}}
  #panel{{width:100%;height:55vh;min-width:0}}
  #map-wrap{{height:45vh}}
}}
</style>
</head>
<body>
<!-- floating particles -->
<div class="particles-container" id="particlesContainer"></div>
<!-- countdown overlay -->
<div class="countdown-overlay" id="countdownOverlay"></div>
<!-- screen flash -->
<div class="screen-flash" id="screenFlash"></div>

<div id="app">
  <!-- ===== 左側面板 ===== -->
  <div id="panel">
    <div class="panel-header">
      <h1>台鐵車站抽籤機</h1>
      <p>排除自強號停靠站，探索秘境小站</p>
    </div>
    <div class="stats">
      <span>全部 <em>{len(stations)}</em> 站</span>
      <span>候選 <em>{len(candidates)}</em> 站</span>
      <span>已排除自強號 <em>{len(stations)-len(candidates)}</em> 站</span>
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

    <div class="history" id="historyWrap" style="display:none">
      <h3>抽籤記錄</h3>
      <div class="history-list" id="historyList"></div>
    </div>
  </div>

  <!-- ===== 右側地圖 ===== -->
  <div id="map-wrap"><div id="map"></div></div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
// ============================================================
// Data
// ============================================================
const allStations  = {data_json};
const candidates   = {candidates_json};
const expressStations = allStations.filter(s => s.express);

// ============================================================
// Web Audio API — Sound Effects
// ============================================================
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
function ensureAudio() {{ if (!audioCtx) audioCtx = new AudioCtx(); }}

function playTick(pitch) {{
  ensureAudio();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.frequency.value = 600 + pitch * 400;
  gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.06);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.06);
}}

function playCountdownBeep(isGo) {{
  ensureAudio();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = isGo ? 'square' : 'sine';
  osc.frequency.value = isGo ? 880 : 440;
  gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + (isGo ? 0.3 : 0.15));
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + (isGo ? 0.3 : 0.15));
}}

function playFanfare() {{
  ensureAudio();
  const notes = [523, 659, 784, 1047];
  notes.forEach((freq, i) => {{
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.value = freq;
    const t = audioCtx.currentTime + i * 0.12;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.12, t + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(t);
    osc.stop(t + 0.5);
  }});
}}

function playDrumRoll() {{
  ensureAudio();
  for (let i = 0; i < 20; i++) {{
    const t = audioCtx.currentTime + i * 0.04;
    const noise = audioCtx.createBufferSource();
    const buffer = audioCtx.createBuffer(1, audioCtx.sampleRate * 0.03, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let j = 0; j < data.length; j++) data[j] = (Math.random() * 2 - 1) * 0.3;
    noise.buffer = buffer;
    const gain = audioCtx.createGain();
    gain.gain.setValueAtTime(0.06 + i * 0.004, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
    noise.connect(gain);
    gain.connect(audioCtx.destination);
    noise.start(t);
  }}
}}

// ============================================================
// Floating Particles (ambient)
// ============================================================
(function initParticles() {{
  const container = document.getElementById('particlesContainer');
  const colors = ['#38bdf8','#818cf8','#6366f1','#f472b6','#34d399'];
  for (let i = 0; i < 25; i++) {{
    const p = document.createElement('div');
    p.className = 'particle';
    const size = 2 + Math.random() * 4;
    p.style.width = size + 'px';
    p.style.height = size + 'px';
    p.style.left = Math.random() * 100 + '%';
    p.style.background = colors[Math.floor(Math.random() * colors.length)];
    p.style.animationDuration = (8 + Math.random() * 12) + 's';
    p.style.animationDelay = (Math.random() * 15) + 's';
    container.appendChild(p);
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

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19,
}}).addTo(map);

const markerLayers = {{}};

expressStations.forEach(s => {{
  const m = L.circleMarker([s.lat, s.lng], {{
    radius: 3, fillColor: '#475569', color: '#334155',
    weight: 1, fillOpacity: 0.5,
  }}).addTo(map);
  m.bindTooltip(s.name, {{ className: 'dark-tooltip', direction: 'top', offset: [0,-5] }});
  markerLayers[s.name] = m;
}});

candidates.forEach(s => {{
  const m = L.circleMarker([s.lat, s.lng], {{
    radius: 5, fillColor: '#818cf8', color: '#6366f1',
    weight: 1.5, fillOpacity: 0.7,
  }}).addTo(map);
  m.bindTooltip(s.name, {{ className: 'dark-tooltip', direction: 'top', offset: [0,-5] }});
  markerLayers[s.name] = m;
}});

let resultMarkers = [];

function clearResultMarkers() {{
  resultMarkers.forEach(m => map.removeLayer(m));
  resultMarkers = [];
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
    radius: 10, fillColor: '#38bdf8', color: '#fff',
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

function startMapFlicker() {{
  flickerInterval = setInterval(() => {{
    // reset previous
    flickerHighlighted.forEach(name => {{
      const m = markerLayers[name];
      if (m) m.setStyle({{ fillColor: '#818cf8', color: '#6366f1', radius: 5, fillOpacity: 0.7 }});
    }});
    flickerHighlighted = [];
    // highlight 3 random candidates
    for (let i = 0; i < 3; i++) {{
      const s = candidates[Math.floor(Math.random() * candidates.length)];
      const m = markerLayers[s.name];
      if (m) {{
        m.setStyle({{ fillColor: '#fbbf24', color: '#f59e0b', radius: 9, fillOpacity: 1 }});
        flickerHighlighted.push(s.name);
      }}
    }}
  }}, 150);
}}

function stopMapFlicker() {{
  if (flickerInterval) clearInterval(flickerInterval);
  flickerInterval = null;
  flickerHighlighted.forEach(name => {{
    const m = markerLayers[name];
    if (m) m.setStyle({{ fillColor: '#818cf8', color: '#6366f1', radius: 5, fillOpacity: 0.7 }});
  }});
  flickerHighlighted = [];
}}

// ============================================================
// Suspense Text
// ============================================================
const suspenseMessages = [
  '命運之輪啟動中...',
  '宇宙正在為你挑選...',
  '車站們在竊竊私語...',
  '鐵軌的盡頭是驚喜...',
  '月台正在向你招手...',
  '列車即將抵達命運站...',
  '緣分正在加速中...',
  '秘境小站已經迫不及待了...',
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
    const steps = ['3', '2', '1', 'GO!'];
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
function spawnConfetti() {{
  const wrap = slotWindow;
  const colors = ['#38bdf8','#818cf8','#f472b6','#34d399','#fbbf24','#fb923c'];
  for (let i = 0; i < 50; i++) {{
    const c = document.createElement('div');
    c.className = 'confetti';
    c.style.left = Math.random() * 100 + '%';
    c.style.top = (30 + Math.random() * 20) + '%';
    c.style.background = colors[Math.floor(Math.random() * colors.length)];
    c.style.animationDelay = (Math.random() * 0.5) + 's';
    c.style.animationDuration = (1.5 + Math.random() * 1) + 's';
    c.style.width = (6 + Math.random() * 8) + 'px';
    c.style.height = (6 + Math.random() * 8) + 'px';
    c.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    wrap.appendChild(c);
    setTimeout(() => c.remove(), 3000);
  }}
}}

function spawnFullScreenConfetti() {{
  const colors = ['#38bdf8','#818cf8','#f472b6','#34d399','#fbbf24','#fb923c','#e879f9','#22d3ee'];
  for (let i = 0; i < 60; i++) {{
    const c = document.createElement('div');
    c.className = 'confetti-big';
    const size = 8 + Math.random() * 12;
    c.style.width = size + 'px';
    c.style.height = size + 'px';
    c.style.left = Math.random() * 100 + 'vw';
    c.style.top = '-20px';
    c.style.background = colors[Math.floor(Math.random() * colors.length)];
    c.style.borderRadius = Math.random() > 0.5 ? '50%' : '3px';
    c.style.animationDelay = (Math.random() * 0.8) + 's';
    c.style.animationDuration = (2 + Math.random() * 2) + 's';
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 5000);
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
const ITEM_H = 50;

let isSpinning = false;
let history = [];

function buildTrack() {{
  slotTrack.innerHTML = '';
  const pool = [];
  for (let i = 0; i < 80; i++) {{
    pool.push(candidates[Math.floor(Math.random() * candidates.length)]);
  }}
  pool.forEach((s, i) => {{
    const div = document.createElement('div');
    div.className = 'slot-item';
    div.textContent = s.name + '\uff08' + s.city + '\uff09';
    div.dataset.index = i;
    slotTrack.appendChild(div);
  }});
  slotTrack.style.transform = 'translateY(75px)';
  return pool;
}}

// main draw — now with countdown + suspense + flicker + sound
async function startDraw() {{
  if (isSpinning) return;
  isSpinning = true;
  btnDraw.disabled = true;
  ensureAudio();

  const count = parseInt(document.getElementById('drawCount').value);
  const shuffled = [...candidates].sort(() => Math.random() - 0.5);
  const winners = shuffled.slice(0, count);

  clearResultMarkers();
  map.flyTo([23.7, 121.0], 8, {{ duration: 1.0 }});
  resultCard.classList.remove('has-result', 'reveal-anim');
  resultCard.innerHTML = '<span class="placeholder">準備中...</span>';

  // ---- COUNTDOWN ----
  await runCountdown();

  // ---- SEQUENTIAL ANIMATION ----
  let seq = 0;
  function animateOne() {{
    const winner = winners[seq];
    const pool = buildTrack();

    const landIndex = 60 + Math.floor(Math.random() * 5);
    const landItem = slotTrack.children[landIndex];
    landItem.textContent = winner.name + '\uff08' + winner.city + '\uff09';

    slotWindow.classList.add('spinning');
    slotWindow.classList.remove('landed');

    // start effects
    startSuspenseText();
    startMapFlicker();
    playDrumRoll();

    const targetY = 75 - landIndex * ITEM_H;
    const duration = 3500 + Math.random() * 500;
    const startTime = performance.now();
    const startY = 75;
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

        // big reveal!
        playFanfare();
        triggerScreenFlash();
        spawnConfetti();
        spawnFullScreenConfetti();

        // show on map
        addResultMarker(winner);

        // update result card with animation
        showResult(winners.slice(0, seq + 1));
        resultCard.classList.remove('reveal-anim');
        void resultCard.offsetWidth;
        resultCard.classList.add('reveal-anim');

        // add to history
        history.unshift(winner);
        updateHistory();

        seq++;
        if (seq < winners.length) {{
          setTimeout(animateOne, 1800);
        }} else {{
          // all done — fly map
          if (winners.length === 1) {{
            map.flyTo([winner.lat, winner.lng], 13, {{ duration: 1.5 }});
          }} else {{
            const bounds = L.latLngBounds(winners.map(w => [w.lat, w.lng]));
            map.flyToBounds(bounds.pad(0.3), {{ duration: 1.5 }});
          }}
          isSpinning = false;
          btnDraw.disabled = false;
        }}
      }}
    }}
    requestAnimationFrame(tick);
  }}

  animateOne();
}}

function showResult(winners) {{
  resultCard.classList.add('has-result');
  if (winners.length === 1) {{
    const w = winners[0];
    resultCard.innerHTML =
      '<div class="station-name">' + w.name + '</div>' +
      '<div class="station-meta">' + w.city + ' \u00b7 ' + w.line + '</div>';
  }} else {{
    resultCard.innerHTML = winners.map((w, i) =>
      '<div style="margin-bottom:4px">' +
      '<span class="station-name" style="font-size:1.3rem">[' + (i+1) + '] ' + w.name + '</span>' +
      ' <span class="station-meta" style="font-size:.78rem">' + w.city + '</span></div>'
    ).join('');
  }}
}}

function updateHistory() {{
  const wrap = document.getElementById('historyWrap');
  const list = document.getElementById('historyList');
  wrap.style.display = 'block';
  list.innerHTML = history.slice(0, 20).map(h =>
    '<span class="history-tag">' + h.name + '</span>'
  ).join('');
}}

// init
buildTrack();
</script>
</body>
</html>"""

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已產出: {OUT_PATH}")
    print(f"  全部車站: {len(stations)} 站")
    print(f"  候選車站: {len(candidates)} 站 (排除自強號)")
    print(f"  請用瀏覽器開啟 draw_station.html")


if __name__ == "__main__":
    main()
