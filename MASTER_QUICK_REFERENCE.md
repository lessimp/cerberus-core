# 🚀 Master Directive Quick Reference Card

**Version:** 2.0 | **Date:** February 1, 2026 | **Status:** ✅ READY FOR EXECUTION

---

## 📋 4-Phase Execution Checklist

### ✅ Phase 1: Flutter Widget Keys (COMPLETE)
- [x] `phone_input` Key added (login_screen.dart:468)
- [x] `login_button` Key added (login_screen.dart:504)
- [x] `otp_input` Key added (otp_verification_screen.dart:293)
- [x] `verify_button` Key added (otp_verification_screen.dart:368)
- [x] iOS app rebuilt: `flutter build ios --simulator` ✅

**Build Path:** `~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app`

---

### 📝 Phase 2: Cerberus Service Library

**URL:** http://localhost:8888/ServiceList.jsp

**Service:** GetShuffleUser
- **Method:** POST
- **Path:** `%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute`
- **Headers:**
  - `Content-Type: application/json`
  - `Accept: application/json`
  - `Authorization: Bearer %SHUFFLE_API_TOKEN%` (cloud only)

**JSON Path Mappings:**
```
$.shuffled_user.email      → %EMAIL%
$.shuffled_user.password   → %PASSWORD%
$.shuffled_user.phone      → %PHONE% (CRITICAL: Step 10)
$.shuffled_user.otp        → %OTP% (CRITICAL: Step 13)
$.shuffled_user.name       → %USER_NAME%
$.shuffled_user.id         → %USER_ID%
```

**Verify:**
```bash
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" -d '{}' | jq '.shuffled_user'
```

---

### 🧪 Phase 3: 15-Step Test Case

**URL:** http://localhost:8888/TestCaseList.jsp

**Test Case:** TC001_LoginWithShuffleHandshake

| Step | Action | Value1 | Value2 | Fatal | Purpose |
|------|--------|--------|--------|-------|---------|
| 1 | `callService` | GetShuffleUser | - | N | Get credentials from Shuffle |
| 2 | `verifyNumericEquals` | %LASTSERVICE_HTTPSTATUS% | 200 | **Y** | Verify Shuffle success |
| 3 | `calculateProperty` | SHUFFLED_USER_LOG | Email=%EMAIL%... | N | Log for traceability |
| 4 | `verifyStringDifferent` | %PHONE% | (empty) | **Y** | Validate PHONE exists |
| 5 | `verifyStringDifferent` | %OTP% | (empty) | **Y** | Validate OTP exists |
| 6 | `verifyStringDifferent` | %EMAIL% | (empty) | N | Validate EMAIL (future) |
| 7 | `verifyStringDifferent` | %PASSWORD% | (empty) | N | Validate PASSWORD (future) |
| 8 | `openApplication` | Runner.app path | - | N | Launch Lessimp app |
| 9 | `waitForElementPresent` | identifier=phone_input | 15000 | **Y** | Wait for login screen |
| 10 | `type` | identifier=phone_input | **%PHONE%** | N | **INJECT PHONE** |
| 11 | `click` | identifier=login_button | - | N | Trigger Firebase OTP |
| 12 | `waitForElementPresent` | xpath=.../Verification | 20000 | **Y** | Wait for OTP screen |
| 13 | `type` | identifier=otp_input | **%OTP%** | N | **INJECT OTP** |
| 14 | `click` | identifier=verify_button | - | N | Submit OTP |
| 15 | `verifyElementVisible` | xpath=.../Home | - | N | Verify login success |

**Import:** Use `CERBERUS_TC001_DATABASE_IMPORT.json`

---

### 🔐 Phase 4: Firebase OTP Bypass

**URL:** https://console.firebase.google.com/

**Path:** Authentication → Sign-in method → Phone → "Phone numbers for testing"

**Add 5 numbers:**
```
+15555551001  →  123456
+15555551002  →  123456
+15555551003  →  123456
+15555551004  →  123456
+15555551005  →  123456
```

**Verify:**
```bash
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py
```

---

## 🔀 Hybrid Shuffle Environment Switching

### Global Properties

**URL:** http://localhost:8888/PropertyList.jsp

| Property | Local Value | Cloud Value |
|----------|-------------|-------------|
| `SHUFFLE_BASE_URL` | `http://localhost:3001` | `https://shuffler.io` |
| `SHUFFLE_API_TOKEN` | (empty or dummy) | `<real_token>` |

**Switch to Local:**
1. Set `SHUFFLE_BASE_URL` = `http://localhost:3001`
2. Authorization header optional

**Switch to Cloud:**
1. Set `SHUFFLE_BASE_URL` = `https://shuffler.io`
2. Set `SHUFFLE_API_TOKEN` = your token
3. Ensure Authorization header in service

---

## 🎯 Critical Data Flow

```
SHUFFLE WORKFLOW (Step 1)
    ↓
JSON Response: {shuffled_user: {phone: "5555551003", otp: "123456"}}
    ↓
Extract via JSON Path: $.shuffled_user.phone → %PHONE%
    ↓
INJECT in Step 10: type → identifier=phone_input → %PHONE%
    ↓
Firebase Auth: Send OTP to +15555551003
    ↓
Firebase Test Number: Auto-provide OTP "123456"
    ↓
INJECT in Step 13: type → identifier=otp_input → %OTP%
    ↓
Firebase Auth: Validate OTP → ✅ SUCCESS
    ↓
LOGIN SUCCESS (Step 15)
```

---

## 🛠️ Pre-Flight Commands

### Start Infrastructure
```bash
# Cerberus
cd ~/Documents/GitHub/cerberus-core
docker-compose up -d

# Shuffle Local (if using local)
cd ~/shuffle
docker-compose up -d

# iOS Simulator
xcrun simctl boot "iPhone 16 Pro"
open -a Simulator
```

### Build Flutter App
```bash
cd ~/Documents/GitHub/lessimp
flutter build ios --simulator
# Output: ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
```

### Verify Services
```bash
# Cerberus
curl -I http://localhost:8888/

# Shuffle Local
curl http://localhost:3001/api/v1/workflows

# Shuffle Workflow Execution
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" -d '{}' | jq '.shuffled_user'
```

---

## 📊 Appium Locator Strategies

| Element | Preferred Locator | Fallback XPath |
|---------|-------------------|----------------|
| Phone Input | `identifier=phone_input` | `xpath=//XCUIElementTypeTextField[@label='Phone Number']` |
| Login Button | `identifier=login_button` | `xpath=//XCUIElementTypeButton[@label='Login']` |
| OTP Input | `identifier=otp_input` | `xpath=//XCUIElementTypeTextField[1]` |
| Verify Button | `identifier=verify_button` | `xpath=//XCUIElementTypeButton[@label='Verify']` |
| OTP Screen | `xpath=//XCUIElementTypeStaticText[contains(@label, 'Verification')]` | - |
| Home Screen | `xpath=//XCUIElementTypeOther[contains(@label, 'Home')]` | - |

---

## 🚨 Fatal Step Logic

**Step 2: Verify Shuffle HTTP 200 (Fatal=YES)**
- If Shuffle returns 401/500/timeout → **STOP TEST**
- Prevents wasting time on UI automation with no credentials

**Step 4-5: Verify PHONE & OTP (Fatal=YES)**
- If variables empty → **STOP TEST**
- Prevents typing empty strings into UI

**Step 9: Wait for phone_input (Fatal=YES)**
- If app doesn't load login screen → **STOP TEST**
- Prevents NoSuchElement errors in later steps

**Step 12: Wait for OTP screen (Fatal=YES)**
- If Firebase doesn't show OTP screen → **STOP TEST**
- Prevents typing OTP into wrong screen

---

## 🎯 Expected Test Result

**Duration:** 45-60 seconds

**Outcome:** ✅ ALL 15 STEPS PASS

**Visual Flow:**
1. Shuffle returns user: `{phone: "5555551003", otp: "123456"}`
2. App opens → Login screen appears
3. Phone "5555551003" typed into phone_input
4. Login button clicked → Firebase triggered
5. OTP screen appears
6. OTP "123456" typed into otp_input
7. Verify button clicked → Firebase validates
8. Home screen appears → **LOGIN SUCCESS**

---

## 📁 Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `MASTER_DIRECTIVE_COMPLETE.md` | Complete integration guide | 30 KB |
| `CERBERUS_TC001_DATABASE_IMPORT.json` | Test case import file | 12 KB |
| `GLOBAL_PROPERTY_GUIDE.md` | Environment switching guide | 18 KB |
| `PHASE2_EXECUTION_REPORT.md` | Phase 2 status report | 28 KB |
| `MASTER_QUICK_REFERENCE.md` | This file | 6 KB |

**Total Documentation:** 94 KB / 5 files

---

## 🔧 Troubleshooting

### Issue: Step 1 fails (callService)
```bash
# Test Shuffle endpoint
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" -d '{}'
# Expected: {"success": true, "shuffled_user": {...}}
```

### Issue: Step 2 fails (HTTP != 200)
- Check Shuffle logs: `docker-compose logs -f backend`
- Verify workflow ID: `5e611ec1-350b-4395-9794-c0b08a098649`
- Test manually: see above curl command

### Issue: Step 9 fails (element not found)
```bash
# Verify app built
ls -lh ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app

# Rebuild if needed
cd ~/Documents/GitHub/lessimp
flutter build ios --simulator
```

### Issue: Step 13 fails (OTP incorrect)
```bash
# Verify Firebase test numbers
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py

# Check Firebase Console
open https://console.firebase.google.com/
# Navigate to: Authentication → Sign-in method → Phone
```

---

## 🎖️ Success Criteria

- [ ] Cerberus running on http://localhost:8888/
- [ ] GetShuffleUser service created and tested
- [ ] Global properties set (SHUFFLE_BASE_URL, SHUFFLE_API_TOKEN)
- [ ] TC001_LoginWithShuffleHandshake created (15 steps)
- [ ] Firebase test numbers configured (5 numbers, OTP: 123456)
- [ ] iOS Simulator booted with Runner.app
- [ ] Test execution: ALL 15 STEPS PASS
- [ ] User logged in to home screen

---

## 🚀 One-Command Test Execution

```bash
# Automated test execution (requires Cerberus CLI or API - v4.20 may not support)
# Manual: Run → Test Queue → TC001_LoginWithShuffleHandshake → [Execute]
```

**Cerberus UI Path:**
1. http://localhost:8888/
2. Run → Test Queue
3. Manual Execution
4. Test: LoginTests
5. Test Case: TC001_LoginWithShuffleHandshake
6. Country: US
7. Environment: [Your environment]
8. Click: [Add to Queue]
9. Click: [Run]

---

**Status:** ✅ READY FOR EXECUTION  
**Version:** 2.0  
**Last Updated:** February 1, 2026  
**Author:** GitHub Copilot AI Agent

---

## 📞 Support Resources

- **Cerberus UI:** http://localhost:8888/
- **Shuffle Local:** http://localhost:3001/
- **Firebase Console:** https://console.firebase.google.com/
- **Documentation Root:** `~/Documents/GitHub/cerberus-core/`
- **Flutter Project:** `~/Documents/GitHub/lessimp/`

**Next Steps:**
1. Review `MASTER_DIRECTIVE_COMPLETE.md` for full details
2. Configure Cerberus using Phase 2 & 3 instructions
3. Execute TC001_LoginWithShuffleHandshake
4. Verify all 15 steps pass
5. Celebrate successful Shuffle Handshake integration! 🎉
