#!/bin/bash

# Cerberus Testing - Create Test Case Script
# This script creates a simple test case to navigate to a website and verify text

CERBERUS_URL="http://localhost:8888"
USERNAME="admin"
PASSWORD="admin"

echo "Creating Cerberus Test Case..."

# Create Test Case
curl -X POST "${CERBERUS_URL}/api/public/testcase" \
  -H "Content-Type: application/json" \
  -u "${USERNAME}:${PASSWORD}" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "description": "Navigate to a website and verify text element",
    "application": "Google",
    "status": "WORKING",
    "priority": 3,
    "targetBuild": "",
    "targetRev": "",
    "comment": "Created via API",
    "steps": [
      {
        "sort": 1,
        "description": "Open website",
        "useStep": "N",
        "useStepTest": "",
        "useStepTestCase": "",
        "useStepStep": 0,
        "actions": [
          {
            "sort": 1,
            "action": "openUrl",
            "value1": "https://example.com",
            "value2": "",
            "description": "Navigate to example.com",
            "screenshotFileName": "",
            "forceExeStatus": ""
          }
        ],
        "controls": []
      },
      {
        "sort": 2,
        "description": "Verify text on page",
        "useStep": "N",
        "useStepTest": "",
        "useStepTestCase": "",
        "useStepStep": 0,
        "actions": [
          {
            "sort": 1,
            "action": "verifyTextInPage",
            "value1": "Example Domain",
            "value2": "",
            "description": "Verify 'Example Domain' text is present",
            "screenshotFileName": "",
            "forceExeStatus": ""
          }
        ],
        "controls": []
      }
    ]
  }'

echo -e "\n\nTest case created! View it at: ${CERBERUS_URL}/TestCaseScript.jsp?test=MyFirstTest&testcase=TC001_VerifyWebsiteText"
