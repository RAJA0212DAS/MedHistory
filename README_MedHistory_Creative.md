::: {align="center"}
# 🩺 MedHistory

### Turn scattered medication history into clearer safety signals.

**An open-source, local-first prototype for prescription text extraction
and rule-based drug--drug interaction (DDI) checks.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Open
Source](https://img.shields.io/badge/Open%20Source-Community%20Driven-20BFA9?style=for-the-badge&logo=github&logoColor=white)](LICENSE)

*Read. Match. Flag. Review.*
:::

------------------------------------------------------------------------

## 💡 Why MedHistory?

Medication details can live in handwritten prescriptions, uploaded
images, discharge notes, and patient-reported lists. Comparing those
sources manually can be slow---and a missed interaction deserves
attention.

**MedHistory is a prototype built to make that review workflow more
structured.** It accepts medication text or a prescription image,
identifies candidate drug names, compares them against a configurable
set of interaction rules, and presents explainable alerts for human
review.

> **The goal:** help people inspect medication information---not replace
> a qualified healthcare professional.

## ✨ What it can do

  -----------------------------------------------------------------------
  Feature                             What it means
  ----------------------------------- -----------------------------------
  📝 Text input                       Paste medication names or
                                      prescription text into the app.

  🖼️ Image input                      Upload a prescription image; local
                                      OCR can extract its text.

  🔎 Medication matching              Identify candidate medicine names
                                      using the prototype's matching
                                      logic.

  ⚖️ Rule-based DDI checks            Compare detected medicines with the
                                      rules in `data/ddi_rules.json`.

  🚦 Severity signals                 Display configured interaction
                                      severity and explanation.

  📄 Exportable results               Download analysis output for review
                                      and debugging.

  🧰 Command-line skill               Run a medication-pair check from
                                      the terminal.

  🏠 Local-first workflow             Run the prototype on your own
                                      machine; avoid sending prescription
                                      images to a hosted AI service by
                                      default.
  -----------------------------------------------------------------------

**Current implementation note:** medication matching in the demo is
dictionary-based. The optional biomedical NER component is experimental
and is not a validated medication-specific NER system. OCR depends on a
local Tesseract installation.

## 🧭 How the workflow works

``` text
Prescription image or pasted text
                │
                ▼
       Optional local OCR
                │
                ▼
     Candidate medicine matching
                │
                ▼
      Configured DDI rule engine
                │
                ▼
   Severity + explanation + report
                │
                ▼
       Human / clinician review
```

The interaction checker uses explicit rules rather than asking a
generative model to invent an interaction. This makes configured results
easier to inspect and reproduce. However, the quality of the result
still depends on the completeness and accuracy of the rules and the
extracted medicine names.

## 🧪 Try the demo

The app includes two useful demonstration scenarios:

-   **Scenario A --- Warfarin + Aspirin:** the sample rule set is
    expected to raise a configured critical alert.
-   **Scenario B --- Metformin + Amoxicillin:** the current sample rules
    contain no configured interaction for this pair, so the demo should
    report no matching rule.

⚠️ **"No matching rule found" does not mean "safe."** The rule set is a
small demonstration dataset, not a comprehensive interaction database.

## 🚀 Get started

### 1. Requirements

-   Python 3.10 or newer recommended
-   `pip`
-   Optional: [Tesseract
    OCR](https://github.com/tesseract-ocr/tesseract) for image text
    extraction

### 2. Download and enter the project

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd MedHistory
```

If you downloaded the project ZIP instead, extract it and open the
`MedHistory` folder in VS Code.

### 3. Create a virtual environment

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

``` powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Optional: enable OCR

On macOS with Homebrew:

``` bash
brew install tesseract
```

Confirm that it is available:

``` bash
tesseract --version
```

OCR may not work until Tesseract is installed and discoverable on your
system's `PATH`.

### 6. Launch MedHistory

``` bash
streamlit run app.py
```

Streamlit will print a local URL---usually
`http://localhost:8501`---that you can open in your browser.

## ⌨️ Run the interaction checker from the terminal

From the project root, try the sample CLI:

``` bash
python .agents/skills/medhistory-ddi/scripts/check_ddi.py \
  --new "Aspirin, Paracetamol" \
  --history "Warfarin, Atorvastatin"
```

The CLI compares the supplied names with the configured rules in
`data/ddi_rules.json`. Results only reflect rules currently present in
that file.

## 🗂️ Project map

``` text
MedHistory/
├── .agents/
│   └── skills/
│       └── medhistory-ddi/
│           ├── SKILL.md
│           └── scripts/
│               └── check_ddi.py
├── data/
│   └── ddi_rules.json
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

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `app.py`                            Streamlit interface and analysis
                                      flow

  `engine/ocr_reader.py`              Optional image-to-text extraction

  `engine/biobert_ner.py`             Experimental biomedical
                                      entity-extraction component

  `engine/safety_checker.py`          Rule matching and alert generation

  `data/ddi_rules.json`               Small, editable set of example
                                      interaction rules

  `check_ddi.py`                      Command-line interaction checker

  `SKILL.md`                          Documents the reusable MedHistory
                                      DDI skill
  -----------------------------------------------------------------------

## 🛡️ Privacy, safety, and limitations

MedHistory is designed around a local-first demo workflow, but **local
execution alone is not a complete privacy or security guarantee**.
Review dependencies, logs, downloads, backups, and the environment where
you run it before using any sensitive information.

Please keep these limitations in mind:

-   This is a **research and hackathon prototype**, not a certified
    medical device.
-   The sample interaction rules are limited and have not been presented
    as a comprehensive, clinically validated database.
-   OCR and medicine-name extraction can misread, omit, or confuse drug
    names, strengths, and dosage instructions.
-   A configured alert is a signal for review, not a diagnosis or
    individualized treatment recommendation.
-   An absent alert does not rule out an interaction or other
    medication-related risk.
-   Do not use the prototype to make treatment decisions or to
    prescribe, start, stop, or change medication.
-   Do not upload identifiable patient information unless you have the
    appropriate authorization and safeguards.

For real clinical use, the project would need qualified clinical
oversight, validated and maintained interaction data, rigorous testing,
privacy and security review, and an appropriate regulatory assessment.

## 🧱 Roadmap

-   [ ] Add unit tests for rule matching, normalization, and edge cases.
-   [ ] Expand the rule set using trustworthy, traceable clinical
    sources and expert review.
-   [ ] Evaluate medication-specific NER models against a labeled test
    dataset.
-   [ ] Add confidence indicators and a clear path to correct extracted
    medicine names.
-   [ ] Improve OCR handling for low-quality and handwritten
    prescriptions.
-   [ ] Add versioning, provenance, and update dates for each
    interaction rule.
-   [ ] Create regression fixtures for the demo scenarios.
-   [ ] Conduct privacy, security, usability, and clinical validation
    before any real-world deployment.

## 🤝 Contributing

Contributions are welcome---especially improvements that make the
prototype more transparent, testable, and safe.

1.  Fork the repository.
2.  Create a focused branch: `git checkout -b feat/your-improvement`
3.  Make your change and add tests where possible.
4.  Run the app and CLI locally.
5.  Open a pull request describing the change, its evidence, and any
    limitations.

**High-value contributions:** rule provenance, reproducible tests,
medication-name evaluation datasets, OCR robustness, accessibility,
documentation, and clinician-reviewed safety guidance.

Please do not contribute unverified interaction claims as if they were
established clinical facts. When adding a rule, document its source,
review date, scope, and limitations.

## 🌱 Open source, built to be questioned

The most important part of a safety tool is not how confident it
sounds---it is whether people can inspect what it does, test how it
behaves, and understand what it cannot tell them.

Explore the code. Challenge the rules. Improve the tests. Help make the
limitations visible.

::: {align="center"}
### **MedHistory --- clearer signals, human judgment.**

*Built for learning, experimentation, and open-source collaboration.*
:::

------------------------------------------------------------------------

## 📜 License

See [`LICENSE`](LICENSE) for the project's license terms.
