# app.py
# Streamlit app: Chrono + Pression (Salle de coronarographie)
# Copy-paste direct dans streamlit.app

import time
import json
from datetime import datetime
from pathlib import Path

import streamlit as st

# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="Chrono Pression | Cathlab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path("cathlab_chrono_pression.json")

ARTERES = [
    "IVA (LAD)",
    "ACx (LCx)",
    "CD (RCA)",
    "TC (LM)",
    "DIAG (D)",
    "Marginale (OM)",
    "Autre",
]

# -----------------------------
# Helpers
# -----------------------------
def load_persisted():
    if DATA_FILE.exists():
        try:
            payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return payload.get("devices", []), payload.get("events", [])
        except Exception:
            return [], []
    return [], []


def save_persisted(devices, events):
    try:
        DATA_FILE.write_text(
            json.dumps({"devices": devices, "events": events}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        # Sur streamlit.app, le FS peut être éphémère. On garde au moins la session.
        pass


def device_label(d):
    # d: dict with type, diameter, length
    return f"{d['type']} {d['diameter']} × {d['length']} mm"


def now_str():
    return datetime.now().strftime("%H:%M:%S")


def dt_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def big_time(seconds: float) -> str:
    return f"{seconds:0.2f}"


def ensure_state():
    if "devices" not in st.session_state or "events" not in st.session_state:
        devices, events = load_persisted()
        st.session_state.devices = devices
        st.session_state.events = events

    st.session_state.setdefault("phase", "setup")  # setup | run | pressure
    st.session_state.setdefault("running", False)
    st.session_state.setdefault("t0", None)
    st.session_state.setdefault("elapsed", 0.0)
    st.session_state.setdefault("start_clock", None)

    st.session_state.setdefault("selected_artery", ARTERES[0])
    st.session_state.setdefault("selected_device_idx", None)
    st.session_state.setdefault("custom_artery", "")

    st.session_state.setdefault("pending_elapsed", None)
    st.session_state.setdefault("pending_start_clock", None)
    st.session_state.setdefault("pending_device", None)
    st.session_state.setdefault("pending_artery", None)

    st.session_state.setdefault("refresh_key", 0)


def add_device_if_new(device_dict):
    # device_dict keys: type, diameter, length
    label = device_label(device_dict)
    existing_labels = [device_label(d) for d in st.session_state.devices]
    if label not in existing_labels:
        st.session_state.devices.append(device_dict)
        save_persisted(st.session_state.devices, st.session_state.events)
    # return index
    existing_labels = [device_label(d) for d in st.session_state.devices]
    return existing_labels.index(label)


def add_event(event_dict):
    # event_dict keys: datetime, start_clock, duration_s, pressure_atm, artery, device_label
    st.session_state.events.insert(0, event_dict)
    save_persisted(st.session_state.devices, st.session_state.events)


def soft_rerun():
    # On évite les loops agressifs: petit incrément puis rerun
    st.session_state.refresh_key += 1
    st.rerun()


ensure_state()

# -----------------------------
# CSS (ultra modern, grandes zones tactiles)
# -----------------------------
st.markdown(
    """
<style>
:root{
  --bg: #0b0f17;
  --card: rgba(255,255,255,0.06);
  --card2: rgba(255,255,255,0.08);
  --stroke: rgba(255,255,255,0.12);
  --txt: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.62);
  --accent: #7c5cff;
  --good: #27d3a2;
  --bad: #ff4d6d;
}

html, body, [class*="css"]  {
  background: radial-gradient(1200px 600px at 20% 0%, rgba(124,92,255,0.22), transparent 50%),
              radial-gradient(1000px 600px at 90% 10%, rgba(39,211,162,0.16), transparent 55%),
              var(--bg) !important;
  color: var(--txt) !important;
}

.block-container {
  padding-top: 1.1rem;
  padding-bottom: 2rem;
  max-width: 1200px;
}

.card {
  background: var(--card);
  border: 1px solid var(--stroke);
  border-radius: 22px;
  padding: 18px 18px;
  box-shadow: 0 14px 40px rgba(0,0,0,0.25);
}

.card2 {
  background: var(--card2);
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 14px 14px;
}

.title {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: 0.2px;
  margin: 0 0 6px 0;
}

.subtitle {
  font-size: 16px;
  color: var(--muted);
  margin: 0;
}

.timer {
  font-size: 90px;
  font-weight: 900;
  letter-spacing: 1px;
  line-height: 1;
  text-align: center;
  margin: 8px 0 0 0;
}

.micro {
  font-size: 13px;
  color: var(--muted);
}

.pill {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,0.05);
  color: var(--muted);
  font-size: 13px;
}

.bigbutton button {
  width: 100% !important;
  height: 110px !important;
  border-radius: 22px !important;
  border: 1px solid var(--stroke) !important;
  font-size: 34px !important;
  font-weight: 900 !important;
}

.primary button {
  background: linear-gradient(135deg, rgba(124,92,255,1), rgba(39,211,162,0.85)) !important;
  color: #0b0f17 !important;
}

.stop button {
  background: linear-gradient(135deg, rgba(255,77,109,1), rgba(124,92,255,0.95)) !important;
  color: #0b0f17 !important;
}

.smallbutton button {
  height: 52px !important;
  border-radius: 16px !important;
  font-size: 18px !important;
  font-weight: 800 !important;
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
  font-size: 18px !important;
  font-weight: 800 !important;
}

.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
  border-radius: 16px !important;
  border: 1px solid var(--stroke) !important;
  background: rgba(255,255,255,0.05) !important;
  color: var(--txt) !important;
  min-height: 54px !important;
  font-size: 18px !important;
}

hr {
  border-color: rgba(255,255,255,0.08) !important;
}

table {
  border-collapse: separate !important;
  border-spacing: 0 !important;
}

thead tr th {
  background: rgba(255,255,255,0.06) !important;
  border-bottom: 1px solid rgba(255,255,255,0.10) !important;
  font-size: 14px !important;
}

tbody tr td {
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  font-size: 16px !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
left, right = st.columns([3, 1], vertical_alignment="center")
with left:
    st.markdown('<div class="title">Chrono Pression</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Chronomètre (2 décimales) + saisie de pression + historique (optimisé tablette)</p>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f'<div style="text-align:right"><span class="pill">Heure système</span><br><span style="font-size:28px;font-weight:900">{now_str()}</span></div>',
        unsafe_allow_html=True,
    )

st.write("")

# -----------------------------
# Layout principal
# -----------------------------
colA, colB = st.columns([1.1, 0.9], gap="large")

# ============
# Colonne A : Setup + Timer
# ============
with colA:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    setup_col, info_col = st.columns([1.2, 0.8], vertical_alignment="top")

    # --- Setup (artère + dispositif)
    with setup_col:
        st.markdown('<div class="card2">', unsafe_allow_html=True)
        st.markdown('<div class="title" style="font-size:20px;margin-bottom:6px;">Préparation</div>', unsafe_allow_html=True)

        # Artère
        artery = st.selectbox("Artère traitée", ARTERES, index=ARTERES.index(st.session_state.selected_artery) if st.session_state.selected_artery in ARTERES else 0)
        st.session_state.selected_artery = artery
        if artery == "Autre":
            st.session_state.custom_artery = st.text_input("Préciser", value=st.session_state.custom_artery, placeholder="Ex: pontage, Graft, etc.")
        effective_artery = st.session_state.custom_artery.strip() if artery == "Autre" and st.session_state.custom_artery.strip() else artery

        st.write("")

        # Choix dispositif existant
        device_labels = [device_label(d) for d in st.session_state.devices]
        use_existing = st.toggle("Réutiliser un dispositif déjà saisi", value=(len(device_labels) > 0))
        selected_existing = None
        if use_existing and device_labels:
            selected_existing = st.selectbox("Dispositif", device_labels, index=0)
        elif use_existing and not device_labels:
            st.info("Aucun dispositif enregistré pour l’instant. Ajoutez-en un ci-dessous.")

        st.write("")

        # Ajout nouveau dispositif
        st.markdown('<div class="micro" style="margin-bottom:6px;">Nouveau dispositif</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            dtype = st.selectbox("Type", ["Ballon", "Stent"], index=0)
        with c2:
            diameter = st.number_input("Diamètre (mm)", min_value=1.0, max_value=10.0, value=3.0, step=0.25, format="%.2f")
        with c3:
            length = st.number_input("Longueur (mm)", min_value=5, max_value=60, value=15, step=1)

        add_now = st.button("Ajouter / Mémoriser", use_container_width=True)

        if add_now:
            new_dev = {"type": dtype, "diameter": f"{diameter:.2f}", "length": str(int(length))}
            add_device_if_new(new_dev)
            st.success("Dispositif mémorisé.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Déterminer dispositif actif
        active_device = None
        if use_existing and selected_existing:
            # retrouver dict
            idx = device_labels.index(selected_existing)
            active_device = st.session_state.devices[idx]
        else:
            # device du formulaire courant (même si pas encore mémorisé)
            active_device = {"type": dtype, "diameter": f"{diameter:.2f}", "length": str(int(length))}

    # --- Info à droite
    with info_col:
        st.markdown('<div class="card2">', unsafe_allow_html=True)
        st.markdown('<div class="title" style="font-size:20px;margin-bottom:6px;">Contexte</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="pill">Artère</div><div style="font-size:22px;font-weight:900;margin-top:6px">{effective_artery}</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="pill">Dispositif</div><div style="font-size:22px;font-weight:900;margin-top:6px">{device_label(active_device)}</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="micro">Astuce: gros boutons, champs larges (OK pour tablette sous champ stérile).</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Timer
    timer_box = st.container()
    with timer_box:
        if st.session_state.running and st.session_state.t0 is not None:
            st.session_state.elapsed = time.perf_counter() - st.session_state.t0

        st.markdown(
            f'<div class="timer">{big_time(st.session_state.elapsed)}</div>',
            unsafe_allow_html=True,
        )
        small_l, small_r = st.columns([1, 1])
        with small_l:
            sc = st.session_state.start_clock if st.session_state.start_clock else "—"
            st.markdown(f'<div class="micro">Heure début inflation: <b>{sc}</b></div>', unsafe_allow_html=True)
        with small_r:
            st.markdown(f'<div class="micro" style="text-align:right;">Précision: <b>0,01 s</b></div>', unsafe_allow_html=True)

        st.write("")

        # Bouton Start/Stop
        if not st.session_state.running:
            st.markdown('<div class="bigbutton primary">', unsafe_allow_html=True)
            start = st.button("DÉMARRER", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if start:
                # Mémoriser dispositif si pas déjà (optionnel, mais utile pour réutilisation)
                add_device_if_new(active_device)

                st.session_state.running = True
                st.session_state.t0 = time.perf_counter()
                st.session_state.elapsed = 0.0
                st.session_state.start_clock = now_str()
                st.session_state.phase = "run"
                soft_rerun()
        else:
            st.markdown('<div class="bigbutton stop">', unsafe_allow_html=True)
            stop = st.button("STOP", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if stop:
                # figer temps
                final_elapsed = time.perf_counter() - st.session_state.t0
                st.session_state.running = False
                st.session_state.t0 = None
                st.session_state.elapsed = final_elapsed

                # préparer saisie pression
                st.session_state.pending_elapsed = final_elapsed
                st.session_state.pending_start_clock = st.session_state.start_clock
                st.session_state.pending_device = device_label(active_device)
                st.session_state.pending_artery = effective_artery
                st.session_state.phase = "pressure"
                soft_rerun()

        # Rafraîchissement pendant le run
        if st.session_state.running:
            # rafraîchit ~20 fois/sec
            time.sleep(0.05)
            soft_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============
# Colonne B : Saisie pression + Historique
# ============
with colB:
    # --- Saisie pression après STOP
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title" style="font-size:20px;">Saisie pression</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Après STOP, renseigner la pression et valider.</p>', unsafe_allow_html=True)
    st.write("")

    if st.session_state.phase == "pressure" and st.session_state.pending_elapsed is not None:
        st.markdown('<div class="card2">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="micro">Dispositif: <b>{st.session_state.pending_device}</b></div>
            <div class="micro">Artère: <b>{st.session_state.pending_artery}</b></div>
            <div class="micro">Heure début: <b>{st.session_state.pending_start_clock}</b></div>
            <div class="micro">Durée inflation: <b>{big_time(st.session_state.pending_elapsed)} s</b></div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        with st.form("pressure_form", clear_on_submit=True):
            pressure = st.number_input("Pression (atm)", min_value=0.0, max_value=40.0, value=12.0, step=0.5, format="%.1f")
            c_ok, c_cancel = st.columns([1, 1])
            with c_ok:
                ok = st.form_submit_button("OK", use_container_width=True)
            with c_cancel:
                cancel = st.form_submit_button("Annuler", use_container_width=True)

            if ok:
                add_event(
                    {
                        "datetime": dt_str(),
                        "start_clock": st.session_state.pending_start_clock,
                        "duration_s": round(float(st.session_state.pending_elapsed), 2),
                        "pressure_atm": round(float(pressure), 1),
                        "artery": st.session_state.pending_artery,
                        "device": st.session_state.pending_device,
                    }
                )

                # reset pending
                st.session_state.pending_elapsed = None
                st.session_state.pending_start_clock = None
                st.session_state.pending_device = None
                st.session_state.pending_artery = None
                st.session_state.phase = "setup"
                st.success("Enregistré.")
                soft_rerun()

            if cancel:
                st.session_state.pending_elapsed = None
                st.session_state.pending_start_clock = None
                st.session_state.pending_device = None
                st.session_state.pending_artery = None
                st.session_state.phase = "setup"
                soft_rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucune saisie en attente. Démarrez puis stoppez pour enregistrer une pression.")

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Historique
    st.markdown('<div class="title" style="font-size:20px;">Historique</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Derniers enregistrements (heure, durée, pression, artère, dispositif).</p>', unsafe_allow_html=True)
    st.write("")

    if st.session_state.events:
        # Table simple
        rows = []
        for e in st.session_state.events[:60]:
            rows.append(
                {
                    "Date/Heure": e.get("datetime", ""),
                    "Début": e.get("start_clock", ""),
                    "Durée (s)": e.get("duration_s", ""),
                    "Pression (atm)": e.get("pressure_atm", ""),
                    "Artère": e.get("artery", ""),
                    "Dispositif": e.get("device", ""),
                }
            )
        st.dataframe(rows, use_container_width=True, height=420)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.markdown('<div class="smallbutton">', unsafe_allow_html=True)
            if st.button("Effacer l’historique", use_container_width=True):
                st.session_state.events = []
                save_persisted(st.session_state.devices, st.session_state.events)
                soft_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            export = json.dumps({"devices": st.session_state.devices, "events": st.session_state.events}, ensure_ascii=False, indent=2)
            st.download_button(
                "Exporter JSON",
                data=export.encode("utf-8"),
                file_name="cathlab_chrono_pression_export.json",
                mime="application/json",
                use_container_width=True,
            )

        with c3:
            up = st.file_uploader("Importer JSON", type=["json"], label_visibility="collapsed")
            if up is not None:
                try:
                    payload = json.loads(up.read().decode("utf-8"))
                    st.session_state.devices = payload.get("devices", [])
                    st.session_state.events = payload.get("events", [])
                    save_persisted(st.session_state.devices, st.session_state.events)
                    st.success("Import OK.")
                    soft_rerun()
                except Exception:
                    st.error("Fichier JSON invalide.")

    else:
        st.warning("Historique vide pour le moment.")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Footer utilitaire
# -----------------------------
st.write("")
st.markdown(
    '<div class="micro">Sécurité: cette app ne remplace pas la traçabilité officielle. Utilisez-la comme aide rapide au champ stérile.</div>',
    unsafe_allow_html=True,
        )
