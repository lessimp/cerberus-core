# 🧪 Cerberus Test Case Configuration - Lessimp Mobile Login

## Complete Step-by-Step Guide

---

## Part 1: Configure Lessimp_Mobile Application in Cerberus

### Step 1: Access Cerberus UI
```
URL: http://localhost:8888/
Username: admin
Password: admin
```

### Step 2: Create System (if not exists)
```
Navigation: Administration → Invariants → System

Click: [+ Add System]

Fields:
  System:          PROD_SYSTEM
  Description:     Production System for Lessimp Mobile App
  Active:          ✅ Yes
  
Click: [Save]
```

### Step 3: Create Application
```
Navigation: Administration → Application

Click: [+ Create Application]

Fields:
  Application:     Lessimp_Mobile
  Type:            MOBILE  ⬅️ CRITICAL: Select MOBILE, not WEB
  System:          PROD_SYSTEM
  SubSystem:       (leave empty)
  Description:     Lessimp Dating Mobile App - iOS
  Active:          ✅ Yes
  
  Deploy Type:     (leave default)
  Maven Group ID:  (leave empty for mobile)
  
  Mobile Platform: iOS  ⬅️ CRITICAL
  
Click: [Create]
```

**✅ Verification:**
- Go to Administration → Application
- Find "Lessimp_Mobile" in the list
- Confirm Type = "MOBILE" and System = "PROD_SYSTEM"

---

## Part 2: Create Object Library (Widget Locators)

### Step 1: Navigate to Object Library
```
Navigation: TestData → Object Repository

Application: Select "Lessimp_Mobile" from dropdown
```

### Step 2: Add Login Screen Objects

#### Object 1: Phone Input
```
Click: [+ Create Object]

Fields:
  Application:    Lessimp_Mobile
  Object:         phone_input
  Type:           getFromTestData
  Value:          
  ScreenshotFileName: (optional)
  UsrCreated:     (auto-filled)
  DateCreated:    (auto-filled)
  UsrModif:       (auto-filled)
  DateModif:      (auto-filled)

Click: [Save]
```

#### Object 2: Login Button
```
Click: [+ Create Object]

Fields:
  Application:    Lessimp_Mobile
  Object:         login_button
  Type:           getFromTestData
  
Click: [Save]
```

#### Object 3: OTP Input
```
Click: [+ Create Object]

Fields:
  Application:    Lessimp_Mobile
  Object:         otp_input
  Type:           getFromTestData
  
Click: [Save]
```

#### Object 4: Verify Button
```
Click: [+ Create Object]

Fields:
  Application:    Lessimp_Mobile
  Object:         verify_button
  Type:           getFromTestData
  
Click: [Save]
```

### Complete Object Library List
| Object Name | Type | Screen | Purpose |
|-------------|------|--------|---------|
| phone_input | getFromTestData | Login | Phone number TextField |
| country_code_picker | getFromTestData | Login | Country code selector |
| login_button | getFromTestData | Login | Submit login button |
| keep_logged_in_checkbox | getFromTestData | Login | Remember me checkbox |
| otp_input | getFromTestData | OTP | 6-digit OTP input |
| verify_button | getFromTestData | OTP | Submit OTP button |
| resend_otp_link | getFromTestData | OTP | Resend OTP link |

---

## Part 3: Create Test Case

### Step 1: Create Test
```
Navigation: Test → Test

Click: [+ Create Test]

Fields:
  Test:           LoginTests
  Active:         ✅ Yes
  Description:    Automated tests for Lessimp mobile login flow
  
Click: [Create]
```

### Step 2: Create Test Case
```
Navigation: Test → Test Case

Click: [+ Create Test Case]

Fields:
  Test:           LoginTests
  TestCase:       TC001_LoginWithShuffle
  Application:    Lessimp_Mobile
  Active:         ✅ Yes
  Status:         WORKING
  Priority:       1
  Description:    Login test using Shuffle randomized data
  
  Detailed Description:
    This test case automates the Lessimp mobile login flow:
    1. Get random user data from Shuffle API
    2. Launch Lessimp iOS app
    3. Enter phone number
    4. Submit login
    5. Enter OTP
    6. Verify successful login
    
Click: [Create]
```

---

## Part 4: Configure Test Steps

### Navigation
```
Test → Test Case → Select "TC001_LoginWithShuffle" → [Edit]
Scroll down to "Test Case Steps" section
```

### Step 1: Get Shuffle Data
```
Click: [+ Add Step]

Fields:
  Step:           1
  Sort:           1
  Loop:           (empty)
  ConditionOper:  always
  ConditionVal1:  
  ConditionVal2:  
  ConditionVal3:  
  
  Description:    Get random test user from Shuffle API
  
  Action:         callUrl
  Value1:         http://localhost:5000/shuffle/get_user
  Value2:         GET
  Value3:         
  
  Properties:
    - Property: PHONE
      Type: getFromJson
      Value: $.phone
      
    - Property: COUNTRY_CODE
      Type: getFromJson
      Value: $.countryCode
      
    - Property: FULL_PHONE
      Type: getFromJson
      Value: $.fullPhone
      
    - Property: OTP
      Type: getFromJson
      Value: $.otp

Click: [Save Step]
```

### Step 2: Launch App
```
Click: [+ Add Step]

Fields:
  Step:           2
  Sort:           2
  Description:    Launch Lessimp iOS app on simulator
  
  Action:         openApplication
  Value1:         /Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
  Value2:         
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

### Step 3: Wait for Login Screen
```
Click: [+ Add Step]

Fields:
  Step:           3
  Sort:           3
  Description:    Wait for phone input field to appear
  
  Action:         waitForElementPresent
  Value1:         identifier=phone_input
  Value2:         10000 (10 seconds timeout)
  Value3:         
  
Click: [Save Step]
```

### Step 4: Enter Phone Number
```
Click: [+ Add Step]

Fields:
  Step:           4
  Sort:           4
  Description:    Enter phone number from Shuffle data
  
  Action:         type
  Value1:         identifier=phone_input
  Value2:         %PHONE%
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

### Step 5: Click Login Button
```
Click: [+ Add Step]

Fields:
  Step:           5
  Sort:           5
  Description:    Submit login to trigger OTP
  
  Action:         click
  Value1:         identifier=login_button
  Value2:         
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

### Step 6: Wait for OTP Screen
```
Click: [+ Add Step]

Fields:
  Step:           6
  Sort:           6
  Description:    Wait for OTP input screen
  
  Action:         waitForElementPresent
  Value1:         identifier=otp_input
  Value2:         15000 (15 seconds timeout)
  Value3:         
  
Click: [Save Step]
```

### Step 7: Enter OTP
```
Click: [+ Add Step]

Fields:
  Step:           7
  Sort:           7
  Description:    Enter 6-digit OTP from Shuffle data
  
  Action:         type
  Value1:         identifier=otp_input
  Value2:         %OTP%
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

### Step 8: Click Verify Button
```
Click: [+ Add Step]

Fields:
  Step:           8
  Sort:           8
  Description:    Submit OTP for verification
  
  Action:         click
  Value1:         identifier=verify_button
  Value2:         
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

### Step 9: Verify Login Success
```
Click: [+ Add Step]

Fields:
  Step:           9
  Sort:           9
  Description:    Confirm user reached home screen
  
  Action:         verifyElementPresent
  Value1:         xpath=//XCUIElementTypeOther[contains(@label, 'Home')]
  Value2:         
  Value3:         
  
  Screenshot:     ✅ Take Screenshot After

Click: [Save Step]
```

---

## Part 5: Configure Appium Capabilities

### Step 1: Navigate to Application Settings
```
Navigation: Administration → Application → Edit "Lessimp_Mobile"
```

### Step 2: Add Mobile Specific Parameters
```
Scroll to "Mobile Application Settings" section

Fields:
  Platform Name:       iOS
  Platform Version:    26.0
  Device Name:         iPhone 16 Pro
  Automation Name:     XCUITest
  App Path:            /Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
  UDID:                908D1BF9-3008-4000-AF43-313441294EA7
  No Reset:            false
  Full Reset:          false
  Auto Accept Alerts:  true
  New Command Timeout: 300
  WDA Local Port:      8100

Click: [Save]
```

---

## Part 6: Setup Shuffle Data Provider

### Option A: Run Shuffle API Server
```bash
# Install dependencies
pip3 install flask flask-cors

# Start Shuffle API server
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000
```

**Verify:**
```bash
curl http://localhost:5000/shuffle/get_user
```

**Expected Output:**
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
  "timestamp": "2026-02-01T10:30:00.123456",
  "source": "shuffle_provider"
}
```

### Option B: Use Static JSON File
```bash
# Generate shuffle_data.json
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --json > shuffle_data.json
```

**Modify Test Case Step 1:**
- Change Action to: `executeSQLLib` or `getFromDataLib`
- Read from: `shuffle_data.json`

---

## Part 7: Setup Firebase Test Phone Numbers

### Step 1: Open Firebase Console
```
URL: https://console.firebase.google.com/
Project: (Your Lessimp project)
```

### Step 2: Configure Test Numbers
```
Navigation: Authentication → Sign-in method → Phone

Scroll to: "Phone numbers for testing"

Click: [+ Add phone number]

Add each Shuffle test number:
  +15555551001 → OTP: 123456
  +15555551002 → OTP: 123456
  +15555551003 → OTP: 123456
  +15555551004 → OTP: 123456
  +15555551005 → OTP: 123456

Click: [Save]
```

**✅ Important:** These test numbers will bypass actual SMS sending and accept the fixed OTP `123456`

---

## Part 8: Pre-Flight Checklist

Before running the test:

- [ ] **Cerberus Running:** http://localhost:8888/ accessible
- [ ] **Shuffle API Running:** http://localhost:5000/shuffle/health returns 200
- [ ] **iOS Simulator Running:**
  ```bash
  xcrun simctl list devices | grep Booted
  # Should show: iPhone 16 Pro (908D1BF9-3008-4000-AF43-313441294EA7) (Booted)
  ```
- [ ] **App Built:**
  ```bash
  ls -d ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
  # Should exist
  ```
- [ ] **Appium Server Running:**
  ```bash
  appium -p 4723
  ```
- [ ] **Firebase Test Numbers Configured:** All 5 numbers added with OTP 123456

---

## Part 9: Run Test Execution

### Step 1: Navigate to Test Execution
```
Navigation: Run → Test Queue → Manual Execution

Select:
  Test:       LoginTests
  TestCase:   TC001_LoginWithShuffle
  Country:    (select appropriate)
  Environment: (select appropriate)
  
Click: [Run Test]
```

### Step 2: Monitor Execution
```
Navigation: Run → Execution History

Find: Latest execution of TC001_LoginWithShuffle

Click: [View Details]

Monitor:
  - Step-by-step execution log
  - Screenshots at each step
  - Variable values (PHONE, OTP, etc.)
  - Execution time
```

### Step 3: Review Results
```
Expected Outcome:
  Status: OK (green checkmark)
  
  Steps:
    ✅ Step 1: Shuffle API call successful
    ✅ Step 2: App launched
    ✅ Step 3: Phone input found
    ✅ Step 4: Phone number entered
    ✅ Step 5: Login button clicked
    ✅ Step 6: OTP screen appeared
    ✅ Step 7: OTP entered
    ✅ Step 8: Verify button clicked
    ✅ Step 9: Home screen verified
```

---

## Part 10: Troubleshooting

### Issue: Shuffle API Connection Failed
**Error:** "Could not connect to http://localhost:5000/shuffle/get_user"

**Fix:**
```bash
# Verify Shuffle API is running
curl http://localhost:5000/shuffle/health

# If not running, start it:
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api
```

---

### Issue: Widget Not Found
**Error:** "Element 'phone_input' not found"

**Possible Causes:**
1. Widget keys not added to Flutter code
2. Using wrong locator strategy
3. App not fully loaded

**Fix:**
```
1. Verify widget keys exist in Flutter code (WIDGET_LOCATOR_AUDIT.md)
2. Use fallback XPath locators:
   - phone_input: xpath=//XCUIElementTypeTextField[@label='Phone Number']
   - login_button: xpath=//XCUIElementTypeButton[@label='Login']
3. Increase wait timeout in Step 3 from 10000 to 20000
```

---

### Issue: OTP Verification Failed
**Error:** "Firebase authentication failed"

**Fix:**
```
1. Verify test phone numbers in Firebase Console
2. Confirm OTP is exactly "123456"
3. Check Firebase authentication is enabled
4. Review Firebase project settings
```

---

### Issue: Appium Session Timeout
**Error:** "Session timeout after 60 seconds"

**Fix:**
```
Increase newCommandTimeout in Application settings:
  New Command Timeout: 300 (5 minutes)
```

---

## Part 11: Docker Environment Health Check

### Verify Cerberus Containers
```bash
cd ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql
docker-compose ps
```

**Expected Output:**
```
NAME                                      STATUS
cerberus-tomcat-mysql-cerberus-1          Up
cerberus-tomcat-mysql-database-1          Up
```

### Verify Database Connection
```bash
docker exec cerberus-tomcat-mysql-database-1 mysql -ucerberus -pcerberus -e "SELECT COUNT(*) FROM application WHERE Application='Lessimp_Mobile';" cerberus
```

**Expected:** `1` (application exists)

### Verify Platform Setting (Apple Silicon)
```bash
grep "platform:" ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql/docker-compose.yml
```

**Expected:**
```yaml
platform: linux/amd64
```

---

## Part 12: Next Steps

After successful test execution:

1. **Create Additional Test Cases:**
   - TC002_InvalidPhoneNumber
   - TC003_InvalidOTP
   - TC004_ResendOTP
   - TC005_KeepLoggedIn

2. **Setup CI/CD Integration:**
   - Integrate with Jenkins/GitHub Actions
   - Schedule nightly test runs
   - Generate test reports

3. **Expand Object Library:**
   - Add signup screen objects
   - Add profile screen objects
   - Add settings screen objects

4. **Implement Data-Driven Testing:**
   - Use Cerberus Data Library
   - Parameterize test data
   - Run tests with multiple users

---

**Document Version:** 1.0  
**Last Updated:** February 1, 2026  
**Status:** Ready for test execution
