# Customers Documentation

This repository contains technical documentation for various security architecture and integration projects.

## Documentation Files

- `SOAR_Architecture_SIEM_TI_Integration_Documentation.md` - SOAR Platform Architecture and Integration documentation including Threat Intelligence (TI) feeds and SIEM integrations
- `HA_DR_Architecture_Documentation.md` - High Availability and Disaster Recovery Architecture
- `HA_DR_Architecture_Documentation_dt3.md` - High Availability and Disaster Recovery Architecture (DT3 variant)
- `secura-customer-security-documentation.md` - Customer Security Documentation
- `securaa-information-security-risk-assesment-process.md` - Information Security Risk Assessment Process

## Generating PDFs

This repository includes tools to generate PDF versions of the documentation with proper rendering of all diagrams and images.

### Prerequisites

- Node.js (v14 or higher)
- npm

### Installation

```bash
npm install
```

### Generate PDF

To generate a PDF from the TI and Integration documentation:

```bash
npm run generate-pdf
```

This will create `SOAR_Architecture_SIEM_TI_Integration_Documentation.pdf` with:
- All mermaid diagrams properly rendered
- Properly formatted tables
- No cut-off images or diagrams
- Professional styling and formatting

### Testing

To verify the PDF was generated correctly:

```bash
npm test
```

This will validate:
- PDF file exists and has reasonable size
- All mermaid diagrams are present in source
- Configuration files are properly set up

### PDF Generation Features

- **Automatic Mermaid Diagram Rendering**: All mermaid diagrams in the markdown are converted to images in the PDF
- **Page Break Control**: Tables, code blocks, and diagrams are kept together to avoid awkward splits
- **Responsive Sizing**: Diagrams are automatically scaled to fit within page width
- **Professional Styling**: Includes custom CSS for better readability

### Configuration

PDF generation settings can be customized in `.md2pdf.config.js`:
- Page size and margins
- Custom styling (via `pdf-styles.css`)
- Syntax highlighting themes
- Puppeteer launch options

### Manual Generation

You can also generate PDFs manually using:

```bash
node generate-pdf.js
```

## File Structure

```
.
├── .md2pdf.config.js              # PDF generation configuration
├── pdf-styles.css                 # Custom CSS for PDF styling
├── generate-pdf.js                # PDF generation script
├── package.json                   # Node.js dependencies
├── *.md                           # Markdown documentation files
└── *.pdf                          # Generated PDF files
```

## Notes

- Generated PDF files are not tracked in git (see `.gitignore`)
- The PDF generation process may take a few minutes for large documents with many diagrams
- Chrome/Chromium is required for PDF generation (used by Puppeteer)
