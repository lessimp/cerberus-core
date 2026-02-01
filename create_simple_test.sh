#!/bin/bash

# Cerberus Testing - Simple Test Case Creator
# Creates a test case to navigate to a website and verify text

CERBERUS_URL="http://localhost:8888"
USERNAME="admin"
PASSWORD="admin"

echo "============================================================"
echo "  🚀 Cerberus Test Case Creator"
echo "============================================================"
echo ""
echo "Creating test case: TC001_VerifyWebsiteText"
echo "Target URL: https://example.com"
echo "Verify Text: 'Example Domain'"
echo ""

# Step 1: Create the test case structure
echo "Step 1: Creating test case structure..."
CREATE_RESPONSE=$(curl -s -X POST "${CERBERUS_URL}/api/public/testcase" \
  -H "Content-Type: application/json" \
  -u "${USERNAME}:${PASSWORD}" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "description": "Navigate to a website and verify text element",
    "application": "Google",
    "status": "WORKING",
    "priority": 3,
    "comment": "Created via script",
    "steps": []
  }')

echo "   ✅ Test case created"
echo ""

# Step 2: Add Step 1 - Open URL
echo "Step 2: Adding Step 1: Open URL..."
STEP1_RESPONSE=$(curl -s -X POST "${CERBERUS_URL}/api/public/testcasestep" \
  -H "Content-Type: application/json" \
  -u "${USERNAME}:${PASSWORD}" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "sort": 1,
    "description": "Open website",
    "useStep": "N",
    "actions": [
      {
        "sort": 1,
        "action": "openUrl",
        "value1": "https://example.com",
        "value2": "",
        "description": "Navigate to example.com"
      }
    ]
  }')

echo "   ✅ Step 1 added: Open URL"
echo ""

# Step 3: Add Step 2 - Verify Text
echo "Step 3: Adding Step 2: Verify Text..."
STEP2_RESPONSE=$(curl -s -X POST "${CERBERUS_URL}/api/public/testcasestep" \
  -H "Content-Type: application/json" \
  -u "${USERNAME}:${PASSWORD}" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "sort": 2,
    "description": "Verify text on page",
    "useStep": "N",
    "actions": [
      {
        "sort": 1,
        "action": "verifyTextInPage",
        "value1": "Example Domain",
        "value2": "",
        "description": "Verify Example Domain text is present"
      }
    ]
  }')

echo "   ✅ Step 2 added: Verify Text"
echo ""

echo "============================================================"
echo "  ✨ Test Case Created Successfully!"
echo "============================================================"
echo ""
echo "📋 Test Details:"
echo "   Test: MyFirstTest"
echo "   Test Case: TC001_VerifyWebsiteText"
echo "   Steps: 2"
echo ""
echo "🔗 View your test case:"
echo "   ${CERBERUS_URL}/TestCaseScript.jsp?test=MyFirstTest&testcase=TC001_VerifyWebsiteText"
echo ""
echo "▶️  Run your test:"
echo "   ${CERBERUS_URL}/RunTests.jsp"
echo ""
echo "🎉 Happy Testing!"
