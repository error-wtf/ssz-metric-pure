#!/bin/bash
# SSZ φ-Spiral Metric - Installation Script for Linux/macOS
# © 2025 Carmen Wrede & Lino Casu
# Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}SSZ φ-Spiral Metric - Installation (Linux/macOS)${NC}"
echo -e "${CYAN}v1.0.0 FINAL - Complete & Validated${NC}"
echo -e "${CYAN}================================================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ ERROR: Python not found. Please install Python 3.10 or later.${NC}"
    echo -e "${YELLOW}  Ubuntu/Debian: sudo apt install python3 python3-pip${NC}"
    echo -e "${YELLOW}  macOS: brew install python3${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"

# Check if version is 3.10+
VERSION_CHECK=$($PYTHON_CMD -c "import sys; print(1 if sys.version_info >= (3, 10) else 0)")
if [ "$VERSION_CHECK" != "1" ]; then
    echo -e "${RED}✗ ERROR: Python 3.10+ required, found $PYTHON_VERSION${NC}"
    exit 1
fi

echo ""

# Check pip
echo -e "${YELLOW}Checking pip...${NC}"
if $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${GREEN}✓ pip is available${NC}"
else
    echo -e "${RED}✗ ERROR: pip not found. Installing pip...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install pip${NC}"
        exit 1
    fi
fi

echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
echo "  • numpy"
echo "  • scipy"
echo "  • sympy"
echo "  • matplotlib"
echo ""

packages=("numpy" "scipy" "sympy" "matplotlib")

for package in "${packages[@]}"; do
    echo -e "${GRAY}Installing $package...${NC}"
    $PYTHON_CMD -m pip install --upgrade "$package" --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✓ $package installed${NC}"
    else
        echo -e "${RED}  ✗ Failed to install $package${NC}"
        exit 1
    fi
done

echo ""
echo -e "${GREEN}✓ All dependencies installed successfully!${NC}"

echo ""

# Ask if user wants to run tests
echo -e "${CYAN}================================================================${NC}"
read -p "Run validation tests? (y/n): " run_tests

if [[ "$run_tests" == "y" || "$run_tests" == "Y" ]]; then
    echo ""
    echo -e "${YELLOW}Running validation tests...${NC}"
    echo ""
    
    $PYTHON_CMD tests/test_validation_ssz_calibrated.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ All tests passed!${NC}"
    else
        echo ""
        echo -e "${RED}✗ Some tests failed. Check output above.${NC}"
    fi
fi

echo ""

# Ask if user wants to generate validation report
echo -e "${CYAN}================================================================${NC}"
read -p "Generate complete validation report? (y/n): " gen_report

if [[ "$gen_report" == "y" || "$gen_report" == "Y" ]]; then
    echo ""
    echo -e "${YELLOW}Generating validation report...${NC}"
    echo "This will create:"
    echo "  • 3 plots (300 DPI)"
    echo "  • 2 certificates"
    echo "  • 1 JSON file"
    echo "  • Complete scientific report"
    echo ""
    
    $PYTHON_CMD generate_validation_report.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Validation report generated successfully!${NC}"
        echo ""
        echo "Reports available in:"
        echo -e "${CYAN}  reports/SSZ_VALIDATION_REPORT.md${NC}"
        echo -e "${CYAN}  reports/SSZ_VALIDATION_REPORT.tex${NC}"
        echo -e "${CYAN}  reports/SSZ_CERTIFICATE_EARTH.txt${NC}"
        echo -e "${CYAN}  reports/SSZ_CERTIFICATE_SUN.txt${NC}"
        echo -e "${CYAN}  reports/ssz_validation_certificate.json${NC}"
        echo -e "${CYAN}  reports/figures/*.png${NC}"
    else
        echo ""
        echo -e "${RED}✗ Report generation failed. Check output above.${NC}"
    fi
fi

echo ""
echo -e "${CYAN}================================================================${NC}"
echo -e "${GREEN}INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}================================================================${NC}"
echo ""
echo -e "${YELLOW}Quick Start:${NC}"
echo ""
echo "  # Run all validation tests:"
echo -e "${CYAN}  $PYTHON_CMD tests/test_validation_ssz_calibrated.py${NC}"
echo ""
echo "  # Run consistency validator:"
echo -e "${CYAN}  $PYTHON_CMD src/ssz_metric_pure/ssz_validator.py${NC}"
echo ""
echo "  # Generate complete report:"
echo -e "${CYAN}  $PYTHON_CMD generate_validation_report.py${NC}"
echo ""
echo "  # Compare all metric forms:"
echo -e "${CYAN}  $PYTHON_CMD FINAL_COMPARISON_AND_INTERPRETATION.py${NC}"
echo ""
echo "  # View final summary:"
echo -e "${CYAN}  $PYTHON_CMD FINAL_SUMMARY_AND_REPORT.py${NC}"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  • MASTER_README.md - Complete overview"
echo "  • INDEX.md - File navigation"
echo "  • reports/SSZ_VALIDATION_REPORT.md - Scientific validation"
echo ""
echo -e "${GRAY}© 2025 Carmen Wrede & Lino Casu${NC}"
echo -e "${GRAY}Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4${NC}"
echo ""
echo -e "${CYAN}\"No Singularities. Pure Physics. φ-Driven.\"${NC}"
echo ""
