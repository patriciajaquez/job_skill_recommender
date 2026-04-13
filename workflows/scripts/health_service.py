# workflows/scripts/health_service.py
from flask import Flask, jsonify, request
from datetime import datetime
import time
import sys
import os

# Add project root to path so we can import our existing code
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from scripts.api_integration import JobAPIIntegrator

app = Flask(__name__)

class APIHealthChecker:
    """Professional health checker that tests real APIs"""
    
    def __init__(self):
        # Use your existing API integrator
        self.integrator = JobAPIIntegrator()
        # Define the APIs we want to test
        self.apis = ['adzuna', 'reed', 'muse', 'coursera', 'rapidapi', 'theirstack']
    
    def check_api_health(self, api_name, test_function):
        """Check health of a single API"""
        start_time = time.time()
        try:
            result = test_function()
            response_time = round(time.time() - start_time, 2)
            
            if result and len(result) > 0:
                return {
                    'status': 'healthy',
                    'data_count': len(result),
                    'response_time_seconds': response_time,
                    'last_checked': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': 'No data returned',
                    'response_time_seconds': response_time,
                    'last_checked': datetime.utcnow().isoformat()
                }
        except Exception as e:
            response_time = round(time.time() - start_time, 2)
            return {
                'status': 'unhealthy',
                'error': str(e),
                'response_time_seconds': response_time,
                'last_checked': datetime.utcnow().isoformat()
            }

    def collect_job_data(self, queries=['data science', 'software engineer', 'python developer']):
        """Collect actual job data from healthy APIs"""
        print("Starting job data collection...")
        all_jobs = []
        collection_stats = {
            'total_jobs': 0,
            'sources_used': [],
            'collection_timestamp': datetime.now().isoformat(),
            'queries_used': queries
        }
        
        # Define how to test each API using correct function signatures
        api_tests = {
            'adzuna': lambda: self.integrator.get_adzuna_jobs('python', 'us'),
            'reed': lambda: self.integrator.get_reed_jobs('python', 'remote'),
            'muse': lambda: self.integrator.get_muse_jobs('python', 'remote'),
            'coursera': lambda: self.integrator.get_coursera_courses('python'),
            'rapidapi': lambda: self.integrator.get_rapidapi_jobs('python', 'remote'),
            'theirstack': lambda: self.integrator.get_theirstack_jobs('python', 'remote')
        }
        
        # Check which APIs are healthy first
        healthy_apis = []
        for api_name, test_func in api_tests.items():
            result = self.check_api_health(api_name, test_func)
            if result['status'] == 'healthy':
                healthy_apis.append(api_name)
        
        print(f"Collecting from healthy APIs: {healthy_apis}")
        
        # Collect data from healthy APIs
        for api_name in healthy_apis:
            try:
                print(f"Collecting jobs from {api_name}...")
                
                # Use the same test functions but get more data
                if api_name in api_tests:
                    api_data = api_tests[api_name]()
                    
                    if api_data and len(api_data) > 0:
                        # Standardize job data format
                        for job in api_data:
                            standardized_job = {
                                'id': job.get('id', f"{api_name}_{len(all_jobs)}"),
                                'title': job.get('title', 'Unknown Title'),
                                'company': job.get('company', 'Unknown Company'),
                                'location': job.get('location', 'Unknown Location'),
                                'salary_min': job.get('salary_min'),
                                'salary_max': job.get('salary_max'),
                                'description': job.get('description', ''),
                                'source': api_name,
                                'posted_date': job.get('posted_date', datetime.now().isoformat()),
                                'url': job.get('url'),
                                'remote_allowed': 'remote' in job.get('location', '').lower(),
                                'collected_at': datetime.now().isoformat()
                            }
                            all_jobs.append(standardized_job)
                        
                        collection_stats['sources_used'].append(api_name)
                        print(f"✅ Collected {len(api_data)} jobs from {api_name}")
                
            except Exception as e:
                print(f"❌ Error collecting from {api_name}: {str(e)}")
        
        collection_stats['total_jobs'] = len(all_jobs)
        
        return {
            'jobs': all_jobs,
            'collection_stats': collection_stats
        }

@app.route('/health', methods=['GET'])
def comprehensive_health_check():
    """
    Main health check endpoint that N8N will call
    Tests all APIs and returns comprehensive health report
    """
    checker = APIHealthChecker()
    
    # Define how to test each API using correct function signatures
    api_tests = {
        'adzuna': lambda: checker.integrator.get_adzuna_jobs('python', 'us'),
        'reed': lambda: checker.integrator.get_reed_jobs('python', 'remote'),
        'muse': lambda: checker.integrator.get_muse_jobs('python', 'remote'),
        'coursera': lambda: checker.integrator.get_coursera_courses('python'),
        'rapidapi': lambda: checker.integrator.get_rapidapi_jobs('python', 'remote'),
        'theirstack': lambda: checker.integrator.get_theirstack_jobs('python', 'remote')
    }
    
    health_results = {}
    healthy_apis = []
    unhealthy_apis = []
    
    # Test each API one by one
    print("🔍 Testing APIs...")
    for api_name, test_func in api_tests.items():
        print(f"   Testing {api_name}...")
        result = checker.check_api_health(api_name, test_func)
        health_results[api_name] = result
        
        if result['status'] == 'healthy':
            healthy_apis.append(api_name)
            print(f"   ✅ {api_name}: {result['data_count']} records in {result['response_time_seconds']}s")
        else:
            unhealthy_apis.append(api_name)
            print(f"   ❌ {api_name}: {result['error']}")
    
    # Calculate overall system health
    total_apis = len(api_tests)
    healthy_count = len(healthy_apis)
    health_percentage = round((healthy_count / total_apis) * 100, 1)
    
    # Return comprehensive health report
    return jsonify({
        'overall_status': 'healthy' if healthy_count >= 2 else 'degraded',
        'health_percentage': health_percentage,
        'healthy_apis': healthy_apis,
        'unhealthy_apis': unhealthy_apis,
        'healthy_count': healthy_count,
        'total_apis': total_apis,
        'use_backup': healthy_count < 2,
        'detailed_results': health_results,
        'timestamp': datetime.utcnow().isoformat(),
        'service_version': '1.0.0'
    })

@app.route('/health/simple', methods=['GET'])
def simple_health_check():
    """Simple endpoint to check if the service itself is running"""
    return jsonify({
        'status': 'service_running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/collect-jobs', methods=['GET'])
def collect_jobs():
    """Collect actual job data from healthy APIs"""
    try:
        # Get query parameters
        queries = request.args.getlist('queries') or ['data science', 'software engineer', 'python developer']
        
        print(f"🔄 Starting job collection with queries: {queries}")
        
        # Create health checker instance
        checker = APIHealthChecker()
        
        # Use the health checker to collect job data
        job_data = checker.collect_job_data(queries)
        
        return jsonify({
            'success': True,
            'message': f"Successfully collected {job_data['collection_stats']['total_jobs']} jobs",
            'data': job_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error in job collection: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

if __name__ == '__main__':
    print("🏥 Starting Professional API Health Service...")
    print("📊 Main endpoint: http://localhost:5679/health")
    print("⚡ Simple endpoint: http://localhost:5679/health/simple")
    print("🚀 Job collection endpoint: http://localhost:5679/collect-jobs")
    print("🔄 Service will test all 6 APIs and provide real health data")
    app.run(host='localhost', port=5679, debug=True)
