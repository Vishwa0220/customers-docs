#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const mdToPdf = require('md-to-pdf').mdToPdf;

async function generatePDF() {
  try {
    const inputFile = 'SOAR_Architecture_SIEM_TI_Integration_Documentation.md';
    const outputFile = 'SOAR_Architecture_SIEM_TI_Integration_Documentation.pdf';
    
    console.log(`Generating PDF from ${inputFile}...`);
    console.log('This may take a few minutes as mermaid diagrams are being rendered...');
    
    // Load custom configuration
    const config = require('./.md2pdf.config.js');
    
    const pdf = await mdToPdf(
      { path: inputFile },
      {
        dest: outputFile,
        ...config
      }
    );
    
    if (pdf) {
      console.log(`✓ PDF successfully generated: ${outputFile}`);
      
      // Get file size
      const stats = fs.statSync(outputFile);
      const fileSizeInMB = (stats.size / (1024 * 1024)).toFixed(2);
      console.log(`  File size: ${fileSizeInMB} MB`);
      
      return true;
    } else {
      console.error('✗ Failed to generate PDF');
      return false;
    }
  } catch (error) {
    console.error('✗ Error generating PDF:', error.message);
    if (error.stack) {
      console.error(error.stack);
    }
    return false;
  }
}

// Run the PDF generation
generatePDF().then(success => {
  process.exit(success ? 0 : 1);
});
