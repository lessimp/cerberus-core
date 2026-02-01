#!/usr/bin/env python3
"""
Firebase Test Phone Numbers Configuration Helper

This script generates the configuration instructions and validation checks
for Firebase Console "Phone numbers for testing" setup.

Usage:
    python3 firebase_test_numbers_helper.py

It will output:
1. List of phone numbers to add to Firebase Console
2. curl commands to validate Shuffle API returns these numbers
3. Instructions for manual Firebase Console configuration
"""

import json

# Test numbers from shuffle_provider.py
TEST_NUMBERS = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "phone": "5555551001",
        "countryCode": "+1",
        "fullPhone": "+15555551001",
        "otp": "123456"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "phone": "5555551002",
        "countryCode": "+1",
        "fullPhone": "+15555551002",
        "otp": "123456"
    },
    {
        "id": 3,
        "name": "Carol Davis",
        "phone": "5555551003",
        "countryCode": "+1",
        "fullPhone": "+15555551003",
        "otp": "123456"
    },
    {
        "id": 4,
        "name": "David Wilson",
        "phone": "5555551004",
        "countryCode": "+1",
        "fullPhone": "+15555551004",
        "otp": "123456"
    },
    {
        "id": 5,
        "name": "Eve Martinez",
        "phone": "5555551005",
        "countryCode": "+1",
        "fullPhone": "+15555551005",
        "otp": "123456"
    }
]


def print_header(title):
    """Print formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_firebase_instructions():
    """Print Firebase Console configuration instructions."""
    print_header("📱 Firebase Console Configuration")
    
    print("1. Open Firebase Console:")
    print("   https://console.firebase.google.com/")
    print()
    print("2. Select your Lessimp project")
    print()
    print("3. Navigate to:")
    print("   Authentication → Sign-in method → Phone")
    print()
    print("4. Scroll to section:")
    print("   'Phone numbers for testing'")
    print()
    print("5. Click: [+ Add phone number]")
    print()
    print("6. Add each of these numbers:")
    print()


def print_firebase_numbers_table():
    """Print formatted table of test numbers."""
    print("┌────────────────┬────────────────┬─────────────────────┐")
    print("│ Phone Number   │ Verification   │ User                │")
    print("│                │ Code           │                     │")
    print("├────────────────┼────────────────┼─────────────────────┤")
    
    for user in TEST_NUMBERS:
        phone = user["fullPhone"]
        otp = user["otp"]
        name = user["name"]
        print(f"│ {phone:14s} │ {otp:14s} │ {name:19s} │")
    
    print("└────────────────┴────────────────┴─────────────────────┘")
    print()


def print_firebase_manual_steps():
    """Print step-by-step manual entry instructions."""
    print_header("📝 Manual Entry Steps (Repeat for Each Number)")
    
    print("For each phone number above:")
    print()
    print("  a) Click: [+ Add phone number]")
    print("  b) Enter Phone Number: (e.g., +15555551001)")
    print("  c) Enter Verification Code: 123456")
    print("  d) Click: [Save]")
    print()
    print("After adding all 5 numbers, click [Save] at the bottom.")
    print()


def print_validation_commands():
    """Print validation commands."""
    print_header("✅ Validation Commands")
    
    print("After configuring Firebase, validate Shuffle API returns these numbers:")
    print()
    print("# Get a random user and check the phone number")
    print("curl -s http://localhost:5000/shuffle/get_user | jq '.fullPhone, .otp'")
    print()
    print("# Expected output (one of):")
    for user in TEST_NUMBERS:
        print(f'# "{user["fullPhone"]}"')
    print('# "123456"')
    print()
    
    print("# Get all users")
    print("curl -s http://localhost:5000/shuffle/get_all | jq '.users[] | .fullPhone'")
    print()
    print("# Expected output (all 5):")
    for user in TEST_NUMBERS:
        print(f'# "{user["fullPhone"]}"')
    print()


def print_verification_checklist():
    """Print verification checklist."""
    print_header("📋 Verification Checklist")
    
    print("Before running Cerberus tests, verify:")
    print()
    print("[ ] Shuffle API running:")
    print("    curl http://localhost:5000/shuffle/health")
    print()
    print("[ ] All 5 test numbers added to Firebase Console")
    print()
    print("[ ] All test numbers have OTP: 123456")
    print()
    print("[ ] Firebase Phone Authentication enabled:")
    print("    Authentication → Sign-in method → Phone → Enabled")
    print()
    print("[ ] Test a number manually in Lessimp app:")
    print("    - Enter: 5555551001")
    print("    - Receive OTP screen (no SMS sent)")
    print("    - Enter: 123456")
    print("    - Login successful")
    print()


def export_json_config():
    """Export test numbers to JSON for reference."""
    print_header("📄 JSON Configuration Reference")
    
    config = {
        "firebase_test_numbers": [
            {
                "phoneNumber": user["fullPhone"],
                "verificationCode": user["otp"],
                "userName": user["name"]
            }
            for user in TEST_NUMBERS
        ],
        "notes": [
            "Add these to Firebase Console → Authentication → Phone numbers for testing",
            "All test numbers use the same OTP: 123456",
            "These numbers will bypass actual SMS sending",
            "Shuffle API will randomly select from these numbers",
            "Cerberus test cases will inject these into Lessimp mobile UI"
        ]
    }
    
    print(json.dumps(config, indent=2))
    print()
    print("Save this to: firebase_test_numbers.json")
    print()


def print_troubleshooting():
    """Print troubleshooting guide."""
    print_header("🔧 Troubleshooting")
    
    print("Issue: 'Invalid phone number' in Firebase")
    print("Fix: Ensure format is +1XXXXXXXXXX (country code + 10 digits)")
    print()
    
    print("Issue: OTP verification fails")
    print("Fix: Verify OTP is exactly '123456' (six digits, no spaces)")
    print()
    
    print("Issue: Test number not working in app")
    print("Fix:")
    print("  1. Check Firebase Console → Authentication → Phone")
    print("  2. Verify number is listed under 'Phone numbers for testing'")
    print("  3. Try deleting and re-adding the number")
    print()
    
    print("Issue: Shuffle returns wrong phone format")
    print("Fix:")
    print("  - Use $.fullPhone in Cerberus (includes country code)")
    print("  - NOT $.phone (digits only)")
    print()


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("  🔐 Firebase Test Phone Numbers Configuration Helper")
    print("=" * 70)
    
    print_firebase_instructions()
    print_firebase_numbers_table()
    print_firebase_manual_steps()
    print_validation_commands()
    print_verification_checklist()
    export_json_config()
    print_troubleshooting()
    
    print("=" * 70)
    print("  Configuration helper complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Follow the manual entry steps above")
    print("2. Run validation commands")
    print("3. Execute Cerberus test case: TC001_LoginWithShuffleHandshake")
    print()


if __name__ == '__main__':
    main()
