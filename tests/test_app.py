#!/usr/bin/env python3
"""
Quick test script to verify the app is ready for launch
"""

import sys
import importlib

def test_app():
    """Test if the app is ready to launch"""
    try:
        # Test imports
        import streamlit as st
        import app
        print("✅ All imports successful")
        
        # Test key functions
        data = app.get_global_job_data()
        assert 'locations' in data, "Missing locations data"
        assert 'skills' in data, "Missing skills data"
        assert 'job_titles' in data, "Missing job_titles data"
        print("✅ Global data structure is valid")
        
        # Test data generation
        salary_data = app.generate_realistic_salary_data()
        assert len(salary_data) > 0, "No salary data generated"
        print(f"✅ Salary data generated: {len(salary_data)} records")
        
        # Test main function exists
        assert hasattr(app, 'main'), "Main function not found"
        print("✅ Main function exists")
        
        print("\n🎉 SUCCESS: App is ready to launch!")
        print("Run: streamlit run app.py")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_app()
    sys.exit(0 if success else 1)
