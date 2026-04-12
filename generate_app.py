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

# ---------------------------------------------------------------------------
# 車站附近美食與景點  { 站名: { "food": [...], "sight": [...] } }
# ---------------------------------------------------------------------------
STATION_INFO = {
    # ===== 縱貫線北段 =====
    "三坑": {
        "food": ["三坑老街米粉湯", "基隆廟口鄰近小吃", "三坑在地排骨飯"],
        "sight": ["三坑老街散步", "基隆河畔自行車道", "獅球嶺隧道"]
    },
    "百福": {
        "food": ["百福社區麵店", "七堵咖哩飯", "七堵鐵路便當"],
        "sight": ["百福公園", "瑪陵坑溪生態", "七堵鐵道紀念公園"]
    },
    "暖暖": {
        "food": ["暖暖老街小吃", "暖暖碳烤三明治", "阿嬌老店切仔麵"],
        "sight": ["暖暖親水公園", "暖東峽谷步道", "西勢水庫"]
    },
    "海科館": {
        "food": ["八斗子海鮮餐廳", "漁港現炸天婦羅", "小卷米粉"],
        "sight": ["國立海洋科技博物館", "潮境公園", "望幽谷步道"]
    },
    "八斗子": {
        "food": ["八斗子漁港海鮮", "飛魚卵香腸", "鬼頭刀魚排"],
        "sight": ["八斗子車站海景月台", "望幽谷", "潮境公園巨型掃把裝置藝術"]
    },
    "五堵": {
        "food": ["汐止老街肉羹", "五堵在地麵攤", "北港鹹粥"],
        "sight": ["星光橋", "新山夢湖步道", "五堵隧道自行車道"]
    },
    "汐科": {
        "food": ["汐科商圈便當街", "韓式料理聚集區", "遠雄百貨美食街"],
        "sight": ["遠雄購物中心", "基隆河自行車道", "白雲公園"]
    },
    "浮洲": {
        "food": ["板橋湳雅夜市", "浮洲圓環豆花", "在地越南河粉"],
        "sight": ["浮洲藝術河濱公園", "板橋435藝文特區", "溪北公園"]
    },
    "南樹林": {
        "food": ["樹林興仁花園夜市", "紅燒鰻魚羹", "樹林肉圓"],
        "sight": ["鹿角溪人工溼地", "山佳百年車站步行可達", "大同山登山步道"]
    },
    "山佳": {
        "food": ["山佳車站旁古早味冰店", "樹林排骨酥麵", "山佳老街碗粿"],
        "sight": ["山佳百年車站（古蹟）", "大棟山觀景台", "鹿角溪人工溼地"]
    },
    "鳳鳴": {
        "food": ["鶯歌老街伴手禮", "厚道飲食店古早味便當", "阿婆壽司"],
        "sight": ["鶯歌陶瓷博物館", "鶯歌老街", "三鶯藝術村"]
    },
    "內壢": {
        "food": ["內壢黃昏市場小吃", "阿霞粉圓冰", "內壢火車站旁滷肉飯"],
        "sight": ["元智大學校園", "忠孝公園", "內壢老街區"]
    },
    "埔心": {
        "food": ["埔心牧場旁餐廳", "客家粄條", "楊梅富岡老街小吃"],
        "sight": ["埔心牧場", "楊梅故事館", "秀才登山步道"]
    },
    "富岡": {
        "food": ["富岡老街客家菜包", "富岡市場油飯", "客家鹹豬肉"],
        "sight": ["富岡老街日式建築群", "伯公岡公園", "富岡運動公園"]
    },
    "新富": {
        "food": ["富岡老街碗粿", "客家粢粑", "在地客家小炒"],
        "sight": ["新富車站田園風光", "湖口老街（鄰近）", "新豐紅毛港"]
    },
    "北湖": {
        "food": ["湖口老街手工麵線", "湖口大鍋牛肉麵", "客家擂茶"],
        "sight": ["湖口老街", "湖口好客文創園區", "金獅寺步道"]
    },
    # ===== 內灣線 =====
    "竹中": {
        "food": ["竹東客家粄條", "中央市場米粉", "客家菜包"],
        "sight": ["竹中車站鐵道風光", "高鐵新竹站（六家線轉乘）", "頭前溪生態"]
    },
    "六家": {
        "food": ["高鐵站區美食街", "竹北光明商圈小吃", "新竹米粉"],
        "sight": ["高鐵新竹站", "六家古厝群", "竹北水圳森林公園"]
    },
    "上員": {
        "food": ["竹東市場客家菜", "上員在地麵店", "客家草仔粿"],
        "sight": ["上員崎頂步道", "頭前溪自行車道", "竹東圳"]
    },
    "榮華": {
        "food": ["竹東中央市場小吃", "客家鹹湯圓", "薑絲大腸"],
        "sight": ["竹東動漫園區", "蕭如松藝術園區", "五指山登山口"]
    },
    "竹東": {
        "food": ["竹東中央市場粄條", "竹東排骨酥麵", "客家菜包阿金姐"],
        "sight": ["竹東文創藝術村", "蕭如松藝術園區", "軟橋彩繪村"]
    },
    "橫山": {
        "food": ["橫山在地客家小吃", "野薑花粽子", "客家擂茶"],
        "sight": ["大山背人文生態館", "騎龍古道", "橫山大山背休閒農業區"]
    },
    "九讚頭": {
        "food": ["內灣野薑花粽", "客家鹹湯圓", "山產野菜"],
        "sight": ["九讚頭文化協會", "內灣老街（鄰近）", "合興愛情車站（鄰近）"]
    },
    "合興": {
        "food": ["合興車站旁愛情飲品店", "內灣老街粄條", "野薑花粽"],
        "sight": ["合興愛情車站", "薰衣草森林（鄰近）", "愛情候車亭裝置藝術"]
    },
    "富貴": {
        "food": ["內灣客家菜", "山豬肉香腸", "客家擂茶"],
        "sight": ["富貴車站山林風光", "內灣吊橋（鄰近）", "油羅溪谷"]
    },
    "內灣": {
        "food": ["內灣老街野薑花粽", "客家粄條", "劉興欽漫畫餐廳"],
        "sight": ["內灣老街", "內灣吊橋", "內灣戲院（懷舊電影院）"]
    },
    "北新竹": {
        "food": ["新竹城隍廟口肉圓", "鴨肉許", "新竹米粉"],
        "sight": ["新竹護城河親水公園", "新竹美術館", "東門城"]
    },
    "千甲": {
        "food": ["千甲部落農產品", "在地原住民風味餐", "新竹客家美食"],
        "sight": ["千甲聚落（里山生活）", "世博台灣館", "關東橋商圈"]
    },
    "新莊": {
        "food": ["新竹關東橋小吃", "清大夜市", "科學園區便當街"],
        "sight": ["新竹科學園區", "交通大學校園", "十八尖山步道"]
    },
    "三姓橋": {
        "food": ["新竹南寮漁港海鮮", "香山甕仔雞", "三姓橋在地小吃"],
        "sight": ["香山濕地賞蟹步道", "南寮漁港", "青青草原溜滑梯"]
    },
    "香山": {
        "food": ["香山甕仔雞", "海鮮快炒", "香山市場在地小吃"],
        "sight": ["香山濕地", "青青草原", "香山天后宮"]
    },
    "崎頂": {
        "food": ["崎頂小吃攤", "竹南在地米粉", "竹南市場花枝羹"],
        "sight": ["崎頂子母隧道", "崎頂觀景台看海", "崎頂海水浴場"]
    },
    # ===== 海岸線 =====
    "談文": {
        "food": ["談文在地小吃", "後龍黑輪伯", "後龍杏仁露"],
        "sight": ["談文車站（木造老站房）", "好望角風景區（鄰近）", "談文溪口"]
    },
    "大山": {
        "food": ["後龍小吃", "客家米食", "在地花生糖"],
        "sight": ["大山車站（日式木造站房）", "後龍好望角", "過港貝化石層"]
    },
    "龍港": {
        "food": ["後龍海鮮", "龍港漁村小吃", "外埔漁港海產"],
        "sight": ["好望角觀景步道", "外埔漁港", "後龍鎮海宮"]
    },
    "新埔": {
        "food": ["通霄海鮮快炒", "白沙屯媽祖廟旁小吃", "手工豆花"],
        "sight": ["新埔車站（木造老站）", "秋茂園", "通霄海水浴場"]
    },
    "豐富": {
        "food": ["苗栗客家湯圓", "苗栗市場肉圓", "苗栗餡餅"],
        "sight": ["客家圓樓", "苗栗高鐵站區", "貓裏客家學苑"]
    },
    "南勢": {
        "food": ["苗栗市場小吃", "客家粄條", "苗栗肉圓"],
        "sight": ["功維敘隧道（七彩燈光）", "南勢溪步道", "貓貍山公園"]
    },
    "泰安": {
        "food": ["泰安舊站附近客家餐廳", "后里豬血湯", "后里馬場旁小吃"],
        "sight": ["泰安舊站鐵道文化園區", "泰安櫻花林（季節限定）", "后豐鐵馬道"]
    },
    "日南": {
        "food": ["大甲芋頭酥", "日南在地麵攤", "大甲奶油酥餅"],
        "sight": ["日南車站（國定古蹟）", "日南海堤夕陽", "大甲鎮瀾宮（鄰近）"]
    },
    "臺中港": {
        "food": ["梧棲漁港海鮮", "梧棲老街鹹蛋糕", "漁港現撈快炒"],
        "sight": ["梧棲漁港觀光魚市", "高美濕地（鄰近）", "三井OUTLET"]
    },
    "龍井": {
        "food": ["東海雞爪凍", "東海藝術街小吃", "龍井在地肉圓"],
        "sight": ["麗水漁港", "龍井大排壁畫", "磺溪書院"]
    },
    "栗林": {
        "food": ["豐原廟東夜市小吃", "豐原太平洋鹹酥雞", "排骨麵"],
        "sight": ["栗林車站新站體", "葫蘆墩公園", "豐原慈濟宮"]
    },
    "頭家厝": {
        "food": ["潭子臭豆腐", "潭子在地麵攤", "豐原廟東小吃"],
        "sight": ["潭雅神綠園道自行車道", "摘星山莊古厝", "潭子運動公園"]
    },
    "松竹": {
        "food": ["北屯大坑芋圓", "松竹路越南美食", "舊社公園旁小吃"],
        "sight": ["大坑步道群", "北屯兒童公園", "松竹捷運站（台鐵捷運共構）"]
    },
    "太原": {
        "food": ["太原夜市小吃", "旱溪臭豆腐", "大坑竹筍大餐"],
        "sight": ["旱溪夜市（鄰近）", "太原綠園道", "大坑步道"]
    },
    "精武": {
        "food": ["台中肉圓（精武路）", "台中第二市場老賴紅茶", "麻葉茶館"],
        "sight": ["台中公園", "一中商圈", "台中放送局"]
    },
    "五權": {
        "food": ["台中第五市場蚵仔粥", "樂群街蒸餃", "美村路小吃"],
        "sight": ["國立台灣美術館", "草悟道", "審計新村文創園區"]
    },
    "大慶": {
        "food": ["大慶夜市小吃", "忠孝路夜市", "南區米糕"],
        "sight": ["中興大學校園", "健康公園", "台中文化創意產業園區"]
    },
    "烏日": {
        "food": ["烏日啤酒廠香腸", "知高圳步道旁在地小吃", "烏日市場肉羹"],
        "sight": ["台灣啤酒觀光工廠", "知高圳步道", "烏日聚奎居（歷史建築）"]
    },
    # ===== 縱貫線南段 =====
    "花壇": {
        "food": ["花壇肉羹", "花壇在地爌肉飯", "茉莉花茶"],
        "sight": ["花壇八卦山大佛（鄰近）", "花壇虎山巖", "茉莉花壇夢想館"]
    },
    "大村": {
        "food": ["大村葡萄（季節限定）", "大村當歸鴨", "進昌咖啡烘焙館"],
        "sight": ["大村葡萄隧道", "進昌咖啡烘焙館（巴洛克建築）", "平和社區賞花"]
    },
    "永靖": {
        "food": ["永靖市場米糕", "員林蜜餞", "永靖在地炸粿"],
        "sight": ["成美文化園", "余三館古厝", "永靖公學校宿舍"]
    },
    "源泉": {
        "food": ["二水在地爌肉飯", "龍眼乾", "田中在地小吃"],
        "sight": ["源泉車站（小站風情）", "八堡圳取水口", "二水自行車道"]
    },
    "濁水": {
        "food": ["集集山蕉蛋捲", "濁水在地小吃", "集集火車站便當"],
        "sight": ["濁水車站", "集集綠色隧道", "武昌宮地震紀念館"]
    },
    "龍泉": {
        "food": ["集集山蕉甜點", "集集老街小吃", "在地竹筍料理"],
        "sight": ["龍泉車站旁綠色隧道", "集集攔河堰", "明新書院"]
    },
    "集集": {
        "food": ["集集火車站前香蕉蛋捲", "集集老街臭豆腐", "山蕉冰淇淋"],
        "sight": ["集集車站（木造站房）", "集集綠色隧道", "特有生物中心"]
    },
    "水里": {
        "food": ["水里肉圓", "水里二坪枝仔冰", "水里蛇窯旁餐廳"],
        "sight": ["水里蛇窯", "二坪枝仔冰", "水里溪步道"]
    },
    "車埕": {
        "food": ["車埕老街木桶便當", "梅子酒", "車埕在地野菜料理"],
        "sight": ["車埕木業展示館", "車埕老街", "明潭水庫壩頂"]
    },
    "石榴": {
        "food": ["斗六西市場肉圓", "斗六炊仔飯", "石榴在地麵攤"],
        "sight": ["石榴車站（百年老站）", "斗六人文公園", "雲中街生活聚落"]
    },
    "石龜": {
        "food": ["斗南米糕", "斗南炸粿", "在地鵝肉"],
        "sight": ["石龜溪生態", "他里霧文化園區（斗南）", "石龜車站風光"]
    },
    "水上": {
        "food": ["嘉義雞肉飯", "嘉義涼麵涼圓", "水上在地豆花"],
        "sight": ["北回歸線太陽館", "白人牙膏觀光工廠", "南靖糖廠"]
    },
    "南靖": {
        "food": ["南靖糖廠冰品", "嘉義火雞肉飯", "南靖車站旁小吃"],
        "sight": ["南靖糖廠", "南靖車站日式站房", "嘉義蒜頭糖廠（鄰近）"]
    },
    "嘉北": {
        "food": ["嘉義文化路夜市", "嘉義噴水雞肉飯", "御香屋葡萄柚綠茶"],
        "sight": ["嘉義文化路商圈", "森林之歌裝置藝術", "嘉義公園"]
    },
    "後壁": {
        "food": ["後壁古早味割稻飯", "後壁冰糖醬鴨", "無米樂社區農家餐"],
        "sight": ["無米樂社區（菁寮老街）", "後壁土溝農村美術館", "墨林文物館"]
    },
    "柳營": {
        "food": ["柳營牛奶鍋", "柳營鮮奶酪", "在地牛肉湯"],
        "sight": ["柳營酪農區", "德元埤荷蘭村", "劉啟祥美術紀念館"]
    },
    "林鳳營": {
        "food": ["林鳳營鮮乳製品", "麻豆碗粿", "在地古早味冰品"],
        "sight": ["林鳳營車站（日式老站房）", "六甲落羽松森林", "烏山頭水庫（鄰近）"]
    },
    "隆田": {
        "food": ["隆田酒廠在地小吃", "善化牛肉湯", "麻豆碗粿"],
        "sight": ["隆田CHA CHA文化資產教育園區", "烏山頭水庫", "官田水雉生態園區"]
    },
    "拔林": {
        "food": ["善化在地小吃", "善化牛肉湯", "在地碗粿"],
        "sight": ["拔林車站（迷你秘境站）", "善化糖廠", "大內南瀛天文館"]
    },
    "南科": {
        "food": ["南科園區商圈美食", "善化牛肉湯", "新市在地小吃"],
        "sight": ["南科考古館", "南科迎曦湖", "樹谷生活科學館"]
    },
    "新市": {
        "food": ["新市肉粿", "在地虱目魚粥", "新市豆菜麵"],
        "sight": ["新市社內遺址", "大新營區自行車道", "南科園區公園"]
    },
    "大橋": {
        "food": ["永康大橋鱔魚意麵", "永康復國市場小吃", "台南鹽酥雞"],
        "sight": ["永康公園", "永康探索教育公園", "台南大橋都會風光"]
    },
    "仁德": {
        "food": ["仁德阿裕牛肉湯", "仁德在地蝦捲", "仁德萬國通路手作觀光工廠餐廳"],
        "sight": ["十鼓仁糖文創園區", "奇美博物館", "台南都會公園"]
    },
    "中洲": {
        "food": ["保安車站周邊古早味", "仁德在地小吃", "車路墘肉粿"],
        "sight": ["保安車站（永保安康）", "虎山林場步道", "歸仁老街"]
    },
    "長榮大學": {
        "food": ["歸仁在地肉燥飯", "大學城周邊小吃", "歸仁豆花"],
        "sight": ["長榮大學校園", "歸仁公園", "歸仁仁壽宮"]
    },
    "沙崙": {
        "food": ["高鐵站美食街", "歸仁在地美食", "台南鮮魚湯"],
        "sight": ["高鐵台南站", "台南沙崙綠能科學城", "歸仁十三甲武當山"]
    },
    # ===== 高雄 =====
    "大湖": {
        "food": ["路竹鵝肉", "岡山羊肉爐", "在地小吃攤"],
        "sight": ["大湖車站田園風光", "路竹農場", "岡山之眼（鄰近）"]
    },
    "路竹": {
        "food": ["路竹夜市小吃", "路竹鵝肉", "在地虱目魚料理"],
        "sight": ["路竹體育園區", "蔡文國小日式校舍", "高雄科學園區"]
    },
    "左營(舊城)": {
        "food": ["左營眷村美食", "劉家酸菜白肉鍋", "左營大路汾陽餛飩"],
        "sight": ["鳳山縣舊城", "左營蓮池潭", "見城館"]
    },
    "內惟": {
        "food": ["內惟市場小吃", "美術館周邊咖啡廳", "內惟在地碗粿"],
        "sight": ["內惟藝術中心", "高雄美術館", "柴山自然公園"]
    },
    "美術館": {
        "food": ["美術館周邊文青咖啡", "明誠路餐廳街", "馬家麵線"],
        "sight": ["高雄市立美術館", "美術館雕塑公園", "柴山步道入口"]
    },
    "鼓山": {
        "food": ["哈瑪星古早味", "鼓山渡船頭海之冰", "西子灣海產"],
        "sight": ["哈瑪星鐵道文化園區", "武德殿", "西子灣隧道"]
    },
    "三塊厝": {
        "food": ["三塊厝老街小吃", "鹽埕區古早味", "大溝頂市場"],
        "sight": ["三塊厝車站（百年站房）", "愛河之心", "高雄願景館"]
    },
    "民族": {
        "food": ["自強夜市小吃", "民族路烤肉", "高雄肉燥飯"],
        "sight": ["高雄科工館（鄰近）", "三民公園", "建功路眷村文化"]
    },
    "科工館": {
        "food": ["九如路美食", "科工館旁便當街", "三民市場小吃"],
        "sight": ["國立科學工藝博物館", "三民家商旁公園", "本和里滯洪公園"]
    },
    "正義": {
        "food": ["鳳山中華夜市", "正義路小吃", "鳳山肉圓"],
        "sight": ["衛武營國家藝術文化中心", "鳳山城隍廟", "大東文化藝術中心"]
    },
    # ===== 屏東線 =====
    "六塊厝": {
        "food": ["屏東夜市小吃", "萬丹紅豆餅", "在地粿仔條"],
        "sight": ["六塊厝車站田園風光", "屏東公園", "萬丹鄉間風情"]
    },
    "歸來": {
        "food": ["屏東肉圓", "在地鮮魚湯", "歸來社區小吃"],
        "sight": ["歸來車站（小站風情）", "屏東菸葉廠", "麟洛車站鐵馬道"]
    },
    "麟洛": {
        "food": ["麟洛客家粄條", "客家鹹豬肉", "屏東夜市"],
        "sight": ["麟洛運動公園", "六堆客家文化園區（鄰近）", "屏東自行車國道"]
    },
    "西勢": {
        "food": ["六堆客家菜", "西勢粄條", "客家封肉"],
        "sight": ["六堆客家文化園區", "西勢車站（客庄風情）", "竹田驛園"]
    },
    "竹田": {
        "food": ["竹田驛園旁客家菜", "客家擂茶", "竹田在地碗粿"],
        "sight": ["竹田驛園（日式站房）", "竹田老街", "達達港水利公園"]
    },
    "崁頂": {
        "food": ["崁頂在地肉燥飯", "東港黑鮪魚（鄰近）", "萬丹紅豆湯"],
        "sight": ["崁頂田園風光", "力社北院媽祖廟", "東港大鵬灣（鄰近）"]
    },
    "鎮安": {
        "food": ["林邊黑珍珠蓮霧", "東港海鮮", "在地虱目魚料理"],
        "sight": ["鎮安車站（小站秘境）", "林邊溪堤防步道", "光采濕地"]
    },
    "佳冬": {
        "food": ["佳冬蓮霧", "海鮮快炒", "客家粄條"],
        "sight": ["佳冬蕭家古厝", "佳冬客家聚落", "楊氏宗祠"]
    },
    "東海": {
        "food": ["枋寮海產", "東海在地小吃", "芒果冰（季節限定）"],
        "sight": ["東海車站海景", "枋寮藝術村（鄰近）", "東海漁港"]
    },
    # ===== 南迴線 =====
    "內獅": {
        "food": ["枋山芒果（季節限定）", "枋寮海鮮", "原住民風味餐"],
        "sight": ["內獅車站（最少人的車站之一）", "獅子鄉原鄉風情", "雙流國家森林遊樂區"]
    },
    "枋山": {
        "food": ["枋山芒果", "愛文芒果冰", "在地海鮮"],
        "sight": ["枋山車站海景", "枋山超級56K觀海涼亭", "枋山沿海公路風光"]
    },
    "瀧溪": {
        "food": ["原住民野菜料理", "小米酒", "山產風味餐"],
        "sight": ["瀧溪車站秘境", "大武山自然保留區（遠眺）", "太平洋海岸線"]
    },
    "山里": {
        "food": ["台東米苔目", "山里在地部落美食", "小米粽"],
        "sight": ["山里車站（到不了的車站）", "山里教堂", "初鹿牧場（鄰近）"]
    },
    # ===== 臺東線 =====
    "瑞源": {
        "food": ["鹿野紅烏龍茶", "在地釋迦冰品", "原住民風味餐"],
        "sight": ["瑞源小學日式校長宿舍", "鹿野鄉田園風光", "二層坪水橋"]
    },
    "瑞和": {
        "food": ["關山便當", "關山米做成的米乖乖", "在地茶飲"],
        "sight": ["瑞和車站（稻田小站）", "關山親水公園（鄰近）", "197縣道田園單車道"]
    },
    "海端": {
        "food": ["布農族風味餐", "小米飯", "山豬肉串"],
        "sight": ["海端鄉布農族文化館", "霧鹿峽谷（上游）", "南橫公路入口"]
    },
    "東竹": {
        "food": ["富里農會便當", "花東縱谷米食", "在地野菜料理"],
        "sight": ["東竹車站田園秘境", "富里稻田景觀", "羅山瀑布（鄰近）"]
    },
    "東里": {
        "food": ["玉里麵", "玉里臭豆腐（鄰近）", "在地米食料理"],
        "sight": ["東里車站（稻田中的車站）", "玉富自行車道", "六十石山（季節金針花）"]
    },
    "三民": {
        "food": ["玉里麵", "玉里橋頭臭豆腐", "瑞穗鮮乳製品"],
        "sight": ["三民車站鐵道風光", "赤科山（季節金針花）", "玉里神社遺址"]
    },
    "富源": {
        "food": ["瑞穗鮮奶饅頭", "富源在地小吃", "蝴蝶谷附近餐廳"],
        "sight": ["富源國家森林遊樂區（蝴蝶谷）", "拉索埃湧泉", "富源車站"]
    },
    "大富": {
        "food": ["光復糖廠冰淇淋", "阿美族野菜", "在地豐年餐"],
        "sight": ["大富平地森林園區", "大農大富花海（季節限定）", "光復糖廠"]
    },
    "萬榮": {
        "food": ["光復糖廠冰品", "太巴塱部落風味餐", "紅糯米飯"],
        "sight": ["萬榮林田山林業文化園區", "馬太鞍溼地", "太巴塱部落"]
    },
    "南平": {
        "food": ["鳳林剝皮辣椒", "鳳林韭菜臭豆腐", "客家菜包"],
        "sight": ["南平車站田園風光", "鳳林客家文物館", "箭瑛大橋"]
    },
    "豐田": {
        "food": ["豐田在地日式料理", "壽豐豆花", "在地有機蔬食"],
        "sight": ["豐田移民村（日式遺跡）", "豐田玉展示館", "碧蓮寺"]
    },
    "平和": {
        "food": ["壽豐在地小吃", "志學周邊學生美食", "壽豐豆花"],
        "sight": ["平和車站秘境", "鯉魚潭（鄰近）", "東華大學校園"]
    },
    # ===== 北迴線 =====
    "景美": {
        "food": ["新城老街小吃", "佳興冰果室檸檬汁", "原住民風味餐"],
        "sight": ["景美車站鐵道風光", "新城照相館", "三棧溪戲水（季節限定）"]
    },
    "崇德": {
        "food": ["崇德在地小吃", "太魯閣附近原住民料理", "花蓮扁食"],
        "sight": ["崇德海灘（最美海灘之一）", "清水斷崖眺望點", "太魯閣國家公園入口"]
    },
    "和仁": {
        "food": ["太魯閣周邊餐廳", "原住民獵人便當", "在地山產"],
        "sight": ["和仁海灘", "清水斷崖北端", "蘇花公路絕美海景"]
    },
    "漢本": {
        "food": ["漢本車站旁雜貨店", "南澳在地原住民小吃", "蘇花沿線便當"],
        "sight": ["漢本車站（絕壁小站）", "漢本海灘", "蘇花公路最美路段"]
    },
    "武塔": {
        "food": ["南澳建華冰店", "泰雅族風味餐", "南澳在地小吃"],
        "sight": ["武塔部落泰雅文化", "南澳古道入口", "武塔車站鐵道風光"]
    },
    "東澳": {
        "food": ["東澳粉鳥林漁港海鮮", "東岳湧泉旁小吃", "在地飛魚料理"],
        "sight": ["東澳灣", "粉鳥林漁港秘境", "東岳湧泉（夏季戲水）"]
    },
    "永樂": {
        "food": ["蘇澳冷泉附近小吃", "蘇澳海鮮", "白米木屐村旁餐廳"],
        "sight": ["永樂車站海灣風光", "白米木屐村", "蘇澳冷泉（鄰近）"]
    },
    # ===== 宜蘭線 =====
    "新馬": {
        "food": ["蘇澳海鮮", "蘇澳冷泉汽水", "南方澳魚丸"],
        "sight": ["新馬車站", "冬山河下游", "蘇澳冷泉公園"]
    },
    "中里": {
        "food": ["羅東夜市小吃", "羅東肉羹番", "包心粉圓"],
        "sight": ["中里車站（迷你小站）", "羅東運動公園", "冬山河自行車道"]
    },
    "二結": {
        "food": ["二結在地小吃", "宜蘭蔥油餅", "鴨賞"],
        "sight": ["二結穀倉稻農文化館", "宜蘭傳統藝術中心（鄰近）", "冬山河"]
    },
    "四城": {
        "food": ["礁溪蔥油餅", "礁溪溫泉拉麵", "甕仔雞"],
        "sight": ["四城車站田園風光", "礁溪溫泉（鄰近）", "吳沙紀念館"]
    },
    "頂埔": {
        "food": ["礁溪溫泉蔬菜", "礁溪蔥油餅", "柯氏蔥油餅"],
        "sight": ["頂埔車站鄉村風光", "礁溪五峰旗瀑布（鄰近）", "林美石磐步道"]
    },
    "外澳": {
        "food": ["頭城老街小吃", "阿宗芋冰城", "外澳衝浪區餐廳"],
        "sight": ["外澳海灘（衝浪勝地）", "外澳服務區觀景", "龜山島眺望點"]
    },
    "龜山": {
        "food": ["龜山島海鮮", "在地魚丸", "頭城老街小吃"],
        "sight": ["龜山車站（最靠近龜山島）", "龜山島眺望", "北關海潮公園"]
    },
    "大溪": {
        "food": ["大溪漁港海鮮", "大溪蜜餞", "現撈仔漁獲"],
        "sight": ["大溪漁港", "大溪車站海景", "蜜月灣（衝浪）"]
    },
    "大里": {
        "food": ["大里天公廟旁小吃", "石花凍", "頭城海鮮"],
        "sight": ["大里天公廟", "草嶺古道入口", "大里海岸步道"]
    },
    "石城": {
        "food": ["石城在地小吃攤", "石花凍", "草嶺古道出口旁小店"],
        "sight": ["石城車站（宜蘭最北站）", "草嶺古道北端", "石城海岸礁石步道"]
    },
    "四腳亭": {
        "food": ["四腳亭在地小吃", "瑞芳美食街", "礦工便當"],
        "sight": ["四腳亭砲台古蹟", "瑞芳老街（鄰近）", "四腳亭步道"]
    },
    "猴硐": {
        "food": ["猴硐貓村咖啡廳", "礦工便當", "古早味麵食"],
        "sight": ["猴硐貓村", "猴硐煤礦博物園區", "三貂嶺瀑布步道入口"]
    },
    "三貂嶺": {
        "food": ["三貂嶺咖啡（藝文空間）", "猴硐美食（鄰近）", "在地古早味"],
        "sight": ["三貂嶺瀑布步道", "三貂嶺生態友善隧道", "碩仁國小遺址"]
    },
    "牡丹": {
        "food": ["牡丹老街小吃", "牡丹車站旁麵攤", "在地山產料理"],
        "sight": ["牡丹老街", "牡丹車站日式站房", "貂山古道入口"]
    },
    # ===== 平溪線 =====
    "大華": {
        "food": ["十分老街小吃", "花生捲冰淇淋", "礦工便當"],
        "sight": ["大華壺穴", "大華車站（秘境小站）", "十分瀑布步道"]
    },
    "十分": {
        "food": ["十分老街花生捲冰淇淋", "十分雞翅包飯", "礦工便當"],
        "sight": ["十分瀑布", "十分老街放天燈", "十分車站鐵道風光"]
    },
    "望古": {
        "food": ["平溪老街小吃", "山泉豆花", "在地野菜"],
        "sight": ["望古瀑布（秘境）", "望古車站（最冷門站）", "望古賞螢步道"]
    },
    "嶺腳": {
        "food": ["嶺腳古早味麵店", "平溪老街小吃", "山產料理"],
        "sight": ["嶺腳瀑布", "嶺腳車站", "嶺腳寮山步道"]
    },
    "平溪": {
        "food": ["平溪老街香腸", "芋圓", "古早味冰品"],
        "sight": ["平溪老街放天燈", "平溪防空洞", "孝子山步道"]
    },
    "菁桐": {
        "food": ["菁桐老街雞捲", "菁桐礦工食堂", "紅寶礦場咖啡"],
        "sight": ["菁桐車站（日式站房）", "菁桐老街許願竹筒", "菁桐礦業生活館"]
    },
    # ===== 深澳線 =====
    # 海科館 & 八斗子 已在上方
    # ===== 花蓮臨港線 =====
    "花蓮港": {
        "food": ["花蓮扁食", "液香扁食", "花蓮公正包子"],
        "sight": ["花蓮港觀景台", "太平洋公園", "花蓮市區自強夜市"]
    },
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
    info_json = json.dumps(STATION_INFO, ensure_ascii=False)

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
  justify-content:center;padding:10px 24px;gap:12px;overflow-y:auto;min-height:0}}
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

/* info panel (food & sight) */
.info-panel{{width:100%;display:none;gap:10px;max-height:260px;overflow-y:auto;
  padding:2px 0;scrollbar-width:thin;scrollbar-color:#334155 transparent}}
.info-panel.visible{{display:flex;flex-direction:column}}
.info-section{{padding:0}}
.info-section-title{{font-size:.78rem;font-weight:700;margin-bottom:6px;
  display:flex;align-items:center;gap:6px;padding-left:2px;
  text-transform:uppercase;letter-spacing:1px}}
.info-section-title.food-title{{color:#fbbf24}}
.info-section-title.sight-title{{color:#34d399}}
.info-cards{{display:flex;flex-direction:column;gap:6px}}

/* individual card */
.info-card{{display:flex;align-items:center;gap:12px;
  padding:10px 14px;border-radius:12px;
  transition:all .25s ease;opacity:0;transform:translateY(8px);
  animation:cardFadeIn .4s ease forwards}}
.info-card:hover{{transform:translateY(-1px) scale(1.01)}}
.info-card .card-emoji{{font-size:1.5rem;flex-shrink:0;
  width:38px;height:38px;display:flex;align-items:center;justify-content:center;
  border-radius:10px;background:rgba(255,255,255,.06)}}
.info-card .card-text{{font-size:.82rem;color:#e2e8f0;font-weight:500;
  line-height:1.3}}

/* food card warm tones */
.info-card.food-card{{
  background:linear-gradient(135deg,rgba(251,191,36,.08),rgba(251,146,60,.04));
  border:1px solid rgba(251,191,36,.2)}}
.info-card.food-card:hover{{
  border-color:rgba(251,191,36,.4);
  box-shadow:0 0 16px rgba(251,191,36,.1)}}

/* sight card cool tones */
.info-card.sight-card{{
  background:linear-gradient(135deg,rgba(52,211,153,.08),rgba(56,189,248,.04));
  border:1px solid rgba(52,211,153,.2)}}
.info-card.sight-card:hover{{
  border-color:rgba(52,211,153,.4);
  box-shadow:0 0 16px rgba(52,211,153,.1)}}

/* stagger animation */
@keyframes cardFadeIn{{
  to{{opacity:1;transform:translateY(0)}}
}}

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
  body{{overflow:auto;height:auto}}
  #app{{flex-direction:column;height:auto;min-height:100vh}}
  #panel{{width:100%;min-width:0;height:auto;max-height:none;
    border-right:none;border-bottom:1px solid #334155}}
  #map-wrap{{height:40vh;min-height:280px;position:sticky;bottom:0}}

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

  .info-panel{{max-height:none;padding:0}}
  .info-card{{padding:8px 12px;gap:10px}}
  .info-card .card-emoji{{font-size:1.3rem;width:32px;height:32px;border-radius:8px}}
  .info-card .card-text{{font-size:.78rem}}
  .info-section-title{{font-size:.72rem}}

  .controls{{padding:10px 16px 16px;gap:8px}}
  .btn-draw{{padding:14px;font-size:1rem;letter-spacing:1px}}
  .count-row label{{font-size:.8rem}}
  .count-row select{{padding:5px 10px;font-size:.85rem}}

  .history{{padding:0 16px 12px;max-height:70px}}
  .history-tag{{font-size:.7rem;padding:2px 8px}}

  .countdown-num{{font-size:5rem}}
  .countdown-num.go{{font-size:3.5rem}}
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

      <div class="info-panel" id="infoPanel">
        <div class="info-section" id="infoFood"></div>
        <div class="info-section" id="infoSight"></div>
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
const stationInfo = {info_json};

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
const isMobile = window.matchMedia('(max-width:800px)').matches;
const ITEM_H = isMobile ? 35 : 50;

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
  const initOffset = isMobile ? 52 : 75;
  slotTrack.style.transform = 'translateY(' + initOffset + 'px)';
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
  document.getElementById('infoPanel').classList.remove('visible');

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

    const baseOffset = isMobile ? 52 : 75;
    const targetY = baseOffset - landIndex * ITEM_H;
    const duration = isMobile ? (2800 + Math.random() * 400) : (3500 + Math.random() * 500);
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

        // big reveal!
        playFanfare();
        triggerScreenFlash();
        spawnConfetti();
        spawnFullScreenConfetti();

        // show on map
        addResultMarker(winner);

        // update result card with animation
        showResult(winners.slice(0, seq + 1));
        showStationInfo(winners.slice(0, seq + 1));
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
          // mobile: scroll to map
          if (isMobile) {{
            setTimeout(() => {{
              document.getElementById('map-wrap').scrollIntoView({{ behavior: 'smooth' }});
            }}, 400);
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

// keyword -> emoji mapping
const foodEmojiRules = [
  [/麵|粄條|米粉|麵線/, '🍜'],
  [/飯|便當|米糕|粥|燴飯|油飯/, '🍚'],
  [/冰|冰品|冰淇淋|冰棒|枝仔冰|雪花/, '🍧'],
  [/海鮮|魚|蝦|蟹|蚵|小卷|鮪|虱目|鰻|花枝/, '🦐'],
  [/雞|鵝|鴨|雞肉|鵝肉/, '🍗'],
  [/茶|咖啡|擂茶|紅茶|綠茶|檸檬/, '☕'],
  [/肉|排骨|牛肉|豬|羊肉|香腸|臭豆腐|鹹豬/, '🥩'],
  [/酒|啤酒/, '🍺'],
  [/豆花|甜點|糕|粿|蛋糕|芋圓|圓|餅|酥|蜜餞|蓮霧|芒果|葡萄|釋迦|梅/, '🍰'],
  [/湯|羹|鍋/, '🍲'],
  [/包|捲|粽|餃/, '🥟'],
];
const sightEmojiRules = [
  [/步道|山|登山|古道|嶺/, '⛰️'],
  [/海|漁港|海灘|海岸|灣|衝浪|潮境/, '🏖️'],
  [/老街|車站|古蹟|古厝|日式|眷村|隧道/, '🏮'],
  [/公園|園區|森林|濕地|牧場|農/, '🌿'],
  [/瀑布|溪|湖|泉|水庫|圳|河/, '💧'],
  [/博物館|美術館|文化|藝術|紀念|展示/, '🎨'],
  [/夜市|市場|商圈/, '🏮'],
  [/寺|廟|宮|教堂/, '⛩️'],
  [/自行車|鐵馬|單車/, '🚲'],
  [/觀景|眺望|夕陽|日出/, '🌅'],
];
const defaultFoodEmoji = '🍴';
const defaultSightEmoji = '📍';

function getEmoji(text, rules, fallback) {{
  for (const [re, emoji] of rules) {{
    if (re.test(text)) return emoji;
  }}
  return fallback;
}}

function renderCards(items, type, rules, fallback) {{
  return items.map((text, i) => {{
    const emoji = getEmoji(text, rules, fallback);
    const delay = (i * 0.08).toFixed(2);
    return '<div class="info-card ' + type + '-card" style="animation-delay:' + delay + 's">' +
      '<span class="card-emoji">' + emoji + '</span>' +
      '<span class="card-text">' + text + '</span></div>';
  }}).join('');
}}

function showStationInfo(winners) {{
  const panel = document.getElementById('infoPanel');
  const foodEl = document.getElementById('infoFood');
  const sightEl = document.getElementById('infoSight');

  let allFood = [];
  let allSight = [];
  winners.forEach(w => {{
    const info = stationInfo[w.name];
    if (info) {{
      const prefix = winners.length > 1 ? ('[' + w.name + '] ') : '';
      if (info.food) info.food.forEach(f => allFood.push(prefix + f));
      if (info.sight) info.sight.forEach(s => allSight.push(prefix + s));
    }}
  }});

  if (allFood.length === 0 && allSight.length === 0) {{
    panel.classList.remove('visible');
    return;
  }}

  foodEl.className = 'info-section';
  foodEl.innerHTML =
    '<div class="info-section-title food-title">&#127836; \u7279\u8272\u7f8e\u98df</div>' +
    '<div class="info-cards">' + renderCards(allFood, 'food', foodEmojiRules, defaultFoodEmoji) + '</div>';

  sightEl.className = 'info-section';
  sightEl.innerHTML =
    '<div class="info-section-title sight-title">&#128205; \u89c0\u5149\u666f\u9ede</div>' +
    '<div class="info-cards">' + renderCards(allSight, 'sight', sightEmojiRules, defaultSightEmoji) + '</div>';

  panel.classList.add('visible');
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
