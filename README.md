# MedHistory

**Open-source clinical safety and drug-interaction co-pilot — hackathon prototype**

MedHistory demonstrates a local-first workflow for reviewing prescription text against an active medication history. It includes a Streamlit UI, optional OCR, transparent dictionary-based medication extraction, a deterministic JSON interaction matrix, and a physician-query export.

## Current implementation

- Streamlit interface with two judge-demo presets.
- Paste prescription text or upload a PNG/JPG.
- Optional local OCR through Tesseract + pytesseract.
- Fast dictionary-based extraction of a small set of common drug names, conditions, and dosage strings.
- Deterministic matching against `data/ddi_rules.json`.
- Downloadable physician-query summary and JSON report.
- Agent Skill Open Standard-style `SKILL.md` and CLI script.

## Important scope note

This is a hackathon prototype, **not clinical software**. The included interaction matrix is small and illustrative, not a complete or independently validated clinical database. “No configured interaction found” does not mean a combination is safe. A clinician or pharmacist must review all findings.

The fast UI path deliberately uses dictionary extraction to make the demo predictable. `engine/biobert_ner.py` includes an optional Hugging Face disease NER model, but the selected model is not a dedicated drug NER model. Do not claim that the application uses BioBERT to reliably extract every medication unless you implement and validate a suitable medication NER model.

## Requirements

- Python 3.10+
- macOS / Windows / Linux
- Optional OCR: Tesseract installed on the operating system
- Internet is required initially if pip packages or model weights need downloading; the fast demo does not need model weights.

## Setup on macOS

From the folder containing `app.py`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Optional OCR installation on macOS with Homebrew:

```bash
brew install tesseract
```

Start the app:

```bash
streamlit run app.py
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

## Demo flow

1. Click **Preset A · Warfarin + Aspirin** in the sidebar.
2. Click **Analyze medication safety**. Confirm a red alert appears.
3. Click **Preset B · Metformin + Amoxicillin**.
4. Click **Analyze medication safety**. The demo should report no matching interaction in its current rules.
5. Download the Physician Query Summary.

The second result is not a guarantee of safety; it means only that this limited matrix has no matching rule for that pair.

## Run the agent skill CLI

From the repository root:

```bash
python .agents/skills/medhistory-ddi/scripts/check_ddi.py --new "Aspirin" --history "Warfarin"
```

## Repository layout

```text
MedHistory/
├── .agents/skills/medhistory-ddi/
│   ├── SKILL.md
│   └── scripts/check_ddi.py
├── data/ddi_rules.json
├── engine/
│   ├── __init__.py
│   ├── biobert_ner.py
│   ├── ocr_reader.py
│   └── safety_checker.py
├── app.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Privacy

The demo processes pasted text and OCR locally in the Streamlit process. Do not input identifiable patient information. Review deployment settings, telemetry, logs, storage, and dependencies before making any privacy or compliance claim. “Local-first” is not a certification of HIPAA compliance.

## Data and attribution

- The interaction matrix in `data/ddi_rules.json` is demo content and requires independent clinical validation before real use.
- The optional disease NER model is `alvaroalon2/biobert_diseases_ner`; its model card and license should be checked before redistribution.
- Do not represent `dmis-lab/biobert-v1.1` as a ready-made token-classification medication extractor without adding an appropriate fine-tuned token-classification head and validating it.
- This project is intended to be released under Apache-2.0; review third-party model/data licenses separately.

## Roadmap

- Replace the demo matrix with a properly sourced, versioned, clinically reviewed interaction dataset.
- Add confidence display and human confirmation for OCR/NER.
- Implement validated medication NER.
- Add test coverage, provenance links, and audit logs without retaining unnecessary PHI.
- Explore FHIR interoperability and ONNX Runtime only after the core workflow is validated.
