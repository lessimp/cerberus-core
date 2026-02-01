# 🔧 Cerberus Test Case - Manual Setup Guide

## ⚠️ Important Note

The API endpoints used in the scripts **are not available** in Cerberus version 4.20.

**The error banner you saw** was indicating that the test case `TC001_VerifyWebsiteText` does not exist because the API creation failed silently.

You'll need to create test cases **manually through the UI** for now.

---

## 📋 Manual Test Case Creation (Step-by-Step)

### Step 1: Login to Cerberus

1. Open your browser: **http://localhost:8888/**
2. Login with:
   - **Username:** `admin`
   - **Password:** `admin`

---

### Step 2: Navigate to Test Cases

1. Click on **"Test"** in the top navigation menu
2. Select **"Test Cases"** from the dropdown menu
3. You should see the Test Case List page

---

### Step 3: Create New Test

First, we need to create a "Test" (which is like a folder for test cases):

1. Look for a **"Create Test"** or **"Manage Test"** button/link
2. Click it and create:
   - **Test:** `MyFirstTest`
   - **Description:** `My first automated tests`
   - **Active:** Yes
   
3. Click **Save**

---

### Step 4: Create Test Case

Now create the actual test case:

1. Click the **"+ Create Test Case"** button (or similar)
2. Fill in the following fields:

| Field | Value |
|-------|-------|
| **Test** | `MyFirstTest` (select from dropdown) |
| **Test Case** | `TC001_VerifyWebsiteText` |
| **Description** | `Navigate to a website and verify text element` |
| **Application** | `Google` (or create new application first) |
| **Status** | `WORKING` |
| **Priority** | `3` (1=highest, 5=lowest) |
| **Group** | Leave empty or set to `AUTOMATED` |
| **Origin** | Leave as default |
| **Ref Origin** | Leave empty |
| **Target Sprint** | Leave empty |
| **Target Revision** | Leave empty |

3. Click **Save** or **Create**

---

### Step 5: Add Test Steps

Now you need to add the actual test steps:

#### Adding Step 1: Open URL

1. In your test case, find the **"Steps"** section
2. Click **"+ Add Step"** or **"Add New Step"**
3. Fill in:
   - **Step:** `1` (or auto-numbered)
   - **Description:** `Open website`
   - **Loop:** Leave blank (or set to empty)
   - **Condition Operator:** `always`
   - **Condition Value 1-3:** Leave blank

4. Now add an **Action** to this step:
   - Click **"+ Add Action"** within Step 1
   - **Action:** Select `openUrl` from dropdown
   - **Value 1:** `https://example.com`
   - **Value 2:** Leave empty
   - **Description:** `Navigate to example.com`
   - **Screenshot:** Enable (checkbox)

5. Click **Save** on the action

---

#### Adding Step 2: Verify Text

1. Click **"+ Add Step"** again
2. Fill in:
   - **Step:** `2`
   - **Description:** `Verify text on page`
   - **Condition Operator:** `always`

3. Add an **Action**:
   - Click **"+ Add Action"** within Step 2
   - **Action:** Select `verifyTextInPage` from dropdown
   - **Value 1:** `Example Domain`
   - **Value 2:** Leave empty
   - **Description:** `Verify 'Example Domain' text is present`
   - **Screenshot:** Enable

4. Click **Save**

---

#### Optional: Adding Step 3: Verify Element

1. Click **"+ Add Step"**
2. Fill in:
   - **Step:** `3`
   - **Description:** `Verify content element exists`

3. Add an **Action**:
   - **Action:** `verifyElementPresent`
   - **Value 1:** `id=content`
   - **Value 2:** Leave empty
   - **Description:** `Verify content div exists`

---

### Step 6: Save Everything

1. Make sure all steps and actions are saved
2. Click the main **Save** button if there is one
3. You should see a success message

---

## ▶️ Running Your Test

### Via UI (Recommended)

1. Go to: **Test** → **Run Test**
2. Or directly: http://localhost:8888/RunTests.jsp

3. Configure the test run:
   - **Test:** Select `MyFirstTest`
   - **Test Case:** Select `TC001_VerifyWebsiteText`
   - **Country:** `US` (or your country code)
   - **Environment:** `PROD` (or create an environment)
   - **Browser:** `chrome` or `firefox`
   - **Robot/Executor:** Select available robot

4. Click **"Run Test"** or **"Launch"**

5. Wait for execution to complete

6. View results in the execution report

---

## 📊 Viewing Results

After running the test:

1. Go to: **Reporting** → **Execution Reporting**
2. Or: http://localhost:8888/ReportingExecutionList.jsp

3. Find your test execution
4. Click on it to see:
   - Step-by-step execution log
   - Screenshots of each step
   - Success/Failure status
   - Execution time
   - Error messages (if any)

---

## 🎯 Test Case Structure

Here's what you're creating:

```
MyFirstTest
└── TC001_VerifyWebsiteText
    ├── Step 1: Open website
    │   └── Action: openUrl → https://example.com
    ├── Step 2: Verify text on page
    │   └── Action: verifyTextInPage → "Example Domain"
    └── Step 3: Verify content element exists (optional)
        └── Action: verifyElementPresent → id=content
```

---

## 🔍 Common Actions Reference

When adding actions to steps, here are the most useful ones:

### Navigation
- **openUrl** - Open a URL (Value1: URL)
- **click** - Click element (Value1: element locator)
- **clickAndWait** - Click and wait for page load
- **mouseOver** - Hover over element
- **goBack** - Browser back button
- **refresh** - Refresh page

### Verification
- **verifyTextInPage** - Check text exists on page (Value1: text)
- **verifyTextNotInPage** - Check text doesn't exist
- **verifyElementPresent** - Check element exists (Value1: locator)
- **verifyElementNotPresent** - Check element doesn't exist
- **verifyElementVisible** - Check element is visible
- **verifyTitle** - Check page title (Value1: expected title)
- **verifyUrl** - Check current URL (Value1: expected URL)

### Input
- **type** - Type text into field (Value1: locator, Value2: text)
- **select** - Select from dropdown (Value1: locator, Value2: option)
- **clearField** - Clear input field (Value1: locator)

### Waits
- **wait** - Simple wait (Value1: milliseconds)
- **waitForElementPresent** - Wait for element (Value1: locator, Value2: timeout ms)
- **waitForElementVisible** - Wait for visible element
- **waitForElementNotVisible** - Wait for element to disappear

---

## 🏷️ Element Locators

When specifying elements in Value1, use these formats:

```
id=myElementId              # By ID attribute
name=myElementName          # By name attribute
xpath=//div[@class='test']  # By XPath
css=#myId                   # By CSS selector
css=.myClass                # By CSS class
link=Link Text              # By link text
```

### Examples:
- `id=username` - Find element with id="username"
- `name=password` - Find element with name="password"
- `css=button.submit` - Find button with class "submit"
- `xpath=//input[@type='submit']` - Find submit input via XPath
- `link=Sign In` - Find link with text "Sign In"

---

## 🛠️ Creating an Application (If Needed)

Before creating test cases, you might need to create an "Application":

1. Go to: **Administration** → **Application**
2. Click **"+ Add Application"**
3. Fill in:
   - **Application:** `Google` (or your app name)
   - **Description:** `Google Website`
   - **Type:** `WEB`
   - **System:** Select or create a system
4. Click **Save**

---

## 🌍 Creating an Environment (If Needed)

You might need to configure environments:

1. Go to: **Administration** → **Environment**
2. Create environments like:
   - **Environment:** `PROD`
   - **Description:** `Production Environment`
3. Configure database connections if needed

---

## 🤖 Robot/Executor Setup

To run tests, you need a Selenium executor:

1. Go to: **Administration** → **Robot**
2. Check if any robots are configured
3. If none exist, you might need to set up Selenium Grid or use local browser

**Note:** Cerberus typically requires either:
- Local Selenium WebDriver
- Remote Selenium Grid
- BrowserStack/Sauce Labs integration

---

## ⚠️ Troubleshooting

### "Test Case Not Found" Error
- The banner you saw means the test case doesn't exist yet
- Create it manually following the steps above

### Can't Find "Create Test Case" Button
- Make sure you're logged in
- Check you have the right permissions
- Try navigating to: http://localhost:8888/TestCaseList.jsp

### No Actions Available in Dropdown
- The actions should be pre-configured in Cerberus
- If empty, there might be a database issue
- Check Cerberus logs: `docker-compose logs cerberus`

### Can't Run Test - No Robot Available
- You need to configure a Selenium executor
- Go to Administration → Robot
- Or use a cloud testing service

---

## 📚 Quick Reference

### Important URLs
- **Homepage:** http://localhost:8888/
- **Test Case List:** http://localhost:8888/TestCaseList.jsp
- **Run Tests:** http://localhost:8888/RunTests.jsp
- **Executions:** http://localhost:8888/ReportingExecutionList.jsp
- **Documentation:** http://localhost:8888/documentation/

### Default Credentials
- **Username:** `admin`
- **Password:** `admin`

---

## 🎯 Next Steps

1. ✅ Login to Cerberus UI
2. ✅ Create the Test: `MyFirstTest`
3. ✅ Create the Test Case: `TC001_VerifyWebsiteText`
4. ✅ Add Step 1: openUrl
5. ✅ Add Step 2: verifyTextInPage
6. ✅ Configure a Robot/Executor (if needed)
7. ✅ Run the test
8. ✅ View the results

---

## 💡 Why Manual Creation?

**Cerberus version 4.20** uses older Servlets rather than modern REST APIs:
- `/CreateTestCase` servlet instead of `/api/public/testcase`
- Different authentication mechanism
- UI-based workflow is more reliable

For automation in this version, you would need to:
1. Reverse-engineer the servlet URLs
2. Handle session management properly
3. Submit form data in the expected format

**For now, manual creation through the UI is the recommended approach.**

---

Good luck! Once you've created the test case manually, come back and let me know if you need help running it! 🚀
