#!/bin/bash

################################################################################
# SECURAA Security Documentation PDF Export Tool
#
# This script converts security documentation markdown files to PDF format
# using pandoc and wkhtmltopdf.
################################################################################

# Don't exit on error immediately, we want to handle errors gracefully
# set -e  # Commented out to prevent early exit on pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/pdf-exports"

# Security documents to export
declare -A DOCUMENTS
DOCUMENTS=(
  ["secura-customer-security-documentation.md"]="SECURAA-Platform-Security-Documentation.pdf"
  ["securaa-information-security-risk-assesment-process.md"]="SECURAA-Information-Security-Risk-Assessment-Process.pdf"
)

# Function to print header
print_header() {
  echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║   SECURAA Security Documentation PDF Export Tool      ║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
  echo ""
}

# Function to print success message
print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error message
print_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Function to print warning message
print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to print info message
print_info() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required tools are installed
check_dependencies() {
  print_info "Checking dependencies..."
  
  local missing_deps=0
  
  if ! command -v pandoc &> /dev/null; then
    print_error "pandoc is not installed"
    echo "   Install with: sudo apt-get install pandoc"
    missing_deps=1
  else
    print_success "pandoc is installed: $(pandoc --version | head -n1)"
  fi
  
  if ! command -v wkhtmltopdf &> /dev/null; then
    print_error "wkhtmltopdf is not installed"
    echo "   Install with: sudo apt-get install wkhtmltopdf"
    missing_deps=1
  else
    print_success "wkhtmltopdf is installed: $(wkhtmltopdf --version 2>&1 | head -n1)"
  fi
  
  if [ $missing_deps -eq 1 ]; then
    exit 1
  fi
  
  echo ""
}

# Create output directory if it doesn't exist
ensure_output_directory() {
  if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    print_success "Created output directory: $OUTPUT_DIR"
  fi
}

# Preprocess markdown file to handle external images
preprocess_markdown() {
  local input_file="$1"
  local temp_file="${OUTPUT_DIR}/temp_$(basename "$input_file")"
  
  # Create a temporary file with processed content
  # Remove or comment out external image references that might fail
  sed 's|!\[.*\](https://via.placeholder.com/.*)|<!-- External image removed for PDF export -->|g' "$input_file" > "$temp_file"
  
  echo "$temp_file"
}

# Export a single document to PDF
export_document() {
  local input_file="$1"
  local output_file="$2"
  
  local input_path="${SCRIPT_DIR}/${input_file}"
  local output_path="${OUTPUT_DIR}/${output_file}"
  
  echo ""
  print_info "Processing: ${input_file}"
  echo "   Input:  ${input_file}"
  echo "   Output: ${output_file}"
  
  # Check if input file exists
  if [ ! -f "$input_path" ]; then
    print_error "Input file not found: ${input_path}"
    return 1
  fi
  
  # Check for mermaid diagrams
  if grep -q '```mermaid' "$input_path"; then
    print_warning "Note: Mermaid diagrams will be shown as code blocks in PDF"
    echo "      (Full diagram rendering requires additional setup)"
  fi
  
  # Preprocess markdown to handle external images
  print_info "Preprocessing markdown..."
  local temp_file=$(preprocess_markdown "$input_path")
  
  # Convert to PDF using pandoc
  print_info "Converting to PDF..."
  
  # Run pandoc and capture output, but check if file was created
  pandoc "$temp_file" \
    --pdf-engine=wkhtmltopdf \
    --from markdown \
    --to html5 \
    --standalone \
    --toc \
    --toc-depth=3 \
    --metadata title="SECURAA Security Documentation" \
    --css="${SCRIPT_DIR}/pdf-style.css" \
    --output "$output_path" \
    2>&1 | grep -v "QStandardPaths\|Qt WebEngine\|libva\|dri" | head -20 || true
  
  # Clean up temp file
  rm -f "$temp_file"
  
  # Check if PDF was created successfully
  if [ -f "$output_path" ] && [ -s "$output_path" ]; then
    print_success "Successfully exported to: ${output_file}"
    
    # Get file size
    local file_size=$(du -h "$output_path" | cut -f1)
    echo "   📊 File size: ${file_size}"
    return 0
  else
    print_error "Error exporting ${input_file}"
    return 1
  fi
}

# Display usage information
show_usage() {
  echo "Usage: $0 [OPTIONS] [DOCUMENT]"
  echo ""
  echo "Options:"
  echo "  --all, -a       Export all documents (default)"
  echo "  --help, -h      Show this help message"
  echo ""
  echo "Documents:"
  for doc in "${!DOCUMENTS[@]}"; do
    echo "  - $doc"
  done
  echo ""
  echo "Examples:"
  echo "  $0                                  # Export all documents"
  echo "  $0 --all                            # Export all documents"
  echo "  $0 secura-customer-security-documentation.md"
}

# Main function
main() {
  print_header
  
  # Parse command line arguments
  local export_all=1
  local specific_doc=""
  
  for arg in "$@"; do
    case $arg in
      --help|-h)
        show_usage
        exit 0
        ;;
      --all|-a)
        export_all=1
        ;;
      *)
        if [ -n "$arg" ] && [ "${arg:0:1}" != "-" ]; then
          specific_doc="$arg"
          export_all=0
        fi
        ;;
    esac
  done
  
  # Check dependencies
  check_dependencies
  
  # Ensure output directory exists
  ensure_output_directory
  
  local success_count=0
  local error_count=0
  
  if [ $export_all -eq 1 ]; then
    print_info "Exporting all documents (${#DOCUMENTS[@]} total)..."
    
    for input_file in "${!DOCUMENTS[@]}"; do
      output_file="${DOCUMENTS[$input_file]}"
      if export_document "$input_file" "$output_file"; then
        ((success_count++))
      else
        ((error_count++))
      fi
    done
  else
    if [ -z "$specific_doc" ]; then
      print_error "No document specified"
      echo ""
      show_usage
      exit 1
    fi
    
    if [ -n "${DOCUMENTS[$specific_doc]}" ]; then
      print_info "Exporting specific document: ${specific_doc}"
      
      if export_document "$specific_doc" "${DOCUMENTS[$specific_doc]}"; then
        ((success_count++))
      else
        ((error_count++))
      fi
    else
      print_error "Document not found: ${specific_doc}"
      echo ""
      echo "Available documents:"
      for doc in "${!DOCUMENTS[@]}"; do
        echo "  - $doc"
      done
      exit 1
    fi
  fi
  
  echo ""
  
  # Print summary
  if [ $error_count -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✅ PDF Export Completed Successfully!               ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
  else
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║   ⚠️  PDF Export Completed with Errors                ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════╝${NC}"
  fi
  
  echo ""
  echo "📊 Summary:"
  echo "   ✅ Successful: $success_count"
  echo "   ❌ Failed:     $error_count"
  echo ""
  echo "📂 Output directory: ${OUTPUT_DIR}"
  echo ""
  echo "📝 Usage:"
  echo "   bash export-to-pdf.sh              # Export all documents"
  echo "   bash export-to-pdf.sh <file>       # Export specific document"
  echo "   npm run export-pdf                 # Export all documents (via npm)"
  
  if [ $error_count -gt 0 ]; then
    exit 1
  fi
}

# Run main function
main "$@"
