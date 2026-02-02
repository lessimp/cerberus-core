# 🛡️ Security Incident Response Playbook: "Critical Alert" Protocol

**Version:** 2.0  
**Date:** February 1, 2026  
**Status:** ✅ OPERATIONAL - Ready for Immediate Use  
**Scope:** Gmail CRITICAL Alert Response & Forensic Investigation  
**Owner:** Security Operations Team

---

## 📋 Executive Summary

This playbook provides a **standardized 5-phase response protocol** for handling **Gmail CRITICAL security alerts** triggered by the Lessimp-Secure automated detection system. It establishes clear procedures for:

- **Immediate triage** and alert validation
- **Forensic investigation** using Cerberus Step 6 audit logs
- **Containment** of compromised accounts
- **Eradication** and credential reset procedures
- **Post-incident** documentation and playbook refinement

**Primary Use Case:** When a Gmail alert with subject "🚨 CRITICAL: Unauthorized Login Attempt" arrives at `info@lessimp.com`

---

## 🎯 Quick Reference Card

**When Alert Arrives:**
1. ⏱️ **0-5 min:** Immediate Triage → Verify 8 fields, determine severity
2. 🔍 **5-20 min:** Forensic Investigation → Step 6 logs, Shuffle workflow, Firebase
3. 🔒 **20-40 min:** Containment → Isolate account, revoke tokens
4. 🧹 **40-60 min:** Eradication → Reset credentials, restore operations
5. 📝 **1-7 days:** Post-Incident → Document findings, update playbook

**Success Metrics:**
- Mean Time to Acknowledge (MTTA): **< 5 minutes**
- Mean Time to Investigate (MTTI): **< 20 minutes**
- Mean Time to Resolve (MTTR): **< 60 minutes**

---

## 📧 Phase 1: Immediate Triage & Validation (0-5 minutes)

### 1.1 Alert Arrival Confirmation

**Trigger:** Gmail notification received at `info@lessimp.com` (To) and `wfrancois@lessimp.com` (CC)

**Subject Line Format:**
```
🚨 CRITICAL: Unauthorized Login Attempt - [USERNAME]
```

**Expected Body:** Professional HTML template with:
- Red gradient header
- CRITICAL severity badge
- 8-field incident details table
- 6-item investigation checklist
- CTA buttons: "View Cerberus Logs", "View Firebase Logs"

---

### 1.2 Verify Source Authenticity

**Purpose:** Confirm the alert is legitimate and not a phishing attempt or false positive

**Verification Steps:**

1. **Check Email Headers:**
   ```
   From: security@lessimp.com
   Reply-To: info@lessimp.com
   X-Mailer: Shuffle Workflow Automation
   ```

2. **Validate 8 Dynamic Fields:**
   
   | # | Field Name | Variable Source | Expected Format |
   |---|------------|-----------------|-----------------|
   | 1 | User Identifier | `$finallogic.user` | String (e.g., "intruder_hacker") |
   | 2 | Status | `$finallogic.status` | "unauthorized" |
   | 3 | Timestamp | `$finallogic.timestamp` | ISO 8601 (e.g., "2026-02-01T15:45:30") |
   | 4 | Test Case | `$exec.text.test_case` | "TC001_SecureLogin" |
   | 5 | Phone Number | `$exec.text.phone` | 10 digits (e.g., "5555559999") |
   | 6 | Email Address | `$exec.text.email` | Valid email format |
   | 7 | Hour of Attempt | `$finallogic.hour` | Integer 0-23 |
   | 8 | Severity | `$finallogic.severity` | "CRITICAL" |

3. **Cross-Reference Discord Alert:**
   - Navigate to Discord security channel
   - Verify matching RED notification with same timestamp
   - Confirm user identifier matches Gmail alert

**Red Flags (Potential False Positive or Phishing):**
- ❌ Missing any of the 8 required fields
- ❌ Timestamp format incorrect (not ISO 8601)
- ❌ No matching Discord notification
- ❌ Email from unexpected domain
- ❌ Severity field not "CRITICAL"

---

### 1.3 Determine Severity Level

**Based on FinalLogic Evaluation:**

The alert was triggered because:
```python
if username == "wipedclean" or current_hour == 9:
    # Authorized path - Discord GREEN only
else:
    # Unauthorized path - Gmail CRITICAL + Discord RED
```

**If you receive a Gmail CRITICAL alert, it means:**
- ✅ Username is NOT "wipedclean" (unauthorized user)
- ✅ Hour is NOT 9 (outside business hours window)
- ✅ Both conditions FALSE → CRITICAL severity confirmed

**Severity Classification:**

| Level | Criteria | Response Time |
|-------|----------|---------------|
| **🔴 CRITICAL** | Unknown user + Off-hours (not 9 AM) | **Immediate (< 5 min)** |
| 🟠 HIGH | Known test user + Off-hours | Within 30 min |
| 🟡 MEDIUM | Unknown user + 9 AM (business hours) | Within 1 hour |
| 🟢 LOW | Known test user + 9 AM | Document only |

**Note:** All Gmail alerts are classified as **CRITICAL** by default since they only trigger when unauthorized conditions are met.

---

### 1.4 Initial Response Actions

**Immediate Steps (First 5 Minutes):**

1. **Acknowledge Alert:**
   ```
   Subject: RE: 🚨 CRITICAL: Unauthorized Login Attempt - [USERNAME]
   Body: Alert acknowledged by [YOUR NAME] at [CURRENT TIME].
         Beginning investigation per Security Incident Response Playbook.
         Status: INVESTIGATING
   ```

2. **Record Incident Details:**
   
   Create incident tracking entry:
   ```
   Incident ID: SEC-2026-02-01-001
   Date/Time: [TIMESTAMP from alert]
   User Identifier: [USERNAME from alert]
   Phone Number: [PHONE from alert]
   Email Address: [EMAIL from alert]
   Hour of Attempt: [HOUR from alert]
   Test Case: [TEST_CASE from alert]
   Acknowledged By: [YOUR NAME]
   Status: INVESTIGATING
   ```

3. **Notify Team (if needed):**
   - For CRITICAL severity: Alert security lead immediately
   - For HIGH severity: Send Slack/Discord notification to security channel
   - For MEDIUM/LOW: Continue investigation, notify in daily standup

---

## 🔍 Phase 2: Forensic Investigation (Chain of Custody) (5-20 minutes)

### 2.1 Access Cerberus Execution History

**Objective:** Locate the exact test execution that triggered the alert and retrieve Step 6 forensic logs

**Navigation Path:**
1. Open browser: `http://localhost:8888/TestCaseExecutionList.jsp`
2. Filter criteria:
   - **Test:** "LoginTests" (or leave blank to see all)
   - **Test Case:** "TC001_SecureLogin"
   - **Start Date:** [Date from alert timestamp]
   - **End Date:** [Date from alert timestamp]

3. **Locate Matching Execution:**
   - Look for execution with timestamp matching alert (±5 minutes)
   - Verify test case name: "TC001_SecureLogin"
   - Check execution status: Could be PASS, FAIL, or WARNING

4. **Click Execution ID** to view detailed logs

---

### 2.2 Verify Step 6: TEST_IDENTITY_LOG Property

**Critical Forensic Evidence:**

Step 6 in TC001_SecureLogin uses `calculateProperty` to create an audit trail:

**Property Name:** `TEST_IDENTITY_LOG`

**Property Value Format:**
```
Testing with: PHONE=%PHONE%, USER=%USER_NAME%, EMAIL=%EMAIL%, USER_ID=%USER_ID%
```

**Investigation Steps:**

1. **Navigate to Step 6** in execution log
2. **Locate Property Section** (usually under "Properties" or "Variables" tab)
3. **Find TEST_IDENTITY_LOG** entry
4. **Extract Values:**
   ```
   Phone: [VALUE]
   User: [VALUE]
   Email: [VALUE]
   User ID: [VALUE]
   ```

5. **Cross-Reference with Gmail Alert:**
   
   | Data Point | Step 6 Value | Gmail Alert Value | Match? |
   |------------|--------------|-------------------|--------|
   | Phone Number | PHONE=%PHONE% | $exec.text.phone | ✅ / ❌ |
   | User Name | USER=%USER_NAME% | $finallogic.user | ✅ / ❌ |
   | Email Address | EMAIL=%EMAIL% | $exec.text.email | ✅ / ❌ |

**Expected Result:** All values should match perfectly. This confirms the Gmail alert corresponds to this specific Cerberus execution.

**Red Flags:**
- ❌ Step 6 property missing or empty
- ❌ Values don't match Gmail alert
- ❌ Property format incorrect
- ❌ Execution not found for alert timestamp

---

### 2.3 Check Shuffle Workflow Execution Logs

**Objective:** Verify FinalLogic node output and confirm alert routing logic

**Access Shuffle UI:**
1. Navigate: `http://localhost:3001/workflows`
2. Find workflow: "ShuffleSecurity_LoginTrigger" or similar name
3. Filter by date: Match alert timestamp
4. Click latest execution

**Key Information to Extract:**

1. **Webhook Trigger Node Output:**
   ```json
   {
     "user": "intruder_hacker",
     "phone": "5555559999",
     "email": "hacker@malicious.com",
     "test_case": "TC001_SecureLogin"
   }
   ```

2. **FinalLogic Python Node Output:**
   ```json
   {
     "status": "unauthorized",
     "severity": "CRITICAL",
     "user": "intruder_hacker",
     "phone": "5555559999",
     "email": "hacker@malicious.com",
     "timestamp": "2026-02-01T15:45:30",
     "hour": 15,
     "alert_channel": "gmail",
     "color": 15158332,
     "message": "🚨 UNAUTHORIZED LOGIN ATTEMPT: User 'intruder_hacker'"
   }
   ```

3. **Decision Logic Verification:**
   
   FinalLogic should show:
   ```python
   # Evaluation:
   username = "intruder_hacker"  # From webhook
   current_hour = 15             # Server time (3 PM)
   
   # Logic:
   if username == "wipedclean" or current_hour == 9:
       # False or False = False
   else:
       # This path executed → Gmail CRITICAL
       alert_channel = "gmail"
   ```

4. **Gmail SMTP Node Execution:**
   - Verify node executed (status: success)
   - Check recipient: info@lessimp.com
   - Verify CC: wfrancois@lessimp.com
   - Confirm body type: HTML (not plain text)

5. **Discord Node Execution:**
   - Verify red embed sent (color: 15158332)
   - Check webhook URL executed
   - Confirm severity: CRITICAL

**Red Flags:**
- ❌ FinalLogic output shows `alert_channel: "discord"` (should be "gmail" for CRITICAL)
- ❌ Gmail node didn't execute or failed
- ❌ Workflow execution not found for timestamp
- ❌ Python evaluation error in FinalLogic node

---

### 2.4 Correlate with Firebase Authentication Logs

**Objective:** Determine if the login attempt reached Firebase (actual authentication attempt) or failed earlier in the flow

**Access Firebase Console:**
1. Navigate: `https://console.firebase.google.com/`
2. Select project: "Lessimp Dating" (or your project name)
3. Go to: **Authentication → Users**

**Investigation Steps:**

1. **Search for User by Phone Number:**
   - Enter phone from Gmail alert: `+1+[PHONE]` (e.g., +1+5555559999)
   - Check if user exists in Firebase

2. **If User Exists:**
   ```
   User Found: [UID]
   Email: [EMAIL from alert]
   Phone: [PHONE from alert]
   Last Sign-In: [TIMESTAMP]
   Created: [DATE]
   ```
   
   **Compare Timestamps:**
   - Alert timestamp: `2026-02-01T15:45:30`
   - Firebase last sign-in: Should be within ±2 minutes
   
   **Implications:**
   - ✅ **Timestamps match:** User successfully authenticated (HIGH severity - breach confirmed)
   - ❌ **No recent sign-in:** Authentication failed, but attempt was made (MEDIUM severity)

3. **If User Does NOT Exist:**
   ```
   User Not Found in Firebase
   ```
   
   **Implications:**
   - This was a test attempt with synthetic credentials
   - Authentication never reached Firebase (stopped at OTP verification or earlier)
   - **Severity: LOW** (test artifact, not a real breach)

4. **Check Sign-In Method:**
   - Verify: Phone authentication enabled
   - Check: Any unusual sign-in patterns (multiple failed attempts, different IPs)

**Red Flags:**
- ❌ User exists with recent sign-in matching alert → **Real breach, escalate immediately**
- ❌ Multiple failed authentication attempts in short timeframe → **Brute force attack**
- ❌ Sign-in from unusual IP or location → **Compromised credentials**

---

### 2.5 Forensic Timeline Reconstruction

**Create Complete Timeline:**

| Time | Event | Source | Details |
|------|-------|--------|---------|
| [T-0] | Test Execution Started | Cerberus | TC001_SecureLogin triggered |
| [T+10s] | Step 6 Audit Log Created | Cerberus | TEST_IDENTITY_LOG property set |
| [T+45s] | Authentication Attempt | Firebase | Phone: [PHONE], Result: [SUCCESS/FAIL] |
| [T+50s] | Step 16 Webhook Triggered | Cerberus | POST to Shuffle webhook_a76354e0... |
| [T+52s] | FinalLogic Evaluation | Shuffle | username != "wipedclean", hour != 9 → CRITICAL |
| [T+55s] | Gmail Alert Sent | Shuffle | HTML email to info@lessimp.com |
| [T+56s] | Discord Alert Sent | Shuffle | Red embed in security channel |
| [T+60s] | Alert Acknowledged | Response Team | Investigation begins |

**Key Questions to Answer:**

1. **Did authentication succeed?** (Check Firebase last sign-in)
2. **Was this a test or production attempt?** (Check username pattern)
3. **What time did it occur?** (Verify hour != 9 for CRITICAL classification)
4. **Were there multiple attempts?** (Check Cerberus for repeated executions)
5. **Any suspicious patterns?** (IP address, location, frequency)

---

## 🔒 Phase 3: Containment & Mitigation (20-40 minutes)

### 3.1 Determine Containment Strategy

**Based on Investigation Findings:**

| Scenario | Firebase User? | Last Sign-In Match? | Action Required |
|----------|----------------|---------------------|-----------------|
| **A** | ❌ No user | N/A | **LOW:** Document only, no containment |
| **B** | ✅ Yes | ❌ No recent sign-in | **MEDIUM:** Monitor, prepare for escalation |
| **C** | ✅ Yes | ✅ Sign-in matches alert | **CRITICAL:** Immediate containment |

---

### 3.2 Scenario A: Test Artifact (LOW Severity)

**Criteria:**
- User not found in Firebase
- Username pattern indicates test: "intruder_*", "hacker_*", "test_*"
- No actual authentication occurred

**Containment Actions:**
```
✅ No immediate containment required
✅ Document incident for trend analysis
✅ Verify test was intentional (check with QA team)
✅ Update test schedule if needed
```

**Next Steps:**
- Skip to Phase 5 (Post-Incident Activity)
- Document in tracking spreadsheet
- No escalation needed

---

### 3.3 Scenario B: Failed Authentication (MEDIUM Severity)

**Criteria:**
- User exists in Firebase
- Last sign-in does NOT match alert timestamp
- Authentication attempt failed

**Containment Actions:**

1. **Verify Account Status:**
   ```
   Firebase Console → Authentication → [USER]
   Check: Disabled? Email verified? Recent activity?
   ```

2. **Review Recent Sign-In History:**
   - Check past 7 days for unusual patterns
   - Look for multiple failed attempts
   - Verify last successful sign-in was legitimate

3. **Enable Enhanced Monitoring:**
   ```
   Action: Flag account for 24-hour monitoring
   Alert if: Any successful sign-in
   Alert if: >3 failed attempts in 1 hour
   ```

4. **Notify Account Owner (if applicable):**
   ```
   Subject: Security Alert - Unusual Sign-In Attempt
   Body: We detected a failed sign-in attempt to your account.
         Phone: [PHONE]
         Time: [TIMESTAMP]
         If this wasn't you, please reset your password immediately.
   ```

**Next Steps:**
- Continue to Phase 4 (Eradication & Recovery)
- Document in incident report
- Monitor for 24 hours

---

### 3.4 Scenario C: Confirmed Breach (CRITICAL Severity)

**Criteria:**
- User exists in Firebase
- Last sign-in MATCHES alert timestamp (±2 minutes)
- Authentication was successful

**IMMEDIATE CONTAINMENT (< 5 minutes):**

1. **Isolate Account:**
   ```
   Firebase Console → Authentication → [USER]
   Click: [⋮] Menu → "Disable user account"
   Reason: "Security incident - unauthorized access detected"
   ```

2. **Revoke All Active Sessions:**
   ```
   Firebase Console → Authentication → [USER]
   Click: "Force sign-out from all devices"
   Verify: All refresh tokens invalidated
   ```

3. **Document Evidence (CRITICAL - Do NOT modify/delete):**
   ```
   Screenshot: Firebase user profile
   Screenshot: Last sign-in timestamp
   Screenshot: Cerberus Step 6 logs
   Screenshot: Shuffle FinalLogic output
   Screenshot: Gmail alert email
   Export: Firebase audit logs (past 7 days)
   Export: Cerberus execution logs (full)
   Export: Shuffle workflow execution JSON
   ```

4. **Enable Enhanced Logging:**
   ```
   Firebase: Turn on detailed audit logging
   Cerberus: Enable DEBUG mode for TC001_SecureLogin
   Shuffle: Enable verbose logging for security workflow
   ```

5. **Revoke API Access (if applicable):**
   ```
   Firebase Console → Project Settings → Service Accounts
   Check: Any API keys or service accounts associated with compromised user
   Action: Revoke or rotate credentials immediately
   ```

**IMMEDIATE ESCALATION:**

| Role | Contact | Notification Time | Method |
|------|---------|-------------------|--------|
| **Security Lead** | info@lessimp.com | **< 5 min** | Phone + Email |
| **CTO** | wfrancois@lessimp.com | **< 10 min** | Phone + Email |
| **CISO** | [Add contact] | **< 15 min** | Phone |
| **Legal/Compliance** | [Add contact] | **< 30 min** | Email |

**Escalation Email Template:**
```
Subject: 🚨 CRITICAL: Confirmed Security Breach - Immediate Action Required

Priority: CRITICAL
Incident ID: SEC-2026-02-01-001
Time of Breach: [TIMESTAMP]

SUMMARY:
Unauthorized user "[USERNAME]" successfully authenticated using:
- Phone: [PHONE]
- Email: [EMAIL]
- Time: [TIMESTAMP]

ACTIONS TAKEN:
✅ Account disabled in Firebase
✅ All sessions revoked
✅ Evidence preserved (screenshots + logs)
✅ Enhanced logging enabled

NEXT STEPS REQUIRED:
1. Legal review for data breach notification requirements
2. PR/Communications strategy (if customer data accessed)
3. Forensic analysis of account activity (data exfiltration?)
4. Security architecture review to prevent recurrence

CONTACT:
[YOUR NAME]
[YOUR PHONE]
[YOUR EMAIL]

Full incident report in progress. ETA: 2 hours.
```

---

### 3.5 Additional Containment Measures (CRITICAL Scenarios)

**If Breach Confirmed, Also Check:**

1. **Lateral Movement:**
   ```
   Question: Did attacker access other accounts from this compromised account?
   Check: Firebase logs for any account linking, data exports, API calls
   Look for: Unusual read patterns, bulk data access, admin actions
   ```

2. **Data Exfiltration:**
   ```
   Question: What data did the attacker access?
   Check: Firebase logs for:
         - User profile reads
         - Match/swipe history access
         - Chat message access
         - Payment information views
   Export: All accessed data for forensic analysis
   ```

3. **Persistent Access:**
   ```
   Question: Did attacker create backdoor accounts or API keys?
   Check: Firebase for newly created accounts in past 24 hours
   Check: Service accounts for unauthorized API keys
   Check: Cloud Functions for unauthorized code deployments
   ```

4. **Network Indicators:**
   ```
   Question: What IP address did the attack originate from?
   Check: Firebase authentication logs for source IP
   Action: Block IP at firewall/load balancer level
   Action: Check IP reputation (TOR exit node? Known attacker?)
   ```

---

## 🧹 Phase 4: Eradication & Recovery (40-60 minutes)

### 4.1 Reset Compromised Credentials

**For Confirmed Breaches (Scenario C):**

1. **Force Password Reset:**
   ```
   Firebase Console → Authentication → [USER]
   Action: Send password reset email (if email verified)
   Alternative: Delete user account and require re-registration
   ```

2. **Reset Phone Number:**
   ```
   If phone number was compromised:
   Action: Require phone number re-verification
   Action: Clear existing phone number from account
   Note: User must re-authenticate with valid phone + OTP
   ```

3. **Invalidate All Tokens:**
   ```
   Firebase: All refresh tokens already revoked in containment phase
   Backend: Clear any cached authentication tokens
   Mobile App: Force sign-out on next app launch
   ```

4. **Update Firebase Security Rules:**
   ```
   If vulnerability discovered in rules:
   Action: Update Firestore/Realtime DB security rules
   Action: Test new rules in emulator
   Action: Deploy to production
   Action: Verify with security scan
   ```

---

### 4.2 Restore Account to Known Good State

**Decision Matrix:**

| Breach Severity | Firebase User | Recommended Action |
|-----------------|---------------|--------------------|
| LOW (Test) | Does not exist | No action needed |
| MEDIUM (Failed auth) | Exists, no breach | Enable, add to watchlist |
| HIGH (Suspicious activity) | Exists, unclear breach | Reset credentials, notify user |
| CRITICAL (Confirmed breach) | Exists, breach confirmed | **Delete account or full reset** |

**For CRITICAL Scenarios:**

**Option 1: Delete Account (Recommended for test accounts)**
```
Firebase Console → Authentication → [USER]
Click: [⋮] Menu → "Delete user account"
Confirm: Yes, delete permanently
Result: User must re-register from scratch
```

**Option 2: Full Reset (For production user accounts)**
```
Steps:
1. Keep Firebase UID (for audit trail)
2. Clear all user data:
   - Profile information
   - Match history
   - Chat messages (if policy allows)
   - Payment methods
3. Force password reset
4. Force phone number re-verification
5. Require email re-verification
6. Re-enable account with monitoring
7. Notify user of security incident
```

---

### 4.3 Verify System Integrity

**Post-Remediation Checks:**

1. **Test Authentication Flow:**
   ```
   Action: Run TC001_SecureLogin with known-good test account
   Expected: Should pass all 16 steps
   Expected: Should trigger Discord GREEN notification (if wipedclean)
   Expected: Should NOT trigger Gmail CRITICAL (if authorized)
   ```

2. **Verify Forensic Logging:**
   ```
   Check: Step 6 TEST_IDENTITY_LOG still functioning
   Check: Shuffle workflow still triggering
   Check: Gmail/Discord alerts still routing correctly
   ```

3. **Confirm Containment Effectiveness:**
   ```
   If account disabled: Verify cannot sign in
   If IP blocked: Verify cannot access from that IP
   If tokens revoked: Verify old sessions don't work
   ```

4. **Security Rule Validation:**
   ```
   If rules updated: Run security test suite
   If rules updated: Verify no authorized users affected
   If rules updated: Document changes in change log
   ```

---

### 4.4 Communication & Notification

**Internal Communication:**

1. **Security Team Update:**
   ```
   Channel: Security Slack/Discord
   Message: Incident SEC-2026-02-01-001 resolved.
            Account [PHONE] disabled and reset.
            All sessions revoked. Monitoring continues for 7 days.
   ```

2. **Engineering Team Briefing:**
   ```
   Share: Incident summary (sanitized)
   Focus: What went right (detection worked!)
          What needs improvement (if any gaps found)
   ```

**External Communication (If Applicable):**

3. **User Notification (for production accounts):**
   ```
   Subject: Important Security Notice - Your Account
   
   Dear [USER],
   
   We detected unusual activity on your Lessimp account on [DATE].
   As a precautionary measure, we have:
   - Temporarily disabled your account
   - Signed you out of all devices
   - Required a password reset
   
   To restore access:
   1. Click the password reset link below
   2. Verify your phone number
   3. Set a new secure password
   
   If you did not attempt to sign in at [TIME] from [LOCATION],
   please contact our security team immediately.
   
   Best regards,
   Lessimp Security Team
   ```

4. **Regulatory Notification (If Required):**
   ```
   Check: GDPR breach notification requirements (EU users)
   Check: CCPA breach notification requirements (CA users)
   Check: State-specific data breach laws
   Timeline: Most laws require notification within 72 hours
   ```

---

## 📝 Phase 5: Post-Incident Activity (1-7 days)

### 5.1 Complete Incident Report

**Required Sections:**

```markdown
# Security Incident Report: SEC-2026-02-01-001

## 1. Executive Summary
- **Incident ID:** SEC-2026-02-01-001
- **Date/Time:** 2026-02-01 15:45:30 UTC
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Status:** RESOLVED / ONGOING / MONITORING
- **Reporter:** [YOUR NAME]
- **Investigator:** [NAME]
- **Reviewed By:** [SECURITY LEAD NAME]

## 2. Incident Details
- **Alert Source:** Gmail CRITICAL Incident Email
- **Trigger:** Shuffle Workflow (FinalLogic evaluation)
- **User Identifier:** [USERNAME]
- **Phone Number:** [PHONE]
- **Email Address:** [EMAIL]
- **Timestamp:** [ISO 8601]
- **Hour of Attempt:** [0-23]

## 3. Forensic Evidence
### 3.1 Cerberus Execution Logs
- **Execution ID:** [ID]
- **Test Case:** TC001_SecureLogin
- **Step 6 Property (TEST_IDENTITY_LOG):**
  ```
  Testing with: PHONE=[PHONE], USER=[USER], EMAIL=[EMAIL], USER_ID=[ID]
  ```
- **Step 16 Webhook:** Triggered successfully at [TIMESTAMP]

### 3.2 Shuffle Workflow Logs
- **Workflow:** ShuffleSecurity_LoginTrigger
- **Execution ID:** [ID]
- **FinalLogic Output:**
  ```json
  {
    "status": "unauthorized",
    "severity": "CRITICAL",
    "alert_channel": "gmail",
    "hour": 15
  }
  ```

### 3.3 Firebase Authentication Logs
- **User Found:** YES / NO
- **UID:** [UID] (if exists)
- **Last Sign-In:** [TIMESTAMP]
- **Sign-In Match:** YES / NO
- **Result:** Breach confirmed / Failed authentication / Test artifact

## 4. Impact Assessment
- **Accounts Affected:** [NUMBER]
- **Data Accessed:** [DESCRIPTION]
- **Monetary Impact:** $[AMOUNT] (if applicable)
- **Reputation Impact:** LOW / MEDIUM / HIGH
- **Regulatory Impact:** None / GDPR notification / CCPA notification

## 5. Response Actions Taken
### 5.1 Containment (20 minutes)
- ✅ Account disabled in Firebase at [TIME]
- ✅ All sessions revoked at [TIME]
- ✅ Evidence preserved (screenshots + logs)
- ✅ Enhanced logging enabled

### 5.2 Eradication (30 minutes)
- ✅ Credentials reset at [TIME]
- ✅ Phone number re-verification required
- ✅ All tokens invalidated
- ✅ Security rules updated (if applicable)

### 5.3 Recovery (10 minutes)
- ✅ Account restored to known good state
- ✅ User notified of security incident
- ✅ Monitoring enabled for 7 days

## 6. Root Cause Analysis
### Primary Cause:
[Describe root cause - e.g., "Test user credentials used in production environment"]

### Contributing Factors:
- Factor 1: [Description]
- Factor 2: [Description]

### How Did It Happen?
[Detailed explanation of how the incident occurred]

## 7. Preventive Measures
### Immediate (0-7 days):
- [ ] Update test data management policy
- [ ] Enhance FinalLogic with additional validation
- [ ] Implement IP whitelisting for test environments

### Short-Term (1-4 weeks):
- [ ] Add geolocation checks to FinalLogic
- [ ] Implement rate limiting on authentication
- [ ] Deploy MFA for all production accounts

### Long-Term (1-3 months):
- [ ] Security architecture review
- [ ] Penetration testing engagement
- [ ] Staff security training program

## 8. Lessons Learned
### What Went Well:
- ✅ Automated detection system worked perfectly
- ✅ Gmail alert delivered within 10 seconds
- ✅ Forensic logging provided complete audit trail
- ✅ Response time within SLA (MTTR < 60 min)

### What Could Be Improved:
- ❌ [Improvement 1]
- ❌ [Improvement 2]

### Action Items:
1. [ ] Update incident response playbook with [specific improvement]
2. [ ] Add [new detection rule] to FinalLogic
3. [ ] Schedule security team training on [topic]

## 9. Timeline (Complete Chronology)
| Time | Event | Actor |
|------|-------|-------|
| 15:45:30 | Test execution started | Cerberus |
| 15:45:40 | Step 6 audit log created | Cerberus |
| 15:46:15 | Authentication attempted | User |
| 15:46:20 | Step 16 webhook triggered | Cerberus |
| 15:46:22 | FinalLogic evaluated CRITICAL | Shuffle |
| 15:46:25 | Gmail alert sent | Shuffle |
| 15:46:26 | Discord red alert sent | Shuffle |
| 15:48:00 | Alert acknowledged | [YOUR NAME] |
| 15:55:00 | Investigation complete | [YOUR NAME] |
| 16:05:00 | Account disabled | [YOUR NAME] |
| 16:15:00 | Credentials reset | [YOUR NAME] |
| 16:25:00 | Incident resolved | [YOUR NAME] |

## 10. Attachments
- Screenshot: Gmail alert email
- Screenshot: Discord red notification
- Screenshot: Cerberus Step 6 logs
- Screenshot: Shuffle FinalLogic output
- Screenshot: Firebase user profile
- Export: Cerberus execution logs (JSON)
- Export: Shuffle workflow execution (JSON)
- Export: Firebase audit logs (CSV)

## 11. Approval & Sign-Off
- **Investigator:** [NAME], [SIGNATURE], [DATE]
- **Reviewed By:** [SECURITY LEAD], [SIGNATURE], [DATE]
- **Approved By:** [CISO/CTO], [SIGNATURE], [DATE]
```

---

### 5.2 Trend Analysis & Pattern Recognition

**Monthly Security Review:**

Create a tracking spreadsheet to identify trends:

| Incident ID | Date | Time | User | Phone | Severity | Response Time | Outcome | False Positive? |
|-------------|------|------|------|-------|----------|---------------|---------|-----------------|
| SEC-001 | 2026-02-01 | 15:45 | intruder | 5559999 | CRITICAL | 20 min | Resolved | No |
| SEC-002 | 2026-02-03 | 14:30 | test_user | 5558888 | MEDIUM | 15 min | Documented | Yes |
| SEC-003 | 2026-02-05 | 09:15 | hacker | 5557777 | LOW | 5 min | Ignored | Yes (9 AM) |

**Key Metrics to Track:**

1. **Alert Volume:**
   - Total alerts per week/month
   - Peak alert times (hour of day)
   - Day of week patterns

2. **Response Metrics:**
   - Mean Time to Acknowledge (MTTA)
   - Mean Time to Investigate (MTTI)
   - Mean Time to Resolve (MTTR)
   - % of incidents meeting SLA

3. **Accuracy Metrics:**
   - False positive rate (%)
   - True positive rate (%)
   - Incidents escalated to CRITICAL
   - User accounts affected

4. **Prevention Effectiveness:**
   - Repeat incidents (same user/phone)
   - New attack vectors discovered
   - Preventive measures effectiveness

**Quarterly Review Actions:**

- If false positive rate > 20%: Tune FinalLogic detection logic
- If response time increasing: Review team capacity/training
- If new attack patterns: Update incident playbook
- If prevention gaps: Implement additional security controls

---

### 5.3 Update Security Operations Playbook

**Continuous Improvement Process:**

1. **After Each Incident:**
   ```
   Action: Review incident report for lessons learned
   Question: What would make this faster/easier next time?
   Update: Playbook sections that were unclear or missing
   ```

2. **Playbook Versioning:**
   ```
   Version 1.0 → 1.1 (minor updates)
   - Added clarification to Step 6 investigation
   - Updated Firebase navigation instructions
   
   Version 1.1 → 2.0 (major updates)
   - New phase added: Advanced forensics
   - Complete restructure of containment procedures
   ```

3. **Change Log (Track All Updates):**
   ```
   Date       | Version | Change Description                | Updated By
   -----------|---------|-----------------------------------|------------
   2026-02-01 | 1.0     | Initial playbook creation         | Security Team
   2026-02-15 | 1.1     | Added Firebase geolocation check  | [NAME]
   2026-03-01 | 2.0     | Restructured containment phase    | [NAME]
   ```

4. **Team Training on Updates:**
   ```
   When: After each major version update
   Who: All security team members + on-call engineers
   How: 30-minute walkthrough of changes
   Test: Simulated incident drill using new procedures
   ```

---

### 5.4 Schedule Security Drills & Tabletop Exercises

**Quarterly Security Drills:**

**Scenario-Based Training:**
```
Scenario 1: "The 3 AM Breach"
- Time: 3:00 AM on a weekend
- Alert: Gmail CRITICAL for unknown user
- Twist: Firebase shows successful authentication
- Goal: Practice immediate containment under pressure

Scenario 2: "The False Positive Flood"
- Time: 9:15 AM on Monday
- Alert: 20 Gmail alerts in 10 minutes
- Twist: All are test users during business hours
- Goal: Practice rapid triage and false positive filtering

Scenario 3: "The Insider Threat"
- Time: 2:00 PM on Wednesday
- Alert: Authorized user "wipedclean" at unusual hour
- Twist: Credentials may be compromised
- Goal: Practice investigation when trust is in question
```

**Tabletop Exercise:**
```
Format: Conference room discussion (no actual systems)
Duration: 1-2 hours
Participants: Security team, DevOps, Management
Leader: Security lead or external facilitator

Agenda:
1. Present hypothetical critical incident
2. Walk through playbook steps as a team
3. Identify gaps, unclear procedures, missing tools
4. Document improvement opportunities
5. Assign action items for playbook updates
```

**Tool Familiarization:**
```
Schedule: Monthly "lunch and learn" sessions
Topics:
- Month 1: Cerberus deep dive (Step 6 audit logs)
- Month 2: Shuffle workflow debugging
- Month 3: Firebase advanced queries
- Month 4: Forensic analysis best practices
```

---

## 📊 Appendix A: Success Metrics & KPIs

### Response Time Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **MTTA** (Mean Time to Acknowledge) | < 5 min | [TRACK] | 🟢 / 🟡 / 🔴 |
| **MTTI** (Mean Time to Investigate) | < 15 min | [TRACK] | 🟢 / 🟡 / 🔴 |
| **MTTR** (Mean Time to Resolve) | < 60 min | [TRACK] | 🟢 / 🟡 / 🔴 |

**Color Key:**
- 🟢 Green: Within target (Good)
- 🟡 Yellow: 10-25% over target (Needs attention)
- 🔴 Red: >25% over target (Immediate action required)

---

### Quality Metrics

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| **False Positive Rate** | < 10% | [TRACK] | ↑ / → / ↓ |
| **Incident Report Completion** | 100% within 24h | [TRACK] | ↑ / → / ↓ |
| **Playbook Adherence** | 100% | [TRACK] | ↑ / → / ↓ |
| **Prevention Success** | >90% (no repeat incidents) | [TRACK] | ↑ / → / ↓ |

---

### Team Readiness

| Metric | Target | Current | Next Review |
|--------|--------|---------|-------------|
| **Security Training** | 100% team trained annually | [%] | [DATE] |
| **Drill Completion** | Quarterly drills completed | [Q1/Q2/Q3/Q4] | [DATE] |
| **Playbook Currency** | Updated within 30 days of incident | [DAYS] | N/A |
| **On-Call Coverage** | 24/7 availability | [YES/NO] | Weekly |

---

## 📞 Appendix B: Emergency Contacts & Resources

### Primary Contacts

| Role | Name | Email | Phone | Escalation Level |
|------|------|-------|-------|------------------|
| **Security Lead** | [NAME] | info@lessimp.com | [PHONE] | Primary |
| **CTO** | [NAME] | wfrancois@lessimp.com | [PHONE] | HIGH/CRITICAL |
| **CISO** | [NAME] | [EMAIL] | [PHONE] | CRITICAL only |
| **Legal/Compliance** | [NAME] | [EMAIL] | [PHONE] | CRITICAL + data breach |
| **DevOps On-Call** | [ROTATION] | [EMAIL] | [PAGERDUTY] | Infrastructure issues |

---

### Secondary Contacts

| Role | Name | Email | Phone | When to Contact |
|------|------|-------|-------|-----------------|
| **QA Lead** | [NAME] | [EMAIL] | [PHONE] | Test artifact validation |
| **Product Manager** | [NAME] | [EMAIL] | [PHONE] | User communication |
| **PR/Communications** | [NAME] | [EMAIL] | [PHONE] | Public disclosure needed |

---

### External Resources

| Resource | URL/Contact | Purpose | Availability |
|----------|-------------|---------|--------------|
| **Firebase Support** | https://firebase.google.com/support | Platform issues | 24/7 |
| **Shuffle Support** | [SUPPORT EMAIL] | Workflow issues | Business hours |
| **Incident Response Hotline** | [EXTERNAL IR FIRM] | Major breach assistance | 24/7 (retainer) |
| **Legal Counsel** | [LAW FIRM] | Data breach notification | On-demand |

---

## 🔗 Appendix C: Key Resources & Quick Links

### Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| **QUICK_START_GUIDE.md** | `~/Documents/GitHub/cerberus-core/` | 5-minute alert testing |
| **MASTER_INDEX.md** | `~/Documents/GitHub/cerberus-core/` | Navigation for all docs |
| **FINALLOGIC_TECHNICAL_EXPLANATION.md** | `~/Documents/GitHub/cerberus-core/` | Python logic deep-dive |
| **SECURITY_ANALYST_COMMAND_SUMMARY.md** | `~/Documents/GitHub/cerberus-core/` | Agent command responses |

---

### System Access

| System | URL | Credentials | Purpose |
|--------|-----|-------------|---------|
| **Cerberus UI** | http://localhost:8888/ | [CREDS] | Test execution logs |
| **Shuffle Workflows** | http://localhost:3001/workflows | [CREDS] | Workflow debugging |
| **Firebase Console** | https://console.firebase.google.com/ | [GOOGLE ACCOUNT] | User management |
| **Discord Security Channel** | [WEBHOOK URL] | [INVITE LINK] | Real-time alerts |

---

### Tools & Scripts

| Tool | Location | Command | Purpose |
|------|----------|---------|---------|
| **test_intrusion.sh** | `~/Documents/GitHub/cerberus-core/` | `./test_intrusion.sh` | Instant alert testing |
| **Cerberus DB Query** | MySQL Workbench | `SELECT * FROM testcasestepexecutionproperty WHERE Property='TEST_IDENTITY_LOG'` | Forensic queries |
| **Shuffle API** | Postman/curl | `curl http://localhost:3001/api/v1/health` | API health check |

---

## 🎓 Appendix D: Training & Certification

### Required Training

| Training Module | Duration | Frequency | Target Audience |
|-----------------|----------|-----------|-----------------|
| **Incident Response Basics** | 2 hours | Annual | All security team |
| **Cerberus Forensics** | 1 hour | Quarterly | On-call engineers |
| **Shuffle Debugging** | 1 hour | Quarterly | Security team |
| **Firebase Security** | 2 hours | Annual | Security + DevOps |

---

### Certification Tracking

| Team Member | IR Certification | Last Training | Next Training | Status |
|-------------|------------------|---------------|---------------|--------|
| [NAME] | [CERT] | 2026-01-15 | 2027-01-15 | ✅ Current |
| [NAME] | [CERT] | 2025-11-20 | 2026-11-20 | 🟡 Due soon |
| [NAME] | None | N/A | 2026-03-01 | 🔴 Required |

---

## ✅ Appendix E: Incident Response Checklist

**Print this page and keep at your desk for quick reference during incidents.**

### Phase 1: Immediate Triage (0-5 min)
- [ ] Alert received at info@lessimp.com
- [ ] Verify 8 fields populated correctly
- [ ] Check Discord for matching RED notification
- [ ] Determine severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Acknowledge alert via email reply
- [ ] Record incident ID: SEC-[YYYY]-[MM]-[DD]-[###]

### Phase 2: Forensic Investigation (5-20 min)
- [ ] Access Cerberus: http://localhost:8888/TestCaseExecutionList.jsp
- [ ] Find execution matching alert timestamp
- [ ] Verify Step 6 TEST_IDENTITY_LOG property
- [ ] Cross-reference phone/email/user with Gmail alert
- [ ] Check Shuffle workflow logs: http://localhost:3001/workflows
- [ ] Verify FinalLogic output (alert_channel, severity, hour)
- [ ] Search Firebase for user by phone number
- [ ] Determine if authentication succeeded (last sign-in match?)
- [ ] Create forensic timeline reconstruction

### Phase 3: Containment (20-40 min)
- [ ] **If CRITICAL:** Disable Firebase account immediately
- [ ] **If CRITICAL:** Revoke all active sessions
- [ ] **If CRITICAL:** Preserve evidence (screenshots + exports)
- [ ] **If CRITICAL:** Escalate to Security Lead + CTO
- [ ] **If MEDIUM/HIGH:** Enable enhanced monitoring
- [ ] **If LOW:** Document only, no containment needed

### Phase 4: Eradication (40-60 min)
- [ ] Reset compromised credentials
- [ ] Force password reset (if applicable)
- [ ] Clear phone number (require re-verification)
- [ ] Invalidate all tokens
- [ ] Update security rules (if vulnerability found)
- [ ] Test authentication flow with known-good account
- [ ] Verify Step 6 logging still functional
- [ ] Notify user (if production account)

### Phase 5: Post-Incident (1-7 days)
- [ ] Complete full incident report (use template in 5.1)
- [ ] Update incident tracking spreadsheet
- [ ] Calculate response metrics (MTTA, MTTI, MTTR)
- [ ] Identify preventive measures
- [ ] Update playbook with lessons learned
- [ ] Schedule team debrief (within 48 hours)
- [ ] Implement quick wins (< 7 days)
- [ ] Create tickets for long-term improvements

---

## 📝 Document Control

| Attribute | Value |
|-----------|-------|
| **Document Title** | Security Incident Response Playbook: "Critical Alert" Protocol |
| **Version** | 2.0 |
| **Created By** | Security Operations Team |
| **Created Date** | February 1, 2026 |
| **Last Updated** | February 1, 2026 |
| **Next Review** | May 1, 2026 (Quarterly) |
| **Classification** | INTERNAL - Security Team Only |
| **Distribution** | Security Team, DevOps, Management |

---

## 🎉 PLAYBOOK READY FOR OPERATIONAL USE

**This Security Incident Response Playbook is now:**
- ✅ Comprehensive (5 phases, 40+ pages)
- ✅ Actionable (Step-by-step procedures)
- ✅ Tested (Aligned with existing infrastructure)
- ✅ Scalable (Handles LOW → CRITICAL severity)
- ✅ Compliant (Forensic chain of custody preserved)

**When Gmail CRITICAL alert arrives, open this document and start at Phase 1. Follow the checklist in Appendix E. You've got this! 🚀**

---

**END OF SECURITY INCIDENT RESPONSE PLAYBOOK V2.0**
