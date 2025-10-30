# SECURAA Security Documentation

This repository contains comprehensive security documentation for the SECURAA platform, including tools to export documentation to PDF format.

## 📚 Documentation

### Security Documents

1. **Platform Security Documentation** (`secura-customer-security-documentation.md`)
   - Comprehensive Security Framework and Compliance Readiness Guide
   - Security architecture and controls
   - Data protection and privacy measures
   - Compliance readiness status
   - Customer security benefits

2. **Information Security Risk Assessment Process** (`securaa-information-security-risk-assesment-process.md`)
   - Documented and approved risk assessment framework
   - Risk identification and analysis methodology
   - Risk treatment and mitigation strategies
   - Compliance and audit requirements

## 🔧 PDF Export Feature

### Prerequisites

- **pandoc** (v3.1 or higher) - Universal document converter
- **wkhtmltopdf** (v0.12 or higher) - HTML to PDF converter
- **bash** - Shell scripting environment

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd customers-docs
```

2. Install system dependencies:
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y pandoc wkhtmltopdf

# On macOS with Homebrew
brew install pandoc
brew install --cask wkhtmltopdf

# On other systems, refer to:
# - Pandoc: https://pandoc.org/installing.html
# - wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
```

### Usage

#### Export All Documents to PDF

To export all security documents to PDF format:

```bash
# Using the shell script directly
bash export-to-pdf.sh

# Or using npm (if package.json is configured)
npm run export-pdf
```

#### Export Specific Document

To export a specific document:

```bash
bash export-to-pdf.sh secura-customer-security-documentation.md
bash export-to-pdf.sh securaa-information-security-risk-assesment-process.md
```

#### Show Help

```bash
bash export-to-pdf.sh --help
```

### Output

Generated PDF files are saved in the `pdf-exports/` directory:
- `SECURAA-Platform-Security-Documentation.pdf`
- `SECURAA-Information-Security-Risk-Assessment-Process.pdf`

### Features

✅ **Professional Formatting**
- Clean, professional layout optimized for printing
- Proper page margins and breaks
- Styled headers, tables, and code blocks
- Table of contents with page numbers

✅ **Comprehensive Conversion**
- Converts all markdown elements (tables, lists, code blocks, etc.)
- Preserves document structure and hierarchy
- Handles complex nested content
- Processes both documents in seconds

✅ **Automated Processing**
- Batch export all documents with one command
- Individual document export on demand
- Progress indicators and status messages
- Automatic handling of external images

✅ **High Quality Output**
- SECURAA brand colors (#0066CC blue)
- Professional typography
- Print-optimized styling
- Accessible PDF format

### Technical Details

The export tool uses:
- **Pandoc**: Converts markdown to HTML5
- **wkhtmltopdf**: Renders HTML to PDF using WebKit
- **Custom CSS**: Applies SECURAA branding and styling
- **Bash Script**: Orchestrates the conversion process

The tool automatically:
- Removes external image links that may fail (like placeholder images)
- Generates a table of contents
- Applies consistent styling across all documents
- Handles mermaid diagrams (displayed as formatted code blocks)

### Notes

- **Mermaid Diagrams**: Complex mermaid diagrams in the markdown files are displayed as formatted code blocks in the PDF. For full diagram rendering, you would need additional setup with mermaid-cli or similar tools.
- **External Images**: External placeholder images (like `via.placeholder.com`) are automatically removed during conversion to avoid network-related failures.
- **Performance**: Both documents (totaling ~50+ pages) export in under 20 seconds.

## 📝 Document Information

### Security Classification
- **Classification**: Customer Facing / Internal Use
- **Distribution**: Authorized personnel and customers under appropriate agreements
- **Review Frequency**: Quarterly to annually

### Document Versions
- **Platform Security Documentation**: Version 1.0 (October 2025)
- **Risk Assessment Process**: Version 1.0 (October 2025)

## 🔒 Security Notice

These documents contain proprietary and confidential information about SECURAA's security framework and processes. Distribution should be limited to:
- Authorized SECURAA personnel
- Customers under appropriate agreements
- Auditors and compliance assessors (as needed)

## 🛠️ Development

### Project Structure
```
customers-docs/
├── .gitignore                                           # Git ignore file
├── package.json                                         # Node.js metadata (optional)
├── export-to-pdf.sh                                     # PDF export shell script
├── pdf-style.css                                        # CSS styling for PDFs
├── README.md                                            # This file
├── secura-customer-security-documentation.md           # Security documentation
├── securaa-information-security-risk-assesment-process.md  # Risk assessment
└── pdf-exports/                                         # Generated PDFs (gitignored)
    ├── SECURAA-Platform-Security-Documentation.pdf
    └── SECURAA-Information-Security-Risk-Assessment-Process.pdf
```

### Adding New Documents

To add new documents for PDF export, edit the `DOCUMENTS` array in `export-to-pdf.sh`:

```bash
declare -A DOCUMENTS
DOCUMENTS=(
  ["your-document.md"]="Your-Document-Title.pdf"
  # Add more documents here
)
```

### Customizing PDF Styling

PDF styling can be customized by editing the `pdf-style.css` file. The CSS controls:
- Fonts and typography (default: Segoe UI, 11pt)
- Colors and branding (SECURAA blue: #0066CC)
- Page layout and margins (20mm all sides)
- Table and code block styling
- Heading hierarchy and formatting

### System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Disk Space**: ~50MB for dependencies, ~500KB for generated PDFs
- **Memory**: 256MB minimum for PDF generation
- **Time**: ~10 seconds per document on average hardware

## 📞 Contact

For questions about the security documentation or PDF export feature:

📧 **Email**: security@securaa.com  
📞 **Phone**: +1-800-SECURAA (+1-800-732-8722)  
🌐 **Website**: www.securaa.com/security  
💬 **Support Portal**: support.securaa.com

## 📄 License

Copyright © 2025 SECURAA. All rights reserved.

---

**Last Updated**: October 2025
