# 🎯 Phase 2 Execution Report - Shuffle Handshake Implementation

## ✅ Task 1: Widget Key Injection (COMPLETE)

### Changes Made to Flutter Code

#### 1. Modified `lib/ui/widgets/common_widgets.dart`

**Function: `getTextField`**
- **Added parameter:** `Key? key` (line 176)
- **Applied to widget:** `TextFormField(key: key, ...)` (line 192)
- **Purpose:** Allows passing Key to any TextField widget for Appium identification

**Function: `getButton`**
- **Added parameter:** `Key? key` (line 705)
- **Applied to widget:** `MaterialButton(key: key, ...)` (line 716)
- **Purpose:** Allows passing Key to any Button widget for Appium identification

---

#### 2. Modified `lib/ui/screens/common/login_screen.dart`

**Phone Input Field (line 468)**
```dart
getTextField(
    key: const Key('phone_input'),  // ✅ ADDED
    label: phoneNumber,
    textInputType: TextInputType.numberWithOptions(signed: true),
    inputFormatters: [FilteringTextInputFormatter.digitsOnly],
    prefixIcon: CountryCodePicker(...),
    controller: _phoneController
)
```

**Login Button (line 501)**
```dart
getButton(
    key: const Key('login_button'),  // ✅ ADDED
    isLoading: state.status == AuthStatus.loading || state.status == AuthStatus.signUpSendOtpLoading,
    data: login,
    width: width,
    onPressed: () { ... }
)
```

---

#### 3. Modified `lib/ui/screens/common/otp_verification_screen.dart`

**OTP Input Field (line 292)**
```dart
Pinput(
    key: const Key('otp_input'),  // ✅ ADDED
    length: 6,
    controller: pinController,
    focusNode: focusNode,
    defaultPinTheme: defaultPinTheme,
    ...
)
```

**Verify Button (line 366)**
```dart
getButton(
    key: const Key('verify_button'),  // ✅ ADDED
    isLoading: state.status == AuthStatus.verifyotploading || state.status == AuthStatus.infoAtLoginLoading,
    data: verify,
    width: width,
    onPressed: () { ... }
)
```

---

### Build Status

**Command executed:**
```bash
flutter build ios --simulator
```

**Result:** ✅ **Success**
```
Building com.lessimp.lessimp for simulator (ios)...
Running Xcode build...
Xcode build done. 41.4s
✓ Built build/ios/iphonesimulator/Runner.app
```

**Build path:**
```
/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
```

---

### Appium Locator Strategies (Now Available)

| Widget | Key ID | Accessibility ID Locator | XPath Locator (Fallback) |
|--------|--------|--------------------------|---------------------------|
| Phone Input | `phone_input` | `identifier=phone_input` | `xpath=//XCUIElementTypeTextField[@label='Phone Number']` |
| Login Button | `login_button` | `identifier=login_button` | `xpath=//XCUIElementTypeButton[@label='Login']` |
| OTP Input | `otp_input` | `identifier=otp_input` | `xpath=//XCUIElementTypeTextField[1]` |
| Verify Button | `verify_button` | `identifier=verify_button` | `xpath=//XCUIElementTypeButton[@label='Verify']` |

---

## 📋 Task 2: Cerberus Service Library Setup

### Navigation
```
http://localhost:8888/ServiceList.jsp
```

### Service Configuration: GetShuffleUser

Click: **[+ Create Service]**

| Field | Value |
|-------|-------|
| **Service** | `GetShuffleUser` |
| **Group** | `Shuffle` (optional) |
| **Type** | `REST` |
| **Method** | `GET` |
| **Service Path** | `http://localhost:5000/shuffle/get_user` |
| **Description** | `Retrieve random test user from Shuffle data provider for automated testing` |
| **Active** | ✅ Yes |

### Service Headers

Click: **[+ Add Header]**

| Header Name | Header Value |
|-------------|--------------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |

**Note:** No Authorization header needed (shuffle_provider.py has no auth)

---

### Expected Service Response

**Endpoint:** http://localhost:5000/shuffle/get_user

**Response Format:**
```json
{
  "id": 3,
  "name": "Carol Davis",
  "email": "carol.davis@testmail.com",
  "phone": "5555551003",
  "countryCode": "+1",
  "fullPhone": "+15555551003",
  "password": "TestPass789!",
  "otp": "123456",
  "timestamp": "2026-02-01T18:30:00.123456",
  "source": "shuffle_provider"
}
```

---

### JSON Path Mappings for Cerberus Variables

These will be configured in **Test Case Step 1 Properties:**

| Cerberus Variable | JSON Path | Example Value | Purpose |
|-------------------|-----------|---------------|---------|
| `EMAIL` | `$.email` | `carol.davis@testmail.com` | User email (for email/password login) |
| `PASSWORD` | `$.password` | `TestPass789!` | User password (for email/password login) |
| `PHONE` | `$.phone` | `5555551003` | Phone number digits only (for phone login) |
| `COUNTRY_CODE` | `$.countryCode` | `+1` | Country dial code |
| `FULL_PHONE` | `$.fullPhone` | `+15555551003` | Full phone with country code |
| `OTP` | `$.otp` | `123456` | OTP code for Firebase test numbers |
| `USER_NAME` | `$.name` | `Carol Davis` | User full name (for logging) |
| `USER_ID` | `$.id` | `3` | User ID (for logging) |

---

### Service Verification

**Before creating test case, verify service works:**

#### Method 1: Manual Test in Browser
```
http://localhost:5000/shuffle/get_user
```

Expected: JSON response with randomized user

#### Method 2: curl Command
```bash
curl -s http://localhost:5000/shuffle/get_user | jq '.'
```

Expected output:
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
  "timestamp": "2026-02-01T20:15:32.654321",
  "source": "shuffle_provider"
}
```

#### Method 3: Test in Cerberus (After Service Creation)
```
Administration → Service Library → GetShuffleUser
Click: [Test Service]
```

Expected: HTTP 200, JSON response displayed

---

## 🧪 Task 3: 15-Step Test Case Construction

### Navigation
```
http://localhost:8888/TestCaseList.jsp
```

### Test Case Configuration

Click: **[+ Create Test Case]**

| Field | Value |
|-------|-------|
| **Test** | `LoginTests` |
| **Test Case** | `TC001_LoginWithShuffleHandshake` |
| **Application** | `Lessimp_Mobile` |
| **Country** | `US` (or appropriate) |
| **Status** | `WORKING` |
| **Priority** | `1` |
| **Description** | `Automated login using Shuffle Handshake with dynamic credentials from Shuffle API` |
| **Active** | ✅ Yes |

**Click:** [Create]

---

### Test Case Steps (15 Total)

#### 🔹 Step 1: Call Shuffle Service

| Field | Value |
|-------|-------|
| **Step** | `1` |
| **Sort** | `1` |
| **Description** | `Get random user credentials from Shuffle API` |
| **Action** | `callService` |
| **Value1** | `GetShuffleUser` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | Before & After |
| **Fatal** | No |

**Properties (Click [+ Add Property] for each):**

| Property Name | Type | Value (JSON Path) | Database |
|---------------|------|-------------------|----------|
| `EMAIL` | `getFromJson` | `$.email` | (empty) |
| `PASSWORD` | `getFromJson` | `$.password` | (empty) |
| `PHONE` | `getFromJson` | `$.phone` | (empty) |
| `COUNTRY_CODE` | `getFromJson` | `$.countryCode` | (empty) |
| `FULL_PHONE` | `getFromJson` | `$.fullPhone` | (empty) |
| `OTP` | `getFromJson` | `$.otp` | (empty) |
| `USER_NAME` | `getFromJson` | `$.name` | (empty) |
| `USER_ID` | `getFromJson` | `$.id` | (empty) |

---

#### 🔹 Step 2: Verify Shuffle API Success (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `2` |
| **Sort** | `2` |
| **Description** | `Verify Shuffle API returned HTTP 200 OK - STOP TEST IF SHUFFLE UNAVAILABLE` |
| **Action** | `verifyNumericEquals` |
| **Value1** | `%LASTSERVICE_HTTPSTATUS%` |
| **Value2** | `200` |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** (Critical!) |

**Purpose:** Fail-fast if Shuffle API is down or returns error (401, 500, etc.)

---

#### 🔹 Step 3: Validate EMAIL Variable (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `3` |
| **Sort** | `3` |
| **Description** | `Verify EMAIL variable is populated from Shuffle` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%EMAIL%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 4: Validate PASSWORD Variable (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `4` |
| **Sort** | `4` |
| **Description** | `Verify PASSWORD variable is populated from Shuffle` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%PASSWORD%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 5: Validate PHONE Variable (FATAL)

| Field | Value |
|-------|-------|
| **Step** | `5` |
| **Sort** | `5` |
| **Description** | `Verify PHONE variable is populated from Shuffle` |
| **Action** | `verifyStringDifferent` |
| **Value1** | `%PHONE%` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 6: Debug Logging (Traceability)

| Field | Value |
|-------|-------|
| **Step** | `6` |
| **Sort** | `6` |
| **Description** | `Log shuffled user credentials for execution traceability` |
| **Action** | `calculateProperty` |
| **Value1** | `SHUFFLED_USER_LOG` |
| **Value2** | `Shuffle returned: USER_ID=%USER_ID%, NAME=%USER_NAME%, EMAIL=%EMAIL%, PHONE=%PHONE%, OTP=%OTP%` |
| **Value3** | (empty) |
| **Screenshot** | No |
| **Fatal** | No |

**Purpose:** Creates visible log entry in execution history showing which Shuffle user was used

---

#### 🔹 Step 7: Launch Lessimp iOS App

| Field | Value |
|-------|-------|
| **Step** | `7` |
| **Sort** | `7` |
| **Description** | `Launch Lessimp iOS application on simulator` |
| **Action** | `openApplication` |
| **Value1** | `/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Note:** Appium capabilities configured in Application settings (Lessimp_Mobile)

---

#### 🔹 Step 8: Wait for Login Screen

| Field | Value |
|-------|-------|
| **Step** | `8` |
| **Sort** | `8` |
| **Description** | `Wait for phone input field to appear on login screen` |
| **Action** | `waitForElementPresent` |
| **Value1** | `identifier=phone_input` |
| **Value2** | `15000` (15 seconds) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

**Alternative Value1 (if Key not working):** `xpath=//XCUIElementTypeTextField[@label='Phone Number']`

---

#### 🔹 Step 9: Enter Phone Number (SHUFFLE DATA INJECTION!)

| Field | Value |
|-------|-------|
| **Step** | `9` |
| **Sort** | `9` |
| **Description** | `Enter phone number from Shuffle data into phone_input field` |
| **Action** | `type` |
| **Value1** | `identifier=phone_input` |
| **Value2** | `%PHONE%` ← **SHUFFLED DATA** |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**🎯 KEY POINT:** This injects the randomized phone number from Shuffle API!

---

#### 🔹 Step 10: Click Login Button

| Field | Value |
|-------|-------|
| **Step** | `10` |
| **Sort** | `10` |
| **Description** | `Click login button to trigger Firebase OTP` |
| **Action** | `click` |
| **Value1** | `identifier=login_button` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Alternative Value1 (if Key not working):** `xpath=//XCUIElementTypeButton[@label='Login']`

---

#### 🔹 Step 11: Wait for OTP Screen

| Field | Value |
|-------|-------|
| **Step** | `11` |
| **Sort** | `11` |
| **Description** | `Wait for OTP verification screen to appear` |
| **Action** | `waitForElementPresent` |
| **Value1** | `xpath=//XCUIElementTypeStaticText[contains(@label, 'Verification')]` |
| **Value2** | `20000` (20 seconds - Firebase can be slow) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 12: Enter OTP (SHUFFLE DATA INJECTION!)

| Field | Value |
|-------|-------|
| **Step** | `12` |
| **Sort** | `12` |
| **Description** | `Enter 6-digit OTP from Shuffle data` |
| **Action** | `type` |
| **Value1** | `identifier=otp_input` |
| **Value2** | `%OTP%` ← **SHUFFLED DATA (123456)** |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**🎯 KEY POINT:** This injects the OTP (always 123456 for Firebase test numbers)!

**Alternative Value1 (if Key not working):** `xpath=//XCUIElementTypeTextField[1]`

---

#### 🔹 Step 13: Click Verify Button

| Field | Value |
|-------|-------|
| **Step** | `13` |
| **Sort** | `13` |
| **Description** | `Click verify button to submit OTP to Firebase` |
| **Action** | `click` |
| **Value1** | `identifier=verify_button` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Alternative Value1 (if Key not working):** `xpath=//XCUIElementTypeButton[@label='Verify']`

---

#### 🔹 Step 14: Wait for Login Success

| Field | Value |
|-------|-------|
| **Step** | `14` |
| **Sort** | `14` |
| **Description** | `Wait for home screen after successful login` |
| **Action** | `waitForElementPresent` |
| **Value1** | `xpath=//XCUIElementTypeOther[contains(@label, 'Home')]` |
| **Value2** | `15000` (15 seconds) |
| **Value3** | (empty) |
| **Screenshot** | On Failure |
| **Fatal** | ✅ **YES** |

---

#### 🔹 Step 15: Verify Login Success

| Field | Value |
|-------|-------|
| **Step** | `15` |
| **Sort** | `15` |
| **Description** | `Confirm user successfully logged in to home screen` |
| **Action** | `verifyElementPresent` |
| **Value1** | `xpath=//XCUIElementTypeOther[contains(@label, 'Home')]` |
| **Value2** | (empty) |
| **Value3** | (empty) |
| **Screenshot** | After |
| **Fatal** | No |

**Expected Result:** ✅ **Test PASS** - User logged in with Shuffle credentials

---

## 🔐 Task 4: Firebase OTP Bypass Verification

### Check if firebase_test_numbers_helper.py Executed

**Command:**
```bash
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py
```

**Expected Output:**
```
======================================================================
  🔐 Firebase Test Phone Numbers Configuration Helper
======================================================================

...

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

---

### Firebase Console Configuration (Manual)

**URL:** https://console.firebase.google.com/

**Navigation:**
1. Select Lessimp project
2. Authentication → Sign-in method → Phone
3. Scroll to: "Phone numbers for testing"
4. Click: [+ Add phone number]

**Add Each Number:**

| Phone Number | Verification Code |
|--------------|-------------------|
| `+15555551001` | `123456` |
| `+15555551002` | `123456` |
| `+15555551003` | `123456` |
| `+15555551004` | `123456` |
| `+15555551005` | `123456` |

**Click:** [Save]

---

### Verification Checklist

- [ ] All 5 test numbers added to Firebase Console
- [ ] All test numbers have OTP: `123456`
- [ ] Firebase Phone Authentication is **Enabled**
- [ ] Test numbers visible in Firebase Console under "Phone numbers for testing"

---

### Manual Testing (Optional but Recommended)

**Test one number manually in Lessimp app:**

1. Launch app on simulator
2. Enter phone: `5555551001`
3. Click login button
4. **Verify:** OTP screen appears (no SMS sent)
5. Enter OTP: `123456`
6. Click verify button
7. **Expected:** Login successful, home screen appears

If this works, Cerberus automation will work!

---

## 📊 calculateProperty for Traceability

### Purpose

The `calculateProperty` action in Step 6 creates a log entry visible in Cerberus execution history. This provides **traceability** - you can see exactly which Shuffle user was used for each test run.

### Syntax

| Field | Value |
|-------|-------|
| **Action** | `calculateProperty` |
| **Value1** | `PROPERTY_NAME` (e.g., `SHUFFLED_USER_LOG`) |
| **Value2** | `Message with %VARIABLE% substitution` |
| **Value3** | (empty) |

### Example

**Value2:**
```
Shuffle returned: USER_ID=%USER_ID%, NAME=%USER_NAME%, EMAIL=%EMAIL%, PHONE=%PHONE%, OTP=%OTP%
```

**Runtime Substitution:**
```
Shuffle returned: USER_ID=3, NAME=Carol Davis, EMAIL=carol.davis@testmail.com, PHONE=5555551003, OTP=123456
```

### Where to See This

**Cerberus UI:**
1. Run → Execution History
2. Select execution
3. Click [View Details]
4. Look for Step 6
5. See property `SHUFFLED_USER_LOG` with substituted values

**Why This Matters:**
- ✅ Debugging: Know which user was used if test fails
- ✅ Auditing: Track test data used in each execution
- ✅ Reporting: Include in test reports
- ✅ Compliance: Prove randomized testing

---

## 🎯 JSON Mapping Logic for Service Library

### @workspace Response: How to Map JSON to Cerberus Variables

The Shuffle API returns this JSON structure:

```json
{
  "id": 3,
  "name": "Carol Davis",
  "email": "carol.davis@testmail.com",
  "phone": "5555551003",
  "countryCode": "+1",
  "fullPhone": "+15555551003",
  "password": "TestPass789!",
  "otp": "123456",
  "timestamp": "2026-02-01T18:30:00.123456",
  "source": "shuffle_provider"
}
```

### JSON Path Syntax

Cerberus uses **JSON Path** to extract values from API responses.

**Basic Syntax:**
- `$` = Root of JSON object
- `.field` = Access field by name
- `['field']` = Alternative syntax for field access
- `[0]` = Access array element by index

### Mapping Table

| JSON Field | JSON Path | Cerberus Variable | Example Value |
|------------|-----------|-------------------|---------------|
| `id` | `$.id` | `%USER_ID%` | `3` |
| `name` | `$.name` | `%USER_NAME%` | `Carol Davis` |
| `email` | `$.email` | `%EMAIL%` | `carol.davis@testmail.com` |
| `phone` | `$.phone` | `%PHONE%` | `5555551003` |
| `countryCode` | `$.countryCode` | `%COUNTRY_CODE%` | `+1` |
| `fullPhone` | `$.fullPhone` | `%FULL_PHONE%` | `+15555551003` |
| `password` | `$.password` | `%PASSWORD%` | `TestPass789!` |
| `otp` | `$.otp` | `%OTP%` | `123456` |
| `timestamp` | `$.timestamp` | `%TIMESTAMP%` | `2026-02-01T18:30:00.123456` |
| `source` | `$.source` | `%SOURCE%` | `shuffle_provider` |

### How to Configure in Cerberus

**In Test Case Step 1 (callService):**

For each variable you want to store:

1. Click **[+ Add Property]**
2. **Property Name:** `PHONE` (without % symbols)
3. **Type:** `getFromJson`
4. **Value:** `$.phone` (JSON Path)
5. **Database:** (leave empty)
6. Click **[Save]**

**Repeat for all variables:** EMAIL, PASSWORD, PHONE, OTP, etc.

### Using Variables in Later Steps

Once stored, variables are accessed with `%VARIABLE_NAME%` syntax:

**Example (Step 9 - type action):**
- **Value2:** `%PHONE%`
- **Runtime substitution:** `5555551003`

**Example (Step 12 - type action):**
- **Value2:** `%OTP%`
- **Runtime substitution:** `123456`

---

## 🚀 Copy-Paste Ready: Service Library JSON Config

### For Cerberus UI (if there's an import feature)

```json
{
  "service": "GetShuffleUser",
  "group": "Shuffle",
  "type": "REST",
  "method": "GET",
  "servicePath": "http://localhost:5000/shuffle/get_user",
  "description": "Retrieve random test user from Shuffle data provider for automated testing",
  "active": true,
  "headers": [
    {
      "name": "Content-Type",
      "value": "application/json"
    },
    {
      "name": "Accept",
      "value": "application/json"
    }
  ],
  "responseMapping": [
    {"variable": "EMAIL", "jsonPath": "$.email"},
    {"variable": "PASSWORD", "jsonPath": "$.password"},
    {"variable": "PHONE", "jsonPath": "$.phone"},
    {"variable": "COUNTRY_CODE", "jsonPath": "$.countryCode"},
    {"variable": "FULL_PHONE", "jsonPath": "$.fullPhone"},
    {"variable": "OTP", "jsonPath": "$.otp"},
    {"variable": "USER_NAME", "jsonPath": "$.name"},
    {"variable": "USER_ID", "jsonPath": "$.id"}
  ]
}
```

**Note:** Cerberus v4.20 may not support JSON import. Use this as reference for manual entry.

---

## ✅ Phase 2 Execution Summary

### Completed Tasks

- ✅ **Task 1:** Widget Key Injection
  - Modified `common_widgets.dart` (getTextField, getButton functions)
  - Added Key to `phone_input` in login_screen.dart
  - Added Key to `login_button` in login_screen.dart
  - Added Key to `otp_input` in otp_verification_screen.dart
  - Added Key to `verify_button` in otp_verification_screen.dart
  - Built iOS simulator app successfully

- 📝 **Task 2:** Cerberus Service Library Setup (Documentation Provided)
  - Service configuration: GetShuffleUser
  - JSON Path mappings documented
  - Verification commands provided

- 📝 **Task 3:** 15-Step Test Case Construction (Complete Specification Provided)
  - All 15 steps documented with exact fields
  - Shuffle API call with variable storage
  - HTTP status verification (Fatal)
  - Variable validation (Fatal)
  - Mobile UI automation with variable injection
  - Debug logging for traceability

- 📝 **Task 4:** Firebase OTP Bypass (Instructions Provided)
  - firebase_test_numbers_helper.py ready to run
  - Manual Firebase Console configuration steps
  - Verification checklist

### Next Actions Required (User Side)

1. ✅ **Start Shuffle API** (if not running)
   ```bash
   cd ~/Documents/GitHub/cerberus-core
   python3 shuffle_provider.py --api --port 5000
   ```

2. ✅ **Configure Firebase Test Numbers** (manual in Firebase Console)
   - Follow instructions in Task 4 above
   - Add 5 numbers (+15555551001-1005, OTP: 123456)

3. ✅ **Create Cerberus Service** (manual in Cerberus UI)
   - Follow instructions in Task 2 above
   - Service name: GetShuffleUser
   - URL: http://localhost:5000/shuffle/get_user

4. ✅ **Create Cerberus Test Case** (manual in Cerberus UI)
   - Follow instructions in Task 3 above
   - Test case: TC001_LoginWithShuffleHandshake
   - 15 steps with exact configurations

5. ✅ **Execute Test** (Cerberus UI)
   - Run → Test Queue → Manual Execution
   - Select TC001_LoginWithShuffleHandshake
   - Click [Run Test]

---

**Status:** Phase 2 documentation complete. Flutter code modifications committed. Ready for Cerberus UI configuration.

**Date:** February 1, 2026  
**Build Path:** `/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app`  
**Widget Keys Added:** phone_input, login_button, otp_input, verify_button
