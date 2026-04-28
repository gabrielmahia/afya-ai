"""AfyaAI — Kenya health AI assistant."""
import sys, os, json, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st

st.set_page_config(page_title="AfyaAI", page_icon="🏥", layout="centered")
st.markdown("""<style>
    .main > div { padding: 0.5rem 0.8rem 2rem; }
    h1 { font-size: 1.5rem !important; }
</style>""", unsafe_allow_html=True)


def _get_key():
    try:
        import streamlit as st
        k = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if k: return k
    except: pass
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

def _gemini(system, user, api_key, max_tokens=800):
    _BASE = "https://generativelanguage.googleapis.com"
    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.3},
    }
    for model in models:
        url = f"{_BASE}/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
              headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 404): continue
            raise
        except Exception: continue
    raise RuntimeError("Gemini unavailable — check your API key")


NHIF_RATES = [
    (5999, 150), (7999, 300), (11999, 400), (14999, 500),
    (19999, 600), (24999, 750), (29999, 850), (34999, 900),
    (39999, 950), (44999, 1000), (49999, 1100), (59999, 1200),
    (69999, 1300), (79999, 1400), (89999, 1500), (99999, 1600),
    (float("inf"), 1700),
]

HOSPITALS = {
    "Nairobi": ["Kenyatta National Hospital (KNH) — 020 272 6300", "Mama Lucy Kibaki Hospital — 020 558 0040", "Mbagathi District Hospital"],
    "Mombasa": ["Coast General Teaching & Referral Hospital — 041 231 4201", "Tudor District Hospital"],
    "Kisumu": ["Jaramogi Oginga Odinga Teaching & Referral Hospital — 057 202 1153"],
    "Nakuru": ["Nakuru Level 5 Hospital — 051 221 0285"],
    "Eldoret": ["Moi Teaching & Referral Hospital — 053 203 3471"],
    "Garissa": ["Garissa County Referral Hospital — 046 202 1002"],
    "Turkana": ["Lodwar County Referral Hospital — 054 221 021"],
}

SYSTEM_HEALTH = """You are AfyaAI, a Kenya health information assistant.
You provide clear, accurate health information grounded in Kenya's health system.

Key facts you know:
- NHIF (now merging into SHA — Social Health Authority) covers inpatient at public hospitals
- Linda Mama provides free maternity services at all public facilities
- Article 43 of the Constitution guarantees the right to highest attainable standard of health
- The KEPH (Kenya Essential Package for Health) defines what services each level provides
- Level 1=Community, 2=Dispensary, 3=Health Centre, 4=District Hospital, 5=Regional, 6=National

Rules:
- Always answer in the language the user asks (English or Kiswahili)
- Always add: "Tafadhali wasiliana na daktari / Please consult a qualified healthcare provider"
- Never diagnose specific conditions
- For emergencies: immediately say call 0800 720 021 (health helpline) or go to nearest hospital
- Cite the relevant law or programme when discussing rights or entitlements"""

api_key = _get_key()

st.title("🏥 AfyaAI")
st.caption("Kenya health information · Maswali ya afya · Free · EN/SW")

tab1, tab2, tab3, tab4 = st.tabs(["💰 NHIF", "🏥 Hospitals", "🤰 Maternal", "💬 Ask AfyaAI"])

with tab1:
    st.subheader("NHIF / SHA Contribution Calculator")
    salary = st.number_input("Monthly gross salary (KES):", min_value=5000, value=50000, step=5000)
    contribution = next(amt for ceiling, amt in NHIF_RATES if salary <= ceiling)
    col1, col2 = st.columns(2)
    col1.metric("Your monthly contribution", f"KES {contribution:,}")
    col2.metric("Employer matches", f"KES {contribution:,}")
    st.metric("Total NHIF per month", f"KES {contribution*2:,}")
    nhif_info = ("NHIF covers: Inpatient at public hospitals, Maternity (Linda Mama), Surgery, ICU.\n\nNOT covered: Outpatient at most public facilities, Dental, Optical (limited).")
    st.info(nhif_info)
    st.caption("Rates: NHIF Act / SHA Act 2023. Verify at nhif.or.ke")

with tab2:
    st.subheader("Public Hospital Finder")
    county = st.selectbox("Select county:", sorted(HOSPITALS.keys()) + ["Other county"])
    if county in HOSPITALS:
        st.markdown("**Facilities:**")
        for h in HOSPITALS[county]:
            st.markdown(f"- {h}")
    else:
        st.info("Search your county health department or call the health helpline: **0800 720 021** (free)")
    st.caption("Emergency anywhere in Kenya: 999 · 112 · 0800 720 021 (Afya Care)")

with tab3:
    st.subheader("Maternal & Child Health")
    st.success("🤰 **Linda Mama**: Free maternity at ALL public health facilities. No payment required.")
    st.markdown("""
**Antenatal care schedule (minimum):**
- Visit 1: Before 12 weeks
- Visit 2: 20 weeks
- Visit 3: 26 weeks
- Visit 4: 30 weeks
- Visit 5: 36 weeks
- Visit 6: 38-40 weeks

**After birth:**
- Baby vaccination at birth, 6 weeks, 10 weeks, 14 weeks, 9 months, 18 months
- Birth registration: within 6 months at local civil registry (free)
- NHIF covers postnatal care
""")
    st.caption("Source: Ministry of Health Kenya · Linda Mama Programme")

with tab4:
    st.subheader("Ask AfyaAI")
    if not api_key:
        st.info(
            "Add a free Google AI key to chat with AfyaAI.\n\n"
            "Get one free at [aistudio.google.com](https://aistudio.google.com) — no credit card."
        )
        api_key = st.text_input("Google AI key:", type="password", placeholder="AIza...")
    else:
        st.success("✅ AfyaAI ready")

    EXAMPLES = [
        "What does NHIF cover for inpatient?",
        "NHIF inalipa nini kwa mama mjamzito?",
        "When should I go to hospital vs dispensary?",
        "What are my health rights under the Constitution?",
    ]
    st.caption("**Try:** " + " · ".join(f"*{e}*" for e in EXAMPLES[:2]))

    if "afya_msgs" not in st.session_state:
        st.session_state.afya_msgs = []

    for role, msg in st.session_state.afya_msgs[-6:]:
        with st.chat_message(role):
            st.markdown(msg)

    q = st.chat_input("Ask about health in Kenya...")
    if q:
        st.session_state.afya_msgs.append(("user", q))
        with st.chat_message("user"): st.markdown(q)
        with st.chat_message("assistant"):
            if not api_key:
                ans = "Please add a Google AI key above to get answers."
            else:
                with st.spinner("Nafikiri..."):
                    try:
                        ans = _gemini(SYSTEM_HEALTH, q, api_key)
                    except urllib.error.HTTPError as e:
                        ans = "API key not recognised." if e.code == 403 else "Too many requests — please wait a moment."
                    except Exception:
                        ans = "Could not get an answer. Please try again."
            st.markdown(ans)
        st.session_state.afya_msgs.append(("assistant", ans))

st.divider()
st.caption("⚠️ General health information only — not medical advice. Always consult a qualified healthcare provider. © 2026 Gabriel Mahia · CC BY-NC-ND 4.0")
