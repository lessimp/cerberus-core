# 🔀 Shuffle Handshake Implementation Guide

## Complete Configuration for Cerberus + Shuffle + Lessimp Integration

This document provides the **exact specifications** for implementing the Shuffle API call block in Cerberus Testing to automate the Lessimp login flow with dynamic credentials.

---

## 📋 Overview

The **Shuffle Handshake** is a 3-step process:

1. **Cerberus calls Shuffle API** → Get random test user credentials
2. **Cerberus stores credentials** → Map JSON to variables (%EMAIL%, %PASSWORD%, %OTP%)
3. **Cerberus injects credentials** → Type into Lessimp mobile UI elements

---

## 🔀 Step 1: Register Shuffle Service in Cerberus

### Navigation
```
Cerberus UI → Administration → Service Library
```

### Create New Service

Click: **[+ Create Service]**

#### Service Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Service Name** | `GetShuffleUser` | Unique identifier for this service |
| **Group** | `Shuffle` | Logical grouping (optional) |
| **Type** | `REST` | RESTful API service |
| **Method** | `GET` | HTTP method |
| **Service Path** | `http://localhost:5000/shuffle/get_user` | Our shuffle_provider.py endpoint |
| **Description** | `Retrieve random test user from Shuffle data provider` | Documentation |
| **Active** | ✅ Yes | Enable service |

#### Headers Configuration

Click: **[+ Add Header]**

| Header Name | Header Value | Notes |
|-------------|--------------|-------|
| `Content-Type` | `application/json` | JSON response format |
| `Accept` | `application/json` | Accept JSON |

**Note:** No Authorization header needed for local shuffle_provider.py (no auth required)

#### Expected Response Format

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice.johnson@testmail.com",
  "phone": "5555551001",
  "countryCode": "+1",
  "fullPhone": "+15555551001",
  "password": "TestPass123!",
  "otp": "123456",
  "timestamp": "2026-02-01T18:30:00.123456",
  "source": "shuffle_provider"
}
```

#### Response Mapping (JSON Path)

Cerberus will automatically parse the JSON response. Define these mappings in test steps:

| Variable Name | JSON Path | Example Value |
|---------------|-----------|---------------|
| `EMAIL` | `$.email` | `alice.johnson@testmail.com` |
| `PASSWORD` | `$.password` | `TestPass123!` |
| `PHONE` | `$.phone` | `5555551001` |
| `COUNTRY_CODE` | `$.countryCode` | `+1` |
| `FULL_PHONE` | `$.fullPhone` | `+15555551001` |
| `OTP` | `$.otp` | `123456` |
| `OTP_SECRET` | `$.otp` | `123456` (same as OTP for test users) |
| `USER_NAME` | `$.name` | `Alice Johnson` |

**Click:** [Save Service]

---

## 🛠️ Step 2: Implement Shuffle Handshake in Test Case

### Test Case: TC001_LoginWithShuffleHandshake

#### Navigation
```
Cerberus UI → Test → Test Case → TC001_LoginWithShuffle → Edit
```

### Test Case Configuration

| Field | Value |
|-------|-------|
| **Test** | `LoginTests` |
| **Test Case** | `TC001_LoginWithShuffleHandshake` |
| **Application** | `Lessimp_Mobile` |
| **Status** | `WORKING` |
| **Priority** | `1` |
| **Description** | `Automated login using Shuffle Handshake with dynamic credentials` |

---

### Step-by-Step Implementation

#### 🔹 Step 1: Call Shuffle Service

```
Action:         callService
Value1:         GetShuffleUser
Value2:         (empty)
Value3:         (empty)
Description:    Retrieve random user credentials from Shuffle
Screenshot:     No
ReturnCode:     (empty)
ReturnMessage:  (empty)
```

**Properties to Store:**
Click **[+ Add Property]** for each:

| Property Name | Type | Value (JSON Path) | Database | Description |
|---------------|------|-------------------|----------|-------------|
| `EMAIL` | `getFromJson` | `$.email` | (empty) | User email address |
| `PASSWORD` | `getFromJson` | `$.password` | (empty) | User password |
| `PHONE` | `getFromJson` | `$.phone` | (empty) | Phone number (digits only) |
| `COUNTRY_CODE` | `getFromJson` | `$.countryCode` | (empty) | Country dial code |
| `FULL_PHONE` | `getFromJson` | `$.fullPhone` | (empty) | Full phone with country code |
| `OTP` | `getFromJson` | `$.otp` | (empty) | OTP code (123456 for test) |
| `USER_NAME` | `getFromJson` | `$.name` | (empty) | User full name |

---

#### 🔹 Step 2: Verify Shuffle API Success

```
Action:         verifyNumericEquals
Value1:         %LASTSERVICE_HTTPSTATUS%
Value2:         200
Value3:         (empty)
Description:    Verify Shuffle API returned HTTP 200 OK
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes (stop test if Shuffle fails)
```

**Why this matters:** If Shuffle API is down or returns an error (401, 500), the test should FAIL IMMEDIATELY before attempting UI automation.

---

#### 🔹 Step 3: Verify EMAIL Variable Populated

```
Action:         verifyStringDifferent
Value1:         %EMAIL%
Value2:         (empty)
Value3:         (empty)
Description:    Verify EMAIL variable is not empty
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes
```

---

#### 🔹 Step 4: Verify PASSWORD Variable Populated

```
Action:         verifyStringDifferent
Value1:         %PASSWORD%
Value2:         (empty)
Value3:         (empty)
Description:    Verify PASSWORD variable is not empty
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes
```

---

#### 🔹 Step 5: Verify PHONE Variable Populated

```
Action:         verifyStringDifferent
Value1:         %PHONE%
Value2:         (empty)
Value3:         (empty)
Description:    Verify PHONE variable is not empty
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes
```

---

#### 🔹 Step 6: Log Shuffled Credentials (Debug)

```
Action:         calculateProperty
Value1:         SHUFFLED_USER_LOG
Value2:         Shuffle returned: EMAIL=%EMAIL%, PHONE=%PHONE%, OTP=%OTP%
Value3:         (empty)
Description:    Log shuffled credentials for debugging
Screenshot:     No
```

**This creates a log entry visible in execution history for troubleshooting.**

---

#### 🔹 Step 7: Launch Lessimp Mobile App

```
Action:         openApplication
Value1:         /Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
Value2:         (empty)
Value3:         (empty)
Description:    Launch Lessimp iOS app on simulator
Screenshot:     Yes
```

**Appium Capabilities (configured in Application settings):**
```json
{
  "platformName": "iOS",
  "platformVersion": "26.0",
  "deviceName": "iPhone 16 Pro",
  "automationName": "XCUITest",
  "app": "/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app",
  "udid": "908D1BF9-3008-4000-AF43-313441294EA7",
  "noReset": false,
  "autoAcceptAlerts": true,
  "newCommandTimeout": 300
}
```

---

#### 🔹 Step 8: Wait for Login Screen

```
Action:         waitForElementPresent
Value1:         xpath=//XCUIElementTypeTextField[@label='Phone Number']
Value2:         15000 (15 seconds)
Value3:         (empty)
Description:    Wait for phone input field to appear
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes
```

**Alternative locator (if Key added to Flutter):**
- `identifier=phone_input`

---

#### 🔹 Step 9: Enter Phone Number (Shuffled Data)

```
Action:         type
Value1:         xpath=//XCUIElementTypeTextField[@label='Phone Number']
Value2:         %PHONE%
Value3:         (empty)
Description:    Enter phone number from Shuffle data
Screenshot:     Yes
```

**🎯 KEY POINT:** This uses `%PHONE%` variable populated by Shuffle in Step 1.

---

#### 🔹 Step 10: Click Login Button

```
Action:         click
Value1:         xpath=//XCUIElementTypeButton[@label='Login']
Value2:         (empty)
Value3:         (empty)
Description:    Submit login to trigger OTP
Screenshot:     Yes
```

**Alternative locator (if Key added to Flutter):**
- `identifier=login_button`

---

#### 🔹 Step 11: Wait for OTP Screen

```
Action:         waitForElementPresent
Value1:         xpath=//XCUIElementTypeStaticText[contains(@label, 'Verification')]
Value2:         20000 (20 seconds - Firebase SMS can be slow)
Value3:         (empty)
Description:    Wait for OTP verification screen
Screenshot:     Yes (on failure)
Fatal:          ✅ Yes
```

---

#### 🔹 Step 12: Enter OTP (Shuffled Data)

**Option A: If using single OTP input field (Pinput widget)**
```
Action:         type
Value1:         xpath=//XCUIElementTypeTextField[1]
Value2:         %OTP%
Value3:         (empty)
Description:    Enter 6-digit OTP from Shuffle data
Screenshot:     Yes
```

**Option B: If OTP fields are individual digits (6 separate fields)**
```
Step 12a: type → xpath=//XCUIElementTypeTextField[1] → substring(%OTP%, 0, 1)
Step 12b: type → xpath=//XCUIElementTypeTextField[2] → substring(%OTP%, 1, 1)
Step 12c: type → xpath=//XCUIElementTypeTextField[3] → substring(%OTP%, 2, 1)
Step 12d: type → xpath=//XCUIElementTypeTextField[4] → substring(%OTP%, 3, 1)
Step 12e: type → xpath=//XCUIElementTypeTextField[5] → substring(%OTP%, 4, 1)
Step 12f: type → xpath=//XCUIElementTypeTextField[6] → substring(%OTP%, 5, 1)
```

**🎯 KEY POINT:** This uses `%OTP%` variable (always `123456` for Firebase test numbers).

---

#### 🔹 Step 13: Click Verify Button

```
Action:         click
Value1:         xpath=//XCUIElementTypeButton[@label='Verify']
Value2:         (empty)
Value3:         (empty)
Description:    Submit OTP for Firebase verification
Screenshot:     Yes
```

**Alternative locator (if Key added to Flutter):**
- `identifier=verify_button`

---

#### 🔹 Step 14: Wait for Login Success

```
Action:         waitForElementPresent
Value1:         xpath=//XCUIElementTypeOther[contains(@label, 'Home')]
Value2:         15000 (15 seconds)
Value3:         (empty)
Description:    Wait for home screen after successful login
Screenshot:     Yes
Fatal:          ✅ Yes
```

---

#### 🔹 Step 15: Verify Login Success

```
Action:         verifyElementPresent
Value1:         xpath=//XCUIElementTypeOther[contains(@label, 'Home')]
Value2:         (empty)
Value3:         (empty)
Description:    Confirm user successfully logged in
Screenshot:     Yes
Result:         ✅ PASS
```

---

## 🎯 Complete Test Case Summary

| Step | Action | Element | Value | Purpose |
|------|--------|---------|-------|---------|
| 1 | callService | GetShuffleUser | - | Get random user from Shuffle |
| 2 | verifyNumericEquals | %LASTSERVICE_HTTPSTATUS% | 200 | Verify API success |
| 3 | verifyStringDifferent | %EMAIL% | (not empty) | Validate EMAIL populated |
| 4 | verifyStringDifferent | %PASSWORD% | (not empty) | Validate PASSWORD populated |
| 5 | verifyStringDifferent | %PHONE% | (not empty) | Validate PHONE populated |
| 6 | calculateProperty | SHUFFLED_USER_LOG | (log message) | Debug logging |
| 7 | openApplication | Runner.app | - | Launch Lessimp app |
| 8 | waitForElementPresent | phone_input | 15000ms | Wait for login screen |
| 9 | type | phone_input | %PHONE% | **Inject Shuffled phone** |
| 10 | click | login_button | - | Submit login |
| 11 | waitForElementPresent | OTP screen | 20000ms | Wait for OTP screen |
| 12 | type | otp_input | %OTP% | **Inject Shuffled OTP** |
| 13 | click | verify_button | - | Submit OTP |
| 14 | waitForElementPresent | Home screen | 15000ms | Wait for success |
| 15 | verifyElementPresent | Home screen | - | **Verify login success** |

**Total Steps:** 15  
**Shuffled Variables Used:** EMAIL, PASSWORD, PHONE, OTP  
**Expected Result:** ✅ User logged in with randomized credentials

---

## 🔐 Step 3: Configure Firebase Test Phone Numbers

### Firebase Console Configuration

1. **Open Firebase Console:** https://console.firebase.google.com/
2. **Select Lessimp Project**
3. **Navigate to:** Authentication → Sign-in method → Phone
4. **Scroll to:** "Phone numbers for testing"

### Add Shuffle Test Numbers

Click **[+ Add phone number]** for each:

| Phone Number | Verification Code | User |
|--------------|-------------------|------|
| `+15555551001` | `123456` | Alice Johnson |
| `+15555551002` | `123456` | Bob Smith |
| `+15555551003` | `123456` | Carol Davis |
| `+15555551004` | `123456` | David Wilson |
| `+15555551005` | `123456` | Eve Martinez |

**Click:** [Save]

### Verification

```bash
# Test Shuffle API returns these numbers
curl http://localhost:5000/shuffle/get_user | jq '.fullPhone, .otp'

# Expected output (example):
# "+15555551003"
# "123456"
```

---

## 🧪 Step 4: Validate Shuffle Handshake

### Pre-Execution Checklist

- [ ] **Shuffle API Running:**
  ```bash
  cd ~/Documents/GitHub/cerberus-core
  python3 shuffle_provider.py --api --port 5000
  ```

- [ ] **Shuffle API Health:**
  ```bash
  curl http://localhost:5000/shuffle/health
  # Expected: {"status": "healthy", ...}
  ```

- [ ] **Service Registered in Cerberus:**
  - Administration → Service Library → GetShuffleUser exists

- [ ] **Firebase Test Numbers Configured:**
  - All 5 numbers (+15555551001-1005) added with OTP 123456

- [ ] **iOS Simulator Running:**
  ```bash
  xcrun simctl boot "iPhone 16 Pro"
  open -a Simulator
  ```

- [ ] **Lessimp App Built:**
  ```bash
  ls -d ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
  ```

- [ ] **Appium Server Running:**
  ```bash
  appium -p 4723
  # Or if using Cerberus built-in Appium: not needed
  ```

---

### Execute Test Case

1. **Navigate to:** Run → Test Queue → Manual Execution
2. **Select:**
   - Test: `LoginTests`
   - Test Case: `TC001_LoginWithShuffleHandshake`
   - Country: (select appropriate)
   - Environment: (select appropriate)
3. **Click:** [Run Test]

---

### Monitor Execution

1. **Navigate to:** Run → Execution History
2. **Find:** Latest execution of TC001_LoginWithShuffleHandshake
3. **Click:** [View Details]

**Expected Execution Log:**

```
✅ Step 1: callService (GetShuffleUser) - OK
   Response: {"email": "alice.johnson@testmail.com", "phone": "5555551001", ...}
   
✅ Step 2: verifyNumericEquals (%LASTSERVICE_HTTPSTATUS% = 200) - OK
   
✅ Step 3: verifyStringDifferent (%EMAIL% ≠ empty) - OK
   EMAIL = "alice.johnson@testmail.com"
   
✅ Step 4: verifyStringDifferent (%PASSWORD% ≠ empty) - OK
   PASSWORD = "TestPass123!"
   
✅ Step 5: verifyStringDifferent (%PHONE% ≠ empty) - OK
   PHONE = "5555551001"
   
✅ Step 6: calculateProperty (SHUFFLED_USER_LOG) - OK
   Log: "Shuffle returned: EMAIL=alice.johnson@testmail.com, PHONE=5555551001, OTP=123456"
   
✅ Step 7: openApplication (Runner.app) - OK
   App launched on iPhone 16 Pro simulator
   
✅ Step 8: waitForElementPresent (phone_input) - OK
   Element found in 3.2 seconds
   
✅ Step 9: type (phone_input = "5555551001") - OK
   Text entered: "5555551001"
   
✅ Step 10: click (login_button) - OK
   Button clicked, Firebase OTP triggered
   
✅ Step 11: waitForElementPresent (OTP screen) - OK
   OTP screen appeared in 5.8 seconds
   
✅ Step 12: type (otp_input = "123456") - OK
   OTP entered: "123456"
   
✅ Step 13: click (verify_button) - OK
   OTP submitted to Firebase
   
✅ Step 14: waitForElementPresent (Home screen) - OK
   Home screen appeared in 2.1 seconds
   
✅ Step 15: verifyElementPresent (Home screen) - OK
   Login successful!

Test Result: ✅ PASS
Execution Time: 42.3 seconds
Screenshots: 8 captured
```

---

## 🚨 Troubleshooting Shuffle Handshake

### Issue 1: Shuffle API Call Fails (Step 1)

**Error:** `callService failed with HTTP 0 or timeout`

**Possible Causes:**
1. Shuffle API not running
2. Wrong service URL
3. Network issue

**Fix:**
```bash
# Verify Shuffle API is running
curl http://localhost:5000/shuffle/health

# If not running:
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000

# Verify service configuration in Cerberus
# Administration → Service Library → GetShuffleUser
# Service Path: http://localhost:5000/shuffle/get_user (no trailing slash)
```

---

### Issue 2: HTTP Status Not 200 (Step 2)

**Error:** `verifyNumericEquals failed: Expected 200, got 404`

**Fix:**
```bash
# Test Shuffle endpoint manually
curl -v http://localhost:5000/shuffle/get_user

# Verify exact URL in Cerberus Service Library
# Common mistakes:
# ❌ http://localhost:5000/shuffle/get_user/ (trailing slash)
# ❌ http://127.0.0.1:5000/shuffle/get_user (use localhost)
# ✅ http://localhost:5000/shuffle/get_user
```

---

### Issue 3: Variables Not Populated (Steps 3-5)

**Error:** `verifyStringDifferent failed: %EMAIL% is empty`

**Possible Causes:**
1. Wrong JSON path
2. Shuffle response format changed
3. Property not configured in Step 1

**Fix:**
```bash
# Check Shuffle response format
curl http://localhost:5000/shuffle/get_user | jq '.'

# Verify JSON paths in Step 1 Properties:
# EMAIL: $.email (not $.user.email)
# PASSWORD: $.password
# PHONE: $.phone
```

---

### Issue 4: OTP Verification Failed (Step 13)

**Error:** `Firebase authentication failed`

**Possible Causes:**
1. Test phone number not configured in Firebase
2. Wrong OTP code
3. Firebase project misconfigured

**Fix:**
```bash
# Verify test numbers in Firebase Console
# Phone numbers for testing:
# +15555551001 → 123456
# +15555551002 → 123456
# etc.

# Verify Shuffle returns correct OTP
curl http://localhost:5000/shuffle/get_user | jq '.otp'
# Expected: "123456"
```

---

### Issue 5: Element Not Found (Steps 8-15)

**Error:** `waitForElementPresent timeout: element not found`

**Possible Causes:**
1. App not fully loaded
2. Wrong XPath locator
3. Simulator performance issue

**Fix:**
```
# Increase wait timeout from 15000 to 30000
Value2: 30000

# Use alternative locators:
# XPath: xpath=//XCUIElementTypeTextField[@label='Phone Number']
# Accessibility ID (if Key added): identifier=phone_input

# Verify element exists in Flutter DevTools
flutter pub global run devtools
```

---

## 🎯 Success Criteria

The **Shuffle Handshake** is successfully implemented when:

✅ **Service Level:**
- GetShuffleUser service registered in Cerberus
- Service returns HTTP 200 with valid JSON
- Variables (%EMAIL%, %PASSWORD%, %PHONE%, %OTP%) populated correctly

✅ **Test Case Level:**
- All 15 steps execute without errors
- Shuffled credentials injected into mobile UI
- Login successful with randomized user
- Screenshots captured at key steps

✅ **Execution Level:**
- Test runs repeatedly with different users (Shuffle randomization)
- No hardcoded credentials in test case
- Execution history shows variable values
- Each run uses a different Shuffle user

✅ **Validation Level:**
- HTTP status verification prevents bad data
- Variable validation prevents empty injections
- Fatal flags stop test on critical failures
- Debug logging shows Shuffle data

---

## 📊 Benefits of Shuffle Handshake

### ✅ Advantages

1. **Dynamic Data:** Every test run uses different credentials
2. **No Hardcoding:** Zero credentials stored in Cerberus test cases
3. **Scalability:** Easy to add more test users to shuffle_provider.py
4. **Traceability:** Execution logs show which user was used
5. **Error Handling:** Immediate failure if Shuffle unavailable
6. **Debugging:** Variable values visible in execution history
7. **Security:** Test credentials separate from production

### 🔄 Data Flow

```
Shuffle API (shuffle_provider.py)
    ↓ HTTP GET /shuffle/get_user
Cerberus callService (GetShuffleUser)
    ↓ Parse JSON, store variables
Cerberus Variables (%EMAIL%, %PASSWORD%, %PHONE%, %OTP%)
    ↓ Inject into mobile UI
Lessimp Flutter App (phone_input, otp_input)
    ↓ Firebase Phone Auth
Firebase Validation (test number + OTP 123456)
    ↓ Success
User Logged In (Home Screen)
```

---

## 🔧 Optional Enhancements

### Enhancement 1: Add Email/Password Login Flow

If Lessimp supports email/password login (in addition to phone):

**Step 9a (Alternative): Enter Email**
```
Action:         type
Value1:         xpath=//XCUIElementTypeTextField[@label='Email']
Value2:         %EMAIL%
Description:    Enter email from Shuffle data
```

**Step 9b (Alternative): Enter Password**
```
Action:         type
Value1:         xpath=//XCUIElementTypeSecureTextField[@label='Password']
Value2:         %PASSWORD%
Description:    Enter password from Shuffle data
```

---

### Enhancement 2: Add MFA/2FA Flow

If Lessimp uses authenticator app for MFA:

**Step 12 (Alternative): Calculate TOTP**
```
Action:         calculateProperty
Value1:         TOTP_CODE
Value2:         totp(%OTP_SECRET%)
Description:    Generate TOTP from OTP secret
```

**Note:** Cerberus v4.20 may not support TOTP natively. Use external script or REST call.

---

### Enhancement 3: Test Multiple Users in Single Run

**Create a loop:**
```
Step 1-15: Call Shuffle, login, verify, logout
Step 16: goto Step 1 (repeat 5 times)
```

**Result:** Test 5 different Shuffle users in one execution.

---

## 📚 Related Documentation

- **MASTER_TECHNICAL_REFERENCE.md** - Complete system architecture
- **WIDGET_LOCATOR_AUDIT.md** - Flutter widget identification
- **CERBERUS_TEST_CASE_SETUP.md** - Detailed Cerberus configuration
- **shuffle_provider.py** - Test data API implementation
- **INTEGRATION_COMPLETE.md** - Quick start guide

---

## 🎓 For Copilot AI Agent

**Summary Instructions:**

1. **Register Service:**
   - Name: `GetShuffleUser`
   - Type: `REST`, Method: `GET`
   - URL: `http://localhost:5000/shuffle/get_user`

2. **Test Case Steps:**
   - Step 1: `callService` → GetShuffleUser
   - Step 2: `verifyNumericEquals` → %LASTSERVICE_HTTPSTATUS% = 200
   - Steps 3-5: Validate variables (%EMAIL%, %PASSWORD%, %PHONE%)
   - Step 7: `openApplication` → Lessimp
   - Steps 9-13: UI automation with `%PHONE%` and `%OTP%` injection
   - Step 15: `verifyElementPresent` → Success

3. **Error Handling:**
   - Fatal flag on Shuffle API failure
   - Variable validation before UI automation
   - HTTP status check (200 or fail)

4. **Firebase Configuration:**
   - Add test numbers: +15555551001 through +15555551005
   - OTP: 123456 for all test numbers

---

**Status:** ✅ Ready for implementation  
**Version:** 1.0  
**Date:** February 1, 2026  
**Next Step:** Configure Firebase test numbers, then execute TC001_LoginWithShuffleHandshake
