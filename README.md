# SECURAA Customer Documentation

Comprehensive security documentation for SECURAA SOAR platform customers.

## Repository Structure

```
customers-docs/
├── docs/
│   ├── source/                    # Markdown source files
│   │   ├── sdlc/                  # SDLC Documentation
│   │   │   ├── 01_SDLC_Overview.md
│   │   │   ├── 02_Requirements_Phase.md
│   │   │   ├── 03_Design_Phase.md
│   │   │   ├── 04_Development_Phase.md
│   │   │   ├── 05_Testing_Build_Deployment_Operations.md
│   │   │   ├── 06_CI_CD_Security_Pipeline.md
│   │   │   └── README.md
│   │   ├── architecture/          # Architecture Documentation
│   │   │   ├── HA_DR_Architecture_Documentation.md
│   │   │   ├── HA_DR_Architecture_Documentation_dt3.md
│   │   │   └── SOAR_Architecture_SIEM_TI_Integration_Documentation.md
│   │   ├── security/              # Security Policies
│   │   │   ├── SECURAA_SECURE_CODING_POLICY.md
│   │   │   ├── SECURAA_CODE_ANALYSIS_REPORT.md
│   │   │   └── secura-customer-security-documentation.md
│   │   └── compliance/            # Compliance & Risk
│   │       ├── securaa-information-security-risk-assesment-process.md
│   │       └── securaa-sdlc-process.md
│   └── distribution/              # Customer-ready files
│       ├── index.html             # Documentation portal
│       ├── pdf/                   # PDF documents
│       ├── html/                  # HTML documents
│       └── images/                # Rendered diagrams (SVG)
└── README.md
```

## Quick Start

### View Documentation Portal

Open `docs/distribution/index.html` in a web browser to access the full documentation portal with:
- Categorized navigation
- PDF downloads
- HTML viewing
- Complete document index

### Document Categories

| Category | Description | Location |
|----------|-------------|----------|
| **SDLC** | Secure Development Lifecycle | `docs/source/sdlc/` |
| **Architecture** | System & HA/DR Architecture | `docs/source/architecture/` |
| **Security** | Policies & Standards | `docs/source/security/` |
| **Compliance** | Risk Assessment & Processes | `docs/source/compliance/` |

## Distribution Files

The `docs/distribution/` folder contains customer-ready documentation:

- **15 PDF documents** - Professional formatted PDFs with diagrams
- **15 HTML documents** - Web-viewable documentation
- **85 SVG diagrams** - Rendered architecture and workflow diagrams
- **index.html** - Interactive documentation portal

## Contents

### SDLC Documentation
1. SDLC Overview - Executive summary and principles
2. Requirements Phase - Security requirements & threat modeling
3. Design Phase - Secure architecture design
4. Development Phase - Coding standards & Git workflow
5. Testing & Deployment - Security testing & CI/CD
6. CI/CD Security Pipeline - Automated security gates

### Architecture Documentation
- HA/DR Architecture - High availability & disaster recovery
- SOAR Architecture - Platform architecture with SIEM/TI integration

### Security Documentation
- Secure Coding Policy - Development security standards
- Code Analysis Report - Security assessment findings
- Customer Security Doc - Customer-facing security overview

### Compliance Documentation
- Risk Assessment Process - Information security risk management
- SDLC Process - Complete development lifecycle process

## Usage

### For Customers
1. Open `docs/distribution/index.html` in a browser
2. Browse documentation by category
3. Download PDFs or view HTML versions

### For Internal Teams
1. Source markdown files are in `docs/source/`
2. Edit markdown files as needed
3. Regenerate PDFs using build scripts if modified

## Confidentiality

This documentation is **Confidential** and intended for:
- SECURAA customers under NDA
- Internal SECURAA teams
- Authorized security assessors

Not for public distribution.

## Contact

- **Security Team**: security@securaa.com
- **Engineering Team**: engineering@securaa.com
- **Documentation Feedback**: sdlc-feedback@securaa.com

---

*SECURAA - Security Orchestration, Automation and Response*
*Document Version: 2.0 | Last Updated: December 2025*
