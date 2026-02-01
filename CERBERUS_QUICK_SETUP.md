# 🎯 Cerberus Setup - Visual Quick Start

## ✅ What You Need to Do (5 Minutes)

The error you saw means Cerberus needs basic configuration before you can create tests.

---

## 📋 Setup Checklist (Do in Order)

### ☑️ Step 1: Create a System (2 min)

**Page Open:** http://localhost:8888/SystemList.jsp

**What to do:**
1. Click **"Create System"** button
2. Fill in:
   - **System:** `MySystem`
   - **Description:** `My Test System`
   - **Active:** ✅ Check this box
3. Click **Save**

**Why:** Systems organize everything in Cerberus. You need at least one.

---

### ☑️ Step 2: Create an Application (2 min)

**Page Open:** http://localhost:8888/ApplicationList.jsp

**What to do:**
1. Click **"Create Application"** button
2. Fill in:
   - **Application:** `MyWebApp`
   - **Type:** Select `WEB` from dropdown
   - **System:** Select `MySystem` from dropdown
   - **Description:** `Web application for testing`
3. Click **Save**

**Why:** Applications represent what you're testing (website, API, mobile app).

---

### ☑️ Step 3: Create a Test (1 min)

**Go to:** http://localhost:8888/TestCaseList.jsp

**What to do:**
1. Look for **"Manage Test"** or **"Create Test"** button/link
2. Click it
3. Fill in:
   - **Test:** `MyFirstTest`
   - **Description:** `My first automated tests`
   - **System:** Select `MySystem`
   - **Active:** ✅ Check this box
4. Click **Save**

**Why:** Tests are folders that group related test cases.

---

### ☑️ Step 4: Create a Test Case (5 min)

**Stay on:** http://localhost:8888/TestCaseList.jsp

**What to do:**
1. Click **"+ Create Test Case"** button
2. Fill in:
   - **Test:** `MyFirstTest` (dropdown)
   - **Test Case:** `TC001_VerifyWebsiteText`
   - **Application:** `MyWebApp` (dropdown)
   - **Description:** `Navigate to website and verify text`
   - **Status:** `WORKING` (dropdown)
   - **Priority:** `3`
3. Click **Save**

**Result:** Test case structure created! Now add steps...

---

### ☑️ Step 5: Add Test Steps (3 min)

**In your test case** (should still be on the page):

#### Add Step 1:
1. Click **"+ Add Step"** button
2. Fill in:
   - **Sort/Step:** `1`
   - **Description:** `Open website`
   - **Condition:** `always` (default)
3. Click **"+ Add Action"** inside this step
4. Fill in:
   - **Action:** `openUrl` (dropdown)
   - **Value1:** `https://example.com`
   - **Description:** `Navigate to example.com`
   - **Screenshot:** ✅ Enable
5. Save the action

#### Add Step 2:
1. Click **"+ Add Step"** again
2. Fill in:
   - **Sort/Step:** `2`
   - **Description:** `Verify text on page`
3. Click **"+ Add Action"** inside this step
4. Fill in:
   - **Action:** `verifyTextInPage` (dropdown)
   - **Value1:** `Example Domain`
   - **Description:** `Verify text exists`
   - **Screenshot:** ✅ Enable
5. Save the action

6. **Save everything!**

---

## 🎉 You're Done! Now Test It

### Run Your Test:

1. Go to: http://localhost:8888/RunTests.jsp

2. Select:
   - **Test:** `MyFirstTest`
   - **Test Case:** `TC001_VerifyWebsiteText`
   - **Country:** `US`
   - **Environment:** `PROD`
   - **Browser:** `chrome` or `firefox`

3. Click **"Run Test"** or **"Launch"**

4. Watch it execute!

5. View results and screenshots

---

## 📊 What You'll Have

```
MySystem (System)
  │
  └── MyWebApp (Application)
        │
        └── MyFirstTest (Test)
              │
              └── TC001_VerifyWebsiteText (Test Case)
                    ├── Step 1: openUrl → https://example.com
                    └── Step 2: verifyTextInPage → "Example Domain"
```

---

## 🔗 Quick Links (All Opened for You)

- ✅ **System List:** http://localhost:8888/SystemList.jsp
- ✅ **Application List:** http://localhost:8888/ApplicationList.jsp
- 🎯 **Test Case List:** http://localhost:8888/TestCaseList.jsp
- ▶️ **Run Tests:** http://localhost:8888/RunTests.jsp

---

## ⚡ Super Quick Reference

### Create System
```
System:      MySystem
Description: My Test System
Active:      [✓]
```

### Create Application
```
Application: MyWebApp
Type:        WEB
System:      MySystem
Description: Web application for testing
```

### Create Test
```
Test:        MyFirstTest
System:      MySystem
Description: My first automated tests
Active:      [✓]
```

### Create Test Case
```
Test:        MyFirstTest
Test Case:   TC001_VerifyWebsiteText
Application: MyWebApp
Status:      WORKING
Priority:    3
Description: Navigate to website and verify text
```

### Add Actions
```
Step 1:
  Action: openUrl
  Value1: https://example.com

Step 2:
  Action: verifyTextInPage
  Value1: Example Domain
```

---

## 💡 Tips

- **Save frequently** - Click save after each section
- **Use dropdowns** - Don't type system/app names, select them
- **Check Active boxes** - Inactive items won't show up
- **Enable screenshots** - Super helpful for debugging

---

## 🆘 Troubleshooting

**Can't see System dropdown?**
- You need to create System first (Step 1)
- Refresh the page

**Can't see Application dropdown?**
- You need to create Application first (Step 2)
- Make sure Application belongs to same System

**Permission error still showing?**
- Logout and login again
- Make sure System is Active
- Verify you saved everything

**No actions in dropdown?**
- Actions should be pre-populated
- Try refreshing the page
- Check browser console for errors

---

## ✅ Completion Checklist

- [ ] Created System: `MySystem`
- [ ] Created Application: `MyWebApp`
- [ ] Created Test: `MyFirstTest`
- [ ] Created Test Case: `TC001_VerifyWebsiteText`
- [ ] Added Step 1 with openUrl action
- [ ] Added Step 2 with verifyTextInPage action
- [ ] Saved everything
- [ ] Ready to run test!

---

**Total Time:** ~10 minutes  
**Difficulty:** Easy  
**Result:** Working test case! 🎉

Let me know when you're done or if you hit any snags! 🚀
