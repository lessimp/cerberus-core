# 🔍 Widget Locator Audit - Lessimp Flutter App

## Audit Status
- **Date:** February 1, 2026
- **Scope:** Login flow widgets (login_screen.dart, otp_verification_screen.dart)
- **Finding:** ❌ NO Key() attributes found on critical widgets
- **Recommendation:** Add Key() attributes for Appium/Cerberus automation

---

## 1. Current Widget State (WITHOUT Keys)

### Login Screen: `lib/ui/screens/common/login_screen.dart`

#### Phone Number Input (Line ~459)
```dart
// CURRENT CODE (NO KEY)
TextField(
  controller: _phoneController,
  keyboardType: TextInputType.numberWithOptions(signed: true),
  decoration: InputDecoration(
    labelText: "Phone Number",
    // ...
  ),
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeTextField[@label='Phone Number']")`
- `By.iOSNsPredicate("label == 'Phone Number' AND type == 'XCUIElementTypeTextField'")`

**Stability:** ⚠️ Medium - Text label could change with localization

---

#### Login Button (Line ~502)
```dart
// CURRENT CODE (NO KEY)
getButton(
  isLoading: state.authStatus == AuthStatus.loading,
  onPressed: _onLogin,
  text: "Login",
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeButton[@label='Login']")`
- `By.accessibilityId("Login")`

**Stability:** ⚠️ Medium - Text could change with localization

---

#### Keep Logged In Checkbox (Line ~528)
```dart
// CURRENT CODE (NO KEY)
Checkbox(
  value: _keepLoggedIn,
  onChanged: (value) {
    setState(() {
      _keepLoggedIn = value!;
    });
  },
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeButton[contains(@label, 'Keep me Logged In')]")`

**Stability:** ⚠️ Low - Checkbox labels vary by platform

---

### OTP Verification Screen: `lib/ui/screens/common/otp_verification_screen.dart`

#### OTP Input Fields (Line ~278)
```dart
// CURRENT CODE (NO KEY)
Pinput(
  controller: pinController,
  length: 6,
  autofocus: true,
  keyboardType: TextInputType.number,
  // ...
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeTextField[1]")` through `[6]`
- Individual field access by position

**Stability:** ⚠️ Low - Position-based locators are fragile

---

#### Verify Button (Line ~360)
```dart
// CURRENT CODE (NO KEY)
getButton(
  isLoading: state.authStatus == AuthStatus.loading,
  onPressed: _onVerify,
  text: "Verify",
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeButton[@label='Verify']")`
- `By.accessibilityId("Verify")`

**Stability:** ⚠️ Medium - Text could change

---

#### Resend OTP Link (Line ~398)
```dart
// CURRENT CODE (NO KEY)
InkWell(
  onTap: _resendOTP,
  child: Text(
    "Resend ",
    style: TextStyle(color: primaryColor),
  ),
)
```

**Appium Locator Options:**
- `By.xpath("//XCUIElementTypeButton[contains(@label, 'Resend')]")`

**Stability:** ⚠️ Medium

---

## 2. Recommended Widget Modifications (WITH Keys)

### Login Screen: `lib/ui/screens/common/login_screen.dart`

#### Phone Number Input ✅
```dart
// RECOMMENDED CODE (WITH KEY)
TextField(
  key: const Key('phone_input'),  // ← ADD THIS
  controller: _phoneController,
  keyboardType: TextInputType.numberWithOptions(signed: true),
  decoration: const InputDecoration(
    labelText: "Phone Number",
    // ...
  ),
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("phone_input")` ✅ Stable, localization-safe

---

#### Login Button ✅
```dart
// RECOMMENDED CODE (WITH KEY)
getButton(
  key: const Key('login_button'),  // ← ADD THIS to getButton function signature
  isLoading: state.authStatus == AuthStatus.loading,
  onPressed: _onLogin,
  text: "Login",
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("login_button")` ✅ Stable

**Note:** Requires modifying `getButton()` in `common_widgets.dart` to accept `key` parameter

---

#### Keep Logged In Checkbox ✅
```dart
// RECOMMENDED CODE (WITH KEY)
Checkbox(
  key: const Key('keep_logged_in_checkbox'),  // ← ADD THIS
  value: _keepLoggedIn,
  onChanged: (value) {
    setState(() {
      _keepLoggedIn = value!;
    });
  },
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("keep_logged_in_checkbox")` ✅ Stable

---

### OTP Verification Screen: `lib/ui/screens/common/otp_verification_screen.dart`

#### OTP Input Fields ✅
```dart
// RECOMMENDED CODE (WITH KEY)
Pinput(
  key: const Key('otp_input'),  // ← ADD THIS
  controller: pinController,
  length: 6,
  autofocus: true,
  keyboardType: TextInputType.number,
  // ...
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("otp_input")` ✅ Stable
- Can then access individual fields by index if needed

---

#### Verify Button ✅
```dart
// RECOMMENDED CODE (WITH KEY)
getButton(
  key: const Key('verify_button'),  // ← ADD THIS
  isLoading: state.authStatus == AuthStatus.loading,
  onPressed: _onVerify,
  text: "Verify",
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("verify_button")` ✅ Stable

---

#### Resend OTP Link ✅
```dart
// RECOMMENDED CODE (WITH KEY)
InkWell(
  key: const Key('resend_otp_link'),  // ← ADD THIS
  onTap: _resendOTP,
  child: const Text(
    "Resend ",
    style: TextStyle(color: primaryColor),
  ),
)
```

**Appium Locator (With Key):**
- `By.accessibilityId("resend_otp_link")` ✅ Stable

---

## 3. Cerberus Object Library Mapping

### Application: Lessimp_Mobile
**Type:** MOBILE  
**Platform:** iOS

| Object Name | Locator Type | Locator Value | Screen | Description |
|-------------|--------------|---------------|--------|-------------|
| phone_input | accessibility_id | phone_input | Login | Phone number TextField |
| country_code_picker | xpath | //XCUIElementTypeButton[contains(@label, "+1")] | Login | Country code selector |
| login_button | accessibility_id | login_button | Login | Submit login button |
| keep_logged_in_checkbox | accessibility_id | keep_logged_in_checkbox | Login | Remember me checkbox |
| otp_input | accessibility_id | otp_input | OTP | 6-digit OTP input |
| verify_button | accessibility_id | verify_button | OTP | Submit OTP button |
| resend_otp_link | accessibility_id | resend_otp_link | OTP | Resend OTP link |

---

## 4. Implementation Priority

### Phase 1: Critical Widgets (Must Have) 🔴
1. `phone_input` - Essential for login automation
2. `login_button` - Essential for login automation
3. `otp_input` - Essential for OTP verification
4. `verify_button` - Essential for OTP verification

### Phase 2: Supporting Widgets (Should Have) 🟡
5. `keep_logged_in_checkbox` - For testing persistent sessions
6. `resend_otp_link` - For testing OTP resend flow

### Phase 3: Enhancement (Nice to Have) 🟢
7. Country code picker - For testing international numbers
8. Error messages - For negative testing

---

## 5. Code Modification Checklist

- [ ] Modify `lib/ui/widgets/common_widgets.dart`:
  - [ ] Add `Key? key` parameter to `getButton()` function
  - [ ] Add `Key? key` parameter to `getTextField()` function
  - [ ] Pass key to widget constructor

- [ ] Modify `lib/ui/screens/common/login_screen.dart`:
  - [ ] Add `Key('phone_input')` to phone TextField (line ~459)
  - [ ] Add `Key('login_button')` to login button (line ~502)
  - [ ] Add `Key('keep_logged_in_checkbox')` to checkbox (line ~528)

- [ ] Modify `lib/ui/screens/common/otp_verification_screen.dart`:
  - [ ] Add `Key('otp_input')` to Pinput widget (line ~278)
  - [ ] Add `Key('verify_button')` to verify button (line ~360)
  - [ ] Add `Key('resend_otp_link')` to resend link (line ~398)

- [ ] Test modifications:
  - [ ] Run `flutter analyze` to check for errors
  - [ ] Run app on simulator to verify no visual changes
  - [ ] Verify keys appear in Flutter DevTools

---

## 6. Validation Commands

### Check Widget Keys in Running App
```bash
# Launch Flutter DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Open in browser, connect to running app
# Navigate to Widget Inspector
# Search for key: "phone_input", "login_button", etc.
```

### Verify Appium Can Find Widgets
```python
from appium import webdriver

caps = {
    "platformName": "iOS",
    "platformVersion": "26.0",
    "deviceName": "iPhone 16 Pro",
    "app": "/Users/wipedclean/Documents/GitHub/lessimp/build/ios/iphonesimulator/Runner.app",
    "automationName": "XCUITest"
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

# Test finding widgets by accessibility ID
phone_input = driver.find_element_by_accessibility_id("phone_input")
login_button = driver.find_element_by_accessibility_id("login_button")

print("✅ Widgets found successfully!")
driver.quit()
```

---

## 7. Alternative Locator Strategies (If Keys Not Added)

### Semantics-Based Locators (Flutter-specific)
```dart
// Add Semantics wrapper to widgets
Semantics(
  label: 'Phone number input',
  child: TextField(
    controller: _phoneController,
    // ...
  ),
)
```

**Appium Access:**
- `By.accessibilityId("Phone number input")`

### ValueKey vs Key
```dart
// Use ValueKey for dynamic content
TextField(
  key: ValueKey('phone_input_${userId}'),
  // ...
)
```

---

## 8. Best Practices

### ✅ DO:
- Use `const Key('widget_name')` for stable identifiers
- Use lowercase with underscores: `phone_input`, `login_button`
- Keep key names consistent across platforms
- Document all keys in Object Library

### ❌ DON'T:
- Use text labels as primary locators (localization breaks them)
- Use position-based XPath (fragile, breaks with UI changes)
- Mix naming conventions (snake_case vs camelCase)
- Hardcode keys without constants file

---

## 9. Future Enhancements

### Create Keys Constants File
```dart
// lib/constants/test_keys.dart
class TestKeys {
  static const String phoneInput = 'phone_input';
  static const String loginButton = 'login_button';
  static const String otpInput = 'otp_input';
  static const String verifyButton = 'verify_button';
  // ...
}

// Usage:
TextField(
  key: Key(TestKeys.phoneInput),
  // ...
)
```

---

**Audit Completed By:** GitHub Copilot  
**Next Steps:** Apply widget modifications and update Cerberus Object Library  
**Status:** Ready for implementation
