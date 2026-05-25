"""
AfyaAI — Kenya Health Assistant
Maternal health, NHIF/SHA navigation, clinical guidance for Kenya.
"""
import sys, json, urllib.request, ssl
import streamlit as st

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AfyaAI — Kenya Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Gemini API ────────────────────────────────────────────────
def get_gemini_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini(prompt: str, key: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1200}}
    req = urllib.request.Request(
        f"{url}?key={key}", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=40)
    st.title("AfyaAI")
    st.caption("Kenya Health Assistant")
    st.divider()
    mode = st.radio("Select module", [
        "🤰 Maternal Health",
        "💊 General Health",
        "🏥 NHIF / SHA Guide",
        "🧪 Symptoms Checker",
        "💬 Ask AfyaAI"
    ])
    st.divider()
    st.caption("⚠️ Educational only. Always consult a qualified healthcare provider.")
    st.caption("📍 Designed for Kenya health system context.")

key = get_gemini_key()
if not key:
    st.error("Add GOOGLE_API_KEY to Streamlit secrets to enable AI features.")

# ─────────────────────────────────────────────────────────────
# MODULE 1: MATERNAL HEALTH (Third Trimester Focus)
# ─────────────────────────────────────────────────────────────
if mode == "🤰 Maternal Health":
    st.title("🤰 Maternal Health Guide")
    st.markdown("*Evidence-based guidance for pregnancy in Kenya — third trimester focus*")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Third Trimester Overview",
        "🍽️ Nutrition Guide",
        "⚠️ Warning Signs",
        "🏥 Birth Preparedness"
    ])

    with tab1:
        st.subheader("Third Trimester (Weeks 28–40)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**What to expect:**
- Baby weight gain accelerates (gains ~200g/week)
- Braxton Hicks contractions become more frequent
- Shortness of breath as baby grows
- Frequent urination returns
- Swelling in feet/ankles (some is normal)
- Sleep becomes difficult

**Key milestones:**
- 28 weeks: Baby can open eyes
- 32 weeks: Practice breathing movements
- 36 weeks: Baby turns head-down (ideally)
- 37 weeks: Early term — viable outside womb
- 40 weeks: Full term / estimated due date
""")
        with col2:
            st.markdown("""
**Appointments:**
- Every 2 weeks at your health facility from 28 weeks
- Every week from 36 weeks onwards
- Bring your *Mama Card* to every visit
- Request: BP check, urine test, fundal height, foetal heart rate

**Hospital to choose:**
- Ensure it has a **maternity ward and newborn unit**
- Know the route and transport options
- Confirm 24-hour availability
- Pack your hospital bag by **36 weeks**

**Document checklist:**
- ✅ National ID
- ✅ Mama Card / ANC booklet
- ✅ NHIF/SHA card
- ✅ Partner ID (for birth registration)
""")

        if key:
            st.divider()
            week = st.slider("What week of pregnancy are you?", 28, 42, 30)
            if st.button("Get personalised guidance for this week"):
                with st.spinner("Generating guidance..."):
                    prompt = f"""You are AfyaAI, a Kenya maternal health assistant. 
A pregnant woman is at {week} weeks of pregnancy in Kenya.
Provide:
1. What is happening with the baby this week (2-3 sentences)
2. Physical changes she may experience (bullet list, 4-5 points)
3. What she should do at her next antenatal visit (3 points)
4. One important nutrition tip using East African foods (ugali, sukuma wiki, eggs, beans, omena, sweet potato, githeri)
5. Any warning signs specific to this week to watch for (2-3 points)

Keep language simple. Use Kenya health system context (Level 4/5 hospitals, CHVs, Mama Card).
Format with clear headings. Be warm and supportive."""
                    try:
                        resp = gemini(prompt, key)
                        st.markdown(resp)
                    except Exception as e:
                        st.error(f"AI error: {e}")

    with tab2:
        st.subheader("🍽️ Nutrition for Third Trimester")
        st.markdown("*Daily nutritional targets and East African food sources*")

        nutrients = {
            "Iron (27mg/day)": {
                "why": "Prevents anaemia — common in pregnancy",
                "foods": "Beef liver, lean meat, omena (dagaa), beans, lentils, spinach, fortified uji",
                "tip": "Eat with vitamin C (tomatoes, oranges) to boost absorption. Avoid tea with iron-rich foods.",
                "color": "🔴"
            },
            "Calcium (1,000mg/day)": {
                "why": "Baby's bone development, prevents pre-eclampsia",
                "foods": "Milk, yogurt, cheese, fortified uji, sardines with bones, dark green vegetables",
                "tip": "2 cups of milk + 1 cup yogurt provides ~600mg. Make up the rest with fortified foods.",
                "color": "🥛"
            },
            "Protein (71g/day)": {
                "why": "Baby's tissue and brain growth",
                "foods": "Eggs, chicken, beef, beans, lentils, fish (omena, tilapia, salmon), milk",
                "tip": "2 eggs + 1 cup beans + 1 cup milk = ~40g protein. Add meat/fish for the rest.",
                "color": "💪"
            },
            "DHA / Omega-3 (200-300mg/day)": {
                "why": "Baby's brain and eye development",
                "foods": "Omena (dagaa) — richest local source, tilapia, salmon, sardines, DHA supplement",
                "tip": "2 servings of fish per week covers this. Omena is affordable and available nationwide.",
                "color": "🐟"
            },
            "Folate (600mcg/day)": {
                "why": "Neural tube development (critical in all trimesters)",
                "foods": "Dark leafy greens, fortified uji, beans, liver, eggs",
                "tip": "Your prenatal vitamin should cover this. Continue taking it daily.",
                "color": "🥬"
            },
            "Water (8-10 cups/day)": {
                "why": "Reduces swelling, prevents UTIs, maintains amniotic fluid",
                "foods": "Water, coconut water, herbal tea (ginger, rooibos), diluted fresh juice",
                "tip": "Drink a glass of water when you wake up, with every meal, and before bed.",
                "color": "💧"
            }
        }

        for nutrient, info in nutrients.items():
            with st.expander(f"{info['color']} {nutrient}"):
                st.markdown(f"**Why:** {info['why']}")
                st.markdown(f"**Best sources:** {info['foods']}")
                st.info(f"💡 {info['tip']}")

        st.divider()
        st.subheader("Foods to Avoid")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**❌ Avoid:**
- Raw or undercooked meat (suya/nyama choma must be well-done)
- Raw fish / sushi
- Unpasteurised milk or raw milk cheese
- Deli/processed meats (unless heated thoroughly)
- High-mercury fish: swordfish, tilefish, king mackerel
- Raw eggs or runny yolks
- Alcohol (no safe amount in pregnancy)
""")
        with col2:
            st.markdown("""
**⚠️ Limit:**
- Caffeine: max 200mg/day (≈ 1 cup of coffee)
- Added salt — can worsen swelling
- Processed/packaged foods (high sodium)
- Unripe pawpaw (papaya) — avoid completely
- Excess sugar — especially important with GDM risk

**✅ Small, frequent meals:**
6 smaller meals are better than 3 large ones.
Helps with heartburn, energy levels, and blood sugar.
""")

        if key:
            st.divider()
            st.subheader("Get a personalised meal plan")
            budget = st.selectbox("Daily food budget", ["KES 200-300", "KES 300-500", "KES 500-800", "KES 800+"])
            location = st.selectbox("Location", ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Rural area"])
            if st.button("Generate meal plan"):
                with st.spinner("Creating your meal plan..."):
                    prompt = f"""Create a daily meal plan for a pregnant woman in Kenya at 30+ weeks.
Budget: {budget} per day.
Location: {location}.
Use ONLY locally available East African foods (ugali, sukuma wiki, beans, eggs, omena, sweet potato, githeri, uji, chapati, rice, avocado, bananas, tomatoes, onions, milk, yogurt).
Ensure: 27mg iron, 1000mg calcium, 71g protein per day.
Format as 6 small meals (breakfast, mid-morning snack, lunch, afternoon snack, dinner, evening snack).
For each meal: food items, rough cost in KES, key nutrient benefit.
End with a shopping list for the week."""
                    try:
                        resp = gemini(prompt, key)
                        st.markdown(resp)
                    except Exception as e:
                        st.error(f"AI error: {e}")

    with tab3:
        st.subheader("⚠️ Warning Signs — When to Go to Hospital Immediately")
        st.error("**If you experience any of these, go to a Level 4 or 5 hospital immediately. Do not wait.**")

        warnings = [
            ("🩸 Vaginal bleeding", "Any bleeding after 20 weeks is abnormal. Go immediately.", "Placenta previa, abruption — life-threatening"),
            ("💧 Fluid leaking", "A gush or continuous trickle of fluid from the vagina", "Waters breaking — infection risk if untreated"),
            ("👁️ Severe headache + blurred vision", "Headache that won't go away, seeing spots or flashes", "Pre-eclampsia — can progress to eclampsia (seizures)"),
            ("😮 Sudden severe swelling", "Face, hands, or feet suddenly very swollen — especially with headache", "Pre-eclampsia warning sign"),
            ("💫 Dizziness or fainting", "Feeling faint, collapsing, or not able to stand", "Low blood pressure, anaemia, or eclampsia"),
            ("🤰 Decreased or no fetal movement", "Baby has not moved in 12 hours, or movement significantly reduced", "Fetal distress — time-sensitive"),
            ("🔥 Fever above 38°C", "High temperature with chills, especially with pain on urination", "Infection — UTI, malaria (common in Kenya), other"),
            ("😣 Severe abdominal pain", "Constant, severe pain different from normal Braxton Hicks", "Abruption, labour, or other emergency"),
            ("🩺 Convulsions / seizures", "Shaking, loss of consciousness", "Eclampsia — life-threatening emergency"),
        ]

        for sign, detail, risk in warnings:
            with st.expander(sign):
                st.markdown(f"**What it means:** {detail}")
                st.markdown(f"**Possible cause:** {risk}")

        st.divider()
        st.info("""
**What to tell the healthcare provider:**
1. How many weeks pregnant you are
2. When the symptom started
3. How severe it is (scale 1-10 for pain)
4. Any other symptoms alongside it
5. Your blood type if you know it

**Nearest hospitals with maternity wards in Nairobi area:**
- Kenyatta National Hospital (KNH) — main referral, 24hr, Level 6
- Nairobi Hospital — private, Level 5
- Aga Khan University Hospital — private, Level 5
- Pumwani Maternity Hospital — public, specialized maternity
- Mama Lucy Kibaki Hospital — public, Level 4
""")

    with tab4:
        st.subheader("🏥 Birth Preparedness Plan")
        st.markdown("*Prepare by 36 weeks — do not wait until labour starts*")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Choose your delivery facility NOW:**
- Which hospital / health centre?
- Do they have a maternity ward?
- Is there a newborn unit / NICU?
- Do they take NHIF/SHA?
- How far from your home?
- What is the transport plan?

**Save these numbers:**
- Your chosen hospital maternity ward
- Your CHV (Community Health Volunteer)
- A neighbour who can help
- Ambulance / emergency line: **0800 723 253** (Kenya ambulance)
- NHIF helpline: **0800 720 601**
""")
        with col2:
            st.markdown("""
**Hospital bag checklist (pack by 36 weeks):**

*For you:*
- ✅ National ID
- ✅ Mama Card / ANC booklet
- ✅ NHIF / SHA card
- ✅ 2 changes of clothes
- ✅ Sanitary pads (maternity size)
- ✅ Toiletries
- ✅ Phone + charger + airtime

*For baby:*
- ✅ 3 baby vests / bodysuits
- ✅ 3 baby socks
- ✅ 1 warm blanket / shawl
- ✅ Nappies (newborn size)
- ✅ Baby hat

*Finances:*
- ✅ NHIF/SHA card activated
- ✅ Some cash (KES 2,000-5,000) for incidentals
- ✅ M-Pesa airtime topped up
""")

        if key:
            st.divider()
            if st.button("Generate my personalised birth plan"):
                with st.spinner("Creating your birth plan..."):
                    prompt = """Create a detailed birth preparedness plan for a woman at 30 weeks pregnant in Kenya (Nairobi/Manassas area).
Include:
1. Decision checklist: choosing hospital, registering, confirming NHIF coverage
2. Transport plan template (primary and backup)
3. Financial preparation (NHIF, cash)
4. Support person preparation (what they need to know)
5. Signs of labour vs Braxton Hicks (clear distinction)
6. Timeline: what to do at each stage of labour before reaching hospital
7. Post-delivery immediate steps (Vitamin K for baby, skin-to-skin, breastfeeding initiation)

Context: Kenya health system, NHIF/SHA coverage, Level 4/5 hospitals.
Format as an actionable plan with checkboxes. Warm, supportive tone."""
                    try:
                        resp = gemini(prompt, key)
                        st.markdown(resp)
                    except Exception as e:
                        st.error(f"AI error: {e}")

# ─────────────────────────────────────────────────────────────
# MODULE 2: GENERAL HEALTH
# ─────────────────────────────────────────────────────────────
elif mode == "💊 General Health":
    st.title("💊 General Health Information")
    st.info("Select a health topic to get evidence-based information tailored for Kenya.")

    topic = st.selectbox("Choose a health topic", [
        "Malaria prevention and treatment",
        "Diabetes management (Type 2)",
        "Hypertension (high blood pressure)",
        "Tuberculosis (TB)",
        "HIV/AIDS — treatment and prevention",
        "Child immunisation schedule (Kenya EPI)",
        "Mental health — anxiety and depression",
        "Waterborne diseases prevention",
        "Nutrition and anaemia"
    ])

    if key and st.button(f"Get guidance on: {topic}"):
        with st.spinner("Loading health information..."):
            prompt = f"""You are AfyaAI, a Kenya health assistant.
Provide evidence-based health information about: {topic}

Structure your response as:
1. Overview (2-3 sentences, plain language)
2. Key facts for Kenya context (3-4 bullet points)
3. Prevention / management steps (numbered list)
4. When to seek care (Level 2 dispensary vs Level 4/5 hospital)
5. Available treatment / support in Kenya (NHIF coverage, KEMSA medications, community resources)
6. Common misconceptions to avoid

Use plain English. No medical jargon unless explained. Kenya-specific (mention county health departments, CHVs, KEMSA, NHIF where relevant)."""
            try:
                resp = gemini(prompt, key)
                st.markdown(resp)
            except Exception as e:
                st.error(f"AI error: {e}")

# ─────────────────────────────────────────────────────────────
# MODULE 3: NHIF / SHA GUIDE
# ─────────────────────────────────────────────────────────────
elif mode == "🏥 NHIF / SHA Guide":
    st.title("🏥 NHIF / SHA Navigation Guide")
    st.markdown("*Kenya's health insurance — what it covers and how to use it*")

    st.info("""
**SHA (Social Health Authority)** replaced NHIF in late 2023. 
Registration is now mandatory for all Kenyans under the Universal Health Coverage (UHC) programme.
SHA card = your key to subsidised healthcare at public and partner private facilities.
""")

    tab_reg, tab_cov, tab_mat, tab_faq = st.tabs(["Registration", "Coverage", "Maternal Benefits", "FAQ"])

    with tab_reg:
        st.subheader("How to Register for SHA")
        st.markdown("""
**Online:** [sso.health.go.ke](https://sso.health.go.ke)

**Steps:**
1. Visit [sso.health.go.ke](https://sso.health.go.ke)
2. Click "Register as Individual"
3. Enter National ID / Passport number
4. Complete personal details and next of kin
5. Choose payment method (mobile money, bank)
6. Pay monthly contribution (based on income bracket)
7. Download SHA card or collect from nearest SHA office

**Contributions:**
- Formal sector: 2.75% of gross salary (employer matches)
- Informal sector: Flat rate (check current rates at sha.go.ke)
- Indigent / vulnerable: Subsidised by government

**For dependants (add family members):**
- Spouse: registered as beneficiary
- Children under 18: registered as beneficiaries
- Up to 2 parents: can be added
""")

    with tab_cov:
        st.subheader("What SHA Covers")
        coverage = {
            "Outpatient": "Consultation, basic drugs, lab tests, X-rays at accredited facilities",
            "Inpatient": "Ward admission, surgery, meals, nursing care",
            "Maternity": "Antenatal care, normal delivery, Caesarean section, postnatal care",
            "Chronic diseases": "Diabetes, hypertension, cancer, renal failure (dialysis), mental health",
            "Surgery": "Most elective and emergency surgeries at accredited hospitals",
            "Critical illness": "ICU care, ventilator support (limits apply)",
            "Dental": "Basic dental care at Level 4+ hospitals",
            "Optical": "Limited optical coverage at accredited centres",
        }
        for service, detail in coverage.items():
            st.markdown(f"**{service}:** {detail}")

    with tab_mat:
        st.subheader("Maternity Benefits")
        st.success("""
**Linda Mama Programme (under SHA/government):**
Free maternity services for ALL Kenyan women at public health facilities.
This includes: ANC visits, delivery (normal and C-section), postnatal care, newborn care.
You do NOT need SHA registration to access Linda Mama — it is universal.
""")
        st.markdown("""
**What is fully covered:**
- Up to 4 ANC visits at accredited facilities
- Normal (vaginal) delivery — fully covered
- Caesarean section — covered up to SHA limits (top-up may be needed at private hospitals)
- Postnatal visit at 6 weeks
- Newborn immunisations at the health facility

**Private hospital maternity (with SHA):**
SHA covers a set amount. The difference is your responsibility.
Always confirm coverage limits with your hospital before delivery.

**Tips:**
- Carry your SHA card to every ANC visit
- Register your baby for SHA within 3 months of birth
- Keep all receipts for any out-of-pocket expenses
""")

    with tab_faq:
        st.subheader("Frequently Asked Questions")
        faqs = [
            ("I just moved from NHIF to SHA — do I need to re-register?",
             "If you were registered with NHIF, your records were migrated to SHA. Log in to sso.health.go.ke to verify your status. Some individuals need to reactivate their accounts."),
            ("Can my husband's SHA cover my maternity care?",
             "Yes — if you are registered as a dependent/beneficiary on your husband's SHA account, you are covered for maternity benefits at accredited facilities."),
            ("What if the hospital says SHA doesn't cover me?",
             "Request the specific reason in writing. Call SHA helpline: 0800 720 601 (free). You can also lodge a complaint via the SHA portal."),
            ("I'm self-employed — how much do I pay?",
             "Informal sector rates vary. Check the current schedule at sha.go.ke. Payment can be made via M-Pesa Paybill or bank."),
            ("Does SHA cover a private maternity ward?",
             "SHA covers the service, not the room upgrade. If you choose a private room, the difference in ward charges is your responsibility."),
        ]
        for q, a in faqs:
            with st.expander(q):
                st.markdown(a)

        if key:
            st.divider()
            user_q = st.text_input("Ask a specific SHA/NHIF question")
            if user_q and st.button("Get answer"):
                with st.spinner("Looking up SHA guidance..."):
                    prompt = f"""You are AfyaAI, a Kenya health insurance expert.
Answer this question about NHIF/SHA (Kenya's Social Health Authority) specifically:

Question: {user_q}

Base your answer on:
- SHA Act 2023 (replaced NHIF)
- Linda Mama programme for free maternity
- Current SHA coverage policies
- Kenya public health system (Level 2-6 facilities)

Be specific and practical. If you are uncertain, say so and suggest checking sha.go.ke or calling 0800 720 601."""
                    try:
                        resp = gemini(prompt, key)
                        st.markdown(resp)
                    except Exception as e:
                        st.error(f"AI error: {e}")

# ─────────────────────────────────────────────────────────────
# MODULE 4: SYMPTOMS CHECKER
# ─────────────────────────────────────────────────────────────
elif mode == "🧪 Symptoms Checker":
    st.title("🧪 Symptoms Checker")
    st.warning("**This is educational guidance only. Always consult a healthcare professional for diagnosis and treatment.**")

    symptoms = st.text_area("Describe your symptoms", placeholder="E.g.: I have had a fever for 2 days, headache, body aches, and I feel very tired...")
    age_group = st.selectbox("Age group", ["Child (0-12)", "Teenager (13-17)", "Adult (18-60)", "Elderly (60+)"])
    pregnant = st.checkbox("Currently pregnant")
    location = st.selectbox("County", ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Other (rural/semi-arid)"])

    if symptoms and key and st.button("Analyse symptoms"):
        with st.spinner("Analysing..."):
            preg_note = "The person is pregnant." if pregnant else ""
            prompt = f"""You are AfyaAI, a Kenya health triage assistant.
Patient details: {age_group}, {location} county. {preg_note}
Symptoms: {symptoms}

Provide:
1. **Possible conditions** (list 3-4, from most to least likely for Kenya context — consider malaria, typhoid, TB, common in your ranking)
2. **Urgency level**: Emergency (go now) / Urgent (go today) / Soon (within 48 hours) / Self-care possible
3. **Recommended action**: Which level of facility to visit (dispensary, health centre, Level 4, Level 5)
4. **What to tell the healthcare provider** (key information to share)
5. **Self-care measures** while waiting to see a provider (if appropriate)
6. **Red flags**: Signs that mean you must go immediately regardless

Important: 
- For pregnant patients, be conservative — recommend care sooner
- Consider local disease burden (malaria in lakeshore, TB in urban, meningitis in ASALs)
- Do NOT provide definitive diagnosis. Frame as "possible" and "see a provider"
- DEMO disclaimer at the end"""
            try:
                resp = gemini(prompt, key)
                st.markdown(resp)
                st.caption("⚠️ DEMO: This is an educational tool only. Not a substitute for clinical diagnosis.")
            except Exception as e:
                st.error(f"AI error: {e}")

# ─────────────────────────────────────────────────────────────
# MODULE 5: FREE CHAT
# ─────────────────────────────────────────────────────────────
else:
    st.title("💬 Ask AfyaAI")
    st.markdown("*General health questions — Kenya health system context*")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a health question...")
    if user_input and key:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history_text = "\n".join(
                    f"{m['role'].title()}: {m['content']}"
                    for m in st.session_state.chat_history[-6:]
                )
                prompt = f"""You are AfyaAI, a friendly and knowledgeable Kenya health assistant.
You specialise in: maternal health, NHIF/SHA navigation, Kenya health system, common diseases in Kenya (malaria, TB, typhoid), nutrition.

Conversation history:
{history_text}

Respond to the latest user message. Be:
- Warm and supportive
- Specific to Kenya context
- Clear about what requires professional consultation
- Practical (mention specific facilities, programmes, costs where relevant)
- Brief (2-4 paragraphs max)

Always end with: whether they should see a healthcare provider, and if so, at which level."""
                try:
                    resp = gemini(prompt, key)
                    st.markdown(resp)
                    st.session_state.chat_history.append({"role": "assistant", "content": resp})
                except Exception as e:
                    st.error(f"AI error: {e}")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("AfyaAI © 2026 | [GitHub](https://github.com/gabrielmahia/afyaai) | [East African Decision Infrastructure](https://gabrielmahia.github.io) | contact@aikungfu.dev")
st.caption("⚠️ This tool provides educational health information only. It is not a substitute for professional medical advice, diagnosis, or treatment.")
