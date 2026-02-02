#!/bin/bash

################################################################################
# Test Intrusion Script - Shuffle Security Webhook Trigger
# Project: Lessimp-Secure
# Purpose: Trigger unauthorized login alert without running full Cerberus test
# Author: AI Agent
# Date: February 1, 2026
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SHUFFLE_WEBHOOK_URL="https://shuffler.io/api/v1/hooks/webhook_a76354e0-cf09-4754-96e1-682c89084d4c"
CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CURRENT_HOUR=$(date +"%H")

# Banner
echo ""
echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${RED}🚨  PROJECT LESSIMP-SECURE: TEST INTRUSION SCRIPT  🚨${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Intrusion scenarios
echo -e "${YELLOW}Select Intrusion Scenario:${NC}"
echo ""
echo "  1) ${RED}Unauthorized User${NC} (intruder_hacker)"
echo "  2) ${RED}Credential Stuffing${NC} (stolen_credentials)"
echo "  3) ${RED}Brute Force Attempt${NC} (brute_force_bot)"
echo "  4) ${RED}Social Engineering${NC} (phishing_victim)"
echo "  5) ${GREEN}Authorized User${NC} (wipedclean - should trigger Discord green)"
echo ""
echo -n "Enter choice [1-5]: "
read -r SCENARIO

# Scenario configurations
case $SCENARIO in
  1)
    USER="intruder_hacker"
    PHONE="5555559999"
    EMAIL="hacker@malicious.com"
    DESC="Unauthorized login attempt from unknown source"
    ;;
  2)
    USER="stolen_credentials"
    PHONE="5555558888"
    EMAIL="victim@compromised.com"
    DESC="Credential stuffing attack detected"
    ;;
  3)
    USER="brute_force_bot"
    PHONE="5555557777"
    EMAIL="bot@automated.com"
    DESC="Automated brute force attack in progress"
    ;;
  4)
    USER="phishing_victim"
    PHONE="5555556666"
    EMAIL="user@phished.com"
    DESC="Social engineering / phishing attempt"
    ;;
  5)
    USER="wipedclean"
    PHONE="5555551001"
    EMAIL="wipedclean@lessimp.com"
    DESC="Authorized user - testing green path"
    ;;
  *)
    echo -e "${RED}Invalid choice. Exiting.${NC}"
    exit 1
    ;;
esac

# Display scenario details
echo ""
echo -e "${BLUE}═══ Selected Scenario ═══${NC}"
echo -e "User:      ${YELLOW}$USER${NC}"
echo -e "Phone:     ${YELLOW}$PHONE${NC}"
echo -e "Email:     ${YELLOW}$EMAIL${NC}"
echo -e "Hour:      ${YELLOW}$CURRENT_HOUR${NC}"
echo -e "Timestamp: ${YELLOW}$CURRENT_TIMESTAMP${NC}"
echo ""

# Construct payload
PAYLOAD=$(cat <<EOF
{
  "user": "$USER",
  "phone": "$PHONE",
  "email": "$EMAIL",
  "timestamp": "$CURRENT_TIMESTAMP",
  "test_case": "MANUAL_INTRUSION_TEST",
  "status": "login_complete",
  "description": "$DESC"
}
EOF
)

# Display payload
echo -e "${BLUE}═══ Request Payload ═══${NC}"
echo "$PAYLOAD" | python3 -m json.tool 2>/dev/null || echo "$PAYLOAD"
echo ""

# Confirm execution
echo -e "${YELLOW}⚠️  This will trigger real alerts:${NC}"
if [ "$SCENARIO" = "5" ]; then
  echo -e "  - ${GREEN}Discord: Green 'Identity Verified' notification${NC}"
  echo -e "  - Gmail: No alert (authorized user)"
else
  echo -e "  - ${RED}Discord: Red 'Unauthorized' notification${NC}"
  echo -e "  - ${RED}Gmail: CRITICAL incident email to info@lessimp.com${NC}"
fi
echo ""
echo -n "Continue? [y/N]: "
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
  echo -e "${YELLOW}Aborted.${NC}"
  exit 0
fi

# Send request
echo ""
echo -e "${BLUE}═══ Sending Request to Shuffle ═══${NC}"
echo "URL: $SHUFFLE_WEBHOOK_URL"
echo ""

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$SHUFFLE_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Extract HTTP code
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

# Display response
echo -e "${BLUE}═══ Response ═══${NC}"
echo "HTTP Status: $HTTP_CODE"
if [ -n "$BODY" ]; then
  echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
fi
echo ""

# Check result
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "202" ]; then
  echo -e "${GREEN}✅ SUCCESS: Webhook triggered successfully!${NC}"
  echo ""
  echo -e "${YELLOW}Expected Results:${NC}"
  if [ "$SCENARIO" = "5" ]; then
    echo -e "  1. Check Discord: ${GREEN}Green 'Identity Verified' notification${NC}"
    echo -e "  2. Check Gmail: ${GREEN}No email (authorized user)${NC}"
  else
    echo -e "  1. Check Discord: ${RED}Red 'Unauthorized' notification${NC}"
    echo -e "  2. Check Gmail: ${RED}CRITICAL incident email${NC}"
    echo -e "     - To: info@lessimp.com"
    echo -e "     - CC: wfrancois@lessimp.com"
    echo -e "     - Subject: 🚨 CRITICAL: Unauthorized Login Attempt"
  fi
  echo ""
  echo -e "${BLUE}Estimated Alert Delivery Time: 5-10 seconds${NC}"
else
  echo -e "${RED}❌ FAILED: HTTP $HTTP_CODE${NC}"
  echo -e "${RED}Webhook may be unreachable or misconfigured.${NC}"
  exit 1
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Test Intrusion Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
