
# OWASP Juice Shop – Web Application Penetration Testing

## Project Overview

This project documents an authorized web application security assessment conducted against OWASP Juice Shop in a local Kali Linux lab environment.

The assessment demonstrates practical penetration-testing skills, including reconnaissance, API security testing, authentication checks, access-control testing, vulnerability documentation, and remediation recommendations.

**Target:** `http://127.0.0.1:3000`  
**Environment:** Kali Linux and Docker  
**Application:** OWASP Juice Shop  
**Assessment type:** Authorized local lab testing  
**Status:** Assessment completed; remediation retesting pending.

## Objectives

- Perform web application reconnaissance.
- Identify and inspect application API endpoints.
- Evaluate authentication and authorization behavior.
- Test object-level access controls using two controlled test accounts.
- Document potential input-handling and database error disclosure issues.
- Recommend security improvements.
- Produce a structured penetration-testing report.

## Tools and Technologies

- Kali Linux
- OWASP Juice Shop
- Docker
- Nmap
- WhatWeb
- cURL
- Python 3
- Git and GitHub

## Key Findings

### Finding 001 – Potential Database Error Disclosure

**Endpoint:** `/rest/products/search`  
**Parameter:** `q`  
**Status:** Potential issue; SQL injection not confirmed.

Certain combined special-character input caused an HTTP 500 response exposing a SQLite syntax error.

Further validation is required before classifying this as SQL injection.

### Finding 002 – Cross-Account Basket Access (IDOR/BOLA)

**Endpoint:** `GET /rest/basket/{basketId}`  
**Classification:** Broken Access Control  
**OWASP:** A01 – Broken Access Control  
**CWE:** CWE-639  
**Preliminary severity:** Medium  
**Status:** Confirmed in the local lab.

Testing with two controlled accounts demonstrated that Account 1 could retrieve Account 2's basket by requesting its basket ID.

The application returned HTTP 200 and the other basket's object details instead of denying access.

## Remediation Recommendations

- Enforce server-side ownership checks on every basket request.
- Verify the authenticated user's identity against the basket owner.
- Deny unauthorized cross-account access.
- Return HTTP 403 for authenticated users who do not own the requested object.
- Use parameterized database queries.
- Avoid exposing database error details to clients.
- Add automated authorization regression tests.

## Project Structure

```text
.
├── evidence/
│   ├── api/
│   ├── findings/
│   └── screenshots/
├── reconnaissance/
├── remediation/
├── reports/
├── create_pdf_report.py
└── README.md
```

## Deliverables

- Reconnaissance results
- API testing evidence
- Vulnerability finding documentation
- Cross-account access screenshot
- Remediation proposal
- PDF penetration-testing report

## Scope and Authorization

All testing documented in this repository was performed against a locally hosted OWASP Juice Shop instance under the project owner's control.

No third-party production application was targeted.

## Limitations

This is an educational portfolio assessment, not a commercial client engagement.

The remediation recommendations have not yet been implemented or retested. Finding 001 remains a potential issue and must not be interpreted as confirmed SQL injection.

## Author

GitHub: [@cybertraining07](https://github.com/cybertraining07)

## Disclaimer

This project is intended for cybersecurity education and authorized security testing only.
