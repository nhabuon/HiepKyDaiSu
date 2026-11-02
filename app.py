import datetime
import html
import re

import streamlit as st

import trach_cat_core as T

st.set_page_config(page_title="Hiệp Kỷ Đại Sư - Chọn Ngày Tốt", page_icon="📜",
                   layout="centered", initial_sidebar_state="collapsed")

VN_TZ = datetime.timezone(datetime.timedelta(hours=7))
AI_PER_SESSION = 3


# ==============================================================================
# AI BINH GIAI (Gemini) - chi viet loi tu du kien da tinh, KHONG tu tinh
# ==============================================================================
def resolve_gemini_model(name):
    n = (name or "").strip().lower()
    if not n:
        return "gemini-4-argon"
    if n.startswith("gemini-"):
        return n
    m = re.search(r"([0-9]+(?:\.[0-9]+)*)\s*[\-_ ]?\s*(argon|pro|flash|ultra|lite)", n)
    if m:
        return "gemini-%s-%s" % (m.group(1), m.group(2))
    return "gemini-4-argon"


def _secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return default


@st.cache_resource
def _daily_counter():
    return {}


def ai_quota_left():
    limit = int(_secret("AI_DAILY_LIMIT", 200))
    today = datetime.datetime.now(VN_TZ).date().isoformat()
    used_today = _daily_counter().get(today, 0)
    used_session = st.session_state.get("ai_used", 0)
    return min(limit - used_today, AI_PER_SESSION - used_session)


def ai_count_one():
    today = datetime.datetime.now(VN_TZ).date().isoformat()
    c = _daily_counter()
    c[today] = c.get(today, 0) + 1
    st.session_state["ai_used"] = st.session_state.get("ai_used", 0) + 1


AI_SYSTEM = """Bạn là Hiệp Kỷ Đại Sư, người bình giải lịch chọn ngày cho khách của Thương Mại và Công Nghệ MIT.
LUẬT BẮT BUỘC:
1. Chỉ dùng đúng các dữ kiện được cung cấp (can chi, trực, hoàng đạo, sao, thần sát, việc nên/kiêng, xung hợp). Không tự tính lại can chi, không thêm thần sát không có trong dữ kiện.
2. Không đưa con số, phần trăm, điểm số hay xác suất.
3. Không phán sức khỏe, bệnh tật, tuổi thọ, không phán số phận ("khắc", "cô quả", "đại nạn").
4. Không bán hay khuyên mua vật phẩm phong thủy, bùa, đá.
5. Giọng văn điềm đạm, rõ ràng, tiếng Việt phổ thông; thuật ngữ Hán Việt thì giải thích ngắn khi dùng lần đầu.
NHIỆM VỤ: Bình giải vì sao các ngày tốt được chọn (đối chiếu với việc khách định làm và bản mệnh), vì sao các ngày xấu bị loại, rồi gợi ý cách chọn giữa các ngày tốt dựa trên yếu tố thực tế (lịch làm việc, chuẩn bị). Dài khoảng 250-350 chữ, chia mục ngắn."""


def build_ai_prompt(user, task, good, bad):
    def line(d):
        return ("- %s (%s, âm lịch %s), ngày %s, trực %s, %s %s, sao %s. Điểm cộng: %s. Điểm trừ: %s. Lý do loại: %s"
                % (d["date"].strftime("%d/%m/%Y"), d["thu"], d["am_lich"], d["can_chi"], d["truc"],
                   "Hoàng đạo" if d["hoang_dao"] else "Hắc đạo", d["than"], d["sao"],
                   "; ".join(d["tot"]) or "không", "; ".join(d["xau"]) or "không", "; ".join(d["loai"]) or "không"))
    bt = user["vi"]
    return ("BẢN MỆNH (đã tính sẵn): năm %s, tháng %s, ngày %s, giờ %s; Nhật chủ %s.\nVIỆC ĐỊNH LÀM: %s\n\n"
            "NGÀY TỐT ĐÃ CHỌN:\n%s\n\nNGÀY NÊN TRÁNH:\n%s"
            % (bt["nam"], bt["thang"], bt["ngay"], bt["gio"], bt["ngay"].split()[0], task,
               "\n".join(line(d) for d in good) or "(không có)", "\n".join(line(d) for d in bad) or "(không có)"))


def ask_gemini(prompt):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=_secret("GEMINI_API_KEY"))
    resp = client.models.generate_content(
        model=resolve_gemini_model(_secret("GEMINI_MODEL", "Argon")), contents=prompt,
        config=types.GenerateContentConfig(system_instruction=AI_SYSTEM, max_output_tokens=4000))
    return (resp.text or "").strip()


# ==============================================================================
# GIAO DIEN
# ==============================================================================
def esc(s):
    return html.escape(str(s or ""))


st.markdown("""<style>
.stApp {background:#0f0f12;} .stApp, .stApp p, .stApp label, .stApp li {color:#ececf1;}
.hk-head {background:linear-gradient(135deg,#3b2a05 0%,#854d0e 100%); padding:22px; border-radius:0 0 20px 20px;
  text-align:center; margin-top:-50px; border-bottom:2px solid #eab308;}
.hk-head h2 {color:#facc15; margin:0; letter-spacing:2px;} .hk-head p {color:#fde68a; margin:6px 0 0;}
.card {background:#18181b; padding:14px 16px; border-radius:10px; margin-bottom:10px; border-left:5px solid #eab308;}
.card.good {border-left-color:#22c55e;} .card.bad {border-left-color:#ef4444;}
.card .t {font-size:17px; font-weight:700;} .card .s {color:#a1a1aa; font-size:13px; margin:2px 0 6px;}
.card ul {margin:4px 0 0 18px; padding:0;} .card li {font-size:14px; line-height:1.5;}
.tag {display:inline-block; padding:1px 8px; border-radius:9px; font-size:12px; margin-left:6px; background:#27272a;}
.tag.g {color:#4ade80;} .tag.y {color:#facc15;} .tag.n {color:#a1a1aa;} .tag.r {color:#f87171;}
.bazi {display:grid; grid-template-columns:repeat(4,1fr); gap:8px; text-align:center;}
.bazi div {background:#18181b; border:1px solid #854d0e; border-radius:8px; padding:8px;}
.bazi b {display:block; color:#facc15; font-size:17px;} .bazi small {color:#a1a1aa;}
.note {color:#8b8b95; font-size:12px; border-top:1px solid #27272a; padding-top:10px; margin-top:18px;}
#MainMenu, footer, header {visibility:hidden;}
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="hk-head"><h2>📜 HIỆP KỶ ĐẠI SƯ</h2><p>Chọn ngày tốt theo lịch Can Chi và bản mệnh Tứ Trụ · Thương Mại và Công Nghệ MIT</p></div>""",
            unsafe_allow_html=True)

HOURS = {"Không rõ giờ sinh": None, "Tý sớm (0h - 1h)": 0, "Sửu (1h - 3h)": 2, "Dần (3h - 5h)": 4,
         "Mão (5h - 7h)": 6, "Thìn (7h - 9h)": 8, "Tỵ (9h - 11h)": 10, "Ngọ (11h - 13h)": 12,
         "Mùi (13h - 15h)": 14, "Thân (15h - 17h)": 16, "Dậu (17h - 19h)": 18, "Tuất (19h - 21h)": 20,
         "Hợi (21h - 23h)": 22, "Tý muộn (23h - 24h)": 23}

today = datetime.datetime.now(VN_TZ).date()
with st.form("hk"):
    st.markdown("##### 🔮 BƯỚC 1: Ngày giờ sinh (dương lịch)")
    c1, c2 = st.columns([3, 2])
    birth = c1.date_input("Ngày sinh", value=datetime.date(1990, 1, 1), min_value=datetime.date(1920, 1, 1),
                          max_value=today, format="DD/MM/YYYY")
    hour_label = c2.selectbox("Giờ sinh", list(HOURS.keys()))
    ty_moi = st.checkbox("Sinh giờ Tý muộn (23h - 24h) thì tính sang ngày hôm sau",
                         help="Các phái còn tranh cãi chỗ này. Mặc định giữ ngày cũ, chỉ đổi Can giờ.")
    st.markdown("##### 📅 BƯỚC 2: Việc định làm và khoảng ngày cần chọn")
    task = st.selectbox("Việc định làm", list(T.TASKS.keys()))
    c3, c4 = st.columns(2)
    start = c3.date_input("Từ ngày", value=today, format="DD/MM/YYYY")
    end = c4.date_input("Đến ngày", value=today + datetime.timedelta(days=30), format="DD/MM/YYYY")
    go = st.form_submit_button("📜 CHỌN NGÀY TỐT", type="primary", width="stretch")

if go:
    try:
        h = HOURS[hour_label]
        user = T.bat_tu(birth.year, birth.month, birth.day, h, 30 if h == 23 else 0, ty_muon_sang_ngay_moi=ty_moi)
        days = T.quet(start, end, user, task)
        st.session_state["res"] = {"user": user, "task": task, "days": days}
        st.session_state.pop("ai_text", None)
    except ValueError as e:
        st.warning("⚠️ " + str(e))

res = st.session_state.get("res")
if res:
    user, task, days = res["user"], res["task"], res["days"]
    good, bad = T.xep_hang(days)
    v = user["vi"]
    st.markdown("##### Tứ trụ bản mệnh")
    st.markdown(f"""<div class="bazi"><div><small>Năm</small><b>{esc(v['nam'])}</b></div><div><small>Tháng</small><b>{esc(v['thang'])}</b></div>
<div><small>Ngày (Nhật chủ)</small><b>{esc(v['ngay'])}</b></div><div><small>Giờ</small><b>{esc(v['gio'])}</b></div></div>""",
                unsafe_allow_html=True)
    st.caption(f"Tuổi {esc(v['nam'].split()[1])} (con {user['con_giap']}) · Nhật chủ {esc(v['ngay'].split()[0])}")

    TAG = {"Rất hợp": "g", "Hợp": "y", "Bình thường": "n", T.TIER_BAD: "r"}

    def card(d, kind):
        items = d["loai"] + d["xau"] if kind == "bad" else d["tot"] + d["xau"]
        lis = "".join(f"<li>{'✅' if (kind != 'bad' and x in d['tot']) else '⛔' if x in d['loai'] else '⚠️'} {esc(x)}</li>" for x in items)
        st.markdown(f"""<div class="card {kind}"><div class="t">{d['date'].strftime('%d/%m/%Y')} · {esc(d['thu'])}
<span class="tag {TAG[d['bac']]}">{esc(d['bac'])}</span></div>
<div class="s">Ngày {esc(d['can_chi'])} · Âm lịch {esc(d['am_lich'])} · Trực {esc(d['truc'])} · {'Hoàng đạo' if d['hoang_dao'] else 'Hắc đạo'} {esc(d['than'])}</div>
<ul>{lis}</ul></div>""", unsafe_allow_html=True)

    st.markdown(f"##### ✅ Ngày nên chọn cho: {esc(task)}")
    top = [d for d in good if d["bac"] in ("Rất hợp", "Hợp")][:5]
    if top:
        for d in top:
            card(d, "good")
    else:
        st.info("Trong khoảng này không có ngày đạt mức Hợp. Bác thử nới rộng khoảng ngày.")
        for d in good[:3]:
            card(d, "good")

    st.markdown("##### ⛔ Ngày nên tránh")
    for d in bad[:3]:
        card(d, "bad")

    with st.expander(f"📋 Xem toàn bộ {len(days)} ngày"):
        st.dataframe([{"Ngày": d["date"].strftime("%d/%m/%Y"), "Thứ": d["thu"], "Âm lịch": d["am_lich"],
                       "Can chi": d["can_chi"], "Xếp bậc": d["bac"], "Trực": d["truc"],
                       "Thần trực": d["than"] + (" (Hoàng đạo)" if d["hoang_dao"] else " (Hắc đạo)"),
                       "Sao": d["sao"], "Nên": ", ".join(d["nen"]), "Kiêng": ", ".join(d["kieng"]),
                       "Lý do loại": "; ".join(d["loai"])} for d in days],
                     hide_index=True, width="stretch")
    with st.expander("ℹ️ Cách xếp bậc"):
        st.markdown(
            "- **Loại ngay** (Không nên): lịch kiêng đúng việc định làm, ngày xung tuổi hoặc xung Nhật chi, "
            "phạm Nguyệt Phá, hoặc lịch ghi mọi việc không nên.\n"
            "- **Cộng**: lịch ghi nên làm việc này, Hoàng đạo, Trực Thành/Khai/Định, cát tú, cát thần mạnh "
            "(Thiên Đức, Nguyệt Đức, Thiên Ân, Thiên Xá...), hợp tuổi, can ngày hợp Nhật chủ.\n"
            "- **Trừ**: Hắc đạo, Trực Phá/Bế, hung tú, hung sát nặng, Tam Nương, Nguyệt Kỵ, Thất Sát, Không Vong.\n"
            "- Ngày lịch không ghi nên làm việc đã chọn thì cao nhất chỉ đến mức **Bình thường**.")

    # ---- AI binh giai ----
    st.markdown("##### 🧙 Lời bình của Đại Sư")
    if st.session_state.get("ai_text"):
        st.markdown(st.session_state["ai_text"])
    elif not _secret("GEMINI_API_KEY"):
        st.caption("Phần bình giải bằng AI chưa được bật.")
    elif ai_quota_left() <= 0:
        st.caption("Đã hết lượt bình giải hôm nay. Kết quả chọn ngày ở trên vẫn đầy đủ.")
    elif st.button("🧙 Nhờ Đại Sư bình giải", width="stretch"):
        with st.spinner("Đại Sư đang xem lịch..."):
            try:
                txt = ask_gemini(build_ai_prompt(user, task, top or good[:3], bad[:3]))
                ai_count_one()
                st.session_state["ai_text"] = txt or "Đại Sư chưa trả lời được, bác thử lại sau."
                st.rerun()
            except Exception as e:
                print("[HiepKy] AI loi:", e)
                st.warning("Đại Sư đang bận, bác thử lại sau ít phút. Kết quả chọn ngày ở trên vẫn dùng được.")

    st.markdown("""<div class="note">※ GHI CHÚ<br>
Kết quả tính theo quy tắc lịch Can Chi truyền thống: 12 Trực, Hoàng đạo/Hắc đạo, Nhị thập bát tú, thần sát,
xung hợp với tuổi. Bảng việc nên/kiêng lấy theo dữ liệu lịch vạn niên phổ thông (thư viện lunar_python).
Âm lịch tính theo lịch Trung Hoa, đôi khi lệch một ngày so với lịch Việt Nam ở một vài tháng.
Đây là tham khảo văn hóa, chưa có kiểm chứng khoa học; không dùng để trì hoãn việc khám chữa bệnh
hay các quyết định cần chuyên môn.</div>""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;color:#71717a;font-size:12px;margin-top:14px'>© 2026 Thương Mại và Công Nghệ MIT</div>",
            unsafe_allow_html=True)
