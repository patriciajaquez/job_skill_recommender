#!/usr/bin/env python3
"""
Test N8N Integration Components
Verifies that all N8N workflow components work correctly.
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import our N8N integration functions
try:
    from workflows.scripts.n8n_integration import (
        collect_real_job_data,
        get_mock_job_data,
        extract_skills_with_openai,
        extract_skills_mock,
        health_check_apis
    )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestN8NIntegration(unittest.TestCase):
    """Test suite for N8N integration functions."""
    
    def test_mock_job_data_collection(self):
        """Test mock job data collection."""
        print("\n🧪 Testing mock job data collection...")
        
        result = get_mock_job_data("python developer", "remote")
        
        self.assertIsInstance(result, dict)
        self.assertIn('jobs', result)
        self.assertIn('totalJobs', result)
        self.assertGreater(result['totalJobs'], 0)
        self.assertTrue(result.get('isMockData', False))
        
        # Check job structure
        for job in result['jobs']:
            self.assertIn('id', job)
            self.assertIn('title', job)
            self.assertIn('company', job)
            self.assertIn('location', job)
        
        print(f"✅ Mock data collection: {result['totalJobs']} jobs")
    
    def test_real_job_data_collection(self):
        """Test real job data collection (may fall back to mock)."""
        print("\n🧪 Testing real job data collection...")
        
        result = collect_real_job_data("data scientist", "us")
        
        self.assertIsInstance(result, dict)
        self.assertIn('jobs', result)
        self.assertIn('totalJobs', result)
        self.assertGreater(result['totalJobs'], 0)
        
        print(f"✅ Real data collection: {result['totalJobs']} jobs from {len(result.get('sources', []))} sources")
    
    def test_mock_skill_extraction(self):
        """Test mock skill extraction."""
        print("\n🧪 Testing mock skill extraction...")
        
        description = "Python developer with machine learning experience, SQL knowledge, and AWS expertise"
        skills = extract_skills_mock(description)
        
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        
        # Check skill structure
        for skill in skills:
            self.assertIn('skill', skill)
            self.assertIn('category', skill)
            self.assertIn('confidence', skill)
            self.assertIsInstance(skill['confidence'], (int, float))
            self.assertTrue(0 <= skill['confidence'] <= 1)
        
        print(f"✅ Mock skill extraction: {len(skills)} skills found")
        for skill in skills[:3]:  # Show first 3
            print(f"   - {skill['skill']} ({skill['category']}) - {skill['confidence']:.2f}")
    
    def test_openai_skill_extraction(self):
        """Test OpenAI skill extraction (may fall back to mock)."""
        print("\n🧪 Testing OpenAI skill extraction...")
        
        description = "Senior Python developer with 5+ years experience in machine learning, deep learning, SQL databases, and AWS cloud platforms"
        skills = extract_skills_with_openai(description)
        
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        
        # Check skill structure
        for skill in skills:
            self.assertIn('skill', skill)
            self.assertIn('category', skill)
            self.assertIn('confidence', skill)
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print(f"✅ OpenAI skill extraction: {len(skills)} skills found")
        else:
            print(f"✅ OpenAI skill extraction (mock fallback): {len(skills)} skills found")
        
        for skill in skills[:3]:  # Show first 3
            print(f"   - {skill['skill']} ({skill['category']}) - {skill['confidence']:.2f}")
    
    def test_api_health_check(self):
        """Test API health check."""
        print("\n🧪 Testing API health check...")
        
        result = health_check_apis()
        
        self.assertIsInstance(result, dict)
        self.assertIn('healthResults', result)
        self.assertIn('healthyCount', result)
        self.assertIn('totalApis', result)
        self.assertIn('useBackup', result)
        self.assertIn('timestamp', result)
        
        print(f"✅ API health check: {result['healthyCount']}/{result['totalApis']} APIs healthy")
        print(f"   Use backup: {result['useBackup']}")
    
    def test_workflow_file_structure(self):
        """Test that N8N workflow files exist and are valid JSON."""
        print("\n🧪 Testing N8N workflow files...")
        
        workflow_dir = project_root / "workflows" / "n8n"
        
        # Check primary workflow
        primary_workflow = workflow_dir / "job_market_intelligence_pipeline.json"
        self.assertTrue(primary_workflow.exists(), "Primary workflow file not found")
        
        with open(primary_workflow, 'r') as f:
            primary_data = json.load(f)
        
        self.assertIn('name', primary_data)
        self.assertIn('nodes', primary_data)
        self.assertIn('connections', primary_data)
        self.assertGreater(len(primary_data['nodes']), 5)  # Should have multiple nodes
        
        print(f"✅ Primary workflow: {len(primary_data['nodes'])} nodes")
        
        # Check ML enhancement workflow
        ml_workflow = workflow_dir / "ml_enhancement_pipeline.json"
        self.assertTrue(ml_workflow.exists(), "ML enhancement workflow file not found")
        
        with open(ml_workflow, 'r') as f:
            ml_data = json.load(f)
        
        self.assertIn('name', ml_data)
        self.assertIn('nodes', ml_data)
        self.assertIn('connections', ml_data)
        self.assertGreater(len(ml_data['nodes']), 3)  # Should have multiple nodes
        
        print(f"✅ ML enhancement workflow: {len(ml_data['nodes'])} nodes")
    
    def test_project_structure(self):
        """Test that the expected project structure exists."""
        print("\n🧪 Testing project structure...")
        
        expected_files = [
            "workflows/n8n/job_market_intelligence_pipeline.json",
            "workflows/n8n/ml_enhancement_pipeline.json", 
            "workflows/scripts/n8n_integration.py",
            "workflows/N8N_SETUP.md"
        ]
        
        for file_path in expected_files:
            full_path = project_root / file_path
            self.assertTrue(full_path.exists(), f"Missing file: {file_path}")
            print(f"   ✅ {file_path}")
        
        print("✅ Project structure verified")


def run_integration_test():
    """Run a full integration test simulating the N8N workflow."""
    print("\n🚀 Running Full Integration Test (Simulating N8N Workflow)")
    print("=" * 60)
    
    # Step 1: Health Check
    print("\n1️⃣ API Health Check...")
    health = health_check_apis()
    print(f"   APIs Status: {health['healthyCount']}/{health['totalApis']} healthy")
    
    # Step 2: Data Collection
    print("\n2️⃣ Data Collection...")
    if health['useBackup']:
        print("   Using backup data (APIs unhealthy)")
        jobs_result = get_mock_job_data("data scientist", "remote")
    else:
        print("   Using real API data")
        jobs_result = collect_real_job_data("data scientist", "us")
    
    print(f"   Collected: {jobs_result['totalJobs']} jobs")
    
    # Step 3: ML Enhancement
    print("\n3️⃣ ML Enhancement...")
    enhanced_jobs = []
    
    for job in jobs_result['jobs'][:3]:  # Process first 3 jobs for demo
        # Skill extraction
        skills = extract_skills_with_openai(job.get('description', ''))
        job['aiExtractedSkills'] = skills
        
        # Mock salary prediction
        job['aiSalaryPrediction'] = {
            'predictedMin': 90000,
            'predictedMax': 130000,
            'confidence': 0.85
        }
        
        enhanced_jobs.append(job)
        print(f"   Enhanced job: {job['title']} - {len(skills)} skills extracted")
    
    # Step 4: Results
    print("\n4️⃣ Integration Results...")
    print(f"   Total jobs processed: {len(enhanced_jobs)}")
    print(f"   Average skills per job: {sum(len(j.get('aiExtractedSkills', [])) for j in enhanced_jobs) / len(enhanced_jobs):.1f}")
    print(f"   All jobs have salary predictions: {all('aiSalaryPrediction' in j for j in enhanced_jobs)}")
    
    print("\n✅ Integration test completed successfully!")
    return enhanced_jobs


def main():
    """Main test runner."""
    print("🔄 N8N Integration Test Suite")
    print("=" * 40)
    
    # Run unit tests
    print("\n📋 Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=0)
    
    # Run integration test
    run_integration_test()
    
    print("\n🎉 All tests completed!")
    print("\n📖 Next Steps:")
    print("1. Install N8N: npm install n8n -g")
    print("2. Start N8N: n8n start")
    print("3. Import workflows from workflows/n8n/")
    print("4. Follow N8N_SETUP.md for configuration")


if __name__ == "__main__":
    main()
