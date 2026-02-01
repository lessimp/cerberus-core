# 🤖 Copilot AI Agent: Master Directive for Lessimp-Shuffle-Cerberus Integration

**Status:** ✅ **COMPLETE - READY FOR EXECUTION**  
**Date:** February 1, 2026  
**Version:** 2.0 (Hybrid Shuffle + Widget Keys + 15-Step Logic)

---

## 🎯 Objective

Finalize the end-to-end automation of the Lessimp Flutter Login flow by integrating the Cerberus Test Engine (v4.20) with the **Hybrid Shuffle Workflow (Local/Cloud)**.

---

## 1️⃣ Infrastructure & Environment Context

### Cerberus Testing Platform
- **Base URL:** `http://localhost:8888/` (Root context / `ROOT.war`)
- **Version:** v4.20 (Servlet-based, no REST API)
- **Credentials:** admin/admin
- **Architecture:** Tomcat 9.0.109 + MySQL 8.0.42
- **Platform:** Docker `linux/amd64` (Rosetta 2 for Apple Silicon)

### Database
- **MySQL Version:** 8.0.42
- **Port:** 13306 (Host) → 3306 (Container)
- **Credentials:** cerberus/cerberus
- **Tables:** 72 (fully initialized)

### Flutter/Lessimp Application
- **iOS Deployment Target:** 15.0
- **Build Path:** `~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app`
- **Branch:** `copilot/vscode1769957753039`
- **Authentication:** Phone-based with Firebase OTP

### Shuffle Hybrid URIs

**🔀 CRITICAL: Two Execution Endpoints**

| Environment | Base URL | Workflow ID | Full Endpoint |
|-------------|----------|-------------|---------------|
| **Local Engine** | `http://localhost:3001` | `5e611ec1-350b-4395-9794-c0b08a098649` | `http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute` |
| **Cloud Portal** | `https://shuffler.io` | `5e611ec1-350b-4395-9794-c0b08a098649` | `https://shuffler.io/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute` |

**Authentication:**
- **Local Engine:** No authentication required (open endpoint)
- **Cloud Portal:** Requires `Authorization: Bearer %SHUFFLE_API_TOKEN%` header

**Toggle Strategy:**
Use Cerberus **Global Property** `SHUFFLE_BASE_URL` to switch between environments:
- Value for Local: `http://localhost:3001`
- Value for Cloud: `https://shuffler.io`

Service URL becomes: `%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute`

### Appium/Automation
- **iOS Simulator:** iPhone 16 Pro (iOS 18.2)
- **UDID:** `908D1BF9-3008-4000-AF43-313441294EA7`
- **Appium Version:** 2.11.5
- **Driver:** XCUITest

### Firebase Authentication
- **Test Numbers:** +15555551001 to +15555551005
- **Static OTP:** `123456` (OTP bypass for all test numbers)
- **Configuration:** Firebase Console → Authentication → Sign-in Method → Phone

---

## 2️⃣ Phase 1: Flutter Widget Verification ✅

### Current State: **COMPLETE**

All critical widgets have been injected with Key() attributes for Appium/Cerberus identification.

### Widget Keys Verification

| Widget | Key ID | File Location | Line | Status |
|--------|--------|---------------|------|--------|
| Phone Input | `phone_input` | `lib/ui/screens/common/login_screen.dart` | 468 | ✅ Present |
| Login Button | `login_button` | `lib/ui/screens/common/login_screen.dart` | 504 | ✅ Present |
| OTP Input | `otp_input` | `lib/ui/screens/common/otp_verification_screen.dart` | 293 | ✅ Present |
| Verify Button | `verify_button` | `lib/ui/screens/common/otp_verification_screen.dart` | 368 | ✅ Present |

**Note:** Email and password inputs are **NOT USED** in this app (phone-based auth only).

### Appium Locator Strategies

```python
# Preferred: Using Key-based identifiers
phone_input = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "phone_input")
login_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_button")
otp_input = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "otp_input")
verify_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "verify_button")
```

### Build Verification

**Last Build:** February 1, 2026  
**Command:** `flutter build ios --simulator`  
**Result:** ✅ Success (41.4s)  
**Output:** `✓ Built build/ios/iphonesimulator/Runner.app`

**Action Required:** None (widget keys already present and build successful)

---

## 3️⃣ Phase 2: Cerberus Service Library Setup (The Handshake)

### Navigation

```
http://localhost:8888/ServiceList.jsp
```

### Service Configuration: GetShuffleUser

Click: **[+ Create Service]**

| Field | Value |
|-------|-------|
| **Service** | `GetShuffleUser` |
| **Group** | `Shuffle` |
| **Type** | `REST` |
| **Method** | `POST` ← **CRITICAL: POST for workflow execution** |
| **Service Path** | `%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute` |
| **Description** | `Execute Shuffle workflow to retrieve randomized test user credentials` |
| **Active** | ✅ Yes |

### Service Headers

Click: **[+ Add Header]** for each

| Header Name | Header Value | Required For |
|-------------|--------------|--------------|
| `Content-Type` | `application/json` | Both Local & Cloud |
| `Accept` | `application/json` | Both Local & Cloud |
| `Authorization` | `Bearer %SHUFFLE_API_TOKEN%` | **Cloud Only** (optional for Local) |

### Global Properties Configuration

**Navigate to:** Administration → Global Property

| Property Name | Property Value | Description |
|---------------|----------------|-------------|
| `SHUFFLE_BASE_URL` | `http://localhost:3001` | Shuffle execution endpoint (switch to `https://shuffler.io` for cloud) |
| `SHUFFLE_API_TOKEN` | `<your_shuffler_token>` | Cloud authentication token (optional for local) |

### Expected Shuffle Workflow Response

**Endpoint (Local):** `http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute`

**Response Format:**
```json
{
  "success": true,
  "execution_id": "exec_abc123",
  "shuffled_user": {
    "id": 3,
    "name": "Carol Davis",
    "email": "carol.davis@testmail.com",
    "phone": "5555551003",
    "countryCode": "+1",
    "fullPhone": "+15555551003",
    "password": "TestPass789!",
    "otp": "123456"
  }
}
```

### JSON Path Mappings for Cerberus Variables

**Configure in Test Case Step 1 Properties:**

| Cerberus Variable | JSON Path | Example Value | Purpose |
|-------------------|-----------|---------------|---------|
| `EMAIL` | `$.shuffled_user.email` | `carol.davis@testmail.com` | User email (future email/password login) |
| `PASSWORD` | `$.shuffled_user.password` | `TestPass789!` | User password (future email/password login) |
| `PHONE` | `$.shuffled_user.phone` | `5555551003` | **Phone digits only (USED IN STEP 9)** |
| `COUNTRY_CODE` | `$.shuffled_user.countryCode` | `+1` | Country dial code |
| `FULL_PHONE` | `$.shuffled_user.fullPhone` | `+15555551003` | Full phone with country code |
| `OTP` | `$.shuffled_user.otp` | `123456` | **OTP code (USED IN STEP 12)** |
| `USER_NAME` | `$.shuffled_user.name` | `Carol Davis` | User full name (for logging) |
| `USER_ID` | `$.shuffled_user.id` | `3` | User ID (for logging) |

**🚨 CRITICAL:** Note the `$.shuffled_user.` prefix for nested JSON structure!

### Service Verification Commands

**Test Local Endpoint:**
```bash
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'
```

**Test Cloud Endpoint:**
```bash
curl -X POST https://shuffler.io/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{}' | jq '.'
```

**Expected HTTP Status:** 200 OK

---

## 4️⃣ Phase 3: 15-Step Test Case Construction

### Navigation

```
http://localhost:8888/TestCaseList.jsp
```

### Test Case Header Configuration

Click: **[+ Create Test Case]**

| Field | Value |
|-------|-------|
| **Test** | `LoginTests` |
| **Test Case** | `TC001_LoginWithShuffleHandshake` |
| **Application** | `Lessimp_Mobile` |
| **Country** | `US` |
| **Status** | `WORKING` |
| **Priority** | `1` |
| **Description** | `Automated login using Shuffle Handshake with dynamic credentials from Hybrid Shuffle Workflow` |
| **Active** | ✅ Yes |

### 15-Step Test Logic

---

#### 🔹 Step 1: Call Shuffle Workflow

| Field | Value |
|-------|-------|
| **Step** | `1` |
| **Sort** | `1` |
| **Description** | `Execute Shuffle workflow to retrieve randomized test user credentials` |
| **Action** | `callService` |
| **Value1** | `GetShuffleUser` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | Before & After |
| **Fatal** | No |

**Properties (Click [+ Add Property] for each):**

| Property Name | Type | Value (JSON Path) | Database |
|---------------|------|-------------------|----------|
| `EMAIL` | `getFromJson` | `$.shuffled_user.email` | (empty) |
| `PASSWORD` | `getFromJson` | `$.shuffled_user.password` | (empty) |
| `PHONE` | `getFromJson` | `$.shuffled_user.phone` | (empty) |
| `COUNTRY_CODE` | `getFromJson` | `$.shuffled_user.countryCode` | (empty) |
| `FULL_PHONE` | `getFromJson` | `$.shuffled_user.fullPhone` | (empty) |
| `OTP` | `getFromJson` | `$.shuffled_user.otp` | (empty) |
| `USER_NAME` | `getFromJson` | `$.shuffled_user.name` | (empty) |
| `USER_ID` | `getFromJson` | `$.shuffled_user.id` | (empty) |

---

#### 🔹 Step 2: Verify Shuffle Workflow Success (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `2` |
| **Sort** | `2` |
| **Description** | `Verify Shuffle workflow returned HTTP 200 OK - STOP TEST IF SHUFFLE UNAVAILABLE` |
| **Action** | `verifyNumericEquals` |
| **Value1** | `%LASTSERVICE_HTTPSTATUS%` |
| **Value2** | `200` |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** (Critical!) |

**Purpose:** Fail-fast if Shuffle workflow is down or returns error

---

#### 🔹 Step 3: Log Shuffled User (Traceability)

| Field | Value |
|-------|-------|
| **Step** | `3` |
| **Sort** | `3` |
| **Description** | `Log shuffled user credentials for execution traceability` |
| **Action** | `calculateProperty` |
| **Value1** | `SHUFFLED_USER_LOG` |
| **Value2** | `Executing for user: EMAIL=%EMAIL%, PHONE=%PHONE%, USER_ID=%USER_ID%, USER_NAME=%USER_NAME%` |
| **Value3** | (empty) |
| **Screenshot** | No |
| **Fatal** | No |

**Purpose:** Creates visible log entry showing which Shuffle user was used

---

#### 🔹 Step 4: Validate PHONE Variable (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `4` |
| **Sort** | `4` |
| **Description** | `Verify PHONE variable is populated from Shuffle workflow` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%PHONE%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 5: Validate OTP Variable (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `5` |
| **Sort** | `5` |
| **Description** | `Verify OTP variable is populated from Shuffle workflow` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%OTP%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 6: Validate EMAIL Variable (Non-Fatal)

| Field | Value |
|-------|-------|
| **Step** | `6` |
| **Sort** | `6` |
| **Description** | `Verify EMAIL variable is populated (for future email/password login)` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%EMAIL%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | No (not used in current phone-based auth) |

---

#### 🔹 Step 7: Validate PASSWORD Variable (Non-Fatal)

| Field | Value |
|-------|-------|
| **Step** | `7` |
| **Sort** | `7` |
| **Description** | `Verify PASSWORD variable is populated (for future email/password login)` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%PASSWORD%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | No (not used in current phone-based auth) |

---

#### 🔹 Step 8: Launch Lessimp iOS App

| Field | Value |
|-------|-------|
| **Step** | `8` |
| **Sort** | `8` |
| **Description** | `Launch Lessimp iOS application on simulator` |
| **Action** | `openApplication` |
| **Value1** | `/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Note:** Appium capabilities configured in Application settings (Lessimp_Mobile)

---

#### 🔹 Step 9: Wait for Login Screen

| Field | Value |
|-------|-------|
| **Step** | `9` |
| **Sort** | `9` |
| **Description** | `Wait for phone input field to appear on login screen` |
| **Action** | `waitForElementPresent` |
| **Value1** | `identifier=phone_input` |
| **Value2** | `15000` (15 seconds) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

**Alternative Value1:** `xpath=//XCUIElementTypeTextField[@label='Phone Number']`

---

#### 🔹 Step 10: Enter Phone Number (SHUFFLE INJECTION!)

| Field | Value |
|-------|-------|
| **Step** | `10` |
| **Sort** | `10` |
| **Description** | `Enter phone number from Shuffle data into phone_input field` |
| **Action** | `type` |
| **Value1** | `identifier=phone_input` |
| **Value2** | `%PHONE%` ← **SHUFFLED DATA** |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**🎯 KEY POINT:** This injects the randomized phone number from Shuffle workflow!

---

#### 🔹 Step 11: Click Login Button

| Field | Value |
|-------|-------|
| **Step** | `11` |
| **Sort** | `11` |
| **Description** | `Click login button to trigger Firebase OTP` |
| **Action** | `click` |
| **Value1** | `identifier=login_button` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Alternative Value1:** `xpath=//XCUIElementTypeButton[@label='Login']`

---

#### 🔹 Step 12: Wait for OTP Screen

| Field | Value |
|-------|-------|
| **Step** | `12` |
| **Sort** | `12` |
| **Description** | `Wait for OTP verification screen to appear` |
| **Action** | `waitForElementPresent` |
| **Value1** | `xpath=//XCUIElementTypeStaticText[contains(@label, 'Verification')]` |
| **Value2** | `20000` (20 seconds - Firebase can be slow) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 13: Enter OTP (SHUFFLE INJECTION!)

| Field | Value |
|-------|-------|
| **Step** | `13` |
| **Sort** | `13` |
| **Description** | `Enter 6-digit OTP from Shuffle data` |
| **Action** | `type` |
| **Value1** | `identifier=otp_input` |
| **Value2** | `%OTP%` ← **SHUFFLED DATA (123456)** |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**🎯 KEY POINT:** This injects the OTP (123456 for Firebase test numbers)!

**Alternative Value1:** `xpath=//XCUIElementTypeTextField[1]`

---

#### 🔹 Step 14: Click Verify Button

| Field | Value |
|-------|-------|
| **Step** | `14` |
| **Sort** | `14` |
| **Description** | `Click verify button to submit OTP to Firebase` |
| **Action** | `click` |
| **Value1** | `identifier=verify_button` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Alternative Value1:** `xpath=//XCUIElementTypeButton[@label='Verify']`

---

#### 🔹 Step 15: Verify Login Success (SUCCESS_SNACKBAR)

| Field | Value |
|-------|-------|
| **Step** | `15` |
| **Sort** | `15` |
| **Description** | `Verify login success by detecting success snackbar or home screen element` |
| **Action** | `verifyElementVisible` |
| **Value1** | `xpath=//XCUIElementTypeOther[contains(@label, 'Home')]` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Alternative Value1:** `identifier=login_success_snackbar` (if Key added to success snackbar widget)

**Expected Result:** ✅ **Test PASS** - User logged in with Shuffle credentials

---

## 5️⃣ Phase 4: Firebase OTP Bypass

### Configuration Check

**Command:**
```bash
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py
```

**Expected Output:**
```
======================================================================
  🔐 Firebase Test Phone Numbers Configuration Helper
======================================================================

┌────────────────┬────────────────┬─────────────────────┐
│ Phone Number   │ Verification   │ User                │
│                │ Code           │                     │
├────────────────┼────────────────┼─────────────────────┤
│ +15555551001   │ 123456         │ Alice Johnson       │
│ +15555551002   │ 123456         │ Bob Smith           │
│ +15555551003   │ 123456         │ Carol Davis         │
│ +15555551004   │ 123456         │ David Wilson        │
│ +15555551005   │ 123456         │ Eve Martinez        │
└────────────────┴────────────────┴─────────────────────┘
```

### Firebase Console Configuration (Manual)

**URL:** https://console.firebase.google.com/

**Navigation:**
1. Select **Lessimp** project
2. **Authentication** → **Sign-in method** → **Phone**
3. Scroll to: **"Phone numbers for testing"**
4. Click: **[+ Add phone number]**

**Add Each Number:**

| Phone Number | Verification Code |
|--------------|-------------------|
| `+15555551001` | `123456` |
| `+15555551002` | `123456` |
| `+15555551003` | `123456` |
| `+15555551004` | `123456` |
| `+15555551005` | `123456` |

**Click:** [Save]

### Verification Checklist

- [ ] All 5 test numbers added to Firebase Console
- [ ] All test numbers have OTP: `123456`
- [ ] Firebase Phone Authentication is **Enabled**
- [ ] Shuffle workflow returns phone numbers in range +15555551001-1005
- [ ] Test numbers visible in Firebase Console under "Phone numbers for testing"

---

## 🤖 Copilot Execution Commands

### Command 1: Verify Widget Keys

```
@workspace /search "Key(" in lib/
```

**Expected:** Confirmation that `phone_input`, `login_button`, `otp_input`, `verify_button` Keys are present.

---

### Command 2: Explain Global Property Usage

```
@workspace /explain how to use %SHUFFLE_BASE_URL% as a Global Property in Cerberus to toggle between Local (http://localhost:3001) and Cloud (https://shuffler.io) environments.
```

**Expected Response:**
1. Navigate to Administration → Global Property
2. Create property: `SHUFFLE_BASE_URL`
3. Set value to `http://localhost:3001` for local testing
4. Use `%SHUFFLE_BASE_URL%` in Service Path: `%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute`
5. To switch to cloud: Update property value to `https://shuffler.io`
6. Add `Authorization: Bearer %SHUFFLE_API_TOKEN%` header for cloud execution

---

### Command 3: Commit All Changes

```
@workspace commit all changes to branch lessimp-dev.
```

**Expected:** Git commit with message describing Master Directive completion.

---

## 📊 Visual Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     CERBERUS TEST ENGINE                         │
│                    (http://localhost:8888)                       │
└────────────┬─────────────────────────────────────┬───────────────┘
             │                                     │
             │ Step 1: callService                 │ Steps 8-15: Mobile UI
             │ (GetShuffleUser)                    │ Automation
             │                                     │
             ▼                                     ▼
┌────────────────────────────┐      ┌─────────────────────────────┐
│   SHUFFLE WORKFLOW         │      │   APPIUM + iOS SIMULATOR    │
│   (Hybrid Execution)       │      │   (iPhone 16 Pro)           │
├────────────────────────────┤      ├─────────────────────────────┤
│ Local:  localhost:3001     │      │ App: Runner.app             │
│ Cloud:  shuffler.io        │      │ Locators: identifier=       │
└────────────┬───────────────┘      │ - phone_input               │
             │                      │ - login_button              │
             │ Returns:             │ - otp_input                 │
             │ {shuffled_user: {    │ - verify_button             │
             │   phone: "...",      └──────────┬──────────────────┘
             │   otp: "123456"      │          │
             │ }}                   │          │ Firebase Auth
             │                      │          │ Phone + OTP
             └──────────────────────┼──────────▼──────────────────┐
                                    │   FIREBASE CONSOLE          │
                                    │   Test Numbers: +1555555    │
                                    │   1001-1005                 │
                                    │   Static OTP: 123456        │
                                    └─────────────────────────────┘
```

---

## ✅ Execution Readiness Checklist

### Pre-Flight Checks

- [ ] Cerberus running on http://localhost:8888/
- [ ] MySQL database accessible (port 13306)
- [ ] Shuffle workflow accessible (test with curl)
- [ ] iOS Simulator booted: `xcrun simctl boot "iPhone 16 Pro"`
- [ ] Flutter app built: `flutter build ios --simulator`
- [ ] Firebase test numbers configured (5 numbers, OTP: 123456)
- [ ] Appium server running (if external): `appium -p 4723`

### Cerberus Configuration

- [ ] System created: `PROD_SYSTEM`
- [ ] Application created: `Lessimp_Mobile` (Type: MOBILE, Platform: iOS)
- [ ] Global Property created: `SHUFFLE_BASE_URL` = `http://localhost:3001`
- [ ] Service created: `GetShuffleUser` (Method: POST)
- [ ] Test created: `LoginTests`
- [ ] Test Case created: `TC001_LoginWithShuffleHandshake` (15 steps)

### Execution

- [ ] Run test in Cerberus UI: Run → Test Queue → Manual Execution
- [ ] Select: TC001_LoginWithShuffleHandshake
- [ ] Click: [Run Test]
- [ ] Expected: All 15 steps PASS, user logged in

---

## 🚀 Quick Start Commands

### Start Shuffle Local Engine
```bash
# Assumes Shuffle is installed and configured
cd ~/shuffle
docker-compose up -d
# Verify: curl http://localhost:3001/api/v1/workflows
```

### Start Cerberus
```bash
cd ~/Documents/GitHub/cerberus-core
docker-compose up -d
# Access: http://localhost:8888/
```

### Boot iOS Simulator
```bash
xcrun simctl boot "iPhone 16 Pro"
open -a Simulator
```

### Build Flutter App
```bash
cd ~/Documents/GitHub/lessimp
flutter build ios --simulator
```

### Verify Firebase Test Numbers
```bash
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py
```

### Test Shuffle Workflow (Local)
```bash
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.shuffled_user'
```

---

## 📝 Notes & Best Practices

### Shuffle Hybrid Strategy

**When to Use Local:**
- Development/debugging
- No internet connectivity
- Faster execution (no network latency)
- No authentication required

**When to Use Cloud:**
- Production testing
- CI/CD pipelines
- Team collaboration
- Workflow sharing across environments

### Cerberus Variable Naming

**Convention:** Use UPPERCASE for Cerberus variables to distinguish from Shuffle JSON fields.

**Examples:**
- `%PHONE%` (Cerberus variable)
- `$.shuffled_user.phone` (JSON path)
- `%SHUFFLE_BASE_URL%` (Global property)

### Fatal vs Non-Fatal Steps

**Fatal Steps (Stop execution on failure):**
- Step 2: HTTP 200 verification
- Step 4: PHONE validation
- Step 5: OTP validation
- Step 9: Wait for login screen
- Step 12: Wait for OTP screen

**Non-Fatal Steps (Continue execution):**
- Step 3: Logging
- Step 6-7: EMAIL/PASSWORD validation (not used yet)
- Step 10-11: Type/click actions
- Step 13-15: Type/click/verify actions

### Debugging Tips

**If Step 1 fails (callService):**
1. Verify Shuffle endpoint: `curl -X POST <endpoint>`
2. Check Cerberus Service Library configuration
3. Verify Global Property `SHUFFLE_BASE_URL` is set
4. Check network connectivity (for cloud)

**If Step 2 fails (HTTP 200):**
1. Check Shuffle workflow logs
2. Verify workflow ID is correct
3. Check authentication (for cloud)

**If Steps 10-15 fail (Mobile UI):**
1. Verify iOS Simulator is booted
2. Check Runner.app exists at build path
3. Verify Appium capabilities in Lessimp_Mobile application
4. Use Appium Inspector to verify element locators

---

## 📦 Database Import JSON (Next Section)

See `CERBERUS_TC001_DATABASE_IMPORT.json` for complete test case import.

---

**Status:** ✅ **READY FOR EXECUTION**  
**Master Directive Version:** 2.0  
**Last Updated:** February 1, 2026  
**Author:** GitHub Copilot AI Agent
