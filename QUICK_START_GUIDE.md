# 🚀 QUICK START GUIDE - Security Alert Testing

**Status:** ✅ Ready for Immediate Testing  
**Mode:** Security Analyst - API Handshake Verification  
**Time Required:** 5-10 minutes  
**Prerequisites:** All infrastructure operational ✅

---

## 🎯 Objective

Verify the complete **Shuffle Webhook API → FinalLogic → Discord/Gmail** integration chain using the instant alert testing script.

---

## ⚡ 3-Step Quick Start

### Step 1: Navigate to Project Directory

```bash
cd ~/Documents/GitHub/cerberus-core
```

### Step 2: Run Test Script

```bash
./test_intrusion.sh
```

### Step 3: Select Test Scenario

**Option A: Test Authorized Path (Recommended First)**
```
Select intrusion scenario:
1) Unauthorized User (intruder_hacker)
2) Credential Stuffing (stolen_credentials)
3) Brute Force Attack (brute_force_bot)
4) Social Engineering (phishing_victim)
5) Authorized User (wipedclean)           <-- SELECT THIS FIRST
6) Exit

Enter your choice (1-6): 5
```

**Expected Result (5-10 seconds):**
- ✅ HTTP 200 from Shuffle Webhook API
- ✅ Discord GREEN notification: "Identity Restored - User 'wipedclean'"
- ❌ NO Gmail (authorized path skips email)

---

**Option B: Test Unauthorized Path**
```
Enter your choice (1-6): 1
```

**Expected Result (5-10 seconds):**
- ✅ HTTP 200 from Shuffle Webhook API
- 🚨 Discord RED notification: "UNAUTHORIZED LOGIN ATTEMPT"
- 📧 Gmail CRITICAL email to info@lessimp.com with 8-field incident table

---

## 🔍 What Gets Tested

### API Flow (Scenario 5 - Authorized):

```
1. test_intrusion.sh
   ↓ POST JSON payload
   
2. Shuffle Webhook API
   http://localhost:3001/api/v1/hooks/webhook_a76354e0...
   ↓ Receives: {user: "wipedclean", phone: "5555551001", email: "..."}
   
3. FinalLogic Python Node
   ↓ Evaluates: username == "wipedclean" OR current_hour == 9
   ↓ Result: TRUE (username matches)
   ↓ Sets: alert_channel = "discord", color = 3066993 (green)
   
4. Discord Webhook API
   ↓ Executes (condition: alert_channel == "discord")
   ↓ Sends green embed
   
5. Gmail SMTP API
   ↓ SKIPPED (condition: alert_channel == "gmail" is FALSE)
```

**Verification Points:**
- ✅ Shuffle Webhook API accepts POST request
- ✅ FinalLogic correctly evaluates username
- ✅ Discord API receives green notification
- ✅ Gmail API correctly skipped (no false positive)

---

### API Flow (Scenario 1 - Unauthorized):

```
1. test_intrusion.sh
   ↓ POST JSON payload
   
2. Shuffle Webhook API
   http://localhost:3001/api/v1/hooks/webhook_a76354e0...
   ↓ Receives: {user: "intruder_hacker", phone: "5555559999", email: "..."}
   
3. FinalLogic Python Node
   ↓ Evaluates: username == "wipedclean" OR current_hour == 9
   ↓ Result: FALSE (username ≠ "wipedclean" AND hour ≠ 9)
   ↓ Sets: alert_channel = "gmail", severity = "CRITICAL", color = 15158332 (red)
   
4. Gmail SMTP API
   ↓ Executes (condition: alert_channel == "gmail")
   ↓ Sends HTML email with 8-field incident table
   ↓ To: info@lessimp.com, CC: wfrancois@lessimp.com
   
5. Discord Webhook API
   ↓ Executes (also triggered for unauthorized)
   ↓ Sends red embed with CRITICAL severity
```

**Verification Points:**
- ✅ Shuffle Webhook API accepts POST request
- ✅ FinalLogic correctly evaluates username AND hour
- ✅ Gmail SMTP API sends CRITICAL email with 8 fields
- ✅ Discord API receives red notification with matching data

---

## 🧪 Complete Test Matrix (5 Scenarios)

| # | Scenario | User | Phone | Current Time | FinalLogic Result | Discord | Gmail |
|---|----------|------|-------|--------------|-------------------|---------|-------|
| **1** | Unauthorized | `intruder_hacker` | `5555559999` | Not 9 AM | FALSE | 🔴 Red | ✅ Yes |
| **2** | Credential Stuffing | `stolen_credentials` | `5555558888` | Not 9 AM | FALSE | 🔴 Red | ✅ Yes |
| **3** | Brute Force | `brute_force_bot` | `5555557777` | Not 9 AM | FALSE | 🔴 Red | ✅ Yes |
| **4** | Phishing | `phishing_victim` | `5555556666` | Not 9 AM | FALSE | 🔴 Red | ✅ Yes |
| **5** | Authorized | `wipedclean` | `5555551001` | Any time | TRUE | 🟢 Green | ❌ No |

**Note:** If you run Scenarios 1-4 at exactly 9:00-9:59 AM, they will evaluate to TRUE (authorized) because `current_hour == 9` is the second condition in the OR logic. This is by design for business hours testing.

---

## 📧 Gmail Email Details (Scenario 1-4)

**Subject:**
```
🚨 CRITICAL: Unauthorized Login Attempt - intruder_hacker
```

**Body:** Professional HTML template with:
- 🔴 Red gradient header
- ⚠️ CRITICAL severity badge
- 📋 8-field incident table:

| Field | Value Example |
|-------|---------------|
| User Identifier | `intruder_hacker` |
| Status | `unauthorized` |
| Timestamp | `2026-02-01T15:45:30` |
| Test Case | `TC001_SecureLogin` |
| Phone Number | `5555559999` |
| Email Address | `hacker@malicious.com` |
| Hour of Attempt | `15:00` (3 PM) |
| Severity | `CRITICAL` |

- 📝 6-item investigation checklist
- 🔵 CTA buttons: "View Cerberus Logs", "View Firebase Logs"
- 🏢 Professional Lessimp branding footer

---

## 💬 Discord Notification Details

### Authorized (Scenario 5):

**Embed Color:** 🟢 Green (#2ECC71 / 3066993)

**Title:** ✅ Identity Restored

**Message:**
```
User 'wipedclean' logged in successfully at 2026-02-01 15:45:30

Status: Verified
Phone: 5555551001
Email: carol.davis@testmail.com
Test Case: TC001_SecureLogin
```

---

### Unauthorized (Scenarios 1-4):

**Embed Color:** 🔴 Red (#E74C3C / 15158332)

**Title:** 🚨 UNAUTHORIZED LOGIN ATTEMPT

**Message:**
```
User 'intruder_hacker' attempted login at 2026-02-01 15:45:30

Status: Unauthorized
Phone: 5555559999
Email: hacker@malicious.com
Test Case: TC001_SecureLogin
Severity: CRITICAL
```

---

## 🔧 Troubleshooting

### Issue: HTTP 000 (Connection Failed)

**Symptom:** Script shows `HTTP Status: 000`

**Solution:**
```bash
# Verify Shuffle is running
curl http://localhost:3001/api/v1/health

# Expected: {"success": true, ...}
# If failed: Start Shuffle Local Engine
```

---

### Issue: HTTP 200 but No Discord Notification

**Symptom:** Webhook returns success but no Discord message

**Solution:**
1. Check Shuffle workflow execution logs: `http://localhost:3001/workflows`
2. Verify FinalLogic node output: Look for `alert_channel` value
3. Check Discord webhook URL in Shuffle Discord node
4. Verify Discord channel permissions

---

### Issue: HTTP 200 but No Gmail

**Symptom:** Webhook succeeds but no email received

**Solution:**
1. Check spam/junk folder in Gmail
2. Verify recipient: `info@lessimp.com`
3. Check Shuffle Gmail node configuration:
   - Body Type: Must be **HTML** (not plain text)
   - OAuth 2.0 credentials configured
   - SMTP: `smtp.gmail.com:587`
4. Check Shuffle Gmail node execution logs for errors

---

### Issue: Wrong Alert for "wipedclean"

**Symptom:** User 'wipedclean' triggers Gmail CRITICAL email

**Possible Causes:**
1. **Typo in username:** Check if you typed "Wipedclean" (capitalized) or "wiped clean" (space)
   - FinalLogic is **case-sensitive** and requires exact match: `"wipedclean"`
   
2. **FinalLogic code error:** Verify Python node logic:
   ```python
   if username == "wipedclean" or current_hour == 9:
   ```

3. **Variable extraction error:** Check if `$exec.text.user` is correctly mapped in Shuffle

---

### Issue: Intruder Authorized at 9 AM

**Symptom:** User 'intruder' triggers Discord green at 9:30 AM

**This is EXPECTED:** The FinalLogic uses OR logic:
```python
if username == "wipedclean" or current_hour == 9:
```

**Behavior:**
- At 9:00-9:59 AM: **ANY user** is authorized (business hours window)
- At any other hour: Only `wipedclean` is authorized

**To Test Unauthorized Path at 9 AM:**
Wait until 10:00 AM or later, then run Scenario 1 again.

---

## 📋 Post-Test Checklist

After running tests, verify the following:

### ✅ Discord Verification:
- [ ] Discord channel received notification
- [ ] Authorized test (Scenario 5) shows GREEN embed
- [ ] Unauthorized test (Scenario 1) shows RED embed
- [ ] All fields populated: User, Phone, Status, Timestamp

### ✅ Gmail Verification (Unauthorized only):
- [ ] Email received at info@lessimp.com
- [ ] CC received at wfrancois@lessimp.com
- [ ] Subject line shows: "🚨 CRITICAL: Unauthorized Login Attempt"
- [ ] HTML rendering correct (red header, badges, table)
- [ ] All 8 fields populated correctly
- [ ] CTA buttons visible

### ✅ Shuffle API Verification:
- [ ] Script shows HTTP 200 response
- [ ] Navigate to `http://localhost:3001/workflows`
- [ ] Find latest execution matching timestamp
- [ ] Check FinalLogic node output JSON
- [ ] Verify `alert_channel` value ("discord" or "gmail")
- [ ] Verify `status` value ("verified" or "unauthorized")

### ✅ Forensic Audit (Optional):
If you want to verify the complete chain of custody:

1. Navigate: `http://localhost:8888/TestCaseExecutionList.jsp`
2. Note: You won't see execution here yet (mobile test not run)
3. For full forensic validation, run complete TC001_SecureLogin test
4. Then check Step 6 property `TEST_IDENTITY_LOG` in execution history

---

## 🎯 Next Steps After Testing

### If All Tests Pass ✅:

**You have successfully verified:**
- ✅ Shuffle Webhook API integration
- ✅ FinalLogic Python validation logic
- ✅ Discord Webhook API routing
- ✅ Gmail SMTP API routing
- ✅ Dynamic field substitution (8 fields)
- ✅ OR-based authorization logic

**Proceed to:**
1. **Configure TC001_SecureLogin** in Cerberus UI (16 steps)
2. **Execute full mobile test** with iOS Simulator
3. **Verify Step 6 forensic audit trail** in execution history
4. **Train security team** on incident response procedures

**Reference Documentation:**
- FINAL_MASTER_DIRECTIVE_EXECUTION.md - Complete TC001 setup guide
- SECURITY_INCIDENT_RESPONSE_PLAYBOOK.md - 6-phase response protocol
- EXECUTION_FORENSIC_VALIDATION_COMPLETE.md - Scenario A/B walkthroughs

---

### If Tests Fail ❌:

**Review troubleshooting section above, then:**

1. Check Shuffle workflow logs: `http://localhost:3001/workflows`
2. Verify all infrastructure: Cerberus, Shuffle, MySQL
3. Review FinalLogic Python code for syntax errors
4. Verify webhook URL: `webhook_a76354e0-cf09-4754-96e1-682c89084d4c`
5. Check Discord webhook URL (not expired, correct channel)
6. Verify Gmail OAuth 2.0 credentials in Shuffle

**Get Help:**
- Review: SECURITY_ORCHESTRATION_QUICK_REFERENCE.md
- Review: MASTER_INDEX.md (complete navigation guide)
- Review: FINALLOGIC_TECHNICAL_EXPLANATION.md (logic deep-dive)

---

## 📚 Documentation Reference

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **QUICK_START_GUIDE.md** | **This file - Instant testing** | **Right now** |
| MASTER_INDEX.md | Navigation for all 12 documents | General reference |
| SECURITY_ANALYST_COMMAND_SUMMARY.md | Agent command responses | Understanding API logic |
| SECURITY_INCIDENT_RESPONSE_PLAYBOOK.md | Response procedures | When Gmail alert arrives |
| FINALLOGIC_TECHNICAL_EXPLANATION.md | Python logic deep-dive | Tuning detection rules |
| test_intrusion.sh | Test script source | Running tests |

---

## ⏱️ Timeline Summary

**Total Time:** 5-10 minutes

| Step | Action | Time |
|------|--------|------|
| 1 | Navigate to directory | 10 seconds |
| 2 | Run test script | 5 seconds |
| 3 | Select Scenario 5 (authorized) | 10 seconds |
| 4 | Wait for Discord green | 5-10 seconds |
| 5 | Select Scenario 1 (unauthorized) | 10 seconds |
| 6 | Wait for Gmail + Discord red | 5-10 seconds |
| 7 | Verify notifications | 2-3 minutes |

**Total:** ~5 minutes for complete API handshake verification

---

## 🎉 Success Criteria

**You've successfully completed the Final Operational Directive when:**

1. ✅ Scenario 5 triggers Discord GREEN (no Gmail)
2. ✅ Scenario 1 triggers Gmail CRITICAL + Discord RED
3. ✅ All 8 Gmail fields populated correctly
4. ✅ Response time < 10 seconds for each test
5. ✅ HTTP 200 responses from Shuffle Webhook API

**Congratulations! Your Security Operations API integration is 100% operational. 🚀**

---

**Ready to begin? Run:**

```bash
cd ~/Documents/GitHub/cerberus-core
./test_intrusion.sh
```

**Select Scenario 5 first, then Scenario 1. Wait 5-10 seconds each. Verify Discord and Gmail. Done! ✅**
