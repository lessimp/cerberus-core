# 🧪 Cerberus Test Case - Step-by-Step Visual Guide

## ✅ Test Case Successfully Created!

Your first test case has been created and is ready to run!

---

## 📋 What Was Created

### Test Information
```
Test:        MyFirstTest
Test Case:   TC001_VerifyWebsiteText
Description: Navigate to a website and verify text element
Application: Google
Status:      WORKING
Priority:    3
```

### Test Steps

#### Step 1: Open Website
```
Action:      openUrl
Value:       https://example.com
Purpose:     Navigate to the example.com website
```

#### Step 2: Verify Text
```
Action:      verifyTextInPage
Value:       Example Domain
Purpose:     Verify that "Example Domain" text appears on the page
```

---

## 🎯 How to View Your Test

### Option 1: Direct Link
Click this link to view your test case:
```
http://localhost:8888/TestCaseScript.jsp?test=MyFirstTest&testcase=TC001_VerifyWebsiteText
```

### Option 2: Navigate via UI
1. Open: `http://localhost:8888/`
2. Login with `admin` / `admin`
3. Click: **Test** → **Test Cases**
4. Search for: `MyFirstTest`
5. Click on: `TC001_VerifyWebsiteText`

---

## ▶️ How to Run Your Test

### Manual Execution (UI)

1. **Go to Run Tests Page:**
   ```
   http://localhost:8888/RunTests.jsp
   ```

2. **Configure Test:**
   - Test: Select `MyFirstTest`
   - Test Case: Select `TC001_VerifyWebsiteText`
   - Environment: `PROD`
   - Country: `US`
   - Browser: `chrome` (or `firefox`)

3. **Click "Run Test"**

4. **View Results:**
   - You'll be redirected to the execution page
   - Watch the test run in real-time
   - View screenshots of each step

### API Execution (Command Line)

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

## 📊 Expected Results

When you run this test, here's what should happen:

### ✅ Success Scenario
1. Browser opens and navigates to https://example.com
2. Page loads successfully
3. Text "Example Domain" is found on the page
4. **Test Status:** ✅ **PASS**

### ❌ Failure Scenario (if something goes wrong)
1. Browser opens but cannot reach URL → Network error
2. Page loads but text not found → Verification failed
3. **Test Status:** ❌ **FAIL**

---

## 🔧 Modifying Your Test

### Add More Steps

To add more verification steps, you can:

1. **Add Element Verification:**
   ```
   Step 3: verifyElementPresent → id=content
   ```

2. **Add Click Action:**
   ```
   Step 4: click → link=More information...
   ```

3. **Add Wait:**
   ```
   Step 5: waitForElementPresent → css=.domain-info → 5000
   ```

### Edit via UI
1. Go to your test case page
2. Click on any step to edit
3. Add new steps using the "+ Add" button
4. Save changes

---

## 🎨 Test Execution Features

### Screenshots
Cerberus automatically captures screenshots at each step. You can:
- View them in the execution report
- Download them for documentation
- Use them for debugging failures

### Execution Logs
Each execution provides:
- **Step-by-step logs** with timestamps
- **Action results** (success/failure)
- **Error messages** if failures occur
- **Performance metrics** (execution time)

---

## 🧰 Useful Commands

### List All Tests
```bash
curl -s "http://localhost:8888/api/public/testcase" \
  -u "admin:admin" | jq
```

### Run Test and Get Execution ID
```bash
EXEC_ID=$(curl -s -X POST "http://localhost:8888/api/public/runtestcase" \
  -H "Content-Type: application/json" \
  -u "admin:admin" \
  -d '{
    "test": "MyFirstTest",
    "testcase": "TC001_VerifyWebsiteText",
    "country": "US",
    "environment": "PROD",
    "browser": "chrome"
  }' | jq -r '.executionId')

echo "Execution ID: $EXEC_ID"
echo "View at: http://localhost:8888/TestCaseExecution.jsp?executionId=$EXEC_ID"
```

---

## 📚 Next Test Cases to Create

### Beginner Level
1. ✅ **Verify Website Text** (Just completed!)
2. **Verify Multiple Elements** - Check for multiple page elements
3. **Click and Navigate** - Click a link and verify new page

### Intermediate Level
4. **Form Submission** - Fill out and submit a form
5. **Dropdown Selection** - Select options from dropdowns
6. **Wait for Dynamic Content** - Handle AJAX/dynamic loading

### Advanced Level
7. **Multi-Page Flow** - Navigate through multiple pages
8. **Data-Driven Tests** - Use different test data
9. **Conditional Logic** - Tests with if/else conditions

---

## 🎓 Learning Resources

### Cerberus Actions Reference
- **Navigation:** openUrl, click, clickAndWait, goBack, refresh
- **Input:** type, select, clearField, keyPress
- **Verification:** verifyTextInPage, verifyElementPresent, verifyTitle
- **Waits:** waitForElementPresent, waitForElementVisible, wait
- **Screenshots:** takeScreenshot (automatic on each step)

### Official Links
- **Documentation:** http://localhost:8888/documentation/
- **Test Case List:** http://localhost:8888/TestCaseList.jsp
- **Run Tests:** http://localhost:8888/RunTests.jsp
- **Executions:** http://localhost:8888/ReportingExecutionList.jsp
- **API Docs:** http://localhost:8888/api/docs

---

## 💡 Pro Tips

1. **Always Use Waits**
   - Add `waitForElementPresent` before clicking elements
   - Prevents timing issues with dynamic content

2. **Enable Screenshots**
   - Screenshots are enabled by default
   - Invaluable for debugging failed tests

3. **Descriptive Names**
   - Use clear, descriptive names for tests and steps
   - Makes maintenance easier

4. **Test Independence**
   - Each test should work standalone
   - Don't depend on other tests running first

5. **Verify Everything**
   - Don't just perform actions
   - Always verify the expected outcome

---

## 🆘 Troubleshooting

### Test Fails to Run
- **Check browser:** Make sure Chrome/Firefox is specified
- **Check environment:** Ensure environment exists in Cerberus
- **Check application:** Verify application is configured

### Element Not Found
- **Add waits:** Use `waitForElementPresent` before interactions
- **Check locator:** Verify element ID/name/xpath is correct
- **Check timing:** Increase wait timeout if needed

### Network Issues
- **Check URL:** Ensure URL is accessible from your network
- **Check proxy:** Configure proxy settings if needed
- **Check timeout:** Increase page load timeout

---

## 🎉 Congratulations!

You've successfully created your first Cerberus test case! 

**What's Next?**
1. Run the test and see it in action
2. Create more complex test cases
3. Build a test campaign with multiple tests
4. Integrate with CI/CD pipeline

**Happy Testing!** 🚀
