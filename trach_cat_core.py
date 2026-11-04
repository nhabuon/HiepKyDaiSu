# -*- coding: utf-8 -*-
"""
HIEP KY DAI SU - WEB - LOI TINH NGAY (luat co dinh, khong dung AI de tinh)

Thay doi so voi ban desktop V5:
- Tu tru tinh bang lunar_python (tiet khi theo gio giao tiet that). Engine V5 dung
  ngay cat co dinh nen tru thang sai 1,33% so ngay, tru nam sai 0,15% (1940-2040).
- Gio Viet Nam (UTC+7): lunar_python tinh tiet khi theo gio Bac Kinh (UTC+8), nen
  tru nam/thang lay tai thoi diem +1 gio; tru ngay/gio giu gio dia phuong.
- Gio Ty muon (23h-24h): tuy chon "sang ngay moi" hoac "giu ngay cu" (cac phai con tranh cai).
- Du kien tung ngay: 12 Truc, Hoang dao/Hac dao, Nhi thap bat tu, cat than/hung sat,
  viec nen/kieng, xung sat. Nguon: thu vien lunar_python (MIT); bang nen/kieng la
  du lieu lich van nien pho thong, KHONG trich tu Hiep Ky Bien Phuong Thu.
- Tang ca nhan: xung/hop voi tuoi va Nhat tru, Thien can khac (That Sat), Khong Vong.
- Xep hang theo diem luat MINH BACH, hien bang bac (khong in con so diem cho khach).
"""
import datetime

from lunar_python import Solar

import hanviet as H

# ------------------------------------------------------------------------------
# VIEC CAN LAM -> ma viec trong lich (viec chinh dau tien, cac viec phu sau)
# Kham chua benh KHONG dua vao: khong de ai hoan di kham vi "ngay xau".
# ------------------------------------------------------------------------------
TASKS = {
    "Khai trương, mở cửa hàng": ["开市", "纳财", "交易", "挂匾"],
    "Ký hợp đồng, giao dịch lớn": ["立券", "交易"],
    "Cưới hỏi": ["嫁娶", "纳采"],
    "Ăn hỏi, dạm ngõ, đính hôn": ["纳采", "订盟"],
    "Động thổ, khởi công xây dựng": ["动土", "起基", "修造"],
    "Sửa chữa nhà cửa": ["修造", "动土"],
    "Cất nóc, đổ mái": ["上梁", "盖屋"],
    "Nhập trạch, về nhà mới": ["入宅", "移徙", "安香"],
    "Chuyển nhà, chuyển văn phòng": ["移徙", "入宅"],
    "Xuất hành, đi xa, công tác": ["出行"],
    "Nhậm chức, nhận việc mới": ["赴任"],
    "Mua nhà đất, tài sản lớn": ["置产", "交易", "立券"],
    "Thu tiền, nhập hàng": ["纳财", "交易"],
    "Nhập học, khai giảng": ["入学"],
    "Cúng lễ, cầu phúc": ["祭祀", "祈福"],
    "An táng": ["安葬", "破土"],
    "Việc khác (chỉ xét ngày tốt chung)": [],
}

TRUC_TOT = {"成", "开", "定"}
TRUC_XAU = {"破", "闭"}
SAT_NANG = {"月破"}  # loai thang
CAT_THAN_MANH = {"天德", "月德", "天德合", "月德合", "天赦", "天恩", "天愿"}
HUNG_SAT_NANG = {"四废", "四离", "大耗", "往亡", "归忌", "天罡", "河魁"}
TAM_NUONG = {3, 7, 13, 18, 22, 27}
NGUYET_KY = {5, 14, 23}

TIERS = [(7, "Rất hợp"), (4, "Hợp"), (1, "Bình thường")]
TIER_BAD = "Không nên"


# ------------------------------------------------------------------------------
# QUAN HE CAN CHI
# ------------------------------------------------------------------------------
def _ci(z):
    return H.CHI.index(z)


def _gi(g):
    return H.CAN.index(g)


def luc_xung(a, b):
    return (_ci(a) - _ci(b)) % 12 == 6


def luc_hop(a, b):
    return (_ci(a) + _ci(b)) % 12 == 1


def tam_hop(a, b):
    return a != b and _ci(a) % 4 == _ci(b) % 4


def can_hop(a, b):
    return abs(_gi(a) - _gi(b)) == 5


def that_sat(day_gan, user_gan):
    """Can ngay khac Can Nhat chu, cung am duong."""
    d, u = _gi(day_gan), _gi(user_gan)
    return (d // 2 + 2) % 5 == u // 2 and d % 2 == u % 2


# ------------------------------------------------------------------------------
# TU TRU
# ------------------------------------------------------------------------------
def bat_tu(year, month, day, hour=None, minute=0, ty_muon_sang_ngay_moi=False):
    """
    hour=None: khong ro gio sinh (tru gio de trong).
    Tra ve dict can chi chu Han + tieng Viet.
    """
    h = 12 if hour is None else hour
    local = datetime.datetime(year, month, day, h, minute)
    bj = local + datetime.timedelta(hours=1)  # gio Bac Kinh tuong ung de xet tiet khi
    ec_ym = Solar.fromYmdHms(bj.year, bj.month, bj.day, bj.hour, bj.minute, 0).getLunar().getEightChar()
    ec = Solar.fromYmdHms(year, month, day, h, minute, 0).getLunar().getEightChar()
    ec.setSect(1 if ty_muon_sang_ngay_moi else 2)
    zh = {"nam": ec_ym.getYear(), "thang": ec_ym.getMonth(), "ngay": ec.getDay(),
          "gio": ec.getTime() if hour is not None else None}
    return {
        "han": zh,
        "vi": {k: (H.ganzhi_vi(v) if v else "Khuyết giờ") for k, v in zh.items()},
        "khong_vong": ec.getDayXunKong(),
        "con_giap": H.CON_GIAP[_ci(zh["nam"][1])],
    }


def chi_tuoi(user):
    """Ban menh rut gon CHI con tru nam (tuoi). Dung cho phan gui AI va khoa cache loi binh:
    khong mang thang/ngay/gio sinh, nen loi binh dung chung duoc cho moi khach cung tuoi."""
    return {"han": {"nam": user["han"]["nam"], "ngay": None}, "vi": {"nam": user["vi"]["nam"]},
            "khong_vong": "", "con_giap": user["con_giap"]}


# ------------------------------------------------------------------------------
# PHAN TICH MOT NGAY
# ------------------------------------------------------------------------------
def phan_tich_ngay(date, user, task_keys):
    l = Solar.fromYmd(date.year, date.month, date.day).getLunar()
    day_gz = l.getDayInGanZhi()
    yi, ji = l.getDayYi(), l.getDayJi()
    jishen = [x for x in l.getDayJiShen() if x != "无"]
    xiong = [x for x in l.getDayXiongSha() if x != "无"]
    truc = l.getZhiXing()
    ts, ts_type = l.getDayTianShen(), l.getDayTianShenType()
    xiu, xiu_luck = l.getXiu(), l.getXiuLuck()
    lunar_day = l.getDay()

    tot, xau, loai = [], [], []
    pts = 0

    # --- 1. Viec can lam (nen / kieng trong lich) ---
    if task_keys:
        chinh = task_keys[0]
        if "诸事不宜" in yi:
            loai.append("Lịch ghi: mọi việc đều không nên")
        kieng = [k for k in task_keys if k in ji]
        if kieng:
            loai.append("Lịch kiêng: " + ", ".join(H.viec(k) for k in kieng))
        if chinh in yi:
            pts += 3
            tot.append("Lịch ghi nên: " + H.viec(chinh))
        else:
            phu = [k for k in task_keys[1:] if k in yi]
            if phu:
                pts += 1
                tot.append("Lịch ghi nên việc liên quan: " + ", ".join(H.viec(k) for k in phu))
            elif "馀事勿取" in ji:
                loai.append("Lịch ghi: ngoài các việc được nêu, việc khác không nên")
    elif "诸事不宜" in yi:
        loai.append("Lịch ghi: mọi việc đều không nên")

    # --- 2. Hoang dao / Hac dao, Truc, Tu ---
    if ts_type == "黄道":
        pts += 2
        tot.append("Hoàng đạo (%s)" % H.hv(ts))
    else:
        pts -= 2
        xau.append("Hắc đạo (%s)" % H.hv(ts))
    if truc in TRUC_TOT:
        pts += 1
        tot.append("Trực %s" % H.hv(truc))
    elif truc in TRUC_XAU:
        pts -= 1
        xau.append("Trực %s" % H.hv(truc))
    if xiu_luck == "吉":
        pts += 1
        tot.append("Sao %s (cát tú)" % H.XIU[xiu])
    else:
        pts -= 1
        xau.append("Sao %s (hung tú)" % H.XIU[xiu])

    # --- 3. Than sat ---
    manh = [x for x in jishen if x in CAT_THAN_MANH]
    if manh:
        pts += min(2, len(manh))
        tot.append("Cát thần: " + ", ".join(H.hv(x) for x in manh))
    if any(x in SAT_NANG for x in xiong):
        loai.append("Phạm Nguyệt Phá")
    nang = [x for x in xiong if x in HUNG_SAT_NANG]
    if nang:
        pts -= min(2, len(nang))
        xau.append("Hung sát: " + ", ".join(H.hv(x) for x in nang))

    # --- 4. Ngay ky dan gian Viet ---
    if lunar_day in TAM_NUONG:
        pts -= 2
        xau.append("Ngày Tam Nương (mùng %d âm lịch)" % lunar_day)
    if lunar_day in NGUYET_KY:
        pts -= 2
        xau.append("Ngày Nguyệt Kỵ (mùng %d âm lịch)" % lunar_day)

    # --- 5. Tang ca nhan ---
    if user:
        yz = user["han"]["nam"][1]
        nt = user["han"].get("ngay")  # None = chi biet tuoi (xem chi_tuoi): bo qua cac xet theo Nhat tru
        dg, dz = (nt[0], nt[1]) if nt else (None, None)
        gan, zhi = day_gz[0], day_gz[1]
        if luc_xung(zhi, yz):
            loai.append("Xung tuổi %s (ngày %s xung %s)" % (H.CHI_VI[_ci(yz)], H.CHI_VI[_ci(zhi)], H.CHI_VI[_ci(yz)]))
        if dz and luc_xung(zhi, dz) and dz != yz:
            loai.append("Xung Nhật chi %s của bản mệnh" % H.CHI_VI[_ci(dz)])
        hop = [nm for nm, f in (("lục hợp", luc_hop), ("tam hợp", tam_hop))
               for b in {yz, dz} - {None} if f(zhi, b)]
        if hop:
            pts += 2
            tot.append("Chi ngày %s %s với bản mệnh" % (H.CHI_VI[_ci(zhi)], " và ".join(sorted(set(hop)))))
        if dg and can_hop(gan, dg):
            pts += 1
            tot.append("Can ngày %s hợp Nhật chủ %s" % (H.CAN_VI[_gi(gan)], H.CAN_VI[_gi(dg)]))
        if dg and that_sat(gan, dg):
            pts -= 2
            xau.append("Can ngày %s là Thất Sát của Nhật chủ %s" % (H.CAN_VI[_gi(gan)], H.CAN_VI[_gi(dg)]))
        if zhi in user.get("khong_vong", ""):
            pts -= 1
            xau.append("Chi ngày rơi vào Không Vong của Nhật trụ")

    if loai:
        tier = TIER_BAD
    else:
        tier = next((name for floor, name in TIERS if pts >= floor), TIER_BAD)
        # Lich khong ghi nen lam viec nay -> du ngay tot chung cung chi toi "Binh thuong"
        if task_keys and not any(k in yi for k in task_keys) and tier in ("Rất hợp", "Hợp"):
            tier = "Bình thường"
            xau.append("Lịch không ghi việc này trong danh sách nên làm")

    return {
        "date": date, "thu": ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][date.weekday()],
        "am_lich": "%d/%d%s" % (lunar_day, abs(l.getMonth()), " (nhuận)" if l.getMonth() < 0 else ""),
        "can_chi": H.ganzhi_vi(day_gz), "truc": H.hv(truc), "than": H.hv(ts),
        "hoang_dao": ts_type == "黄道", "sao": H.XIU[xiu],
        "nen": [H.viec(x) for x in yi if x not in ("无",)],
        "kieng": [H.viec(x) for x in ji if x not in ("无",)],
        "cat_than": [H.hv(x) for x in jishen], "hung_sat": [H.hv(x) for x in xiong],
        "xung": "Xung tuổi %s" % H.CHI_VI[(_ci(day_gz[1]) + 6) % 12],
        "sat_huong": H.hv(l.getDaySha()),
        "tot": tot, "xau": xau, "loai": loai, "diem": pts, "bac": tier,
    }


MAX_DAYS = 90


def quet(start, end, user, task):
    if end < start:
        raise ValueError("Ngày bắt đầu phải trước ngày kết thúc.")
    if (end - start).days + 1 > MAX_DAYS:
        raise ValueError("Chỉ quét tối đa %d ngày mỗi lần." % MAX_DAYS)
    keys = TASKS.get(task, [])
    out, d = [], start
    while d <= end:
        out.append(phan_tich_ngay(d, user, keys))
        d += datetime.timedelta(days=1)
    return out


def xep_hang(days):
    rank = {"Rất hợp": 0, "Hợp": 1, "Bình thường": 2}
    tot = sorted([d for d in days if d["bac"] != TIER_BAD], key=lambda d: (rank[d["bac"]], -d["diem"], d["date"]))
    xau = sorted([d for d in days if d["bac"] == TIER_BAD], key=lambda d: (len(d["loai"]) == 0, d["diem"], d["date"]))
    return tot, xau
