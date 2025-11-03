#!/usr/bin/env node

/**
 * Test script to validate PDF generation
 */

const fs = require('fs');
const path = require('path');

function testPdfGeneration() {
  console.log('Testing PDF generation...\n');
  
  const pdfPath = 'SOAR_Architecture_SIEM_TI_Integration_Documentation.pdf';
  const mdPath = 'SOAR_Architecture_SIEM_TI_Integration_Documentation.md';
  
  // Test 1: Check if PDF exists
  console.log('Test 1: Checking if PDF exists...');
  if (fs.existsSync(pdfPath)) {
    console.log('✓ PDF file exists');
  } else {
    console.log('✗ PDF file not found');
    return false;
  }
  
  // Test 2: Check PDF file size
  console.log('\nTest 2: Checking PDF file size...');
  const stats = fs.statSync(pdfPath);
  const fileSizeInKB = stats.size / 1024;
  console.log(`  PDF size: ${fileSizeInKB.toFixed(2)} KB`);
  
  if (fileSizeInKB > 100) {
    console.log('✓ PDF has reasonable size (>100KB)');
  } else {
    console.log('✗ PDF seems too small, might be incomplete');
    return false;
  }
  
  // Test 3: Check if markdown source exists
  console.log('\nTest 3: Checking markdown source...');
  if (fs.existsSync(mdPath)) {
    console.log('✓ Markdown source exists');
  } else {
    console.log('✗ Markdown source not found');
    return false;
  }
  
  // Test 4: Count mermaid diagrams in source
  console.log('\nTest 4: Counting mermaid diagrams...');
  const mdContent = fs.readFileSync(mdPath, 'utf8');
  const mermaidCount = (mdContent.match(/```mermaid/g) || []).length;
  console.log(`  Found ${mermaidCount} mermaid diagrams in source`);
  
  if (mermaidCount > 0) {
    console.log('✓ Mermaid diagrams present in source');
  } else {
    console.log('✗ No mermaid diagrams found');
    return false;
  }
  
  // Test 5: Check if configuration files exist
  console.log('\nTest 5: Checking configuration files...');
  const configFiles = ['.md2pdf.config.js', 'pdf-styles.css', 'generate-pdf.js'];
  let allConfigsExist = true;
  
  for (const configFile of configFiles) {
    if (fs.existsSync(configFile)) {
      console.log(`  ✓ ${configFile} exists`);
    } else {
      console.log(`  ✗ ${configFile} missing`);
      allConfigsExist = false;
    }
  }
  
  if (allConfigsExist) {
    console.log('✓ All configuration files present');
  } else {
    console.log('✗ Some configuration files missing');
    return false;
  }
  
  console.log('\n=================================');
  console.log('All tests passed! ✓');
  console.log('=================================');
  return true;
}

// Run tests
const success = testPdfGeneration();
process.exit(success ? 0 : 1);
