# 🎯 Cerberus Testing - Quick Start Guide

## ✅ Your Cerberus Instance
- **URL:** http://localhost:8888/
- **Username:** `admin`
- **Password:** `admin`
- **Status:** ✅ Running and Ready

---

## 🚀 Quick Start: Create Your First Test

### Option 1: Use the Web UI (Recommended for Beginners)

1. **Open Cerberus:** http://localhost:8888/
2. **Login** with `admin` / `admin`
3. **Navigate to:** Test → Test Cases
4. **Click:** "+ Create Test Case" button
5. **Fill in:**
   - Test: `MyFirstTest`
   - Test Case: `TC001_VerifyWebsiteText`
   - Description: `Navigate to a website and verify text`
   - Application: `Google`
   - Status: `WORKING`
6. **Click Save**

7. **Add Steps:**
   
   **Step 1:**
   - Description: `Open website`
   - Add Action: `openUrl`
   - Value1: `https://example.com`
   
   **Step 2:**
   - Description: `Verify text`
   - Add Action: `verifyTextInPage`
   - Value1: `Example Domain`

8. **Run Test:** Test → Run Test → Select your test → Click "Run"

---

### Option 2: Use the Python Script (Automated)

I've created a Python helper script for you:

```bash
# Navigate to your scripts
cd ~/Documents/GitHub

# Run the script to create an example test
python3 cerberus_helper.py example

# Or create a Google search test
python3 cerberus_helper.py google
```

**What the script does:**
- Creates a test case structure
- Adds steps with actions
- Provides URLs to view and run the test

---

### Option 3: Use the Bash Script (Shell)

```bash
# Run the bash script
~/Documents/GitHub/create_cerberus_test.sh
```

---

## 📚 Common Test Actions

### Navigation
```
openUrl                 - Open a URL
click                   - Click an element
clickAndWait            - Click and wait for page load
```

### Verification
```
verifyTextInPage        - Verify text exists
verifyElementPresent    - Verify element exists
verifyTitle             - Verify page title
verifyUrl               - Verify current URL
```

### Input
```
type                    - Type text into field
select                  - Select dropdown option
clearField              - Clear input field
```

### Waits
```
waitForElementPresent   - Wait for element to appear
waitForElementVisible   - Wait for element to be visible
wait                    - Simple wait (milliseconds)
```

---

## 🎯 Example Test Cases

### Example 1: Simple Website Verification
**Goal:** Open a website and verify text

```
Step 1: openUrl → https://example.com
Step 2: verifyTextInPage → Example Domain
Step 3: verifyElementPresent → id=content
```

---

### Example 2: GitHub Homepage
**Goal:** Navigate GitHub and verify elements

```
Step 1: openUrl → https://github.com
Step 2: verifyTextInPage → GitHub
Step 3: verifyElementPresent → css=.octicon-mark-github
Step 4: click → link=Sign in
Step 5: verifyUrl → https://github.com/login
```

---

### Example 3: Google Search
**Goal:** Perform a search and verify results

```
Step 1: openUrl → https://www.google.com
Step 2: type → name=q → Cerberus Testing
Step 3: click → name=btnK
Step 4: waitForElementPresent → id=search → 5000
Step 5: verifyTextInPage → Cerberus
```

---

## 🔍 Element Locators

When specifying elements, use these formats:

```
id=myId                 - Find by ID
name=myName             - Find by name attribute
xpath=//div[@class='x'] - Find by XPath
css=#myId               - Find by CSS selector
link=Click Here         - Find by link text
```

---

## 📖 Helpful Resources

I've created these files for you:

1. **cerberus_helper.py** - Python script to create tests programmatically
2. **create_cerberus_test.sh** - Bash script for quick test creation
3. **cerberus_test_examples.md** - Comprehensive examples and reference

All located in: `~/Documents/GitHub/`

---

## 🎬 Run Your Tests

### Manual Execution
1. Go to: http://localhost:8888/RunTests.jsp
2. Select your test case
3. Choose environment and browser
4. Click "Run Test"

### API Execution
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

---

## 🎉 Next Steps

1. **Login to Cerberus:** http://localhost:8888/
2. **Create your first test** using the UI or Python script
3. **Run the test** to see it in action
4. **View the execution** results and screenshots
5. **Create more complex tests** as you learn

---

## 🆘 Need Help?

- **Documentation:** http://localhost:8888/documentation/
- **Test Case Editor:** http://localhost:8888/TestCaseScript.jsp
- **Run Tests:** http://localhost:8888/RunTests.jsp
- **API Docs:** http://localhost:8888/api/docs

---

## 💡 Pro Tips

1. **Always add waits** before interacting with elements
2. **Enable screenshots** on critical steps for debugging
3. **Use descriptive names** for tests and steps
4. **Keep tests independent** - each test should work standalone
5. **Verify outcomes** - don't just perform actions, verify results

---

Happy Testing! 🚀
