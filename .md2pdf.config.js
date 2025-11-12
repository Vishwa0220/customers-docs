const fs = require('fs');

// Detect Chrome executable path based on platform
function findChromePath() {
  const paths = [
    '/usr/bin/google-chrome',        // Linux
    '/usr/bin/chromium',              // Linux Chromium
    '/usr/bin/chromium-browser',      // Linux Chromium alternative
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  // Windows
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',  // Windows 32-bit
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  // macOS
  ];
  
  for (const path of paths) {
    if (fs.existsSync(path)) {
      return path;
    }
  }
  
  // Return undefined to use puppeteer's bundled Chromium
  return undefined;
}

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
    executablePath: findChromePath(),
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
