# 🔧 Fixing Cerberus Permission Error

## ❌ The Actual Error

```
ERROR - Could not find any data that match the required criteria. 
Verify you have right on object's system
```

This is a **System/Permission** issue, not a missing test case!

---

## 🎯 Root Cause

Cerberus organizes tests by **"Systems"**. The error means:

1. **No System exists** in your Cerberus instance, OR
2. **You don't have permission** to view the System

**Systems** in Cerberus are like organizational units (e.g., "MyWebsite", "MobileApp", "API")

---

## ✅ Solution: Create a System First

### Step 1: Create a System

1. **I've opened the System page for you:**
   - http://localhost:8888/SystemList.jsp

2. **Click "Create System"** (or similar button)

3. **Fill in:**
   ```
   System:      MySystem
   Description: My Test System
   ```

4. **Click Save**

---

### Step 2: Create an Application

Applications belong to Systems. Now create one:

1. **Go to Application page:**
   - Navigate to: **Administration** → **Application**
   - Or: http://localhost:8888/ApplicationList.jsp

2. **Click "Create Application"**

3. **Fill in:**
   ```
   Application: MyWebApp
   Description: My Web Application
   Type:        WEB
   System:      MySystem (select the one you just created)
   ```

4. **Click Save**

---

### Step 3: Verify User Permissions

Make sure the admin user has access:

1. **Go to User Management:**
   - Navigate to: **Administration** → **User**
   - Or: http://localhost:8888/UserList.jsp

2. **Find user "admin"**

3. **Edit the user** and check:
   - **System:** Make sure `MySystem` is in the allowed systems list
   - **Role:** Should be `Administrator` or have test creation rights

4. **Save if you made changes**

---

### Step 4: Now Create the Test Case

With System and Application configured, now you can create tests:

1. **Go to Test Case List:**
   - http://localhost:8888/TestCaseList.jsp

2. **Create Test:**
   - Click "Create Test" or manage tests
   - **Test:** `MyFirstTest`
   - **Description:** `My first automated tests`
   - **System:** `MySystem`
   - **Active:** Yes

3. **Create Test Case:**
   - **Test:** `MyFirstTest`
   - **Test Case:** `TC001_VerifyWebsiteText`
   - **Application:** `MyWebApp`
   - **Description:** `Navigate to website and verify text`
   - **Status:** `WORKING`
   - **Priority:** `3`

4. **Add Steps:**
   - **Step 1:** openUrl → https://example.com
   - **Step 2:** verifyTextInPage → Example Domain

---

## 🎯 Quick Setup Checklist

Complete these in order:

- [ ] **Step 1:** Create System (`MySystem`)
- [ ] **Step 2:** Create Application (`MyWebApp`) under `MySystem`
- [ ] **Step 3:** Verify admin user has access to `MySystem`
- [ ] **Step 4:** Create Test (`MyFirstTest`) under `MySystem`
- [ ] **Step 5:** Create Test Case (`TC001_VerifyWebsiteText`) using `MyWebApp`
- [ ] **Step 6:** Add test steps and actions
- [ ] **Step 7:** Run the test!

---

## 📋 Understanding Cerberus Hierarchy

```
System (MySystem)
  └── Application (MyWebApp)
        └── Test (MyFirstTest)
              └── Test Case (TC001_VerifyWebsiteText)
                    ├── Step 1: openUrl
                    ├── Step 2: verifyTextInPage
                    └── Step 3: ...
```

**Every test case** must be linked to:
- ✅ A **Test** (folder/group)
- ✅ An **Application**
- ✅ A **System**

**Users** must have permission to access the **System**.

---

## 🔗 Quick Navigation Links

I've opened these pages for you:

1. **System List** (open now):
   - http://localhost:8888/SystemList.jsp
   - **Action:** Create `MySystem`

2. **Application List** (open next):
   - http://localhost:8888/ApplicationList.jsp
   - **Action:** Create `MyWebApp`

3. **Test Case List** (open after setup):
   - http://localhost:8888/TestCaseList.jsp
   - **Action:** Create test case

---

## 🎨 Example System Configuration

### System
```
System:      MySystem
Description: General testing system
Active:      Yes
```

### Application
```
Application: MyWebApp
Type:        WEB
System:      MySystem
Description: Web application for testing
```

### Test
```
Test:        MyFirstTest
Description: Basic website verification tests
System:      MySystem
Active:      Yes
```

### Test Case
```
Test:        MyFirstTest
Test Case:   TC001_VerifyWebsiteText
Application: MyWebApp
Description: Verify example.com text
Status:      WORKING
Priority:    3
```

---

## ⚠️ Common Issues

### Still Getting Permission Error?
1. **Logout and login again** - permissions cache
2. **Check System is Active** - disabled systems won't show
3. **Verify user System access** - admin must have access to MySystem

### Can't Create System?
- Make sure you're logged in as `admin`
- Admin should have full permissions
- Check: Administration → User → admin → Systems

### Application Not Showing in Dropdown?
- Application must belong to the same System as your Test
- Application must be Active
- Refresh the page

---

## 🚀 Next Steps

1. **Create System** (System List page is open)
2. **Create Application** (link above)
3. **Create Test & Test Case** (follow CERBERUS_MANUAL_SETUP.md)
4. **Run your test!**

---

## 💡 Why This Happens

Cerberus **requires organizational structure** before you can create tests:

1. **Systems** = High-level organization (like departments/projects)
2. **Applications** = What you're testing (websites, APIs, apps)
3. **Tests** = Groups of related test cases
4. **Test Cases** = Individual test scenarios

This structure helps with:
- **Permissions** - Control who can access what
- **Organization** - Keep tests organized
- **Reporting** - Group results by system/app
- **Multi-project** support

---

## ✅ Summary

**The Error Meant:**
- You tried to view test cases
- But no System exists OR you don't have permission
- Cerberus can't show any data

**The Fix:**
1. Create System first
2. Create Application under that System
3. Ensure admin has System access
4. Then create Tests and Test Cases

**Estimated Time:** 5 minutes total

Let me know once you've created the System and Application, and I'll help you create the actual test case! 🚀
