# 🔐 Master Technical Reference - Cerberus + Lessimp + Shuffle Integration

## 📋 Source of Truth Document

This document provides the complete technical blueprint for automating the **Lessimp Flutter** mobile app testing using **Cerberus Testing** with **Shuffle** data integration.

---

## 1. 🐳 Cerberus Deployment Configuration

### Base URLs & Access
```
Base URL:        http://localhost:8888/
Context Path:    / (ROOT.war deployment)
Wrong URL:       http://localhost:8888/Cerberus/ ❌ (404 error)
```

### Database Configuration
```
Database Host:   cerberus-tomcat-mysql-database-1 (internal Docker)
External Port:   13306:3306
Database Name:   cerberus
User:            cerberus
Password:        cerberus
Root Password:   rootpassword
Tables:          72 tables populated
```

### Credentials
```
Admin User:      admin / admin
Cerberus User:   cerberus / cerberus
```

### Hierarchy Requirement
```
System → Application → Test → Test Case

Example:
PROD_SYSTEM
  └── Lessimp_Mobile
        └── LoginTests
              └── TC001_LoginWithShuffle
```

---

## 2. 📱 Flutter iOS Build Specification (Lessimp)

### Deployment Targets
```
iOS Version:            15.0
Podfile Platform:       platform :ios, '15.0'
Xcode Version:          26.2 (17C52)
Architecture:           arm64 (Apple Silicon)
```

### Build Paths
```
Project Root:           ~/Documents/GitHub/lessimp/
Build Output:           ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
Simulator Target:       iPhone 16 Pro (iOS 26.0)
Simulator ID:           908D1BF9-3008-4000-AF43-313441294EA7
```

### Cleanup & Build Commands
```bash
# Full cleanup and build
flutter clean
flutter pub get
cd ios
pod install --repo-update
cd ..
flutter build ios --simulator

# Verify build exists
ls -d ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
```

### Appium Configuration
```
App Path:               ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
Platform Name:          iOS
Platform Version:       26.0
Device Name:            iPhone 16 Pro
Automation Name:        XCUITest
```

---

## 3. 🔑 Lessimp Login Flow - Object Library

### Login Screen Widgets

Based on code analysis from `lib/ui/screens/common/login_screen.dart`:

#### Phone Number Input
```dart
// Location: Line 459
TextField/TextFormField
  - Label: "Phone Number"
  - Controller: _phoneController
  - Type: TextInputType.numberWithOptions(signed: true)
  - Validation: 6-15 digits
  - Country Code Picker: Initial selection 'US', dial code '+1'
  
Cerberus Locator Strategy:
  - By Text: "Phone Number"
  - By Accessibility ID: TBD (needs key added)
  - By XPath: //XCUIElementTypeTextField[@label="Phone Number"]
```

#### Country Code Picker
```dart
// Location: Line 470
CountryCodePicker
  - Initial Selection: 'US' (countrycodesidentifier)
  - Dial Code: '+1' (countrycodes)
  - Shows: Flag + Country + Dial Code
  
Cerberus Locator Strategy:
  - By Text: "+1" or country name
  - By XPath: //XCUIElementTypeButton[contains(@label, "+1")]
```

#### Login Button
```dart
// Location: Line 502
ElevatedButton (via getButton widget)
  - Text: "Login"
  - Loading State: Shows spinner when processing
  - Enabled: Only when phone number valid
  
Cerberus Locator Strategy:
  - By Text: "Login"
  - By Accessibility ID: TBD (needs key added)
  - By XPath: //XCUIElementTypeButton[@label="Login"]
```

#### Keep Me Logged In Checkbox
```dart
// Location: Line 528
Checkbox
  - Label: "Keep me Logged In"
  - State: _keepLoggedIn boolean
  - Saves phone to SharedPreferences
  
Cerberus Locator Strategy:
  - By Text: "Keep me Logged In"
  - By XPath: //XCUIElementTypeButton[@label="Keep me Logged In"]
```

---

### OTP Verification Screen Widgets

Based on code analysis from `lib/ui/screens/common/otp_verification_screen.dart`:

#### OTP Input Fields
```dart
// Location: Line 278
Pinput Widget (6 digits)
  - Controller: pinController
  - Length: 6
  - Keyboard Type: Number
  - Auto-focus: Yes
  - Validation: Must be 6 digits
  
Cerberus Locator Strategy:
  - By XPath: //XCUIElementTypeTextField[position()=1] through [position()=6]
  - Individual digit fields
```

#### Verify Button
```dart
// Location: Line 360
ElevatedButton (via getButton)
  - Text: "Verify"
  - Loading State: Shows spinner
  - Enabled: Only when OTP length = 6
  
Cerberus Locator Strategy:
  - By Text: "Verify"
  - By XPath: //XCUIElementTypeButton[@label="Verify"]
```

#### Resend OTP Link
```dart
// Location: Line 398
InkWell/Text
  - Text: "Resend"
  - Enabled: After countdown completes
  - Countdown: 14 seconds
  
Cerberus Locator Strategy:
  - By Text: "Resend"
  - By XPath: //XCUIElementTypeButton[@label="Resend "]
```

---

## 4. 🎲 Shuffle Integration Strategy

### Data Structure

Since no Shuffle-specific files were found, we'll create the integration:

#### Mock Data File: `shuffle_data.json`
```json
{
  "users": [
    {
      "id": 1,
      "phone": "1234567890",
      "countryCode": "+1",
      "name": "Test User 1",
      "email": "testuser1@example.com"
    },
    {
      "id": 2,
      "phone": "9876543210",
      "countryCode": "+1",
      "name": "Test User 2",
      "email": "testuser2@example.com"
    }
  ]
}
```

#### Shuffle API Integration (if using API)
```bash
# Endpoint
GET http://localhost:PORT/shuffle/get_user

# Response
{
  "phone": "1234567890",
  "countryCode": "+1",
  "otp": "123456" (for testing only)
}
```

---

## 5. 🎯 Cerberus Test Case Structure

### Application Configuration

```
Application Name:    Lessimp_Mobile
Type:                MOBILE (not WEB)
Platform:            iOS
System:              PROD_SYSTEM
Active:              Yes
```

### Test Case: TC001_LoginWithShuffleData

#### Prerequisites
1. Shuffle data file exists OR Shuffle API is running
2. iOS Simulator is running (iPhone 16 Pro)
3. Lessimp app is built: `Runner.app` exists
4. Appium server is running

#### Test Steps

##### Step 1: Get Shuffle Data
```
Action:         callUrl (or executeSQLQuery if using database)
Value1:         http://localhost:PORT/shuffle/get_user
Value2:         GET
Description:    Retrieve randomized user data from Shuffle
Store Result:   PHONE_NUMBER, COUNTRY_CODE, OTP
```

##### Step 2: Launch App
```
Action:         openApplication  
Value1:         ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app
Value2:         (Appium capabilities)
Description:    Launch Lessimp iOS app on simulator
Screenshot:     Yes
```

##### Step 3: Wait for Login Screen
```
Action:         waitForElementPresent
Value1:         xpath=//XCUIElementTypeTextField[@label="Phone Number"]
Value2:         10000 (10 seconds timeout)
Description:    Wait for login screen to load
```

##### Step 4: Enter Phone Number
```
Action:         type
Value1:         xpath=//XCUIElementTypeTextField[@label="Phone Number"]
Value2:         %PHONE_NUMBER% (from Shuffle)
Description:    Enter phone number from Shuffle data
Screenshot:     Yes
```

##### Step 5: Click Login Button
```
Action:         click
Value1:         xpath=//XCUIElementTypeButton[@label="Login"]
Value2:         
Description:    Trigger OTP send
Screenshot:     Yes
```

##### Step 6: Wait for OTP Screen
```
Action:         waitForElementPresent
Value1:         xpath=//XCUIElementTypeStaticText[contains(@label, "Verification")]
Value2:         15000 (15 seconds)
Description:    Wait for OTP screen to appear
```

##### Step 7: Enter OTP (Digit 1)
```
Action:         type
Value1:         xpath=//XCUIElementTypeTextField[position()=1]
Value2:         %OTP_DIGIT_1%
Description:    Enter first OTP digit
```

##### Step 8-12: Enter remaining OTP digits
(Repeat for positions 2-6)

##### Step 13: Click Verify Button
```
Action:         click
Value1:         xpath=//XCUIElementTypeButton[@label="Verify"]
Value2:         
Description:    Submit OTP for verification
Screenshot:     Yes
```

##### Step 14: Verify Login Success
```
Action:         verifyElementPresent
Value1:         xpath=//XCUIElementTypeOther[contains(@label, "Home")]
Value2:         
Description:    Confirm user reached home screen
Screenshot:     Yes
```

---

## 6. 🔧 Appium Capabilities (for Cerberus)

### Desired Capabilities JSON
```json
{
  "platformName": "iOS",
  "platformVersion": "26.0",
  "deviceName": "iPhone 16 Pro",
  "automationName": "XCUITest",
  "app": "/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app",
  "udid": "908D1BF9-3008-4000-AF43-313441294EA7",
  "noReset": false,
  "fullReset": false,
  "autoAcceptAlerts": true,
  "autoDismissAlerts": false,
  "newCommandTimeout": 300,
  "wdaLocalPort": 8100,
  "useNewWDA": false,
  "usePrebuiltWDA": true
}
```

---

## 7. 🚀 Environment Health Check Commands

### Verify Cerberus
```bash
# Check containers
cd ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql
docker-compose ps

# Verify web access
curl -I http://localhost:8888/

# Check database
docker exec cerberus-tomcat-mysql-database-1 mysql -ucerberus -pcerberus -e "SHOW TABLES;" cerberus | wc -l
```

### Verify Lessimp Build
```bash
# Check build exists
ls -d ~/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app

# List simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot "iPhone 16 Pro"
```

### Verify Shuffle Integration
```bash
# Find Shuffle files
find ~/Documents/GitHub/lessimp -name "*shuffle*"

# If API: Check Shuffle service
curl http://localhost:PORT/shuffle/health
```

### Verify docker-compose.yml
```bash
# Confirm platform setting
grep -A 2 "database:" ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql/docker-compose.yml | grep platform
```

Expected output:
```yaml
platform: linux/amd64
```

---

## 8. 📝 Recommended Widget Keys (To Add)

To improve Cerberus automation, add these keys to Lessimp Flutter widgets:

### Login Screen (`lib/ui/screens/common/login_screen.dart`)
```dart
// Phone number input (around line 459)
TextField(
  key: Key('phone_input'),  // ← ADD THIS
  controller: _phoneController,
  // ... rest of config
)

// Login button (around line 502)
ElevatedButton(
  key: Key('login_button'),  // ← ADD THIS
  // ... rest of config
)

// Checkbox (around line 528)
Checkbox(
  key: Key('keep_logged_in_checkbox'),  // ← ADD THIS
  // ... rest of config
)
```

### OTP Screen (`lib/ui/screens/common/otp_verification_screen.dart`)
```dart
// OTP input (around line 278)
Pinput(
  key: Key('otp_input'),  // ← ADD THIS
  controller: pinController,
  // ... rest of config
)

// Verify button (around line 360)
ElevatedButton(
  key: Key('verify_button'),  // ← ADD THIS
  // ... rest of config
)

// Resend link (around line 398)
InkWell(
  key: Key('resend_otp_link'),  // ← ADD THIS
  // ... rest of config
)
```

---

## 9. 🔐 Firebase Phone Auth Flow

### Authentication Sequence
```
1. User enters phone number
2. App calls Firebase verifyPhoneNumber()
3. Firebase sends SMS with OTP
4. User enters 6-digit OTP
5. App calls verifyOtp() with verificationId
6. Firebase validates OTP
7. App receives PhoneAuthCredential
8. App calls signInWithPhone()
9. User authenticated, navigate to home
```

### Cerberus Considerations
- **OTP Handling:** Cannot intercept real SMS
- **Solutions:**
  - Use Firebase Test Phone Numbers
  - Mock the OTP flow for testing
  - Use Shuffle to provide known test OTPs

### Firebase Test Phone Numbers Setup
```
Firebase Console → Authentication → Sign-in method → Phone
→ Phone numbers for testing

Add:
Phone Number: +1 5555551234
OTP: 123456
```

---

## 10. 📊 Cerberus Data Library Integration

### Option 1: Use Cerberus Data Library
```
Administration → Data Library → Create Data Set

Name: ShuffleUsers
Type: STATIC
Columns:
  - phone (TEXT)
  - countryCode (TEXT)
  - otp (TEXT)
  - email (TEXT)

Data:
+1,1234567890,123456,testuser1@example.com
+1,9876543210,123456,testuser2@example.com
```

### Option 2: Shuffle API Call in Test Step
```
Step 1:
  Action: executeSqlLib
  Database: shuffle_db
  Query: SELECT phone, countryCode, otp FROM users ORDER BY RAND() LIMIT 1
  Store: PHONE, COUNTRY_CODE, OTP
```

### Option 3: REST API Call
```
Step 1:
  Action: callUrl
  Value1: http://localhost:5000/shuffle/get_user
  Value2: GET
  Store Response: JSON → Extract phone, countryCode, otp
```

---

## 11. 🎯 Complete Test Case Template

```xml
Test: LoginTests
System: PROD_SYSTEM
Application: Lessimp_Mobile

Test Case: TC001_LoginWithShuffleData
Description: Automated login using randomized Shuffle data
Priority: 1
Status: WORKING

Steps:
1. callUrl → Get Shuffle user data
2. openApplication → Launch Lessimp app
3. waitForElementPresent → Wait for phone input
4. type → Enter phone number (%PHONE%)
5. click → Click login button
6. waitForElementPresent → Wait for OTP screen
7-12. type → Enter OTP digits
13. click → Click verify button
14. verifyElementPresent → Confirm home screen
```

---

## 12. 🔍 Validation & Testing Checklist

- [ ] Cerberus accessible at http://localhost:8888/
- [ ] PROD_SYSTEM created in Cerberus
- [ ] Lessimp_Mobile application configured (Type: MOBILE, Platform: iOS)
- [ ] Runner.app built and exists
- [ ] iOS Simulator running (iPhone 16 Pro)
- [ ] Appium server running (port 4723)
- [ ] Shuffle data source ready (file/API/database)
- [ ] Test case created with all steps
- [ ] Firebase test phone numbers configured
- [ ] Widget keys added to Flutter code (optional but recommended)

---

## 13. 📚 Reference Files

- **Cerberus Docs:** `~/Documents/GitHub/cerberus-core/SETUP_FIXES_README.md`
- **Login Screen:** `~/Documents/GitHub/lessimp/lib/ui/screens/common/login_screen.dart`
- **OTP Screen:** `~/Documents/GitHub/lessimp/lib/ui/screens/common/otp_verification_screen.dart`
- **Auth Cubit:** `~/Documents/GitHub/lessimp/lib/cubits/auth/auth_cubit.dart`
- **Auth Repository:** `~/Documents/GitHub/lessimp/lib/repository/auth_repository.dart`

---

## 14. 🚨 Known Issues & Workarounds

### Issue 1: Real OTP Cannot Be Intercepted
**Workaround:** Use Firebase Test Phone Numbers with fixed OTPs

### Issue 2: Appium Session Timeout
**Workaround:** Increase `newCommandTimeout` to 300 seconds

### Issue 3: Widget Locators Not Stable
**Workaround:** Add `Key()` widgets to Flutter code

### Issue 4: Simulator Boot Time
**Workaround:** Pre-boot simulator before running tests

---

**Last Updated:** February 1, 2026  
**Environment:** Apple Silicon Mac, Docker, iOS Simulator, Flutter 3.35.6  
**Status:** Ready for implementation
