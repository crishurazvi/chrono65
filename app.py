import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Timer Coronarographie + Pression",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# (opțional) ascunde UI Streamlit ca să arate “app-like”
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      .block-container {padding-top: 0.8rem; padding-bottom: 0.8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Timer Coronarographie + Pression</title>
  <style>
    :root{
      --bg0:#070A12;
      --bg1:#0B1020;
      --panel: rgba(255,255,255,0.06);
      --stroke: rgba(255,255,255,0.10);
      --text:#EAF0FF;
      --muted: rgba(234,240,255,0.70);
      --danger:#FF4D6D;

      --radius: 22px;
      --shadow: 0 18px 60px rgba(0,0,0,0.55);
      --shadow2: 0 10px 30px rgba(0,0,0,0.35);

      --tap2: 60px;
      --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
    }

    *{ box-sizing:border-box; }
    html,body{ height:100%; }

    /* Mise en page robuste: scroll interne (Historique), pas de scroll global */
    body{
      margin:0;
      font-family: var(--font);
      color: var(--text);
      background:
        radial-gradient(1100px 700px at 20% 10%, rgba(124,92,255,0.22), transparent 60%),
        radial-gradient(900px 650px at 85% 20%, rgba(45,226,230,0.18), transparent 55%),
        radial-gradient(900px 650px at 50% 95%, rgba(255,77,109,0.10), transparent 55%),
        linear-gradient(160deg, var(--bg0), var(--bg1));
      display:flex;
      align-items:stretch;
      justify-content:center;

      height: auto;
      overflow: auto;
    }

    .wrap{
      width:min(1100px, 100%);
      padding:18px;
      display:flex;
      gap:14px;

      height: 100%;
      min-height: 0;
      overflow: auto;
    }

    .col{
      flex:1;
      display:flex;
      flex-direction:column;
      gap:14px;
      min-width: 0;
      min-height: 0;
    }

    .card{
      background: var(--panel);
      border: 1px solid var(--stroke);
      border-radius: var(--radius);
      box-shadow: var(--shadow2);
      overflow:auto;
      min-height: 0;
    }

    .cardHeader{
      padding:16px 18px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      background: linear-gradient(180deg, rgba(255,255,255,0.06), transparent);
    }

    .title{
      font-weight: 820;
      letter-spacing: 0.2px;
      font-size: 18px;
      line-height:1.2;
    }

    .sub{
      font-size: 13px;
      color: var(--muted);
      margin-top:3px;
    }

    .clockChip{
      font-variant-numeric: tabular-nums;
      padding:12px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.10);
      color: rgba(234,240,255,0.92);
      font-size: 13px;
      min-width: 190px;
      text-align:center;
      user-select:none;
    }

    .cardBody{
      padding:16px 18px;
      min-height:0;
    }

    .grid2{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap:12px;
    }

    label{
      display:block;
      font-size: 13px;
      color: var(--muted);
      margin: 0 0 7px 2px;
      user-select:none;
    }

    .input, select{
      width:100%;
      height: var(--tap2);
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.06);
      color: var(--text);
      padding: 0 14px;
      font-size: 17px;
      outline: none;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
      -webkit-tap-highlight-color: transparent;
    }
    select{
      appearance:none;
      background-image:
        linear-gradient(45deg, transparent 50%, rgba(234,240,255,0.7) 50%),
        linear-gradient(135deg, rgba(234,240,255,0.7) 50%, transparent 50%);
      background-position: calc(100% - 22px) calc(50% - 3px), calc(100% - 16px) calc(50% - 3px);
      background-size: 6px 6px, 6px 6px;
      background-repeat: no-repeat;
      padding-right: 40px;
    }
    .input:focus, select:focus{
      border-color: rgba(124,92,255,0.55);
      box-shadow: 0 0 0 4px rgba(124,92,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .row{
      display:flex;
      gap:12px;
      align-items:center;
      flex-wrap:wrap;
    }

    .btn{
      height: var(--tap2);
      border-radius: 16px;
      padding: 0 16px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.08);
      color: var(--text);
      font-weight: 780;
      font-size: 16px;
      letter-spacing: 0.15px;
      cursor:pointer;
      user-select:none;
      -webkit-tap-highlight-color: transparent;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      transition: transform .08s ease, background .15s ease, border-color .15s ease, box-shadow .15s ease;
      touch-action: manipulation;
    }
    .btn:active{ transform: scale(0.99); }
    .btnPrimary{
      border-color: rgba(124,92,255,0.38);
      background: linear-gradient(135deg, rgba(124,92,255,0.95), rgba(45,226,230,0.75));
      box-shadow: 0 18px 50px rgba(124,92,255,0.22);
    }
    .btnDanger{
      border-color: rgba(255,77,109,0.45);
      background: linear-gradient(135deg, rgba(255,77,109,0.95), rgba(124,92,255,0.65));
      box-shadow: 0 18px 50px rgba(255,77,109,0.16);
    }
    .btnGhost{
      background: rgba(255,255,255,0.06);
      border-color: rgba(255,255,255,0.12);
      box-shadow:none;
    }

    .pill{
      padding:12px 14px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.05);
      color: rgba(234,240,255,0.90);
      font-size: 13px;
      user-select:none;
    }

    .timerWrap{
      display:flex;
      flex-direction:column;
      gap:14px;
      align-items:stretch;
      min-height:0;
    }

    .timerDisplay{
      border-radius: var(--radius);
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.10);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
      padding: 18px;
      display:flex;
      align-items:center;
      justify-content:center;
      min-height: 170px;
    }

    .time{
      font-variant-numeric: tabular-nums;
      font-weight: 900;
      font-size: clamp(62px, 6.4vw, 92px);
      letter-spacing: 0.5px;
      line-height:1;
      text-shadow: 0 16px 50px rgba(0,0,0,0.45);
    }

    .bigButton{
      height: 98px;
      border-radius: 24px;
      font-size: 22px;
      font-weight: 900;
      letter-spacing: 0.4px;
    }

    .hint{
      font-size: 13px;
      color: var(--muted);
      text-align:center;
      padding: 0 10px;
      user-select:none;
    }

    .list{
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    .item{
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.05);
      padding: 12px 12px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
    }
    .itemLeft{ min-width:0; }
    .itemTitle{
      font-weight: 850;
      font-size: 15px;
      white-space:nowrap;
      overflow:auto;
      text-overflow:ellipsis;
    }
    .itemMeta{
      margin-top:6px;
      font-size: 13px;
      color: var(--muted);
      display:flex;
      gap:10px;
      flex-wrap:wrap;
    }
    .tag{
      padding: 7px 11px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.04);
      font-size: 13px;
      color: rgba(234,240,255,0.90);
      font-variant-numeric: tabular-nums;
      user-select:none;
    }

    .divider{
      height: 1px;
      background: rgba(255,255,255,0.08);
      margin: 12px 0;
    }

    .stateBanner{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding: 12px 12px;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.05);
      user-select:none;
    }

    .badge{
      padding: 9px 11px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 850;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.05);
      font-variant-numeric: tabular-nums;
    }
    .badgeReady{ border-color: rgba(45,226,230,0.35); background: rgba(45,226,230,0.10); }
    .badgeRun{ border-color: rgba(45,226,230,0.35); background: rgba(45,226,230,0.10); }
    .badgeIdle{ border-color: rgba(255,77,109,0.35); background: rgba(255,77,109,0.10); }

    .mutedSmall{ font-size:13px; color: var(--muted); }

    /* scroll interne */
    .scrollY{
      overflow: auto;
      min-height: 0;
    }
    .scrollY::-webkit-scrollbar{ width: 10px; }
    .scrollY::-webkit-scrollbar-thumb{
      background: rgba(255,255,255,0.18);
      border-radius: 999px;
      border: 2px solid rgba(0,0,0,0.15);
    }

    .cardGrow{
      flex: 1;
      min-height: 0;
      display:flex;
      flex-direction:column;
      overflow: auto;
    }
    .cardGrow .cardBody{
      flex: 1;
      min-height: 0;
      display:flex;
      flex-direction:column;
    }
    .historyScroll{
      flex: 1;
      min-height: 0;
    }

    /* Modal */
    .modal{
      position:fixed;
      inset:0;
      background: rgba(0,0,0,0.55);
      display:none;
      align-items:center;
      justify-content:center;
      padding:18px;
      z-index: 50;
    }
    .modal.show{ display:flex; }
    .modalPanel{
      width:min(540px, 100%);
      background: rgba(15,18,35,0.88);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 24px;
      box-shadow: var(--shadow);
      overflow:auto;
      backdrop-filter: blur(10px);
    }
    .modalBody{ padding:16px 18px 18px; }
    .modalTitle{
      font-size: 18px;
      font-weight: 900;
    }
    .modalSubtitle{
      margin-top:7px;
      font-size: 13px;
      color: var(--muted);
      line-height:1.4;
    }
    .modalActions{
      display:flex;
      gap:12px;
      margin-top:14px;
    }
    .modalActions .btn{ flex:1; }

    @media (max-width: 980px){
      .wrap{ flex-direction:column; }
      body{ overflow:auto; }
      .wrap{ height:auto; overflow: auto;}
      .cardGrow{ flex: unset; }
      .historyScroll{ max-height: 360px; }
    }
    /* ===== MOBILE FIX: 1 col + texte care se văd complet ===== */
@media (max-width: 720px){
  .wrap{
    flex-direction: column;
    height: auto;
    overflow: auto;
  }

  body{
    overflow: auto; /* permite scroll normal pe mobil */
  }

  .cardHeader{
    flex-direction: column;     /* titlu + chip pe rânduri */
    align-items: flex-start;
    gap: 10px;
  }

  .clockChip{
    width: 100%;
    min-width: 0;              /* important: nu mai forțează lățime mare */
    text-align: left;
    white-space: normal;       /* să se rupă pe linii dacă e nevoie */
  }

  .title{
    font-size: 20px;           /* opțional: mai lizibil */
    line-height: 1.15;
  }

  .sub{
    font-size: 14px;
    line-height: 1.25;
    max-width: 100%;
    white-space: normal;
  }

  /* în bannerul cu dispozitiv: lasă textul să se rupă */
  .stateBanner{
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .itemTitle{
    white-space: normal;       /* în loc de nowrap */
    overflow: visible;
    text-overflow: unset;
  }

  /* selecturi/inputuri pe mobil să nu fie tăiate */
  select, .input{
    font-size: 18px;
  }
}
@media (max-width: 720px){
  body{
    height: 100%;
    overflow: auto !important;
  }
  .wrap{
    height: auto !important;
    overflow: auto;
  }
}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="col">
      <div class="card">
        <div class="cardHeader">
          <div>
            <div class="title">Configuration du dispositif</div>
            <div class="sub">Choisissez ou créez un ballon / stent, puis passez au chronométrage</div>
          </div>
          <div id="clockChip" class="clockChip">Heure système : --:--:--</div>
        </div>

        <div class="cardBody">
          <div class="stateBanner">
            <div>
              <div class="itemTitle" id="selectedDeviceTitle">Aucun dispositif sélectionné</div>
              <div class="mutedSmall" id="selectedDeviceMeta">Choisissez dans la liste ou créez-en un nouveau</div>
            </div>
            <div class="badge badgeIdle" id="stateBadge">INACTIF</div>
          </div>

          <div class="divider"></div>

          <div class="grid2">
            <div>
              <label for="arterySelect">Artère</label>
              <select id="arterySelect">
                <option value="IVA">IVA (LAD)</option>
                <option value="ACx">ACx (LCx)</option>
                <option value="CD">CD (RCA)</option>
                <option value="TC">TC (Tronc commun)</option>
                <option value="DG">DG (Diagonal)</option>
                <option value="MG">MG (Marginale)</option>
                <option value="Autre">Autre</option>
              </select>
            </div>

            <div>
              <label for="deviceSelect">Sélectionner un dispositif existant</label>
              <select id="deviceSelect">
                <option value="">(Aucun)</option>
              </select>
            </div>

            <div>
              <label for="arteryOther" id="arteryOtherLabel" style="display:none;">Autre (préciser)</label>
              <input id="arteryOther" class="input" inputmode="text" placeholder="Ex : branche postéro-latérale..." style="display:none;" />
            </div>

            <div class="row" style="justify-content:flex-end; align-self:end;">
              <button class="btn btnGhost" id="btnClearDevice" type="button">Réinitialiser la sélection</button>
            </div>
          </div>

          <div class="divider"></div>

          <div class="grid2">
            <div>
              <label for="deviceType">Type</label>
              <select id="deviceType">
                <option value="Ballon">Ballon</option>
                <option value="Stent">Stent</option>
              </select>
            </div>
            <div>
              <label for="deviceName">Nom court (optionnel)</label>
              <input id="deviceName" class="input" inputmode="text" placeholder="Ex : NC, DES, UHP..." />
            </div>

            <div>
              <label for="diameter">Diamètre (mm)</label>
              <input id="diameter" class="input" inputmode="decimal" placeholder="Ex : 3.0" />
            </div>
            <div>
              <label for="length">Longueur (mm)</label>
              <input id="length" class="input" inputmode="decimal" placeholder="Ex : 15" />
            </div>
          </div>

          <div class="row" style="margin-top:12px;">
            <button class="btn btnPrimary" id="btnSaveDevice" type="button">Enregistrer et sélectionner</button>
            <div class="pill" id="deviceCount">0 dispositifs enregistrés</div>
          </div>

          <div class="hint" style="margin-top:10px;">
            Interface pensée pour tablette tactile, sous champ stérile : boutons simples, gros, minimalistes.
          </div>
        </div>
      </div>

      <div class="card cardGrow">
        <div class="cardHeader">
          <div>
            <div class="title">Historique des inflations</div>
            <div class="sub">Chaque entrée inclut artère, dispositif, durée, pression et heure de début</div>
          </div>
          <div class="row">
            <button class="btn btnGhost" id="btnExport" type="button">Exporter CSV</button>
            <button class="btn btnGhost" id="btnClearHistory" type="button">Effacer l’historique</button>
          </div>
        </div>

        <div class="cardBody">
          <div class="scrollY historyScroll">
            <div class="list" id="historyList"></div>
            <div class="hint" id="historyEmptyHint">Aucune entrée pour le moment. Lancez le chrono et saisissez la pression au STOP.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="col">
      <div class="card">
        <div class="cardHeader">
          <div>
            <div class="title">Chronomètre</div>
            <div class="sub">Précision 2 décimales, gros bouton Start/Stop</div>
          </div>
          <div class="pill" id="activeDevicePill">Dispositif : (non sélectionné)</div>
        </div>

        <div class="cardBody">
          <div class="timerWrap">
            <div class="timerDisplay">
              <div class="time" id="timeDisplay">00.00</div>
            </div>

            <button class="btn btnPrimary bigButton" id="btnToggle" type="button" disabled>
              DÉMARRER
            </button>

            <div class="row" style="justify-content:space-between;">
              <div class="pill" id="startTimePill">Heure de début : --:--:--</div>
              <button class="btn btnGhost" id="btnResetTimer" type="button" disabled>Réinitialiser</button>
            </div>

            <div class="hint">
              Flux : sélectionner dispositif + artère → DÉMARRER à l’inflation → STOP à l’aspiration → saisir la pression.
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="cardHeader">
          <div>
            <div class="title">Stockage local</div>
            <div class="sub">Les données restent sur la tablette (localStorage du navigateur)</div>
          </div>
        </div>
        <div class="cardBody">
          <div class="row">
            <button class="btn btnGhost" id="btnResetAll" type="button">Réinitialisation totale</button>
            <span class="mutedSmall">Attention : efface dispositifs + historique.</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal" id="pressureModal" role="dialog" aria-modal="true" aria-labelledby="pressureTitle">
    <div class="modalPanel">
      <div class="cardHeader">
        <div>
          <div class="modalTitle" id="pressureTitle">Saisir la pression</div>
          <div class="modalSubtitle" id="pressureSubtitle">Indiquez la pression (atm), puis validez.</div>
        </div>
        <div class="tag" id="modalElapsedTag">Durée : 0.00 s</div>
      </div>

      <div class="modalBody">
        <div class="grid2">
          <div style="grid-column:1 / -1;">
            <label for="pressureInput">Pression (atm)</label>
            <input id="pressureInput" class="input" inputmode="decimal" placeholder="Ex : 12" />
          </div>
        </div>

        <div class="modalActions">
          <button class="btn btnGhost" id="btnCancelPressure" type="button">Annuler</button>
          <button class="btn btnPrimary" id="btnOkPressure" type="button">OK</button>
        </div>

        <div class="hint" style="margin-top:10px;">
          Astuce : saisie rapide sur tablette (ex : 14) ou décimales (ex : 14.5).
        </div>
      </div>
    </div>
  </div>

  <script>
    const pad2 = (n) => String(n).padStart(2,'0');
    const fmtClock = (d) => `${pad2(d.getHours())}:${pad2(d.getMinutes())}:${pad2(d.getSeconds())}`;
    const nowISO = () => new Date().toISOString();
    const safeNum = (v) => {
      if (v === null || v === undefined) return null;
      const s = String(v).trim().replace(',', '.');
      if (!s) return null;
      const n = Number(s);
      return Number.isFinite(n) ? n : null;
    };
    const uid = () => Math.random().toString(16).slice(2) + Date.now().toString(16);

    const KEY_DEVICES = "coro_devices_streamlit_v1";
    const KEY_HISTORY = "coro_history_streamlit_v1";
    const KEY_ARTERY  = "coro_artery_streamlit_v1";

    function loadDevices(){ try { return JSON.parse(localStorage.getItem(KEY_DEVICES) || "[]"); } catch { return []; } }
    function saveDevices(arr){ localStorage.setItem(KEY_DEVICES, JSON.stringify(arr)); }
    function loadHistory(){ try { return JSON.parse(localStorage.getItem(KEY_HISTORY) || "[]"); } catch { return []; } }
    function saveHistory(arr){ localStorage.setItem(KEY_HISTORY, JSON.stringify(arr)); }
    function loadArtery(){ try { return JSON.parse(localStorage.getItem(KEY_ARTERY) || "{}"); } catch { return {}; } }
    function saveArtery(obj){ localStorage.setItem(KEY_ARTERY, JSON.stringify(obj)); }

    let devices = loadDevices();
    let history = loadHistory();
    let arteryState = loadArtery();

    let selectedDeviceId = "";
    let running = false;
    let startPerf = 0;
    let startSystemISO = "";
    let rafId = 0;
    let lastElapsed = 0;

    const clockChip = document.getElementById("clockChip");

    const arterySelect = document.getElementById("arterySelect");
    const arteryOther = document.getElementById("arteryOther");
    const arteryOtherLabel = document.getElementById("arteryOtherLabel");

    const deviceSelect = document.getElementById("deviceSelect");
    const deviceType = document.getElementById("deviceType");
    const deviceName = document.getElementById("deviceName");
    const diameter = document.getElementById("diameter");
    const length = document.getElementById("length");
    const btnSaveDevice = document.getElementById("btnSaveDevice");
    const btnClearDevice = document.getElementById("btnClearDevice");
    const deviceCount = document.getElementById("deviceCount");

    const selectedDeviceTitle = document.getElementById("selectedDeviceTitle");
    const selectedDeviceMeta = document.getElementById("selectedDeviceMeta");
    const activeDevicePill = document.getElementById("activeDevicePill");

    const stateBadge = document.getElementById("stateBadge");

    const timeDisplay = document.getElementById("timeDisplay");
    const btnToggle = document.getElementById("btnToggle");
    const btnResetTimer = document.getElementById("btnResetTimer");
    const startTimePill = document.getElementById("startTimePill");

    const historyList = document.getElementById("historyList");
    const historyEmptyHint = document.getElementById("historyEmptyHint");
    const btnClearHistory = document.getElementById("btnClearHistory");
    const btnExport = document.getElementById("btnExport");

    const btnResetAll = document.getElementById("btnResetAll");

    const pressureModal = document.getElementById("pressureModal");
    const pressureInput = document.getElementById("pressureInput");
    const btnCancelPressure = document.getElementById("btnCancelPressure");
    const btnOkPressure = document.getElementById("btnOkPressure");
    const modalElapsedTag = document.getElementById("modalElapsedTag");
    const pressureSubtitle = document.getElementById("pressureSubtitle");

    function arteryLabel(){
      const main = arterySelect.value;
      if (main === "Autre"){
        const o = (arteryOther.value || "").trim();
        return o ? o : "Autre";
      }
      return main;
    }

    function deviceLabel(d){
      const nm = (d.name && d.name.trim()) ? ` ${d.name.trim()}` : "";
      return `${d.type}${nm} ${d.diameter}×${d.length} mm`;
    }

    function setBadge(state){
      stateBadge.textContent = state;
      stateBadge.classList.remove("badgeReady","badgeRun","badgeIdle");
      if (state === "EN COURS") stateBadge.classList.add("badgeRun");
      else if (state === "PRÊT") stateBadge.classList.add("badgeReady");
      else stateBadge.classList.add("badgeIdle");
    }

    function setSelectedDevice(id){
      selectedDeviceId = id || "";
      const d = devices.find(x => x.id === selectedDeviceId);

      if (!d){
        selectedDeviceTitle.textContent = "Aucun dispositif sélectionné";
        selectedDeviceMeta.textContent = "Choisissez dans la liste ou créez-en un nouveau";
        activeDevicePill.textContent = "Dispositif : (non sélectionné)";
        btnToggle.disabled = true;
        return;
      }

      selectedDeviceTitle.textContent = deviceLabel(d);
      selectedDeviceMeta.textContent = "Sélectionné pour le chronométrage";
      activeDevicePill.textContent = "Dispositif : " + deviceLabel(d);
      btnToggle.disabled = false;
    }

    function renderDeviceSelect(){
      deviceSelect.innerHTML = `<option value="">(Aucun)</option>`;
      for (const d of devices){
        const opt = document.createElement("option");
        opt.value = d.id;
        opt.textContent = deviceLabel(d);
        deviceSelect.appendChild(opt);
      }
      deviceSelect.value = selectedDeviceId || "";
      deviceCount.textContent = `${devices.length} dispositifs enregistrés`;
    }

    function renderHistory(){
      historyList.innerHTML = "";
      if (!history.length){
        historyEmptyHint.style.display = "block";
        return;
      }
      historyEmptyHint.style.display = "none";

      const sorted = [...history].sort((a,b) => (b.createdAt || "").localeCompare(a.createdAt || ""));
      for (const h of sorted){
        const d = devices.find(x => x.id === h.deviceId);
        const title = d ? deviceLabel(d) : (h.deviceLabel || "Dispositif (supprimé)");

        const item = document.createElement("div");
        item.className = "item";

        const left = document.createElement("div");
        left.className = "itemLeft";

        const t = document.createElement("div");
        t.className = "itemTitle";
        t.textContent = title;

        const meta = document.createElement("div");
        meta.className = "itemMeta";

        const tagArtery = document.createElement("span");
        tagArtery.className = "tag";
        tagArtery.textContent = `Artère : ${h.artery || "—"}`;

        const tagP = document.createElement("span");
        tagP.className = "tag";
        tagP.textContent = `Pression : ${h.pressureAtm} atm`;

        const tagT = document.createElement("span");
        tagT.className = "tag";
        tagT.textContent = `Durée : ${Number(h.elapsedSec).toFixed(2)} s`;

        const tagS = document.createElement("span");
        tagS.className = "tag";
        tagS.textContent = `Heure début : ${h.startClock}`;

        meta.appendChild(tagArtery);
        meta.appendChild(tagP);
        meta.appendChild(tagT);
        meta.appendChild(tagS);

        left.appendChild(t);
        left.appendChild(meta);

        const right = document.createElement("div");
        right.style.display = "flex";
        right.style.gap = "10px";
        right.style.alignItems = "center";

        const btnUse = document.createElement("button");
        btnUse.className = "btn btnGhost";
        btnUse.type = "button";
        btnUse.textContent = "Utiliser";
        btnUse.onclick = () => {
          if (d){
            deviceSelect.value = d.id;
            setSelectedDevice(d.id);
            renderDeviceSelect();
            setBadge("PRÊT");
          }
        };

        const btnDel = document.createElement("button");
        btnDel.className = "btn btnGhost";
        btnDel.type = "button";
        btnDel.textContent = "Supprimer";
        btnDel.onclick = () => {
          history = history.filter(x => x.id !== h.id);
          saveHistory(history);
          renderHistory();
        };

        right.appendChild(btnUse);
        right.appendChild(btnDel);

        item.appendChild(left);
        item.appendChild(right);

        historyList.appendChild(item);
      }
    }

    function tickClock(){
      const d = new Date();
      clockChip.textContent = "Heure système : " + fmtClock(d);
    }
    setInterval(tickClock, 250);
    tickClock();

    function updateDisplay(elapsedSec){
      timeDisplay.textContent = elapsedSec.toFixed(2);
    }

    function loop(){
      if (!running) return;
      const elapsed = (performance.now() - startPerf) / 1000;
      lastElapsed = elapsed;
      updateDisplay(elapsed);
      rafId = requestAnimationFrame(loop);
    }

    function startTimer(){
      if (!selectedDeviceId) return;

      running = true;
      startPerf = performance.now();
      startSystemISO = nowISO();

      const startClock = fmtClock(new Date());
      startTimePill.textContent = "Heure de début : " + startClock;

      btnToggle.textContent = "STOP";
      btnToggle.classList.remove("btnPrimary");
      btnToggle.classList.add("btnDanger");
      btnResetTimer.disabled = true;

      setBadge("EN COURS");

      lastElapsed = 0;
      updateDisplay(0);

      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(loop);
    }

    function stopTimer(){
      running = false;
      cancelAnimationFrame(rafId);

      btnToggle.textContent = "DÉMARRER";
      btnToggle.classList.remove("btnDanger");
      btnToggle.classList.add("btnPrimary");
      btnResetTimer.disabled = false;

      const d = devices.find(x => x.id === selectedDeviceId);
      const label = d ? deviceLabel(d) : "Dispositif";

      modalElapsedTag.textContent = "Durée : " + lastElapsed.toFixed(2) + " s";
      pressureSubtitle.textContent = `Dispositif : ${label} | Artère : ${arteryLabel()} | Saisir la pression (atm) puis valider.`;
      openPressureModal();
      setBadge("PRÊT");
    }

    function resetTimer(){
      running = false;
      cancelAnimationFrame(rafId);
      lastElapsed = 0;
      updateDisplay(0);
      startTimePill.textContent = "Heure de début : --:--:--";
      btnResetTimer.disabled = true;
      if (selectedDeviceId) setBadge("PRÊT");
      else setBadge("INACTIF");
    }

    function openPressureModal(){
      pressureInput.value = "";
      pressureModal.classList.add("show");
      setTimeout(() => pressureInput.focus(), 50);
    }
    function closePressureModal(){
      pressureModal.classList.remove("show");
      pressureInput.blur();
    }

    function savePressureEntry(){
      const p = safeNum(pressureInput.value);
      if (p === null){
        pressureInput.focus();
        pressureInput.style.borderColor = "rgba(255,77,109,0.75)";
        setTimeout(() => pressureInput.style.borderColor = "rgba(255,255,255,0.12)", 450);
        return;
      }

      const d = devices.find(x => x.id === selectedDeviceId);
      const startDate = startSystemISO ? new Date(startSystemISO) : new Date();
      const entry = {
        id: uid(),
        artery: arteryLabel(),
        deviceId: selectedDeviceId,
        deviceLabel: d ? deviceLabel(d) : "Dispositif",
        pressureAtm: Number(p).toFixed(1).replace(/\.0$/, ""),
        elapsedSec: Number(lastElapsed.toFixed(2)),
        startClock: fmtClock(startDate),
        startISO: startSystemISO || nowISO(),
        createdAt: nowISO()
      };

      history.push(entry);
      saveHistory(history);
      renderHistory();

      closePressureModal();
      resetTimer();
    }

    function applyArteryState(){
      const main = arteryState.main || "IVA";
      arterySelect.value = main;
      const showOther = (main === "Autre");
      arteryOther.style.display = showOther ? "block" : "none";
      arteryOtherLabel.style.display = showOther ? "block" : "none";
      arteryOther.value = arteryState.other || "";
    }

    function persistArteryState(){
      arteryState = { main: arterySelect.value, other: (arteryOther.value || "").trim() };
      saveArtery(arteryState);
    }

    arterySelect.addEventListener("change", () => {
      if (arterySelect.value === "Autre"){
        arteryOther.style.display = "block";
        arteryOtherLabel.style.display = "block";
        setTimeout(() => arteryOther.focus(), 50);
      } else {
        arteryOther.style.display = "none";
        arteryOtherLabel.style.display = "none";
      }
      persistArteryState();
    });
    arteryOther.addEventListener("input", persistArteryState);

    deviceSelect.addEventListener("change", () => {
      if (running) return;
      setSelectedDevice(deviceSelect.value);
      renderDeviceSelect();
      setBadge(selectedDeviceId ? "PRÊT" : "INACTIF");
    });

    btnClearDevice.addEventListener("click", () => {
      if (running) return;
      deviceSelect.value = "";
      setSelectedDevice("");
      renderDeviceSelect();
      resetTimer();
      setBadge("INACTIF");
    });

    btnSaveDevice.addEventListener("click", () => {
      if (running) return;

      const type = deviceType.value;
      const nm = (deviceName.value || "").trim();
      const dia = safeNum(diameter.value);
      const len = safeNum(length.value);

      if (dia === null || len === null){
        const bump = (el) => {
          el.style.borderColor = "rgba(255,77,109,0.75)";
          setTimeout(() => el.style.borderColor = "rgba(255,255,255,0.12)", 450);
        };
        if (dia === null) bump(diameter);
        if (len === null) bump(length);
        return;
      }

      const key = (x) => `${x.type}|${(x.name||"").trim().toLowerCase()}|${x.diameter}|${x.length}`;
      const cand = { type, name: nm, diameter: Number(dia), length: Number(len) };
      const existing = devices.find(x => key(x) === key(cand));

      let id;
      if (existing){
        id = existing.id;
      } else {
        id = uid();
        devices.push({ id, ...cand, createdAt: nowISO() });
        saveDevices(devices);
      }

      renderDeviceSelect();
      setSelectedDevice(id);
      deviceSelect.value = id;

      setBadge("PRÊT");
      btnResetTimer.disabled = true;
      updateDisplay(0);
      startTimePill.textContent = "Heure de début : --:--:--";
    });

    btnToggle.addEventListener("click", () => {
      if (!selectedDeviceId) return;
      if (!running) startTimer();
      else stopTimer();
    });

    btnResetTimer.addEventListener("click", () => {
      if (running) return;
      resetTimer();
    });

    btnCancelPressure.addEventListener("click", () => {
      closePressureModal();
      resetTimer();
    });

    btnOkPressure.addEventListener("click", savePressureEntry);

    pressureModal.addEventListener("click", (e) => {
      if (e.target === pressureModal){
        closePressureModal();
        resetTimer();
      }
    });

    pressureInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter"){
        e.preventDefault();
        savePressureEntry();
      }
    });

    btnClearHistory.addEventListener("click", () => {
      if (!confirm("Effacer tout l’historique des inflations ?")) return;
      history = [];
      saveHistory(history);
      renderHistory();
    });

    btnExport.addEventListener("click", () => {
      const rows = [];
      rows.push(["createdAt","artery","device","pressureAtm","elapsedSec","startClock","startISO"].join(","));
      const sorted = [...history].sort((a,b) => (a.createdAt||"").localeCompare(b.createdAt||""));
      for (const h of sorted){
        const d = devices.find(x => x.id === h.deviceId);
        const dev = (d ? deviceLabel(d) : (h.deviceLabel || "Dispositif")).replaceAll('"','""');
        const art = String(h.artery || "").replaceAll('"','""');
        rows.push([
          h.createdAt,
          `"${art}"`,
          `"${dev}"`,
          h.pressureAtm,
          Number(h.elapsedSec).toFixed(2),
          h.startClock,
          h.startISO
        ].join(","));
      }
      const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "coro_historique.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    });

    btnResetAll.addEventListener("click", () => {
      const ok = confirm("Réinitialisation totale : effacer dispositifs + historique + artère. Continuer ?");
      if (!ok) return;
      localStorage.removeItem(KEY_DEVICES);
      localStorage.removeItem(KEY_HISTORY);
      localStorage.removeItem(KEY_ARTERY);
      devices = [];
      history = [];
      selectedDeviceId = "";
      arteryState = {};
      renderDeviceSelect();
      setSelectedDevice("");
      renderHistory();
      applyArteryState();
      resetTimer();
      setBadge("INACTIF");
    });

    applyArteryState();
    renderDeviceSelect();
    renderHistory();
    setSelectedDevice(selectedDeviceId);
    setBadge(selectedDeviceId ? "PRÊT" : "INACTIF");
  </script>
</body>
</html>
"""

# Important: height mare ca să arate ca o aplicație full-screen
components.html(html, height=920, scrolling=True)
