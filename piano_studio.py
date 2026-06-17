"""
📚 Studio & Vita — App completa con login multiutente
Avvia con:  streamlit run piano_studio.py
"""

import streamlit as st
import json, os, uuid, calendar as cal_lib, hashlib
from datetime import date, timedelta
from pathlib import Path

st.set_page_config(page_title="📚 Studio & Vita", page_icon="📚",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1a1a2e 0%,#16213e 55%,#0f3460 100%);
}
section[data-testid="stSidebar"] * { color:#e0e0e0 !important; }
.gradient-title {
    background: linear-gradient(135deg,#667eea,#764ba2);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    font-size:2rem; font-weight:800; margin-bottom:0;
}
.subtitle { color:#888; font-size:1rem; margin-top:2px; margin-bottom:16px; }
div[data-testid="metric-container"] {
    background:#f8f9fa; border-radius:12px; padding:12px 16px;
    border-left:4px solid #667eea; box-shadow:0 2px 8px rgba(0,0,0,.06);
}
.login-box {
    max-width:420px; margin:60px auto; padding:40px;
    background:white; border-radius:20px;
    box-shadow:0 8px 32px rgba(102,126,234,.15);
    border-top:4px solid #667eea;
}
.day-card { background:white; border-radius:16px; padding:20px 22px;
            box-shadow:0 4px 20px rgba(0,0,0,.08); border-top:4px solid #667eea; }
.slot-box { border-radius:10px; padding:10px 14px; margin-bottom:8px; }
.apt-row  { border-radius:8px; padding:8px 12px; margin-bottom:5px;
            border-left:4px solid; background:#fafafa; }
.subj-card{ background:white; border-radius:14px; padding:16px 20px;
            box-shadow:0 2px 10px rgba(0,0,0,.07); border-left:5px solid;
            margin-bottom:14px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  AUTH — SISTEMA LOGIN/REGISTRAZIONE
# ═══════════════════════════════════════════════════════════
USERS_FILE = "users.json"

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users: dict):
    with open(USERS_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,indent=2,ensure_ascii=False)

def register_user(username:str, name:str, password:str) -> tuple[bool,str]:
    users = load_users()
    username = username.strip().lower()
    if not username or not name.strip() or not password:
        return False, "Compila tutti i campi."
    if len(username)<3:
        return False, "Username deve avere almeno 3 caratteri."
    if len(password)<6:
        return False, "Password deve avere almeno 6 caratteri."
    if username in users:
        return False, "Username già esistente. Scegline un altro."
    users[username] = {"name":name.strip(),"password":hash_pw(password)}
    save_users(users)
    return True, "ok"

def login_user(username:str, password:str) -> tuple[bool,str,str]:
    users = load_users()
    username = username.strip().lower()
    if username not in users:
        return False, "", "Username non trovato."
    if users[username]["password"] != hash_pw(password):
        return False, "", "Password errata."
    return True, users[username]["name"], "ok"

# Gestione sessione
if "auth_user"   not in st.session_state: st.session_state.auth_user   = None
if "auth_name"   not in st.session_state: st.session_state.auth_name   = None

# ─── PAGINA LOGIN / REGISTRAZIONE ────────────────────────
if not st.session_state.auth_user:
    st.markdown("""
    <div style='text-align:center;padding:40px 0 10px'>
        <span style='font-size:3rem'>📚</span>
        <h1 style='background:linear-gradient(135deg,#667eea,#764ba2);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            font-size:2.2rem;font-weight:800;margin:0'>Studio & Vita</h1>
        <p style='color:#888;margin-top:4px'>Il tuo piano di studio personale</p>
    </div>
    """, unsafe_allow_html=True)

    col_c = st.columns([1,2,1])[1]
    with col_c:
        tab_login, tab_reg = st.tabs(["🔑 Accedi","✨ Registrati"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            l_user = st.text_input("Username", key="l_user", placeholder="il tuo username")
            l_pw   = st.text_input("Password", key="l_pw", type="password", placeholder="••••••")
            if st.button("Accedi →", key="btn_login", type="primary", use_container_width=True):
                if l_user and l_pw:
                    ok, name, msg = login_user(l_user, l_pw)
                    if ok:
                        st.session_state.auth_user = l_user.strip().lower()
                        st.session_state.auth_name = name
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.warning("Inserisci username e password.")

        with tab_reg:
            st.markdown("<br>", unsafe_allow_html=True)
            r_name = st.text_input("Nome",     key="r_name", placeholder="es. Lorena")
            r_user = st.text_input("Username", key="r_user", placeholder="es. lorena24")
            r_pw   = st.text_input("Password", key="r_pw",   type="password", placeholder="min. 6 caratteri")
            r_pw2  = st.text_input("Ripeti password", key="r_pw2", type="password", placeholder="••••••")
            if st.button("Crea account →", key="btn_reg", type="primary", use_container_width=True):
                if r_pw != r_pw2:
                    st.error("❌ Le password non coincidono.")
                else:
                    ok, msg = register_user(r_user, r_name, r_pw)
                    if ok:
                        st.success("✅ Account creato! Ora accedi dal tab **Accedi**.")
                    else:
                        st.error(f"❌ {msg}")
    st.stop()

# ═══════════════════════════════════════════════════════════
#  DA QUI IN POI: UTENTE LOGGATO
#  Tutti i dati sono isolati per utente
# ═══════════════════════════════════════════════════════════
CURRENT_USER = st.session_state.auth_user
USER_DIR     = Path(f"userdata/{CURRENT_USER}")
USER_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE    = USER_DIR / "study_data.json"
UPLOAD_BASE  = USER_DIR / "uploads"
UPLOAD_BASE.mkdir(exist_ok=True)

# ═══ COSTANTI ═══════════════════════════════════════════════
MONTHS_IT   = ["","Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
               "Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]
WDAYS_SHORT = ["Lun","Mar","Mer","Gio","Ven","Sab","Dom"]
WDAYS_LONG  = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]

APPOINTMENT_TYPES = {
    "🏋️ Palestra":"#e74c3c","🧘 Yoga":"#9b59b6","🥗 Nutrizionista":"#27ae60",
    "🧠 Psicologa":"#3498db","💆 Massaggio":"#e67e22","👩‍⚕️ Medico":"#1abc9c",
    "👥 Amici/Uscita":"#f39c12","🏠 Famiglia":"#e91e63","✈️ Viaggio":"#2980b9",
    "📝 Altro":"#95a5a6",
}
SUBJECT_COLORS = [
    "#e74c3c","#e67e22","#27ae60","#3498db","#9b59b6",
    "#1abc9c","#e91e63","#ff5722","#607d8b","#f39c12",
    "#2ecc71","#16a085","#8e44ad","#d35400","#2980b9",
]
STUDY_SLOTS = [
    ("morning",   "🌅 Mattina",    "#fff8e1"),
    ("afternoon", "☀️ Pomeriggio", "#e8f4fd"),
    ("evening",   "🌙 Sera",       "#f3e5f5"),
]

# ═══ DATI (per utente) ══════════════════════════════════════
def default_data():
    today = date.today()
    return {"subjects":{},"calendar":{},
            "settings":{"start_date":str(today),
                        "end_date":str(today+timedelta(days=60))}}

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return default_data()

def save_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

# Reset session data se cambia utente
if st.session_state.get("_loaded_user") != CURRENT_USER:
    st.session_state["_loaded_user"] = CURRENT_USER
    st.session_state["data"]         = load_data()
    st.session_state["selected_date"]= str(date.today())
    st.session_state["cal_month"]    = date.today().replace(day=1)

def sd():      return st.session_state.data
def persist(): save_data(sd())

# ═══ HELPERS ════════════════════════════════════════════════
def get_subjects(): return sd().get("subjects",{})
def get_settings(): return sd().get("settings",{})
def get_start():
    return date.fromisoformat(get_settings().get("start_date",str(date.today())))
def get_end():
    return date.fromisoformat(get_settings().get("end_date",
           str(date.today()+timedelta(days=60))))
def fmt_date(d:date):
    return f"{WDAYS_LONG[d.weekday()]} {d.day} {MONTHS_IT[d.month]} {d.year}"
def days_left(d:date): return (d-date.today()).days
def next_color():
    used={s["color"] for s in get_subjects().values()}
    for c in SUBJECT_COLORS:
        if c not in used: return c
    return SUBJECT_COLORS[0]

def subject_dates(sid):
    subj=get_subjects().get(sid,{})
    deadline=date.fromisoformat(subj.get("deadline",str(get_end())))
    start=get_start(); end=min(deadline,get_end())
    out=[]; d=start
    while d<=end: out.append(d); d+=timedelta(days=1)
    return out

def active_subjects_on(d:date):
    start=get_start()
    return [(sid,s) for sid,s in get_subjects().items()
            if start<=d<=date.fromisoformat(s.get("deadline",str(get_end())))]

def get_day(d_str): return sd().get("calendar",{}).get(d_str,{})
def init_day(d_str):
    if "calendar" not in sd(): sd()["calendar"]={}
    if d_str not in sd()["calendar"]:
        sd()["calendar"][d_str]={"morning":{},"afternoon":{},"evening":{},
                                  "appointments":[],"notes":""}

def day_has_content(d_str):
    dc=get_day(d_str)
    return (any(dc.get(s,{}).get("objective") for s,_,_ in STUDY_SLOTS)
            or bool(dc.get("appointments",[])))

def get_day_objectives(sid:str, d_str:str) -> list:
    return (sd()["subjects"].get(sid,{})
              .get("days",{}).get(d_str,{}).get("objectives",[]))

def ensure_day(sid:str, d_str:str):
    if "days" not in sd()["subjects"][sid]:
        sd()["subjects"][sid]["days"]={}
    if d_str not in sd()["subjects"][sid]["days"]:
        sd()["subjects"][sid]["days"][d_str]={"objectives":[]}

def add_day_objective(sid:str, d_str:str, text:str):
    ensure_day(sid,d_str)
    sd()["subjects"][sid]["days"][d_str].setdefault("objectives",[]).append(
        {"id":str(uuid.uuid4())[:8],"text":text.strip(),"done":False})
    persist()

def toggle_day_objective(sid:str, d_str:str, obj_id:str, value:bool):
    ensure_day(sid,d_str)
    for o in sd()["subjects"][sid]["days"][d_str].get("objectives",[]):
        if o["id"]==obj_id: o["done"]=value
    persist()

def delete_day_objective(sid:str, d_str:str, obj_id:str):
    ensure_day(sid,d_str)
    objs=sd()["subjects"][sid]["days"][d_str].get("objectives",[])
    sd()["subjects"][sid]["days"][d_str]["objectives"]=[o for o in objs if o["id"]!=obj_id]
    persist()

def obj_progress(sid:str):
    days=subject_dates(sid); total=0; done=0
    for d in days:
        objs=get_day_objectives(sid,str(d))
        total+=len(objs); done+=sum(1 for o in objs if o.get("done",False))
    return done, total, (int(done/total*100) if total else 0)

# ═══ SIDEBAR ════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## 📚 Studio & Vita")
    st.markdown(
        f"<div style='background:#ffffff22;border-radius:10px;padding:8px 12px;margin-bottom:8px'>"
        f"👤 <b>{st.session_state.auth_name}</b><br>"
        f"<small style='color:#aaa'>@{CURRENT_USER}</small></div>",
        unsafe_allow_html=True)
    st.caption(f"📅 {fmt_date(date.today())}")
    st.markdown("---")

    subjects   = get_subjects()
    base_pages = ["🏠 Dashboard","📅 Calendario","📚 Materie & Esami"]
    subj_pages = [f"📖 {s['name']}" for s in subjects.values()]
    page = st.radio("Nav", base_pages+subj_pages, label_visibility="collapsed")

    if subjects:
        st.markdown("---")
        st.markdown("**📊 Progressi**")
        for sid,s in subjects.items():
            done,total,pct=obj_progress(sid)
            dl=days_left(date.fromisoformat(s["deadline"]))
            icon="✅" if dl<0 else "⏳"
            label=f"{pct}%"+(f" ({done}/{total})" if total>0 else "")
            st.markdown(
                f"<small><span style='color:{s['color']};font-size:14px'>■</span> "
                f"<b>{s['name'][:18]}</b> <span style='color:#aaa'>{icon}{abs(dl)}g</span></small>",
                unsafe_allow_html=True)
            st.progress(pct/100, text=label)

    st.markdown("---")
    if st.button("🚪 Esci", use_container_width=True):
        st.session_state.auth_user = None
        st.session_state.auth_name = None
        st.session_state.data      = None
        st.rerun()
    st.caption("v4.0 — Studio & Vita")

# ═══ DASHBOARD ══════════════════════════════════════════════
if page=="🏠 Dashboard":
    st.markdown('<p class="gradient-title">🏠 Dashboard</p>',unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Ciao, <b>{st.session_state.auth_name}</b>! Oggi è {fmt_date(date.today())}</p>',
                unsafe_allow_html=True)
    st.markdown("---")
    subjects=get_subjects()
    if not subjects:
        st.info("👋 Vai su **📚 Materie & Esami** per aggiungere le tue materie!"); st.stop()

    today=date.today(); start=get_start(); end=get_end()
    total_d=max(1,(end-start).days+1)
    elaps=max(0,(today-start).days); rem=max(0,(end-today).days)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("📅 Giorni piano",total_d)
    c2.metric("⏳ Trascorsi",elaps)
    c3.metric("🏁 Rimasti",rem)
    c4.metric("📚 Materie",len(subjects))
    st.markdown("---")

    st.markdown("### 📊 Materie")
    cols3=st.columns(min(len(subjects),3))
    for i,(sid,s) in enumerate(subjects.items()):
        done,tot,pct=obj_progress(sid)
        dl=days_left(date.fromisoformat(s["deadline"])); color=s["color"]
        with cols3[i%3]:
            val=round(100/tot,1) if tot>0 else 0
            st.markdown(
                f"<div class='subj-card' style='border-color:{color}'>"
                f"<h4 style='margin:0;color:{color}'>{s['name']}</h4>"
                f"<p style='margin:4px 0;color:#888;font-size:.85rem'>"
                f"📅 {date.fromisoformat(s['deadline']).strftime('%d/%m/%Y')}"
                f" · {'✅ Sostenuto' if dl<0 else f'⏳ {dl}g'}</p></div>",
                unsafe_allow_html=True)
            if tot>0:
                st.progress(pct/100,text=f"{pct}% — {done}/{tot} obiettivi · {val}% cad.")
            else:
                st.progress(0.0,text="Nessun obiettivo ancora")

    st.markdown("---")
    today_str=str(today); dc=get_day(today_str)
    st.markdown("### 📌 Piano di Oggi")
    cs,ca=st.columns(2)
    with cs:
        st.markdown("**📚 Studio**"); found=False
        for sk,slbl,sbg in STUDY_SLOTS:
            slot=dc.get(sk,{}); sid_s=slot.get("subject_id","")
            if sid_s and sid_s in subjects:
                found=True; sc2=subjects[sid_s]["color"]
                objs=get_day_objectives(sid_s,today_str)
                done_c=sum(1 for o in objs if o.get("done"))
                st.markdown(
                    f"<div style='background:{sbg};border-radius:8px;padding:8px 12px;"
                    f"border-left:3px solid {sc2};margin-bottom:6px'>"
                    f"<small>{slbl}</small><br><b style='color:{sc2}'>{subjects[sid_s]['name']}</b>"
                    f"{'<br><small>🎯 '+str(done_c)+'/'+str(len(objs))+' obiettivi</small>' if objs else ''}</div>",
                    unsafe_allow_html=True)
        if not found: st.info("Nessuno studio pianificato.")
    with ca:
        st.markdown("**📋 Impegni**"); apts=dc.get("appointments",[])
        if apts:
            for apt in apts:
                ac=APPOINTMENT_TYPES.get(apt.get("type",""),"#95a5a6"); time=apt.get("time","")
                st.markdown(
                    f"<div class='apt-row' style='border-color:{ac}'>"
                    f"{'<b>'+time+'</b> · ' if time else ''}{apt.get('type','?')}"
                    f"{'<br><small>'+apt['notes']+'</small>' if apt.get('notes') else ''}</div>",
                    unsafe_allow_html=True)
        else: st.info("Nessun impegno oggi.")

    st.markdown("---"); st.markdown("### 🎯 Prossimi Esami")
    upcoming=sorted([(sid,s) for sid,s in subjects.items()
                     if days_left(date.fromisoformat(s["deadline"]))>=0],
                    key=lambda x:x[1]["deadline"])
    for sid,s in upcoming:
        dl=days_left(date.fromisoformat(s["deadline"])); color=s["color"]
        urgency="🔴" if dl<=7 else("🟡" if dl<=14 else "🟢")
        st.markdown(
            f"<div style='background:white;border-radius:10px;padding:10px 16px;"
            f"margin-bottom:6px;box-shadow:0 1px 6px rgba(0,0,0,.06);"
            f"border-left:4px solid {color}'>{urgency} <b style='color:{color}'>{s['name']}</b>"
            f" — 📅 {date.fromisoformat(s['deadline']).strftime('%d/%m/%Y')}"
            f" · <b>{dl} giorni</b></div>",unsafe_allow_html=True)

# ═══ CALENDARIO ═════════════════════════════════════════════
elif page=="📅 Calendario":
    st.markdown('<p class="gradient-title">📅 Calendario</p>',unsafe_allow_html=True)
    subjects=get_subjects(); today=date.today(); start=get_start(); end=get_end()

    n1,n2,n3=st.columns([1,2,1])
    with n1:
        if st.button("◀ Mese precedente",use_container_width=True):
            cm=st.session_state.cal_month
            st.session_state.cal_month=cm.replace(month=cm.month-1) if cm.month>1 \
                                       else cm.replace(year=cm.year-1,month=12)
            st.rerun()
    with n2:
        cm=st.session_state.cal_month
        st.markdown(f"<h3 style='text-align:center;margin:0'>{MONTHS_IT[cm.month]} {cm.year}</h3>",
                    unsafe_allow_html=True)
    with n3:
        if st.button("Mese successivo ▶",use_container_width=True):
            cm=st.session_state.cal_month
            st.session_state.cal_month=cm.replace(month=cm.month+1) if cm.month<12 \
                                       else cm.replace(year=cm.year+1,month=1)
            st.rerun()

    if subjects:
        lg=" &nbsp; ".join(
            f"<span style='background:{s['color']};color:white;padding:3px 10px;"
            f"border-radius:12px;font-size:.78rem'>● {s['name']}</span>"
            for s in subjects.values())
        st.markdown(f"<div style='margin:8px 0'>{lg}</div>",unsafe_allow_html=True)

    st.markdown("---")
    cal_col,panel_col=st.columns([3,2])

    with cal_col:
        cm=st.session_state.cal_month
        hcols=st.columns(7)
        for i,lbl in enumerate(WDAYS_SHORT):
            c="#e74c3c" if i>=5 else "#667eea"
            hcols[i].markdown(
                f"<div style='text-align:center;font-weight:700;color:{c};"
                f"font-size:.82rem;padding-bottom:8px;border-bottom:2px solid {c}22'>{lbl}</div>",
                unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>",unsafe_allow_html=True)

        for week in cal_lib.monthcalendar(cm.year,cm.month):
            wcols=st.columns(7)
            for i,day_num in enumerate(week):
                with wcols[i]:
                    if day_num==0:
                        st.markdown("<div style='min-height:82px'></div>",unsafe_allow_html=True)
                        continue
                    d=date(cm.year,cm.month,day_num); d_str=str(d)
                    in_rng=start<=d<=end; is_tod=d==today
                    is_sel=d_str==st.session_state.selected_date; is_wknd=i>=5

                    dc=get_day(d_str); dots=[]
                    for sk,_,_ in STUDY_SLOTS:
                        sid_s=dc.get(sk,{}).get("subject_id","")
                        if sid_s and sid_s in subjects:
                            objs_d=get_day_objectives(sid_s,d_str)
                            done_c=sum(1 for o in objs_d if o.get("done"))
                            all_done=objs_d and done_c==len(objs_d)
                            dot="✓" if all_done else("●" if objs_d else "·")
                            dots.append(f"<span style='color:{subjects[sid_s]['color']};font-size:9px'>{dot}</span>")
                    apts=dc.get("appointments",[])
                    if apts:
                        ac=APPOINTMENT_TYPES.get(apts[0].get("type",""),"#888")
                        dots.append(f"<span style='color:{ac};font-size:9px'>◆</span>")
                    dots_html="".join(dots)

                    if is_sel:   border,bg="2px solid #667eea","#eef0ff"
                    elif is_tod: border,bg="2px solid #ffc107","#fff8e1"
                    elif in_rng: border,bg="1px solid #d0d0d0","white"
                    else:        border,bg="1px solid #eeeeee","#f8f8f8"

                    if is_tod:
                        num_html=(f"<div style='background:#667eea;color:white;border-radius:50%;"
                                  f"width:26px;height:26px;line-height:26px;font-weight:700;"
                                  f"font-size:.82rem;margin:3px auto 2px;text-align:center'>{day_num}</div>")
                    elif not in_rng:
                        num_html=f"<div style='color:#ccc;text-align:center;font-size:.82rem;padding:3px 0'>{day_num}</div>"
                    else:
                        nc="#e74c3c" if is_wknd else "#333"
                        num_html=f"<div style='color:{nc};font-weight:600;font-size:.85rem;text-align:center;padding:3px 0'>{day_num}</div>"

                    st.markdown(f"<div style='border:{border};background:{bg};border-radius:10px;"
                                f"min-height:82px;padding:2px;overflow:hidden'>{num_html}",
                                unsafe_allow_html=True)
                    if in_rng:
                        btn_lbl="→" if day_has_content(d_str) else "+"
                        if st.button(btn_lbl,key=f"cal_{d_str}",use_container_width=True):
                            st.session_state.selected_date=d_str; st.rerun()
                    if dots_html:
                        st.markdown(f"<div style='text-align:center;line-height:1.4'>{dots_html}</div>",
                                    unsafe_allow_html=True)
                    st.markdown("</div>",unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>",unsafe_allow_html=True)

    with panel_col:
        sel_date=date.fromisoformat(st.session_state.selected_date)
        sel_str=st.session_state.selected_date
        st.markdown(f"<div class='day-card'><h3 style='margin-top:0;color:#667eea'>📋 {fmt_date(sel_date)}</h3>",
                    unsafe_allow_html=True)
        init_day(sel_str)
        pt1,pt2,pt3=st.tabs(["📚 Studio","📋 Impegni","📝 Note"])

        with pt1:
            active=active_subjects_on(sel_date)
            if not active: st.info("Nessuna materia attiva.")
            else:
                subj_map={sid:s["name"] for sid,s in active}
                opts_keys=[""]+list(subj_map.keys())
                opts_lbls={"":"— nessuna —",**subj_map}
                for sk,slbl,sbg in STUDY_SLOTS:
                    slot=sd()["calendar"][sel_str].get(sk,{})
                    cur_sid=slot.get("subject_id","")
                    if cur_sid not in opts_keys: cur_sid=""
                    st.markdown(f"<div class='slot-box' style='background:{sbg}'><b>{slbl}</b></div>",
                                unsafe_allow_html=True)
                    sel_sid=st.selectbox("Materia",options=opts_keys,
                                         format_func=lambda x:opts_lbls.get(x,""),
                                         index=opts_keys.index(cur_sid),
                                         key=f"ss_{sk}_{sel_str}",label_visibility="collapsed")
                    new_slot={"subject_id":sel_sid}
                    if new_slot!={"subject_id":slot.get("subject_id","")}:
                        sd()["calendar"][sel_str][sk]=new_slot; persist()

        with pt2:
            apts=sd()["calendar"][sel_str].get("appointments",[])
            if apts:
                for idx,apt in enumerate(apts):
                    ac=APPOINTMENT_TYPES.get(apt.get("type",""),"#95a5a6"); time=apt.get("time","")
                    with st.expander(f"{apt.get('type','?')}{' · '+time if time else ''}"):
                        nt=st.text_input("Orario",value=time,key=f"at_{sel_str}_{idx}",placeholder="15:30")
                        nd=st.number_input("Durata",15,240,apt.get("duration",60),15,key=f"ad_{sel_str}_{idx}")
                        nn=st.text_area("Note",value=apt.get("notes",""),key=f"an_{sel_str}_{idx}",height=60)
                        sc2,dc2=st.columns(2)
                        with sc2:
                            if st.button("💾",key=f"as_{sel_str}_{idx}"):
                                sd()["calendar"][sel_str]["appointments"][idx].update({"time":nt,"duration":nd,"notes":nn})
                                persist(); st.rerun()
                        with dc2:
                            if st.button("🗑️",key=f"ae_{sel_str}_{idx}"):
                                sd()["calendar"][sel_str]["appointments"].pop(idx)
                                persist(); st.rerun()
            st.markdown("**➕ Aggiungi impegno**")
            new_type=st.selectbox("Tipo",list(APPOINTMENT_TYPES.keys()),key=f"natype_{sel_str}")
            ta,tb=st.columns(2)
            with ta: new_time=st.text_input("Orario",placeholder="10:00",key=f"natime_{sel_str}")
            with tb: new_dur=st.number_input("Durata (min)",15,240,60,15,key=f"nadur_{sel_str}")
            new_note=st.text_input("Note",placeholder="(opzionale)",key=f"nanote_{sel_str}")
            if st.button("➕ Aggiungi",key=f"addapt_{sel_str}",type="primary",use_container_width=True):
                sd()["calendar"][sel_str]["appointments"].append(
                    {"id":str(uuid.uuid4())[:8],"type":new_type,
                     "time":new_time,"duration":new_dur,"notes":new_note})
                persist(); st.rerun()

        with pt3:
            cur_notes=sd()["calendar"][sel_str].get("notes","")
            new_notes=st.text_area("Note",value=cur_notes,height=200,key=f"dnotes_{sel_str}",
                                   placeholder="Note libere...")
            if new_notes!=cur_notes:
                sd()["calendar"][sel_str]["notes"]=new_notes; persist()
        st.markdown("</div>",unsafe_allow_html=True)

# ═══ MATERIE & ESAMI ════════════════════════════════════════
elif page=="📚 Materie & Esami":
    st.markdown('<p class="gradient-title">📚 Materie & Esami</p>',unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Gestisci le tue materie e le date degli esami</p>',
                unsafe_allow_html=True)
    st.markdown("---")
    subjects=get_subjects()

    with st.expander("⚙️ Periodo di Studio",expanded=not bool(subjects)):
        s=get_settings(); c1,c2=st.columns(2)
        with c1: sd_in=st.date_input("📅 Inizio",date.fromisoformat(s.get("start_date",str(date.today()))),key="cfg_s")
        with c2: ed_in=st.date_input("🏁 Fine",date.fromisoformat(s.get("end_date",str(date.today()+timedelta(days=60)))),key="cfg_e")
        if st.button("💾 Salva"):
            sd()["settings"].update({"start_date":str(sd_in),"end_date":str(ed_in)})
            persist(); st.success("✅ Salvate!")

    st.markdown("---"); st.markdown("### ➕ Aggiungi Materia")
    with st.form("add_subj",clear_on_submit=True):
        fa,fb,fc=st.columns([3,2,1])
        with fa: nm=st.text_input("📖 Nome",placeholder="es. Analisi I")
        with fb: dl_d=st.date_input("📅 Data esame",value=date.today()+timedelta(days=30))
        with fc: nc=st.color_picker("🎨",value=next_color())
        if st.form_submit_button("➕ Aggiungi",type="primary",use_container_width=True):
            if nm.strip():
                nid=str(uuid.uuid4())[:8]
                if "subjects" not in sd(): sd()["subjects"]={}
                sd()["subjects"][nid]={"name":nm.strip(),"deadline":str(dl_d),
                                        "color":nc,"days":{}}
                persist(); st.success(f"✅ '{nm}' aggiunta!"); st.rerun()
            else: st.warning("Inserisci un nome.")

    st.markdown("---")
    if subjects:
        st.markdown("### 📚 Le tue Materie")
        for sid,s in list(subjects.items()):
            done,tot,pct=obj_progress(sid)
            deadline=date.fromisoformat(s["deadline"]); dl=days_left(deadline); color=s["color"]
            with st.expander(f"{'✅' if dl<0 else '⏳'} {s['name']} — {deadline.strftime('%d/%m/%Y')} · {pct}%"):
                e1,e2,e3=st.columns([3,2,1])
                with e1: new_nm=st.text_input("Nome",value=s["name"],key=f"en_{sid}")
                with e2: new_dl=st.date_input("Esame",value=deadline,key=f"ed_{sid}")
                with e3: new_c=st.color_picker("",value=color,key=f"ec_{sid}")
                val=round(100/tot,1) if tot>0 else 0
                if tot>0:
                    st.progress(pct/100,text=f"🎯 {pct}% — {done}/{tot} obiettivi · {val}% cad.")
                else:
                    st.info("Aggiungi obiettivi dal Calendario della materia.")
                sv,dv=st.columns([3,1])
                with sv:
                    if st.button("💾 Salva",key=f"esave_{sid}",type="primary"):
                        sd()["subjects"][sid].update({"name":new_nm,"deadline":str(new_dl),"color":new_c})
                        persist(); st.success("✅"); st.rerun()
                with dv:
                    if st.button("🗑️",key=f"edel_{sid}"):
                        del sd()["subjects"][sid]; persist(); st.rerun()
    else:
        st.info("Nessuna materia. Aggiungila qui sopra!")

# ═══ PAGINA SINGOLA MATERIA ═════════════════════════════════
else:
    subjects=get_subjects()
    target_name=page.replace("📖 ","")
    target_sid=next((sid for sid,s in subjects.items() if s["name"]==target_name),None)
    if not target_sid: st.error("Materia non trovata."); st.stop()

    subj=subjects[target_sid]; color=subj["color"]
    deadline=date.fromisoformat(subj["deadline"]); dl=days_left(deadline)

    if "days" not in sd()["subjects"][target_sid]:
        sd()["subjects"][target_sid]["days"]={}

    done_o,tot_o,pct_o=obj_progress(target_sid)
    val_each=round(100/tot_o,1) if tot_o else 0

    st.markdown(f'<p class="gradient-title">📖 {subj["name"]}</p>',unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitle">Esame: <b>{fmt_date(deadline)}</b> · '
        f'{"✅ Sostenuto" if dl<0 else f"⏳ {dl} giorni"}</p>',
        unsafe_allow_html=True)

    st.markdown(
        f"<div style='background:#e0e0e0;border-radius:20px;height:34px;margin-bottom:4px'>"
        f"<div style='background:{color};width:{pct_o}%;height:34px;border-radius:20px;"
        f"display:flex;align-items:center;justify-content:center;"
        f"color:white;font-weight:700;font-size:1.05rem'>{pct_o}%</div></div>",
        unsafe_allow_html=True)
    if tot_o>0:
        st.caption(f"🎯 {done_o}/{tot_o} obiettivi completati · ogni obiettivo vale **{val_each}%**")
    else:
        st.caption("ℹ️ Aggiungi obiettivi nei giorni — la barra si aggiorna da sola.")
    st.markdown("---")

    tab1,tab2,tab3=st.tabs(["📅 Calendario","📋 Riepilogo","📁 Materiale"])

    with tab1:
        st.markdown("### 📅 Calendario — Obiettivi Giornalieri")
        st.caption("Scrivi gli obiettivi per ogni giorno e spuntali man mano che li completi.")

        days_list=subject_dates(target_sid); today=date.today()
        weeks:dict={}
        for d in days_list:
            wl=f"Settimana {d.isocalendar()[1]} — {MONTHS_IT[d.month]}"; weeks.setdefault(wl,[]).append(d)

        for wl,wdays in weeks.items():
            is_curr=any(d==today for d in wdays)
            wk_done=0; wk_tot=0
            for d in wdays:
                objs=get_day_objectives(target_sid,str(d))
                wk_done+=sum(1 for o in objs if o.get("done")); wk_tot+=len(objs)
            label=f"{'📍' if is_curr else '📅'} {wl}"
            if wk_tot>0: label+=f"  [{wk_done}/{wk_tot}]"

            with st.expander(label,expanded=is_curr):
                for d in wdays:
                    ds=str(d)
                    objs=get_day_objectives(target_sid,ds)
                    done_c=sum(1 for o in objs if o.get("done"))
                    itod=d==today; ipas=d<today

                    if itod:                          bg2,bd2="#fff8e1",f"2px solid {color}"
                    elif objs and done_c==len(objs):  bg2,bd2="#e8f5e9","1px solid #a5d6a7"
                    elif ipas and done_c<len(objs):   bg2,bd2="#fce4ec","1px solid #ef9a9a"
                    else:                             bg2,bd2="#f8f8f8","1px solid #e0e0e0"

                    day_label=f"{WDAYS_SHORT[d.weekday()]} {d.day}/{d.month}"
                    if itod: day_label+=" ← OGGI"
                    obj_badge=f" · 🎯 {done_c}/{len(objs)}" if objs else ""

                    st.markdown(
                        f"<div style='background:{bg2};border:{bd2};border-radius:8px;"
                        f"padding:5px 12px;margin-bottom:6px;margin-top:8px'>"
                        f"<b>{day_label}</b><span style='color:#888;font-size:.85rem'>{obj_badge}</span></div>",
                        unsafe_allow_html=True)

                    for o in objs:
                        oc1,oc2,oc3=st.columns([1,8,1])
                        with oc1:
                            new_done=st.checkbox("",value=o.get("done",False),
                                                 key=f"ck_{target_sid}_{ds}_{o['id']}",
                                                 label_visibility="collapsed")
                            if new_done!=o.get("done",False):
                                toggle_day_objective(target_sid,ds,o["id"],new_done); st.rerun()
                        with oc2:
                            sty=("text-decoration:line-through;color:#aaa"
                                 if o.get("done") else f"color:{color};font-weight:500")
                            st.markdown(f"<span style='{sty}'>{o['text']}</span>",unsafe_allow_html=True)
                        with oc3:
                            if st.button("✕",key=f"del_{target_sid}_{ds}_{o['id']}"):
                                delete_day_objective(target_sid,ds,o["id"]); st.rerun()

                    add_col,btn_col=st.columns([6,1])
                    with add_col:
                        new_obj_text=st.text_input("",key=f"new_{target_sid}_{ds}",
                            placeholder=f"+ Aggiungi obiettivo {d.strftime('%d/%m')}...",
                            label_visibility="collapsed")
                    with btn_col:
                        if st.button("＋",key=f"add_{target_sid}_{ds}"):
                            if new_obj_text.strip():
                                add_day_objective(target_sid,ds,new_obj_text); st.rerun()

    with tab2:
        st.markdown("### 📋 Riepilogo")
        m1,m2,m3=st.columns(3)
        m1.metric("🎯 Totale",  tot_o)
        m2.metric("✅ Completati",done_o)
        m3.metric("⬜ Rimanenti",tot_o-done_o)
        if tot_o>0:
            st.progress(pct_o/100,text=f"{pct_o}% · ogni obiettivo vale {val_each}%")
            st.markdown("---")
            rows=[]
            for d in subject_dates(target_sid):
                for o in get_day_objectives(target_sid,str(d)):
                    rows.append({
                        "📅 Giorno":f"{WDAYS_SHORT[d.weekday()]} {d.strftime('%d/%m')}",
                        "🎯 Obiettivo":o["text"],
                        "Stato":"✅" if o.get("done") else "⬜"})
            filt=st.radio("",["📋 Tutti","✅ Completati","⬜ Da fare"],horizontal=True)
            show={"📋 Tutti":rows,
                  "✅ Completati":[r for r in rows if "✅" in r["Stato"]],
                  "⬜ Da fare":  [r for r in rows if "⬜" in r["Stato"]]}[filt]
            if show: st.dataframe(show,use_container_width=True,hide_index=True)
            else:    st.info("Nessun obiettivo in questa categoria.")
        else:
            st.info("Aggiungi obiettivi dal tab **📅 Calendario**!")

    with tab3:
        st.markdown("### 📁 Materiale Didattico")
        updir=UPLOAD_BASE/target_sid; updir.mkdir(exist_ok=True)
        ups=st.file_uploader("📤 Carica file",accept_multiple_files=True,key=f"up_{target_sid}")
        if ups:
            for uf in ups:
                with open(updir/uf.name,"wb") as f: f.write(uf.getbuffer())
            st.success(f"✅ {len(ups)} file caricati!"); st.rerun()

        existing=sorted(updir.iterdir()) if updir.exists() else []
        if existing:
            st.markdown(f"#### 📂 File ({len(existing)})")
            srch=st.text_input("🔍 Cerca",key=f"sr_{target_sid}",placeholder="Nome file...")
            EI={".pdf":"📕",".docx":"📘",".pptx":"📙",".xlsx":"📗",
                ".jpg":"🖼️",".jpeg":"🖼️",".png":"🖼️",".zip":"🗜️",".txt":"📄"}
            for fp in [f for f in existing if srch.lower() in f.name.lower()]:
                icon=EI.get(fp.suffix.lower(),"📄")
                sz=fp.stat().st_size
                szs=f"{sz//1024} KB" if sz<1024*1024 else f"{sz//1024//1024} MB"
                fc1,fc2,fc3=st.columns([5,1,1])
                with fc1: st.markdown(f"{icon} **{fp.name}** `{szs}`")
                with fc2:
                    with open(fp,"rb") as f:
                        st.download_button("⬇️",data=f.read(),file_name=fp.name,
                                           key=f"dl_{target_sid}_{fp.name}")
                with fc3:
                    if st.button("🗑️",key=f"rm_{target_sid}_{fp.name}"):
                        fp.unlink(); st.rerun()
                st.divider()
        else:
            st.info("Nessun file ancora.")
