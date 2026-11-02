# -*- coding: utf-8 -*-
"""Bo test Hiep Ky Dai Su web. Chay: python test_trachcat.py"""
import datetime

from lunar_python import Solar

import hanviet as H
import trach_cat_core as T

R = []


def chk(name, cond):
    R.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


# 1. Tu dien
src = "丁七三上不丑专世丙东丧临乘乙九习了事五井亡亢交亥产亲人仓仪任伐会位作佣修俱元光兔入八六养冠冲出击分刑券刻割动劫勾勿北匮医匾午单南卯危卸厌厕参友发取口司合吉名后吏吠启命咸哭喜嗣器囊四土圣地坎坏坟垣基堂堤塑塞墓墙壁壬复大天奎女娄娶婿嫁子孤学宁宅宇守安官定宜宝室害寅富对寿将小尾居屋岁岫巫己巳市帐平床庙庚府废建开张归往徙德心忌恩愿戊戌成戾房手执扫护拆招挂捉捕掘探摇支收放教敬整斋斗断无日时明易星昴普月服期木未朱机架柩柱柳栽桥梁械武死殓母毕氐民气水求池沐河治浴涂渔渠渡游满火灶灸灾焦煞牛牢牧狗狠猎猪猴玄玉王理生甲申畋畜病癸白益盖盟相眼破碑碓磉磑祀祈神祭祸福离种移稠穴穷空立竖笄符筑箕纯纳经结绘络绝续网罡置羊翼耗胃脊致舍船艺葬薄虎虚蚁蛇蜜血行衣补裁西要角觜解触订讼词诸谢财败货贼赦赴起足车轸辛辰进退逐造道酉酬醮采重金针钻错门闭问阳阴阵陈除雀雇雕青风饰馀香马驿鬼魁鸟鸡鸣鼠龙"
chk("bang am Han Viet khop 1-1 (khong lech)", len(H.CHAR) == len(src))
chk("Han Viet: 天德合 = Thien Duc Hop", H.hv("天德合") == "Thiên Đức Hợp")
chk("Han Viet: 驿马 = Dich Ma (cuoi bang, khong lech)", H.hv("驿马") == "Dịch Mã")
chk("Han Viet: 甲子 = Giap Ty", H.ganzhi_vi("甲子") == "Giáp Tý")

# 2. Tu tru
b = T.bat_tu(1996, 8, 13, 12)
chk("ca kiem chung skill: 13/08/1996 Ngo = Binh Ty - Binh Than - Nham Ngo - Binh Ngo",
    [b["vi"][k] for k in ("nam", "thang", "ngay", "gio")] == ["Bính Tý", "Bính Thân", "Nhâm Ngọ", "Bính Ngọ"])
# Lap Xuan 2025: 03/02 22:10 gio Bac Kinh = 21:10 gio Viet Nam
b1 = T.bat_tu(2025, 2, 3, 21, 30)
b0 = T.bat_tu(2025, 2, 3, 20, 50)
chk("gio VN: sinh 21:30 ngay 3/2/2025 da qua Lap Xuan -> nam At Ty", b1["vi"]["nam"] == "Ất Tỵ")
chk("gio VN: sinh 20:50 cung ngay chua qua Lap Xuan -> nam Giap Thin", b0["vi"]["nam"] == "Giáp Thìn")
chk("khuyet gio -> tru gio de trong", T.bat_tu(1990, 5, 5)["vi"]["gio"] == "Khuyết giờ")
a = T.bat_tu(2026, 11, 2, 23, 30, ty_muon_sang_ngay_moi=False)
c = T.bat_tu(2026, 11, 2, 23, 30, ty_muon_sang_ngay_moi=True)
chk("gio Ty muon: tuy chon doi tru ngay", a["vi"]["ngay"] != c["vi"]["ngay"])

# 3. Quan he can chi
chk("luc xung Ty-Ngo", T.luc_xung("子", "午") and not T.luc_xung("子", "丑"))
chk("luc hop Ty-Suu, Dan-Hoi", T.luc_hop("子", "丑") and T.luc_hop("寅", "亥") and not T.luc_hop("子", "寅"))
chk("tam hop Than-Ty-Thin", T.tam_hop("申", "子") and T.tam_hop("子", "辰") and not T.tam_hop("子", "子"))
chk("can hop Giap-Ky", T.can_hop("甲", "己") and not T.can_hop("甲", "乙"))
chk("That Sat: Canh -> Giap, Giap -> Mau; Tan -> Giap khong (khac am duong)",
    T.that_sat("庚", "甲") and T.that_sat("甲", "戊") and not T.that_sat("辛", "甲"))

# 4. Quet ngay
u = T.bat_tu(1987, 6, 15, 8)
days = T.quet(datetime.date(2026, 11, 1), datetime.date(2026, 12, 31), u, "Khai trương, mở cửa hàng")
chk("quet du 61 ngay", len(days) == 61)
yz = u["han"]["nam"][1]
xung = [d for d in days if T.luc_xung(Solar.fromYmd(d["date"].year, d["date"].month, d["date"].day).getLunar().getDayInGanZhi()[1], yz)]
chk("moi ngay xung tuoi deu bi xep 'Khong nen'", xung and all(d["bac"] == T.TIER_BAD for d in xung))
kieng = [d for d in days if any("Khai Thị" in k for k in d["kieng"])]
chk("ngay lich kieng khai truong deu 'Khong nen'", all(d["bac"] == T.TIER_BAD for d in kieng))
rat = [d for d in days if d["bac"] == "Rất hợp"]
chk("ngay 'Rat hop' deu khong co ly do loai", all(not d["loai"] for d in rat))
ok_task = [d for d in days if d["bac"] in ("Rất hợp", "Hợp")]
chk("ngay 'Hop' tro len deu duoc lich ghi nen viec da chon", ok_task and all(any("Lịch ghi nên" in t for t in d["tot"]) for d in ok_task))
tot, xau = T.xep_hang(days)
RANK = {"Rất hợp": 0, "Hợp": 1, "Bình thường": 2}
chk("xep hang: theo bac truoc, diem sau", [(RANK[d["bac"]], -d["diem"]) for d in tot] == sorted((RANK[d["bac"]], -d["diem"]) for d in tot))
chk("khong co ngay nao dong thoi o ca 2 danh sach", not set(d["date"] for d in tot) & set(d["date"] for d in xau))
try:
    T.quet(datetime.date(2026, 1, 1), datetime.date(2026, 6, 1), u, "Cưới hỏi")
    chk("chan quet qua 90 ngay", False)
except ValueError:
    chk("chan quet qua 90 ngay", True)
chk("khong co viec kham chua benh trong danh sach viec", not any("bệnh" in k for k in T.TASKS))
d0 = T.phan_tich_ngay(datetime.date(2026, 11, 20), None, [])
chk("khong nhap tuoi van chay (chi xet ngay chung)", d0["can_chi"] == "Mậu Tuất" and d0["truc"] == "Bế")

for d in tot[:3]:
    print("  TOT ", d["date"], d["can_chi"], d["bac"], "|", "; ".join(d["tot"]))
for d in xau[:2]:
    print("  XAU ", d["date"], d["can_chi"], "|", "; ".join(d["loai"] + d["xau"]))
print("\nTONG: %d/%d PASS" % (sum(R), len(R)))
