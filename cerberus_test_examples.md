# Cerberus Testing - Test Case Examples

## 📚 Table of Contents
1. [Basic Test: Verify Website Text](#basic-test)
2. [Advanced Test: Form Submission](#advanced-test)
3. [Common Actions Reference](#actions-reference)
4. [Running Tests](#running-tests)

---

## Basic Test: Verify Website Text {#basic-test}

### Test Case Details
- **Test:** `MyFirstTest`
- **Test Case:** `TC001_VerifyWebsiteText`
- **Objective:** Navigate to a website and verify text element exists

### Steps

| Step | Action | Value1 | Value2 | Description |
|------|--------|--------|--------|-------------|
| 1 | `openUrl` | `https://example.com` | - | Open the website |
| 2 | `verifyTextInPage` | `Example Domain` | - | Verify text exists on page |
| 3 | `verifyElementPresent` | `id=content` | - | Verify element exists |

### Expected Result
✅ Test passes if "Example Domain" text is found on the page

---

## Advanced Test: Form Submission {#advanced-test}

### Test Case Details
- **Test:** `MyFirstTest`
- **Test Case:** `TC002_GoogleSearch`
- **Objective:** Perform a Google search and verify results

### Steps

| Step | Action | Value1 | Value2 | Description |
|------|--------|--------|--------|-------------|
| 1 | `openUrl` | `https://www.google.com` | - | Open Google |
| 2 | `type` | `name=q` | `Cerberus Testing` | Enter search term |
| 3 | `click` | `name=btnK` | - | Click search button |
| 4 | `waitForElementPresent` | `id=search` | `5000` | Wait for results (5s timeout) |
| 5 | `verifyTextInPage` | `Cerberus` | - | Verify results contain "Cerberus" |

---

## Common Actions Reference {#actions-reference}

### Navigation Actions
```
openUrl                 - Open a URL
click                   - Click an element
clickAndWait            - Click and wait for page load
doubleClick             - Double click an element
mouseOver               - Hover over an element
```

### Input Actions
```
type                    - Type text into input field
select                  - Select option from dropdown
clearField              - Clear input field
keyPress                - Press a specific key
```

### Verification Actions
```
verifyTextInPage        - Verify text exists on page
verifyTextNotInPage     - Verify text does not exist
verifyElementPresent    - Verify element exists
verifyElementNotPresent - Verify element doesn't exist
verifyElementVisible    - Verify element is visible
verifyTitle             - Verify page title
verifyUrl               - Verify current URL
```

### Wait Actions
```
waitForElementPresent   - Wait for element to appear
waitForElementNotPresent- Wait for element to disappear
waitForElementVisible   - Wait for element to be visible
waitForTextInPage       - Wait for text to appear
wait                    - Simple wait/sleep (milliseconds)
```

### Element Locators
```
id=myId                 - By ID attribute
name=myName             - By name attribute
xpath=//div[@id='test'] - By XPath
css=#myId               - By CSS selector
link=Link Text          - By link text
```

---

## Running Tests {#running-tests}

### Method 1: Manual Execution (UI)
1. Go to **Test** → **Run Test**
2. Select your test case
3. Choose environment and browser
4. Click **"Run Test"**

### Method 2: API Execution
```bash
curl -X POST "http://localhost:8888/api/public/runtestcase" \
  -H "Content-Type: application/json" \
  -u "admin:admin" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "country": "US",
    "environment": "PROD",
    "browser": "chrome"
  }'
```

### Method 3: Campaign Execution
Create a campaign to run multiple tests:
1. Go to **Test** → **Campaign**
2. Create new campaign
3. Add test cases
4. Schedule or run immediately

---

## 🎯 Quick Start Test Case

Here's a simple test you can create right now:

### Test: Verify GitHub Homepage

**Steps:**
1. **openUrl** → `https://github.com`
2. **verifyTextInPage** → `GitHub`
3. **verifyElementPresent** → `css=.octicon-mark-github`
4. **click** → `link=Sign in`
5. **verifyUrl** → `https://github.com/login`

---

## 📝 Best Practices

1. **Use Descriptive Names**
   - Test: `UserAuthentication`
   - Test Case: `TC001_ValidLogin`

2. **Add Screenshots**
   - Enable screenshots on critical steps
   - Helps with debugging failures

3. **Use Waits**
   - Add `waitForElementPresent` before interactions
   - Prevents timing issues

4. **Verify Outcomes**
   - Always verify expected results
   - Don't just perform actions

5. **Keep Tests Atomic**
   - One test case = One scenario
   - Independent and reusable

---

## 🔗 Resources

- **Cerberus Documentation:** http://localhost:8888/documentation/
- **Test Case Editor:** http://localhost:8888/TestCaseScript.jsp
- **Test Execution:** http://localhost:8888/RunTests.jsp
- **API Documentation:** http://localhost:8888/api/docs

---

## 🚀 Next Steps

1. Create your first test case using the UI
2. Run it manually to verify it works
3. Create a campaign with multiple test cases
4. Schedule automated runs
5. Integrate with CI/CD pipeline

Good luck with your testing! 🎉
