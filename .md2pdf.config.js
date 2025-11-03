module.exports = {
  // PDF format options
  pdf_options: {
    format: 'A4',
    margin: {
      top: '20mm',
      right: '20mm',
      bottom: '20mm',
      left: '20mm'
    },
    printBackground: true,
    displayHeaderFooter: false,
    preferCSSPageSize: false,
  },
  
  // Path to custom stylesheet
  stylesheet: 'pdf-styles.css',
  
  // Launch options for puppeteer to use system Chrome
  launch_options: {
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  },
  
  // Body class for additional styling
  body_class: 'markdown-body',
  
  // Enable syntax highlighting and mermaid
  highlight_style: 'github',
  marked_options: {
    headerIds: true,
    mangle: false
  }
};
