import json
from datetime import datetime
import streamlit as st
from engine.biobert_ner import ClinicalNER
from engine.ocr_reader import extract_text_from_image
from engine.safety_checker import SafetyEngine

st.set_page_config(page_title="MedHistory", page_icon="💊", layout="wide")
st.title("💊 MedHistory")
st.caption("Open-source clinical safety and drug-interaction co-pilot • Local-first demo")

st.warning(
    "Hackathon prototype only — not a medical device or a substitute for clinician/pharmacist review. "
    "A green result means only that this demo rule set found no configured interaction."
)

if "active_history" not in st.session_state:
    st.session_state.active_history = "Warfarin"
if "report" not in st.session_state:
    st.session_state.report = None

with st.sidebar:
    st.header("Patient medication history")
    history_text = st.text_area(
        "Current medicines (comma-separated)",
        value=st.session_state.active_history,
        height=100,
        help="Demo data only. Avoid entering real patient identifiers or sensitive records."
    )
    st.session_state.active_history = history_text
    st.divider()
    st.subheader("Demo presets")
    if st.button("Preset A · Warfarin + Aspirin", use_container_width=True):
        st.session_state.active_history = "Warfarin 5 mg"
        st.session_state.demo_text = "New prescription: Aspirin 325 mg for pain relief."
        st.rerun()
    if st.button("Preset B · Metformin + Amoxicillin", use_container_width=True):
        st.session_state.active_history = "Metformin 500 mg"
        st.session_state.demo_text = "New prescription: Amoxicillin 500 mg."
        st.rerun()
    st.caption("Rule set: local JSON file • Model download may occur on first use if enabled.")

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("1 · Prescription ingestion")
    uploaded = st.file_uploader("Upload prescription image", type=["png", "jpg", "jpeg"])
    if uploaded:
        st.image(uploaded, caption="Uploaded document", use_container_width=True)
    default_text = st.session_state.pop("demo_text", "")
    clinical_text = st.text_area(
        "Or paste OCR / prescription text",
        value=default_text,
        height=160,
        placeholder="Example: Aspirin 325 mg. Patient currently takes Warfarin."
    )
    if uploaded and st.button("Run local OCR", use_container_width=True):
        extracted, error = extract_text_from_image(uploaded)
        if error:
            st.error(error)
        else:
            st.session_state.ocr_text = extracted
            st.success("OCR completed. Review the extracted text before analysis.")
            st.code(extracted)
    if st.button("Analyze medication safety", type="primary", use_container_width=True):
        source_text = clinical_text.strip()
        if not source_text and uploaded:
            source_text, error = extract_text_from_image(uploaded)
            if error:
                st.error(error)
        if not source_text:
            st.error("Upload an image or paste prescription text first.")
        else:
            with st.spinner("Extracting entities and checking the local rule matrix…"):
                ner = ClinicalNER(use_model=False)
                entities = ner.extract_entities(source_text)
                # Separate strength strings from names so pair matching can work.
                new_drugs = entities["drugs"]
                history = [x.strip() for x in st.session_state.active_history.split(",") if x.strip()]
                engine = SafetyEngine()
                alerts = engine.check(new_drugs, history)
                status = "CRITICAL" if any(x["severity"] == "CRITICAL" for x in alerts) else (
                    "CAUTION" if alerts else "NO_CONFIGURED_INTERACTION_FOUND"
                )
                st.session_state.report = {
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "source_text": source_text,
                    "extracted_entities": entities,
                    "active_medications": history,
                    "new_drugs": new_drugs,
                    "status": status,
                    "safety_alerts": alerts,
                    "disclaimer": "Prototype output; requires clinician/pharmacist review."
                }

with right:
    st.subheader("2 · Safety analysis")
    report = st.session_state.report
    if not report:
        st.info("Run a preset or analyze a prescription to see extracted entities and safety alerts.")
    else:
        if report["status"] == "CRITICAL":
            st.error("🚨 RED ALERT · Potential high-priority interaction")
        elif report["status"] == "CAUTION":
            st.warning("🟠 AMBER ALERT · Review required")
        else:
            st.success("🟢 NO CONFIGURED INTERACTION FOUND")
        e1, e2, e3 = st.columns(3)
        e1.metric("Drugs extracted", len(report["extracted_entities"]["drugs"]))
        e2.metric("Conditions", len(report["extracted_entities"]["conditions"]))
        e3.metric("Dosages", len(report["extracted_entities"]["dosages"]))
        st.write("**Extracted drugs:**", ", ".join(report["extracted_entities"]["drugs"]) or "None detected")
        st.write("**Conditions:**", ", ".join(report["extracted_entities"]["conditions"]) or "None detected")
        st.write("**Dosages:**", ", ".join(report["extracted_entities"]["dosages"]) or "None detected")
        st.divider()
        st.markdown("#### Drug-interaction findings")
        if report["safety_alerts"]:
            for alert in report["safety_alerts"]:
                heading = f'{alert["risk_title"]} — {alert["new_drug"]} ↔ {alert["history_drug"]}'
                if alert["severity"] == "CRITICAL":
                    st.error(heading)
                else:
                    st.warning(heading)
                st.write("**Mechanism:**", alert["mechanism"])
                st.write("**Suggested next step:**", alert["clinical_action"])
        else:
            st.info("No matching pair was found in this small demo rule matrix. This is not proof that the combination is safe.")
        query = f"""MEDHISTORY — PHYSICIAN QUERY SUMMARY
Generated: {report['created_at']}

Reason for review:
Medication reconciliation / possible drug interaction.

Current medication history:
{', '.join(report['active_medications']) or 'Not provided'}

New medication entities extracted:
{', '.join(report['new_drugs']) or 'None detected'}

System result:
{report['status']}

Findings:
"""
        if report["safety_alerts"]:
            for a in report["safety_alerts"]:
                query += f"\n- {a['new_drug']} + {a['history_drug']}: {a['severity']} — {a['risk_title']}\n  Mechanism: {a['mechanism']}\n  Suggested review: {a['clinical_action']}\n"
        else:
            query += "\n- No matching interaction in the configured demo rule matrix. This does not rule out other risks.\n"
        query += "\nPlease verify the complete medication list, doses, allergies, indications, renal/hepatic function, and relevant monitoring.\n"
        query += "\nPrototype only; not a diagnosis or treatment recommendation.\n"
        st.download_button(
            "⬇ Download Physician Query Summary",
            data=query,
            file_name="medhistory_physician_query.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.download_button(
            "⬇ Download analysis JSON",
            data=json.dumps(report, indent=2),
            file_name="medhistory_analysis.json",
            mime="application/json",
            use_container_width=True
        )

with st.expander("Project limitations and privacy notes"):
    st.markdown("""
- The included drug dictionary and DDI matrix are deliberately small demonstration data, not a complete clinical database.
- OCR may misread medicine names or strengths; review extracted text before use.
- This demo uses dictionary-based drug extraction. Optional biomedical disease NER is available in `engine/biobert_ner.py`, but is not enabled in the fast demo path.
- Local-first does not automatically mean fully offline: dependencies/model weights may need downloading during setup. After setup, disable network access only after confirming all assets are present.
- Do not enter real patient-identifying information in the hackathon demo.
""")
