# -*- coding: utf-8 -*-
"""Dich thuat ngu lich (chu Han gian the tu thu vien lunar_python) sang Han Viet + nghia."""

CHAR = dict(zip(
    "丁七三上不丑专世丙东丧临乘乙九习了事五井亡亢交亥产亲人仓仪任伐会位作佣修俱元光兔入八六养冠冲出击分刑券刻割动劫勾勿北匮医匾午单南卯危卸厌厕参友发取口司合吉名后吏吠启命咸哭喜嗣器囊四土圣地坎坏坟垣基堂堤塑塞墓墙壁壬复大天奎女娄娶婿嫁子孤学宁宅宇守安官定宜宝室害寅富对寿将小尾居屋岁岫巫己巳市帐平床庙庚府废建开张归往徙德心忌恩愿戊戌成戾房手执扫护拆招挂捉捕掘探摇支收放教敬整斋斗断无日时明易星昴普月服期木未朱机架柩柱柳栽桥梁械武死殓母毕氐民气水求池沐河治浴涂渔渠渡游满火灶灸灾焦煞牛牢牧狗狠猎猪猴玄玉王理生甲申畋畜病癸白益盖盟相眼破碑碓磉磑祀祈神祭祸福离种移稠穴穷空立竖笄符筑箕纯纳经结绘络绝续网罡置羊翼耗胃脊致舍船艺葬薄虎虚蚁蛇蜜血行衣补裁西要角觜解触订讼词诸谢财败货贼赦赴起足车轸辛辰进退逐造道酉酬醮采重金针钻错门闭问阳阴阵陈除雀雇雕青风饰馀香马驿鬼魁鸟鸡鸣鼠龙",
    ["Đinh", "Thất", "Tam", "Thượng", "Bất", "Sửu", "Chuyên", "Thế", "Bính", "Đông", "Tang", "Lâm", "Thừa", "Ất", "Cửu", "Tập", "Liễu", "Sự", "Ngũ", "Tỉnh", "Vong", "Cang", "Giao", "Hợi", "Sản", "Thân", "Nhân", "Thương", "Nghi", "Nhậm", "Phạt", "Hội", "Vị", "Tác", "Dung", "Tu", "Câu", "Nguyên", "Quang", "Thố", "Nhập", "Bát", "Lục", "Dưỡng", "Quan", "Xung", "Xuất", "Kích", "Phân", "Hình", "Khoán", "Khắc", "Cát", "Động", "Kiếp", "Câu", "Vật", "Bắc", "Quỹ", "Y", "Biển", "Ngọ", "Đơn", "Nam", "Mão", "Nguy", "Tá", "Yếm", "Xí", "Sâm", "Hữu", "Phát", "Thủ", "Khẩu", "Tư", "Hợp", "Cát", "Danh", "Hậu", "Lại", "Phệ", "Khải", "Mệnh", "Hàm", "Khốc", "Hỷ", "Tự", "Khí", "Nang", "Tứ", "Thổ", "Thánh", "Địa", "Khảm", "Hoại", "Phần", "Viên", "Cơ", "Đường", "Đê", "Tố", "Tắc", "Mộ", "Tường", "Bích", "Nhâm", "Phục", "Đại", "Thiên", "Khuê", "Nữ", "Lâu", "Thú", "Tế", "Giá", "Tý", "Cô", "Học", "Ninh", "Trạch", "Vũ", "Thủ", "An", "Quan", "Định", "Nghi", "Bảo", "Thất", "Hại", "Dần", "Phú", "Đối", "Thọ", "Tướng", "Tiểu", "Vĩ", "Cư", "Ốc", "Tuế", "Tụ", "Vu", "Kỷ", "Tỵ", "Thị", "Trướng", "Bình", "Sàng", "Miếu", "Canh", "Phủ", "Phế", "Kiến", "Khai", "Trương", "Quy", "Vãng", "Tỉ", "Đức", "Tâm", "Kỵ", "Ân", "Nguyện", "Mậu", "Tuất", "Thành", "Lệ", "Phòng", "Thủ", "Chấp", "Tảo", "Hộ", "Sách", "Chiêu", "Quải", "Tróc", "Bộ", "Quật", "Thám", "Dao", "Chi", "Thu", "Phóng", "Giáo", "Kính", "Chỉnh", "Trai", "Đẩu", "Đoạn", "Vô", "Nhật", "Thời", "Minh", "Dịch", "Tinh", "Mão", "Phổ", "Nguyệt", "Phục", "Kỳ", "Mộc", "Mùi", "Chu", "Cơ", "Giá", "Cữu", "Trụ", "Liễu", "Tài", "Kiều", "Lương", "Giới", "Vũ", "Tử", "Liệm", "Mẫu", "Tất", "Đê", "Dân", "Khí", "Thủy", "Cầu", "Trì", "Mộc", "Hà", "Trị", "Dục", "Đồ", "Ngư", "Cừ", "Độ", "Du", "Mãn", "Hỏa", "Táo", "Cứu", "Tai", "Tiêu", "Sát", "Ngưu", "Lao", "Mục", "Cẩu", "Ngận", "Liệp", "Trư", "Hầu", "Huyền", "Ngọc", "Vương", "Lý", "Sinh", "Giáp", "Thân", "Điền", "Súc", "Bệnh", "Quý", "Bạch", "Ích", "Cái", "Minh", "Tướng", "Nhãn", "Phá", "Bi", "Đối", "Tảng", "Ngãi", "Tự", "Kỳ", "Thần", "Tế", "Họa", "Phúc", "Ly", "Chủng", "Di", "Trù", "Huyệt", "Cùng", "Không", "Lập", "Thụ", "Kê", "Phù", "Trúc", "Cơ", "Thuần", "Nạp", "Kinh", "Kết", "Hội", "Lạc", "Tuyệt", "Tục", "Võng", "Cương", "Trí", "Dương", "Dực", "Hao", "Vị", "Tích", "Trí", "Xá", "Thuyền", "Nghệ", "Táng", "Bạc", "Hổ", "Hư", "Nghĩ", "Xà", "Mật", "Huyết", "Hành", "Y", "Bổ", "Tài", "Tây", "Yếu", "Giác", "Chủy", "Giải", "Xúc", "Đính", "Tụng", "Từ", "Chư", "Tạ", "Tài", "Bại", "Hóa", "Tặc", "Xá", "Phó", "Khởi", "Túc", "Xa", "Chẩn", "Tân", "Thìn", "Tiến", "Thoái", "Trục", "Tạo", "Đạo", "Dậu", "Thù", "Tiếu", "Thái", "Trùng", "Kim", "Châm", "Toản", "Thác", "Môn", "Bế", "Vấn", "Dương", "Âm", "Trận", "Trần", "Trừ", "Tước", "Cố", "Điêu", "Thanh", "Phong", "Sức", "Dư", "Hương", "Mã", "Dịch", "Quỷ", "Khôi", "Điểu", "Kê", "Minh", "Thử", "Long"]))

# Ten rieng dung theo thoi quen lich Viet
OVERRIDE = {
    "元武": "Nguyên Vũ", "玄武": "Huyền Vũ", "子": "Tý",
    "东": "Đông", "西": "Tây", "南": "Nam", "北": "Bắc",
}

# Nghia tieng Viet cho cac viec Nen / Kieng
VIEC = {
    "上梁": "cất nóc, gác đòn dông", "习艺": "học nghề", "交易": "giao dịch, mua bán",
    "伐木": "chặt cây", "会亲友": "gặp gỡ họ hàng bạn bè", "作梁": "làm xà nhà",
    "作灶": "làm bếp, đặt bếp", "修坟": "sửa mộ", "修造": "sửa chữa, xây sửa nhà",
    "修门": "sửa cửa", "修饰垣墙": "sửa sang tường rào", "入学": "nhập học",
    "入宅": "nhập trạch, về nhà mới", "入殓": "nhập liệm", "冠笄": "lễ trưởng thành",
    "出火": "di dời bếp, bàn thờ", "出行": "xuất hành, đi xa", "出货财": "xuất hàng, chi tiền",
    "分居": "ra ở riêng", "割蜜": "lấy mật ong", "动土": "động thổ",
    "取渔": "đánh cá", "合寿木": "đóng quan tài dự phòng", "合帐": "may màn trướng",
    "合脊": "lợp nóc", "启钻": "mở huyệt, cải táng", "坏垣": "phá tường cũ",
    "塑绘": "đắp tượng, vẽ tranh", "塞穴": "lấp hang hốc", "嫁娶": "cưới gả",
    "安床": "kê giường", "安机械": "lắp đặt máy móc", "安碓磑": "đặt cối giã, cối xay",
    "安葬": "an táng", "安门": "lắp cửa", "安香": "an vị bàn thờ, thắp hương",
    "定磉": "đặt chân cột", "平治道涂": "sửa đường", "开仓": "mở kho",
    "开光": "khai quang (tượng, đồ thờ)", "开厕": "làm nhà vệ sinh", "开市": "khai trương",
    "开柱眼": "đục lỗ cột", "开池": "đào ao", "开渠": "đào mương", "开生坟": "xây mộ sinh phần",
    "归宁": "về thăm nhà cha mẹ", "归岫": "về quê, ẩn cư", "成服": "lễ thành phục (tang)",
    "扫舍": "quét dọn nhà", "拆卸": "tháo dỡ", "挂匾": "treo biển hiệu",
    "捕捉": "săn bắt, bắt trộm", "掘井": "đào giếng", "放水": "tháo nước",
    "教牛马": "dạy gia súc", "整手足甲": "cắt móng tay chân", "斋醮": "lập đàn cúng lễ",
    "断蚁": "diệt mối kiến", "普渡": "lễ phổ độ", "架马": "dựng giàn giáo",
    "栽种": "trồng trọt", "求医": "đi khám chữa bệnh", "求嗣": "cầu con",
    "沐浴": "tắm gội", "治病": "chữa bệnh", "牧养": "chăn nuôi",
    "理发": "cắt tóc", "畋猎": "săn bắn", "盖屋": "lợp nhà", "破土": "phá thổ (đào đất làm mộ)",
    "破屋": "phá nhà cũ", "祈福": "cầu phúc", "祭祀": "cúng tế",
    "移徙": "chuyển nhà, dời chỗ ở", "移柩": "di quan", "立券": "ký kết hợp đồng, lập khế ước",
    "立碑": "dựng bia", "竖柱": "dựng cột", "筑堤": "đắp đê", "纳婿": "đón rể",
    "纳畜": "mua thêm gia súc", "纳财": "thu tiền, nhập hàng", "纳采": "dạm ngõ, ăn hỏi",
    "经络": "dệt, se sợi", "结网": "đan lưới", "置产": "mua nhà đất, tài sản",
    "补垣": "vá tường", "裁衣": "may đo quần áo", "解除": "giải trừ, tẩy uế",
    "订盟": "đính ước, kết giao", "诸事不宜": "mọi việc đều không nên",
    "谢土": "tạ đất", "赴任": "nhậm chức, nhận việc mới", "起基": "đổ móng",
    "进人口": "nhận người (con nuôi, người làm)", "造仓": "làm kho", "造庙": "xây miếu",
    "造桥": "làm cầu", "造畜稠": "làm chuồng trại", "造船": "đóng thuyền",
    "造车器": "đóng xe cộ, dụng cụ", "酬神": "lễ tạ thần", "针灸": "châm cứu",
    "问名": "hỏi tên (lễ cưới xưa)", "除服": "mãn tang", "雇佣": "thuê người",
    "雕刻": "điêu khắc", "馀事勿取": "các việc khác không nên làm",
    "乘船": "đi thuyền", "探病": "thăm người ốm", "行丧": "đưa tang", "词讼": "kiện tụng",
}

XIU = dict(zip("角亢氐房心尾箕斗牛女虚危室壁奎娄胃昴毕觜参井鬼柳星张翼轸",
               ["Giác", "Cang", "Đê", "Phòng", "Tâm", "Vĩ", "Cơ", "Đẩu", "Ngưu", "Nữ", "Hư", "Nguy",
                "Thất", "Bích", "Khuê", "Lâu", "Vị", "Mão", "Tất", "Chủy", "Sâm", "Tỉnh", "Quỷ",
                "Liễu", "Tinh", "Trương", "Dực", "Chẩn"]))

CAN = "甲乙丙丁戊己庚辛壬癸"
CHI = "子丑寅卯辰巳午未申酉戌亥"
CAN_VI = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_VI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CON_GIAP = ["Chuột", "Trâu", "Hổ", "Mèo", "Rồng", "Rắn", "Ngựa", "Dê", "Khỉ", "Gà", "Chó", "Lợn"]


def hv(term):
    """Han Viet cua mot thuat ngu, vi du 天德合 -> Thiên Đức Hợp."""
    if term in OVERRIDE:
        return OVERRIDE[term]
    return " ".join(CHAR[c] for c in term)


def ganzhi_vi(gz):
    return "%s %s" % (CAN_VI[CAN.index(gz[0])], CHI_VI[CHI.index(gz[1])])


def viec(term):
    """'Khai Thị (khai trương)'"""
    g = VIEC.get(term)
    return "%s (%s)" % (hv(term), g) if g else hv(term)
