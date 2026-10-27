# 🛡️ BrandGuard: Explainable, Evidence-Checked Brand Governance

**Codex 48 – National Level Hackathon | Round 2: The Build**
Organised by We Code Coders

> Protect your brand. Catch risky claims before they go public. Keep humans in control.

> **Note:** BrandGuard is a decision-support prototype. AI findings are advisory and it does not replace human or legal review.

## 🔗 Live links

| What | Link |
|---|---|
| Live demo (web app) | https://brand-guard-alpha.vercel.app |
| Source code | https://github.com/khushiiiiiiii153/BrandGuard.git |

## 👥 Team Visionaries (Dream · Innovate · Build)

| Name | Role |
|---|---|
| Yogesh Mondhe | Team Leader (architecture, AI and backend) |
| Khushi Wanjari | Team Member (UI/UX, research and testing) |

Anjuman College of Engineering and Technology, Nagpur | Department of Computer Science and Engineering

## 📌 Problem statement

Organisations no longer publish content through one team. Employees, agencies, freelancers and AI writing tools all produce posts, ads and documents at the same time, while the brand rulebook, approved facts and logo files sit in different places. This causes three problems:

1. **Unsupported claims:** "India's No.1" or "30% faster" go live with no proof.
2. **Outdated information:** old prices, expired offers and discontinued features keep reappearing because old templates are never re-checked.
3. **Inconsistent voice and visuals:** wrong tone, off-palette colours, low contrast and missing alt text, because long PDF style guides get skimmed.

The Advertising Standards Council of India (ASCI) reported that 56% of scrutinised ads were misleading in its 2024–25 annual report, so claims reaching the public before anyone verifies them is a real and costly problem.

## 💡 Our solution

BrandGuard is a **pre-publication checkpoint**: the layer between "content written" and "content published". It checks content against the company's own brand rules and approved facts, explains every issue with its source, suggests fixes that keep the creator's purpose, and sends everything through a human review and approval workflow.

**Not in scope:** generating marketing copy, posting to social platforms, or replacing legal review.

## ✨ What we built in Round 2

| Module | Status | What it does |
|---|---|---|
| Brand Library Manager | ✅ Completed | Full CRUD portal for tone rules, banned terms, approved facts and colour swatches |
| Hybrid Rule + AI Engine | ✅ Completed | Python rule engine for exact checks, plus the Gemini API for contextual tone checking |
| Evidence Validator | ✅ Completed | Drops any AI finding that does not quote real text or cite a real rule |
| 3-Tier Fix Engine | ✅ Completed | Minimal, Moderate and Full Rewrite suggestions that keep the original intent |
| Multi-Role Approval Workflow | ✅ Completed | Creator / Manager / Admin roles, comments, approve or request changes, side-by-side version diff |
| PII Privacy Scrubber | ✅ Completed | Masks emails, phone numbers and keys before any external LLM call |
| Image Brand Check | ✅ Completed | Palette extraction, WCAG contrast calculation and missing alt-text flags |


## 🧠 What makes it different

1. **Evidence-Checked AI:** exact checks (banned terms, colours, contrast) run as normal code. The AI handles only tone and meaning, must answer in a fixed JSON format, and the validator discards any finding without an exact quote and a valid rule ID. Result: fewer invented flags, and every result can be verified.
2. **Human-in-the-loop:** AI only suggests, humans decide. Low-confidence findings are routed to a reviewer instead of being shown as facts. Nothing is ever applied automatically.
3. **Privacy by design:** sensitive details are redacted before any external AI call, and every AI use is logged with model name, timestamp and redacted data.

## 🔄 How it works

1. **Brand library setup:** Admin defines tone rules, banned terms, approved facts, colour swatches and claim proofs.
2. **Content submitted:** Creator pastes text or uploads .docx / .pdf / image (saved as v1).
3. **Safe pre-processing:** text is extracted and the PII redactor masks emails, phones and secrets.
4. **Hybrid review:** rule engine plus Gemini LLM check the content, and the Evidence Validator filters invalid findings.
5. **Explain and suggest:** Creator sees each finding with reason, source, severity, confidence and 3 fix options, and accepts or rejects each.
6. **Human review:** Manager checks the version diff, adds comments, then approves or requests changes.
7. **Final approval:** approved version, history and AI-usage log are stored.
8. **Insights loop:** recurring issues and dismissals are fed back to the Admin.

Status flow: Draft → Checked → Submitted → Changes requested (back to Draft) → Approved → Ready to publish.

## 🏗️ System architecture
[ UI Layer - Role Based Screens ]
      |
      v
+-------------------------------------------------------------+
|  Rule Engine      |  Source Retrieval   |  AI Orchestrator     |
|  (terms, contrast,|  (TF-IDF + keyword |  (Gemini, strict    |
|   alt text)       |   match)            |   JSON output)       |
+-------------------------------------------------------------+
      |
      v
[ Evidence Validator ] - Drops findings without real rule + exact quote
      |
      v
+-------------------------------------------------------------+
|  Workflow Engine  |  Privacy Layer (PII Redaction + AI-usage Log) |
+-------------------------------------------------------------+
      |
      v
[ SQLite Database + Local File Store ]
Guidelines, Approved Facts, Content Versions, Audit Logs

## 🛠️ Tech stack

| Layer | Tool | Used for |
|---|---|---|
| Language / backend | Python 3 | Application logic, rule engine, validator |
| Interface | Streamlit | Multi-role web app with session state |
| AI review | Google Gemini 1.5 Flash | Tone and meaning checks, returned as structured JSON |
| Retrieval | TF-IDF + keyword match | Fetching only relevant brand rules into the AI prompt |
| Database | SQLite3 | Guidelines, approved facts, version diffs, audit logs |
| Files and images | Pillow, pdfplumber, python-docx | Text extraction, colour palette and contrast checks |
| Version control | Git and GitHub | Source control |

## 🧪 Example

**Input:**

```text
Our product is guaranteed to deliver results and is 30% faster.
```

**Finding:**

- Flagged text: `guaranteed`, `30% faster`
- Reason: matches a restricted-term rule and an unsupported claim with no approved proof
- Source: Brand Library (rule ID and exact quote shown)
- Severity and confidence: shown for every finding
- Fix options: Minimal, Moderate, Full Rewrite (the creator chooses, nothing is auto-applied)

A finding means a *potential* issue under the configured rules. It does not by itself prove that a claim is false or legally non-compliant.

## 📊 Round 2 results (prototype testing)

| Metric | Result |
|---|---|
| Review time per post | Reduced by 72% (about 15 min to 4 min) |
| Violation detection | 91% on a seeded test set of 40 posts |
| Audit coverage | 100% across revisions |
| User research | 6 interviews, 35+ survey responses, 5 testers |

Key insight from research: 82% of writers admit they skim brand guideline PDFs without checking for updates.

## 🚀 Getting started (run locally)

**Prerequisites:** Python 3 and pip. Git is optional.

```bash
git clone https://github.com/khushiiiiiiii153/BrandGuard.git
cd BrandGuard
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

**Gemini API key:** the AI tone check needs a Gemini API key, set as an environment variable (never commit keys to the repository). Without it, the rule-based checks still work.

## 🔮 Round 3 roadmap

1. **Claim Evidence Vault:** link each claim to a proof document with an expiry date, and automatically re-flag pending drafts when proof expires.
2. **Guideline Health:** track rule dismissals and reviewer overrides to find ambiguous guidelines and suggest clearer wording to the Admin.
3. **Hindi and Hinglish support:** localized prompts and term matching for regional marketing copy.

## ⚠️ Known limitations

- Multi-column PDF layouts may need manual copy-paste for text extraction.
- Concurrent editing uses database locking instead of real-time web-sockets.
- AI findings are advisory and English-first.
- Prototype is tested on a fictional sample brand, because real brand data is confidential.

## 🔐 Responsible design

- **Privacy:** emails, phone numbers and custom secrets are masked before external API calls.
- **Prompt-injection safety:** submitted content is treated strictly as data, never as instructions, and AI output must pass the schema and evidence validator.
- **Human oversight:** AI never edits, approves or publishes content. A manager must approve.
- **Transparency:** each finding shows its rule, exact quote and confidence, and the AI service used is disclosed.

## 🙏 Acknowledgements

Open-source libraries: Streamlit, Pillow, pdfplumber, python-docx, SQLite, scikit-learn style TF-IDF retrieval. AI service used: Google Gemini (disclosed in the app). Advertising data: ASCI annual and half-yearly complaints reports.

Built by **Team Visionaries** for **Codex 48 – National Level Hackathon, Round 2: The Build**.

## 📄 License

A license has not been specified yet. Add a `LICENSE` file before distributing as open source.
