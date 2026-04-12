#!/usr/bin/env python3
"""
台鐵車站抽籤程式
自動排除自強號停靠站，從非自強號停靠的車站中隨機抽出一站。
"""

import csv
import random
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "taiwan_railway_stations.csv")


def load_stations(csv_path):
    """讀取 CSV，回傳 (全部站列表, 非自強號站列表)"""
    all_stations = []
    candidates = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_stations.append(row)
            if row["自強號停靠"] == "N":
                candidates.append(row)
    return all_stations, candidates


def draw(candidates, count=1):
    """從候選站中隨機抽出 count 站"""
    count = min(count, len(candidates))
    return random.sample(candidates, count)


def print_result(picks):
    """印出抽籤結果"""
    for i, s in enumerate(picks, 1):
        print(f"  [{i}] {s['車站名稱']}（{s['縣市']}／{s['路線']}）")


def main():
    all_stations, candidates = load_stations(CSV_FILE)

    print("=" * 40)
    print("  台鐵車站抽籤程式")
    print("  （已排除自強號停靠站）")
    print("=" * 40)
    print(f"  全部車站：{len(all_stations)} 站")
    print(f"  排除自強號停靠站後：{len(candidates)} 站")
    print("=" * 40)

    while True:
        ans = input("\n要抽幾站？（輸入數字，或按 q 離開）：").strip()
        if ans.lower() == "q":
            print("掰掰！祝旅途愉快！")
            break
        try:
            count = int(ans)
            if count < 1:
                print("請輸入大於 0 的數字。")
                continue
            if count > len(candidates):
                print(f"最多只能抽 {len(candidates)} 站喔。")
                continue
        except ValueError:
            print("請輸入數字。")
            continue

        picks = draw(candidates, count)
        print(f"\n  抽籤結果：")
        print_result(picks)


if __name__ == "__main__":
    main()
