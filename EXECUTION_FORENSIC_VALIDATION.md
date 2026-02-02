# 🎯 Final Execution & Forensic Validation Directive

**Status:** 🔴 LIVE EXECUTION MODE  
**Phase:** Execution & Forensics  
**Date:** February 1, 2026  
**Version:** 5.0 - PRODUCTION VALIDATION

---

## 🚨 Mission Objective

Execute the **TC001_SecureLogin** test case and verify the end-to-end security handshake between:
- **Cerberus Testing** (v4.20)
- **Lessimp Flutter App** (iOS Simulator)
- **Shuffle Automation Engine** (Local + Cloud)
- **Discord Webhooks** (Green/Red alerts)
- **Gmail SMTP** (Critical incident reports)

---

## 1️⃣ Pre-Flight Infrastructure Check

### Critical Services Status

Before executing tests, verify all infrastructure components are operational:

#### ✅ Service Checklist

| Service | Expected State | Verification Command | Success Indicator |
|---------|----------------|---------------------|-------------------|
| **Cerberus UI** | Running | `curl -I http://localhost:8888/` | HTTP/1.1 200 OK |
| **Shuffle Local Engine** | Active | `curl http://localhost:3001/api/v1/health` | Status: running |
| **Shuffle Data Provider** | Background | `ps aux \| grep shuffle_provider.py` | Process exists |
| **iOS Simulator** | Booted | `xcrun simctl list \| grep Booted` | iPhone 16 Pro (Booted) |
| **Lessimp App** | Installed | `xcrun simctl get_app_container booted com.lessimp.dating` | Path returned |

---

### Infrastructure Startup Commands

#### Start Cerberus (if not running)
```bash
cd ~/Documents/GitHub/cerberus-core
docker-compose up -d
# Wait 30 seconds for MySQL and Tomcat to initialize
sleep 30
curl -I http://localhost:8888/
```

#### Start Shuffle Local Engine (if not running)
```bash
# If using Shuffle Desktop App - launch application
# If using Docker:
docker run -d -p 3001:3001 --name shuffle-backend \
  frikky/shuffle:latest
```

#### Start Shuffle Data Provider (Background Service)
```bash
cd ~/Documents/GitHub/cerberus-core
nohup python3 shuffle_provider.py --api --port 5000 > shuffle_provider.log 2>&1 &
echo $! > shuffle_provider.pid
# Verify it's running
ps aux | grep shuffle_provider.py
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "shuffle_provider",
  "version": "1.0",
  "endpoints": ["/api/users", "/api/random-user"]
}
```

#### Launch iOS Simulator
```bash
cd ~/Documents/GitHub/lessimp
# Boot simulator
open -a Simulator
# Wait for boot
sleep 10
# Run Flutter app
flutter run -d "iPhone 16 Pro"
# Wait for app to appear on home screen
```

---

### Verification Script (All-in-One)

**Save as:** `~/Documents/GitHub/cerberus-core/preflight_check.sh`

```bash
#!/bin/bash

echo "🚀 Project Lessimp-Secure: Pre-Flight Infrastructure Check"
echo "=========================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_service() {
    local name=$1
    local command=$2
    local expected=$3
    
    echo -n "Checking $name... "
    if eval $command | grep -q "$expected"; then
        echo -e "${GREEN}✅ PASS${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        return 1
    fi
}

# Check Cerberus
check_service "Cerberus UI" "curl -s -I http://localhost:8888/" "HTTP/1.1 200"

# Check Shuffle Local Engine
check_service "Shuffle Engine" "curl -s http://localhost:3001/api/v1/health" "running"

# Check Shuffle Provider
check_service "Shuffle Provider" "curl -s http://localhost:5000/health" "healthy"

# Check iOS Simulator
check_service "iOS Simulator" "xcrun simctl list | grep Booted" "iPhone"

# Check Lessimp App
check_service "Lessimp App" "xcrun simctl get_app_container booted com.lessimp.dating" "/Users"

echo ""
echo "=========================================================="
echo "Pre-Flight Check Complete!"
echo ""
```

**Run:**
```bash
chmod +x ~/Documents/GitHub/cerberus-core/preflight_check.sh
~/Documents/GitHub/cerberus-core/preflight_check.sh
```

---

## 2️⃣ Phase 1: Service & Test Case Verification

### Navigate to Cerberus Service Library

**URL:** http://localhost:8888/ServiceList.jsp

### Audit GetShuffleUser Service

**Click:** `GetShuffleUser` → [Edit]

**Verification Checklist:**

| Field | Expected Value | Status |
|-------|---------------|--------|
| **Service** | `GetShuffleUser` | [ ] Verified |
| **Group** | `Shuffle` | [ ] Verified |
| **Method** | `POST` | [ ] Verified |
| **Service Path** | `%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute` | [ ] Verified |
| **Headers** | `Content-Type: application/json` | [ ] Verified |
| **Property: PHONE** | JSON Path: `$.shuffled_user.phone` | [ ] Verified |
| **Property: OTP** | JSON Path: `$.shuffled_user.otp` | [ ] Verified |
| **Property: EMAIL** | JSON Path: `$.shuffled_user.email` | [ ] Verified |
| **Property: USER_NAME** | JSON Path: `$.shuffled_user.name` | [ ] Verified |

**Test Service Manually:**
```bash
# Navigate to Service Library → GetShuffleUser → Test
# Click: [Test Service]
# Expected: HTTP 200, Response contains shuffled_user object
```

---

### Audit TC001_SecureLogin Test Case

**URL:** http://localhost:8888/TestCaseList.jsp

**Click:** `TC001_SecureLogin` → [Edit Steps]

---

#### 🔍 Critical Step Audit: Step 6 (Forensic Log)

**Navigate:** Test Case Steps → Step 6

**Expected Configuration:**

| Field | Expected Value | Status |
|-------|---------------|--------|
| **Step** | `6` | [ ] Verified |
| **Description** | `Log test execution identity for security forensics and audit trail` | [ ] Verified |
| **Action** | `calculateProperty` | [ ] Verified |
| **Value1** | `TEST_IDENTITY_LOG` | [ ] Verified |
| **Value2** | `Testing with: PHONE=%PHONE%, USER=%USER_NAME%, EMAIL=%EMAIL%, USER_ID=%USER_ID%` | [ ] Verified |
| **Fatal** | `No` | [ ] Verified |

**🎯 THIS IS YOUR FORENSIC AUDIT TRAIL!**

**Purpose:**
- Logs which Shuffle user credentials are being used in this test execution
- Provides evidence for security investigations
- Creates permanent record in Cerberus execution history
- Links test run to specific user identity

**Verification:**
1. After test execution, navigate to: http://localhost:8888/TestCaseExecutionList.jsp
2. Find latest `TC001_SecureLogin` execution
3. Click: [View Details]
4. Scroll to Step 6
5. Look for property: **TEST_IDENTITY_LOG**
6. Expected value format:
   ```
   Testing with: PHONE=5555551003, USER=Carol Davis, EMAIL=carol.davis@testmail.com, USER_ID=3
   ```

---

#### 🔍 Critical Step Audit: Step 16 (Security Trigger)

**Navigate:** Test Case Steps → Step 16

**Expected Configuration:**

| Field | Expected Value | Status |
|-------|---------------|--------|
| **Step** | `16` | [ ] Verified |
| **Description** | `🚨 Trigger Shuffle security webhook to validate login and send alerts` | [ ] Verified |
| **Action** | `callService` | [ ] Verified |
| **Value1** | `ShuffleSecurity_LoginTrigger` | [ ] Verified |
| **Fatal** | `No` | [ ] Verified |

**Service Details:**
- **Webhook URL:** `https://shuffler.io/api/v1/hooks/webhook_a76354e0-cf09-4754-96e1-682c89084d4c`
- **Payload:** Includes user, phone, email, timestamp, test_case

**Verification:**
1. Navigate to: http://localhost:8888/ServiceList.jsp
2. Click: `ShuffleSecurity_LoginTrigger` → [Edit]
3. Verify service path contains webhook ID: `webhook_a76354e0-cf09-4754-96e1-682c89084d4c`
4. Verify body template includes:
   ```json
   {
     "user": "wipedclean",
     "phone": "%PHONE%",
     "email": "%EMAIL%",
     "timestamp": "%SYS.TODAY%",
     "test_case": "TC001_SecureLogin",
     "status": "login_complete"
   }
   ```

---

## 3️⃣ Phase 2: Live Execution Scenarios

### Scenario A: Authorized Identity (The Green Path) 🟢

**Condition:** `user == "wipedclean"` OR `hour == 9`

**Expected Outcome:** Discord receives green "Identity Verified" notification

---

#### Step-by-Step Execution

**1. Configure Shuffle Provider for Authorized User**

Edit: `~/Documents/GitHub/cerberus-core/shuffle_provider.py`

**Modify the `/api/random-user` endpoint:**
```python
@app.route('/api/random-user', methods=['GET', 'POST'])
def get_random_user():
    # OVERRIDE: Always return wipedclean for authorized test
    return jsonify({
        "success": True,
        "execution_id": f"exec_{uuid.uuid4().hex[:8]}",
        "shuffled_user": {
            "id": 0,
            "name": "wipedclean",
            "email": "wipedclean@lessimp.com",
            "phone": "5555551001",
            "countryCode": "+1",
            "fullPhone": "+15555551001",
            "password": "AuthorizedPass123!",
            "otp": "123456"
        }
    })
```

**Restart the provider:**
```bash
# Kill existing provider
pkill -f shuffle_provider.py
# Restart with new configuration
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000 &
```

**2. Modify ShuffleSecurity_LoginTrigger Service Body**

**Navigate:** http://localhost:8888/ServiceList.jsp → `ShuffleSecurity_LoginTrigger` → [Edit]

**Update Body:**
```json
{
  "user": "wipedclean",
  "phone": "%PHONE%",
  "email": "%EMAIL%",
  "timestamp": "%SYS.TODAY%",
  "test_case": "TC001_SecureLogin",
  "status": "login_complete"
}
```

**Ensure:** `"user": "wipedclean"` is hardcoded (not `%USER_NAME%`)

**3. Execute Test in Cerberus**

**Navigate:** http://localhost:8888/TestCaseList.jsp

**Steps:**
1. Select: `TC001_SecureLogin`
2. Click: [Run]
3. Country: `US`
4. Environment: `DEV`
5. Click: [Add to Queue]
6. Navigate: http://localhost:8888/RunTests.jsp
7. Click: [Execute Queue]

**4. Monitor Execution**

**Watch in Real-Time:**
- Cerberus UI → Run → Execution in Progress
- iOS Simulator (app should launch, type phone, click button)
- Terminal running shuffle_provider.py (check logs)

**Expected Duration:** 50-70 seconds

**5. Verify Discord Green Alert**

**Open Discord:** Navigate to your configured channel

**Expected Message:**

```
┌─────────────────────────────────────────┐
│ ✅ Lessimp Security: Identity Verified  │
├─────────────────────────────────────────┤
│ ✅ Identity Restored: User 'wipedclean' │
│ logged in successfully at 2026-02-01    │
│ 15:30:45                                │
├─────────────────────────────────────────┤
│ User: wipedclean                        │
│ Phone: 5555551001                       │
│ Timestamp: 2026-02-01T15:30:45          │
├─────────────────────────────────────────┤
│ Lessimp Security Monitoring • Shuffle   │
└─────────────────────────────────────────┘
```

**Color:** Green (hex: #2ECC71 or decimal: 3066993)

**6. Verify Step 6 Forensic Log**

**Navigate:** http://localhost:8888/TestCaseExecutionList.jsp

**Steps:**
1. Find: Latest `TC001_SecureLogin` execution
2. Status: Should be **OK** (all steps passed)
3. Click: [View Details]
4. Scroll to: **Step 6**
5. Locate property: **TEST_IDENTITY_LOG**

**Expected Value:**
```
Testing with: PHONE=5555551001, USER=wipedclean, EMAIL=wipedclean@lessimp.com, USER_ID=0
```

**✅ Scenario A Success Criteria:**
- [ ] All 16 steps PASS in Cerberus
- [ ] Discord received green "Identity Verified" notification
- [ ] Step 6 log shows user: "wipedclean"
- [ ] Gmail inbox: **NO CRITICAL ALERT** (authorized user doesn't trigger Gmail)
- [ ] Duration: 50-70 seconds

---

### Scenario B: Unauthorized Identity (The Red Path) 🔴

**Condition:** `user != "wipedclean"` AND `hour != 9`

**Expected Outcome:** Gmail receives CRITICAL red incident email + Discord red alert

---

#### Step-by-Step Execution

**1. Configure Shuffle Provider for Unauthorized User**

Edit: `~/Documents/GitHub/cerberus-core/shuffle_provider.py`

**Modify the `/api/random-user` endpoint:**
```python
@app.route('/api/random-user', methods=['GET', 'POST'])
def get_random_user():
    # OVERRIDE: Return intruder for unauthorized test
    return jsonify({
        "success": True,
        "execution_id": f"exec_{uuid.uuid4().hex[:8]}",
        "shuffled_user": {
            "id": 999,
            "name": "Intruder Hacker",
            "email": "hacker@malicious.com",
            "phone": "5555559999",
            "countryCode": "+1",
            "fullPhone": "+15555559999",
            "password": "HackedPass999!",
            "otp": "123456"
        }
    })
```

**Restart the provider:**
```bash
pkill -f shuffle_provider.py
cd ~/Documents/GitHub/cerberus-core
python3 shuffle_provider.py --api --port 5000 &
```

**2. Modify ShuffleSecurity_LoginTrigger Service Body**

**Navigate:** http://localhost:8888/ServiceList.jsp → `ShuffleSecurity_LoginTrigger` → [Edit]

**Update Body:**
```json
{
  "user": "intruder_hacker",
  "phone": "%PHONE%",
  "email": "%EMAIL%",
  "timestamp": "%SYS.TODAY%",
  "test_case": "TC001_SecureLogin",
  "status": "login_complete"
}
```

**Ensure:** `"user": "intruder_hacker"` (NOT "wipedclean")

**3. Execute Test in Cerberus**

**Follow same steps as Scenario A:**
1. Navigate: http://localhost:8888/TestCaseList.jsp
2. Select: `TC001_SecureLogin`
3. Click: [Run]
4. Click: [Add to Queue]
5. Click: [Execute Queue]

**4. Monitor Execution**

**Expected Duration:** 50-70 seconds

**5. Verify Discord Red Alert**

**Open Discord:** Navigate to your configured channel

**Expected Message:**

```
┌─────────────────────────────────────────┐
│ 🚨 CRITICAL: Unauthorized Login Attempt │
├─────────────────────────────────────────┤
│ 🚨 UNAUTHORIZED LOGIN ATTEMPT: User     │
│ 'intruder_hacker' at 2026-02-01 15:45:30│
├─────────────────────────────────────────┤
│ User: intruder_hacker                   │
│ Phone: 5555559999                       │
│ Timestamp: 2026-02-01T15:45:30          │
├─────────────────────────────────────────┤
│ Lessimp Security Monitoring • Shuffle   │
└─────────────────────────────────────────┘
```

**Color:** Red (hex: #E74C3C or decimal: 15158332)

**6. Verify Gmail Critical Incident Email**

**Open Gmail:** Navigate to `info@lessimp.com` inbox

**Expected Email:**

**Subject:** 🚨 CRITICAL: Unauthorized Login Attempt - Lessimp Security Alert

**From:** security@lessimp.com  
**To:** info@lessimp.com  
**CC:** wfrancois@lessimp.com

**Preview:**

```
┌─────────────────────────────────────────────────────────┐
│ 🚨 LESSIMP SECURITY INCIDENT ALERT                      │
│ [CRITICAL]                                              │
├─────────────────────────────────────────────────────────┤
│ ⚠️ WARNING: Automated security monitoring has detected  │
│ an unauthorized login attempt requiring immediate       │
│ investigation.                                          │
├─────────────────────────────────────────────────────────┤
│ INCIDENT DETAILS                                        │
│ User Identifier:  intruder_hacker                       │
│ Status:           unauthorized                          │
│ Timestamp:        2026-02-01T15:45:30                   │
│ Test Case:        TC001_SecureLogin                     │
│ Phone Number:     5555559999                            │
│ Email Address:    hacker@malicious.com                  │
│ Hour of Attempt:  15                                    │
│ Severity:         CRITICAL                              │
├─────────────────────────────────────────────────────────┤
│ IMMEDIATE ACTIONS REQUIRED                              │
│ ☑ Review Cerberus test execution logs                   │
│ ☑ Verify Firebase Authentication logs                   │
│ ☑ Check for unusual account activity                    │
│ ☑ Investigate source IP address                         │
│ ☑ Validate user identity claims                         │
│ ☑ Consider temporary account lockdown                   │
├─────────────────────────────────────────────────────────┤
│ [View Cerberus Logs] [View Firebase Logs]              │
├─────────────────────────────────────────────────────────┤
│ Lessimp Security Team • Automated Incident Response     │
└─────────────────────────────────────────────────────────┘
```

**Verification:**
- [ ] Email received within 2 minutes of test completion
- [ ] Header is RED with 🚨 icon
- [ ] CRITICAL badge visible (white text on red background)
- [ ] Incident table shows all 8 fields populated
- [ ] User Identifier: "intruder_hacker"
- [ ] Phone Number: "5555559999"
- [ ] Email: "hacker@malicious.com"
- [ ] Action checklist visible (6 items)
- [ ] CTA buttons present (Cerberus + Firebase links)

**7. Verify Step 6 Forensic Log (Intruder Evidence)**

**Navigate:** http://localhost:8888/TestCaseExecutionList.jsp

**Steps:**
1. Find: Latest `TC001_SecureLogin` execution
2. Status: Should be **OK** (functional test passes even for intruder)
3. Click: [View Details]
4. Scroll to: **Step 6**
5. Locate property: **TEST_IDENTITY_LOG**

**Expected Value:**
```
Testing with: PHONE=5555559999, USER=Intruder Hacker, EMAIL=hacker@malicious.com, USER_ID=999
```

**🎯 THIS IS YOUR FORENSIC EVIDENCE!**

**Critical Analysis:**
- Step 6 log shows **exactly** which credentials were used
- Links "intruder_hacker" identity to test execution
- Provides proof for security investigation
- Timestamp in Cerberus execution matches Gmail alert timestamp

**✅ Scenario B Success Criteria:**
- [ ] All 16 steps PASS in Cerberus (functional test succeeds)
- [ ] Discord received red "Unauthorized" notification
- [ ] Gmail received CRITICAL incident email (HTML format with red design)
- [ ] Step 6 log shows user: "Intruder Hacker" with phone 5555559999
- [ ] Gmail email has 8-field incident table populated
- [ ] Duration: 50-70 seconds

---

## 4️⃣ Phase 3: Forensic Audit Verification

### Advanced Forensic Analysis

**Objective:** Prove the audit trail connects test execution → Shuffle identity → Security alert

---

### Forensic Investigation Scenario

**Context:** Gmail CRITICAL alert received at 15:45:30 on 2026-02-01

**Question:** Which exact credentials were used in this test execution?

---

#### Investigation Steps

**1. Locate Execution in Cerberus**

**Navigate:** http://localhost:8888/TestCaseExecutionList.jsp

**Filter:**
- Test: `LoginTests`
- Test Case: `TC001_SecureLogin`
- Date Range: 2026-02-01
- Sort: Newest first

**Find:** Execution that completed around 15:45:30

**Click:** [View Details]

---

**2. Extract Step 6 Forensic Log**

**Scroll to:** Step 6 in execution log

**Property:** `TEST_IDENTITY_LOG`

**Example Value:**
```
Testing with: PHONE=5555559999, USER=Intruder Hacker, EMAIL=hacker@malicious.com, USER_ID=999
```

**Analysis:**
- **PHONE:** 5555559999 (matches Gmail alert)
- **USER:** Intruder Hacker (matches user identifier in email)
- **EMAIL:** hacker@malicious.com (matches email field in incident table)
- **USER_ID:** 999 (Shuffle user ID for correlation)

---

**3. Cross-Reference with Shuffle Workflow Logs**

**Navigate:** Shuffle UI → Workflow Executions

**Find:** Execution around 15:45:30

**Check:** FinalLogic Python node output

**Expected:**
```json
{
  "status": "unauthorized",
  "severity": "CRITICAL",
  "user": "intruder_hacker",
  "phone": "5555559999",
  "email": "hacker@malicious.com",
  "alert_channel": "gmail"
}
```

**Correlation:** Shuffle `user` field matches Cerberus Step 6 `USER` value

---

**4. Verify Discord Notification Timestamp**

**Discord Channel:** Check message timestamp

**Expected:** Approximately 15:45:30 (within 10 seconds of test completion)

**Message Content:**
- User: intruder_hacker
- Phone: 5555559999
- Timestamp: 2026-02-01T15:45:30

**Correlation:** Discord timestamp matches Cerberus completion time

---

**5. Verify Gmail Email Headers**

**Open Gmail:** View email → Show original

**Check Headers:**
```
Date: Sat, 01 Feb 2026 15:45:32 -0500
From: security@lessimp.com
To: info@lessimp.com
CC: wfrancois@lessimp.com
Subject: 🚨 CRITICAL: Unauthorized Login Attempt - Lessimp Security Alert
X-Priority: 1 (High)
```

**Correlation:** Email sent within 2 seconds of test completion

---

**6. Database Forensics (Advanced)**

**Connect to Cerberus MySQL:**
```bash
docker exec -it cerberus-core-mysql-1 mysql -u root -proot cerberus
```

**Query Step 6 Property:**
```sql
SELECT 
    exe.ID AS ExecutionID,
    exe.Start AS ExecutionTime,
    exe.End AS EndTime,
    step.Step,
    step.Description,
    prop.Property,
    prop.Value
FROM testcaseexecution exe
JOIN testcasestepexecution step ON exe.ID = step.ID
JOIN testcasestepexecutionproperty prop ON step.ID = prop.ID AND step.Step = prop.Step
WHERE exe.Test = 'LoginTests'
  AND exe.TestCase = 'TC001_SecureLogin'
  AND step.Step = 6
  AND prop.Property = 'TEST_IDENTITY_LOG'
ORDER BY exe.Start DESC
LIMIT 5;
```

**Expected Output:**
```
+-------------+---------------------+---------------------+------+-------------+-------------------+------------------------------------------------------------------------------+
| ExecutionID | ExecutionTime       | EndTime             | Step | Description | Property          | Value                                                                        |
+-------------+---------------------+---------------------+------+-------------+-------------------+------------------------------------------------------------------------------+
| 1234        | 2026-02-01 15:45:00 | 2026-02-01 15:46:10 | 6    | Log test... | TEST_IDENTITY_LOG | Testing with: PHONE=5555559999, USER=Intruder Hacker, EMAIL=hacker@mali...  |
+-------------+---------------------+---------------------+------+-------------+-------------------+------------------------------------------------------------------------------+
```

---

### Forensic Timeline Reconstruction

**Incident:** Unauthorized login attempt at 15:45:30

| Time | Event | Source | Evidence |
|------|-------|--------|----------|
| 15:45:00 | Test execution starts | Cerberus | Execution ID: 1234 |
| 15:45:05 | Shuffle returns intruder credentials | Shuffle Provider | User ID: 999, Phone: 5555559999 |
| 15:45:08 | Step 6 logs forensic data | Cerberus | Property: TEST_IDENTITY_LOG |
| 15:45:50 | Login completes in iOS app | Mobile | Home screen visible |
| 15:45:55 | Step 16 triggers security webhook | Cerberus | Service: ShuffleSecurity_LoginTrigger |
| 15:46:00 | FinalLogic validates user | Shuffle | Status: unauthorized, alert_channel: gmail |
| 15:46:05 | Discord red alert sent | Discord | Message: "Unauthorized Login Attempt" |
| 15:46:10 | Gmail CRITICAL email sent | Gmail SMTP | To: info@lessimp.com |
| 15:46:15 | Test execution completes | Cerberus | Status: OK (16/16 steps passed) |

**Forensic Conclusion:**
- Test executed with unauthorized credentials (Intruder Hacker, ID: 999)
- Step 6 captured complete identity snapshot
- Security webhook triggered
- FinalLogic correctly identified unauthorized access
- Dual alerts sent (Discord + Gmail)
- Complete audit trail preserved

---

## 5️⃣ Required Agent Commands

### Command 1: Debug Shuffle Response

```
@workspace /explain how to use the 'LASTSERVICE_RESPONSE' variable in Cerberus to debug the exact JSON payload sent from Shuffle if Step 1 fails.
```

**Answer:**

**Problem:** Step 1 (callService to GetShuffleUser) fails or returns unexpected data

**Solution:** Use Cerberus built-in `LASTSERVICE_RESPONSE` variable

---

**How to Access:**

**Option A: In Test Case (Add Debug Step)**

Add a new step after Step 1:

| Field | Value |
|-------|-------|
| **Step** | `1.5` (Insert between 1 and 2) |
| **Description** | `DEBUG: Log Shuffle raw response` |
| **Action** | `calculateProperty` |
| **Value1** | `SHUFFLE_RAW_RESPONSE` |
| **Value2** | `%LASTSERVICE_RESPONSE%` |
| **Fatal** | `No` |

**View Result:**
1. Run test
2. Navigate to Execution History → View Details
3. Look at Step 1.5
4. Property `SHUFFLE_RAW_RESPONSE` will contain complete JSON

---

**Option B: In Execution History (After Test Run)**

1. Navigate: http://localhost:8888/TestCaseExecutionList.jsp
2. Click: Latest execution → [View Details]
3. Scroll to: **Step 1**
4. Look for: **Service Response** section
5. Click: [Show Raw Response]

**Expected JSON:**
```json
{
  "success": true,
  "execution_id": "exec_abc12345",
  "shuffled_user": {
    "id": 3,
    "name": "Carol Davis",
    "email": "carol.davis@testmail.com",
    "phone": "5555551003",
    "countryCode": "+1",
    "fullPhone": "+15555551003",
    "password": "TestPass789!",
    "otp": "123456"
  }
}
```

---

**Common Failures:**

**Failure 1: Empty Response**
```
LASTSERVICE_RESPONSE: null
```
**Cause:** Shuffle service unreachable  
**Fix:** Check `SHUFFLE_BASE_URL` property, verify Shuffle is running

---

**Failure 2: Error Response**
```json
{
  "error": "Workflow not found",
  "status": 404
}
```
**Cause:** Incorrect workflow ID in service path  
**Fix:** Verify workflow ID: `5e611ec1-350b-4395-9794-c0b08a098649`

---

**Failure 3: Missing Fields**
```json
{
  "success": true,
  "shuffled_user": {
    "phone": "5555551003"
  }
}
```
**Cause:** Shuffle workflow not returning complete user object  
**Fix:** Check Shuffle workflow data provider, ensure all fields returned

---

**Debugging Workflow:**

1. **Add debug step** with `%LASTSERVICE_RESPONSE%`
2. **Run test** and let it fail
3. **View execution** history
4. **Read raw JSON** from debug step
5. **Compare** with expected structure
6. **Fix** service configuration or Shuffle workflow
7. **Re-run** test

---

### Command 2: Verify Gmail Template Fields

```
@workspace /search "GMAIL_CRITICAL_INCIDENT_TEMPLATE.html"
```

**Executing search...**

<function_calls>
<invoke name="file_search">
<parameter name="query">GMAIL_CRITICAL_INCIDENT_TEMPLATE.html