# 🎯 SHUFFLE HANDSHAKE - Quick Reference Card

## 🚀 Complete Implementation in 4 Steps

---

## Step 1: Start Shuffle API

```bash
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000
```

**Verify:**
```bash
curl http://localhost:5000/shuffle/health
# Expected: {"status": "healthy", "service": "shuffle_provider"}
```

---

## Step 2: Configure Firebase Test Numbers

### A. Run Configuration Helper
```bash
python3 ~/Documents/GitHub/cerberus-core/firebase_test_numbers_helper.py
```

### B. Open Firebase Console
1. **URL:** https://console.firebase.google.com/
2. **Navigate:** Authentication → Sign-in method → Phone
3. **Scroll to:** "Phone numbers for testing"

### C. Add 5 Test Numbers

| Phone Number | Verification Code |
|--------------|-------------------|
| `+15555551001` | `123456` |
| `+15555551002` | `123456` |
| `+15555551003` | `123456` |
| `+15555551004` | `123456` |
| `+15555551005` | `123456` |

**Click:** [Save]

---

## Step 3: Configure Cerberus Service

### A. Register GetShuffleUser Service

**Navigation:** Cerberus UI → Administration → Service Library

**Click:** [+ Create Service]

| Field | Value |
|-------|-------|
| **Service Name** | `GetShuffleUser` |
| **Type** | `REST` |
| **Method** | `GET` |
| **Service Path** | `http://localhost:5000/shuffle/get_user` |
| **Active** | ✅ Yes |

**Headers:**
- Content-Type: `application/json`
- Accept: `application/json`

**Click:** [Save]

---

### B. Create Test Case

**Navigation:** Test → Test Case → [+ Create Test Case]

| Field | Value |
|-------|-------|
| **Test** | `LoginTests` |
| **Test Case** | `TC001_LoginWithShuffleHandshake` |
| **Application** | `Lessimp_Mobile` |
| **Status** | `WORKING` |

**Click:** [Create]

---

### C. Add Test Steps

#### Step 1: Call Shuffle API
```
Action:       callService
Value1:       GetShuffleUser
Description:  Get random user from Shuffle

Properties (Store Response):
  EMAIL      → $.email
  PASSWORD   → $.password
  PHONE      → $.phone
  OTP        → $.otp
```

#### Step 2: Verify HTTP 200
```
Action:       verifyNumericEquals
Value1:       %LASTSERVICE_HTTPSTATUS%
Value2:       200
Fatal:        ✅ Yes
```

#### Step 3-5: Validate Variables
```
Action:       verifyStringDifferent
Value1:       %EMAIL% (then %PASSWORD%, then %PHONE%)
Value2:       (empty)
Fatal:        ✅ Yes
```

#### Step 6: Debug Log
```
Action:       calculateProperty
Value1:       SHUFFLED_USER_LOG
Value2:       Shuffle: EMAIL=%EMAIL%, PHONE=%PHONE%, OTP=%OTP%
```

#### Step 7: Launch App
```
Action:       openApplication
Value1:       /Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
```

#### Step 8: Wait for Login Screen
```
Action:       waitForElementPresent
Value1:       xpath=//XCUIElementTypeTextField[@label='Phone Number']
Value2:       15000
```

#### Step 9: Enter Phone (SHUFFLE DATA!)
```
Action:       type
Value1:       xpath=//XCUIElementTypeTextField[@label='Phone Number']
Value2:       %PHONE%  ← INJECTED FROM SHUFFLE
```

#### Step 10: Click Login
```
Action:       click
Value1:       xpath=//XCUIElementTypeButton[@label='Login']
```

#### Step 11: Wait for OTP Screen
```
Action:       waitForElementPresent
Value1:       xpath=//XCUIElementTypeStaticText[contains(@label, 'Verification')]
Value2:       20000
```

#### Step 12: Enter OTP (SHUFFLE DATA!)
```
Action:       type
Value1:       xpath=//XCUIElementTypeTextField[1]
Value2:       %OTP%  ← INJECTED FROM SHUFFLE
```

#### Step 13: Click Verify
```
Action:       click
Value1:       xpath=//XCUIElementTypeButton[@label='Verify']
```

#### Step 14-15: Verify Success
```
Action:       waitForElementPresent
Value1:       xpath=//XCUIElementTypeOther[contains(@label, 'Home')]
Value2:       15000

Action:       verifyElementPresent
Value1:       xpath=//XCUIElementTypeOther[contains(@label, 'Home')]
```

---

## Step 4: Execute Test

### A. Pre-Flight Checklist
```bash
# 1. Shuffle API running
curl http://localhost:5000/shuffle/health

# 2. iOS Simulator booted
xcrun simctl boot "iPhone 16 Pro"
open -a Simulator

# 3. Lessimp app built
ls -d ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app

# 4. Cerberus accessible
curl -I http://localhost:8888/
```

### B. Run Test
1. **Navigate:** Run → Test Queue → Manual Execution
2. **Select:** TC001_LoginWithShuffleHandshake
3. **Click:** [Run Test]

### C. Monitor Execution
1. **Navigate:** Run → Execution History
2. **Find:** Latest execution
3. **Expected Result:** ✅ All 15 steps PASS

---

## 🎯 Expected Test Flow

```
Step 1:  callService → Shuffle returns random user
         Response: {"phone": "5555551003", "otp": "123456", ...}
         
Step 2:  HTTP 200? ✅ YES
         
Step 3:  %EMAIL% populated? ✅ YES (carol.davis@testmail.com)
         
Step 4:  %PASSWORD% populated? ✅ YES (TestPass789!)
         
Step 5:  %PHONE% populated? ✅ YES (5555551003)
         
Step 6:  Log: "Shuffle: EMAIL=carol.davis@testmail.com, PHONE=5555551003, OTP=123456"
         
Step 7:  Launch Lessimp iOS app ✅
         
Step 8:  Phone input field found ✅
         
Step 9:  Type "5555551003" into phone_input ✅ (from Shuffle!)
         
Step 10: Click login button ✅
         
Step 11: OTP screen appeared ✅
         
Step 12: Type "123456" into otp_input ✅ (from Shuffle!)
         
Step 13: Click verify button ✅
         
Step 14: Home screen appeared ✅
         
Step 15: Login success verified ✅

Test Result: ✅ PASS
User: Carol Davis (randomized by Shuffle)
```

---

## 🔧 Troubleshooting

### Issue: Shuffle API call fails
```bash
# Check Shuffle is running
curl http://localhost:5000/shuffle/health

# If not running:
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000
```

### Issue: Variables not populated
**Check JSON paths in Step 1 Properties:**
- EMAIL: `$.email` (not `$.user.email`)
- PASSWORD: `$.password`
- PHONE: `$.phone`
- OTP: `$.otp`

### Issue: OTP verification fails
**Verify Firebase test numbers:**
1. Open Firebase Console
2. Authentication → Sign-in method → Phone
3. Confirm +15555551001-1005 all have OTP: 123456

### Issue: Element not found
**Increase wait timeouts:**
- Step 8: Change 15000 → 30000
- Step 11: Change 20000 → 30000

---

## 📊 Shuffle Data Structure

**API Endpoint:** http://localhost:5000/shuffle/get_user

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
  "timestamp": "2026-02-01T18:30:00",
  "source": "shuffle_provider"
}
```

**Cerberus Variables:**
- `%EMAIL%` = carol.davis@testmail.com
- `%PASSWORD%` = TestPass789!
- `%PHONE%` = 5555551003
- `%FULL_PHONE%` = +15555551003
- `%OTP%` = 123456

---

## ✅ Success Criteria

Test passes when:
- ✅ Shuffle API returns HTTP 200
- ✅ All variables populated (%EMAIL%, %PASSWORD%, %PHONE%, %OTP%)
- ✅ Phone number entered into Lessimp UI (from Shuffle)
- ✅ OTP entered into Lessimp UI (from Shuffle)
- ✅ User reaches home screen (login successful)
- ✅ Each test run uses different Shuffle user (randomized)

---

## 🎓 Key Concepts

### 1. Shuffle Handshake = Dynamic Data Injection
- Cerberus gets credentials from Shuffle API
- Cerberus injects credentials into Lessimp mobile UI
- No hardcoded credentials in test cases

### 2. Error Handling = Fail Fast
- If Shuffle API fails (HTTP ≠ 200) → Test fails immediately
- If variables empty → Test fails before UI automation
- Fatal flags prevent wasted test execution

### 3. Traceability = Debug Logging
- Step 6 logs which Shuffle user was used
- Execution history shows variable values
- Screenshots captured at critical steps

### 4. Firebase Test Numbers = OTP Bypass
- Test numbers bypass actual SMS sending
- All use fixed OTP: 123456
- Configured in Firebase Console

---

## 📚 Full Documentation

For complete details, see:
- **SHUFFLE_HANDSHAKE_IMPLEMENTATION.md** (24 KB complete guide)
- **firebase_test_numbers_helper.py** (configuration helper script)
- **MASTER_TECHNICAL_REFERENCE.md** (system architecture)
- **CERBERUS_TEST_CASE_SETUP.md** (step-by-step setup)

---

## 🚀 Quick Start Commands

```bash
# 1. Start Shuffle API
cd ~/Documents/GitHub/cerberus-core && python3 shuffle_provider.py --api --port 5000 &

# 2. Verify Shuffle
curl http://localhost:5000/shuffle/get_user | jq '.phone, .otp'

# 3. Boot iOS Simulator
xcrun simctl boot "iPhone 16 Pro"

# 4. Open Cerberus
open http://localhost:8888/

# 5. Configure Firebase (manual in browser)
open https://console.firebase.google.com/

# 6. Run Test (in Cerberus UI)
# Run → Test Queue → TC001_LoginWithShuffleHandshake → Run Test
```

---

**Status:** ✅ Ready for implementation  
**Version:** 1.0  
**Date:** February 1, 2026  
**Next Step:** Configure Firebase test numbers, then run TC001_LoginWithShuffleHandshake
