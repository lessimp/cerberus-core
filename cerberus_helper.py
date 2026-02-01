#!/usr/bin/env python3
"""
Cerberus Testing - Python Helper Script
Create and execute test cases programmatically
"""

import requests
import json
import sys
from typing import Dict, List, Optional

class CerberusClient:
    def __init__(self, base_url: str = "http://localhost:8888", username: str = "admin", password: str = "admin"):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        
    def create_test_case(self, test: str, testcase: str, description: str, 
                        application: str = "Google", priority: int = 3) -> Dict:
        """Create a new test case"""
        url = f"{self.base_url}/api/public/testcase"
        
        data = {
            "test": test,
            "testcase": testcase,
            "description": description,
            "application": application,
            "status": "WORKING",
            "priority": priority,
            "steps": []
        }
        
        response = self.session.post(url, json=data)
        return response.json()
    
    def add_step_with_action(self, test: str, testcase: str, step_number: int,
                            step_description: str, action: str, value1: str = "",
                            value2: str = "", action_description: str = "") -> Dict:
        """Add a step with an action to an existing test case"""
        url = f"{self.base_url}/api/public/testcasestep"
        
        data = {
            "test": test,
            "testcase": testcase,
            "sort": step_number,
            "description": step_description,
            "useStep": "N",
            "actions": [
                {
                    "sort": 1,
                    "action": action,
                    "value1": value1,
                    "value2": value2,
                    "description": action_description or f"Execute {action}"
                }
            ]
        }
        
        response = self.session.post(url, json=data)
        return response.json()
    
    def run_test_case(self, test: str, testcase: str, country: str = "US",
                     environment: str = "PROD", browser: str = "chrome") -> Dict:
        """Execute a test case"""
        url = f"{self.base_url}/api/public/runtestcase"
        
        data = {
            "test": test,
            "testcase": testcase,
            "country": country,
            "environment": environment,
            "browser": browser
        }
        
        response = self.session.post(url, json=data)
        return response.json()
    
    def get_execution_status(self, execution_id: int) -> Dict:
        """Get the status of a test execution"""
        url = f"{self.base_url}/api/public/testcaseexecution/{execution_id}"
        response = self.session.get(url)
        return response.json()


def create_example_test():
    """Create an example test case"""
    print("🚀 Creating Cerberus Test Case...\n")
    
    # Initialize client
    client = CerberusClient()
    
    # Create test case
    print("1. Creating test case structure...")
    result = client.create_test_case(
        test="MyFirstTest",
        testcase="TC001_VerifyWebsiteText",
        description="Navigate to a website and verify text element",
        application="Google"
    )
    print(f"   ✅ Test case created: {result.get('messageType', 'Unknown')}")
    
    # Add Step 1: Open URL
    print("\n2. Adding Step 1: Open URL...")
    result = client.add_step_with_action(
        test="MyFirstTest",
        testcase="TC001_VerifyWebsiteText",
        step_number=1,
        step_description="Open website",
        action="openUrl",
        value1="https://example.com",
        action_description="Navigate to example.com"
    )
    print(f"   ✅ Step 1 added: {result.get('messageType', 'Unknown')}")
    
    # Add Step 2: Verify Text
    print("\n3. Adding Step 2: Verify Text...")
    result = client.add_step_with_action(
        test="MyFirstTest",
        testcase="TC001_VerifyWebsiteText",
        step_number=2,
        step_description="Verify text on page",
        action="verifyTextInPage",
        value1="Example Domain",
        action_description="Verify 'Example Domain' text is present"
    )
    print(f"   ✅ Step 2 added: {result.get('messageType', 'Unknown')}")
    
    print("\n" + "="*60)
    print("✨ Test Case Created Successfully!")
    print("="*60)
    print(f"\nView your test case at:")
    print(f"http://localhost:8888/TestCaseScript.jsp?test=MyFirstTest&testcase=TC001_VerifyWebsiteText")
    print(f"\nRun your test at:")
    print(f"http://localhost:8888/RunTests.jsp")


def create_google_search_test():
    """Create a Google search test case"""
    print("🚀 Creating Google Search Test Case...\n")
    
    client = CerberusClient()
    
    # Create test case
    print("1. Creating test case structure...")
    client.create_test_case(
        test="MyFirstTest",
        testcase="TC002_GoogleSearch",
        description="Perform a Google search and verify results"
    )
    print("   ✅ Test case created")
    
    # Add steps
    steps = [
        (1, "Open Google", "openUrl", "https://www.google.com", ""),
        (2, "Enter search term", "type", "name=q", "Cerberus Testing"),
        (3, "Click search button", "click", "name=btnK", ""),
        (4, "Wait for results", "waitForElementPresent", "id=search", "5000"),
        (5, "Verify results", "verifyTextInPage", "Cerberus", "")
    ]
    
    for step_num, desc, action, val1, val2 in steps:
        print(f"\n{step_num + 1}. Adding Step {step_num}: {desc}...")
        client.add_step_with_action(
            test="MyFirstTest",
            testcase="TC002_GoogleSearch",
            step_number=step_num,
            step_description=desc,
            action=action,
            value1=val1,
            value2=val2
        )
        print(f"   ✅ Step {step_num} added")
    
    print("\n" + "="*60)
    print("✨ Google Search Test Created Successfully!")
    print("="*60)
    print(f"\nView your test case at:")
    print(f"http://localhost:8888/TestCaseScript.jsp?test=MyFirstTest&testcase=TC002_GoogleSearch")


if __name__ == "__main__":
    print("="*60)
    print("  Cerberus Testing - Python Helper Script")
    print("="*60)
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "google":
            create_google_search_test()
        elif sys.argv[1] == "example":
            create_example_test()
        else:
            print("Usage:")
            print("  python3 cerberus_helper.py example  - Create example test")
            print("  python3 cerberus_helper.py google   - Create Google search test")
    else:
        # Default: create example test
        create_example_test()
    
    print("\n🎉 Done! Happy Testing!")
