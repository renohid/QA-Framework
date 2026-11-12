# QA Automation Framework Assessment

This repository contains the completed UI and API automation assessment for 24Slides. It is built using Python, Playwright, and Pytest, focusing on clean architecture, parallel execution, and secure, automated authentication.

## 🛠 Tech Stack
* **Language:** Python 3
* **UI Automation:** Playwright
* **API Automation:** `requests` library
* **Testing Framework:** Pytest
* **Parallel Execution:** `pytest-xdist`
* **Reporting:** `pytest-html`

## 📁 Project Architecture
The framework uses a strict Page Object Model (POM) for UI tests and isolates API logic for maximum maintainability.

```text
QA/
├── api_tests/           # API test scenarios (Gmail API)
├── pages/               # Page Object Model classes (CCTV Malang)
├── tests/               # UI test scenarios
├── .env                 # Environment variables (Ignored in Git)
├── pytest.ini           # Pytest configuration
└── requirements.txt     # Python dependencies
