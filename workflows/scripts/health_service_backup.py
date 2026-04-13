# workflows/scripts/health_service.py
from flask import Flask, jsonify, request
fr                # Collect more data for job collection vs health check
                if api_name == 'adzuna':
                    api_data = self.integrator.get_api_data(api_name, limit=100)
                elif api_name == 'reed':
                    api_data = self.integrator.get_api_data(api_name, limit=150)
                else:
                    api_data = self.integrator.get_api_data(api_name, limit=50)time import datetime
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
        
    def run_health_checks(self):
        """Run health checks on all APIs and return results"""
        print("Starting API health checks...")
        results = {}
        
        for api_name in self.apis:
            print(f"Checking {api_name}...")
            try:
                # Get API data to test health
                data = self.integrator.get_api_data(api_name, limit=50 if api_name in ['adzuna', 'reed'] else 20)
                
                if data and len(data) > 0:
                    results[api_name] = {
                        'status': 'healthy',
                        'data_count': len(data),
                        'last_checked': datetime.now().isoformat(),
                        'response_time_seconds': round(time.time() - time.time(), 2)  # Placeholder
                    }
                    print(f"✅ {api_name}: {len(data)} items")
                else:
                    results[api_name] = {
                        'status': 'unhealthy',
                        'error': 'No data returned',
                        'last_checked': datetime.now().isoformat(),
                        'response_time_seconds': round(time.time() - time.time(), 2)
                    }
                    print(f"❌ {api_name}: No data")
                    
            except Exception as e:
                results[api_name] = {
                    'status': 'unhealthy',
                    'error': str(e),
                    'last_checked': datetime.now().isoformat(),
                    'response_time_seconds': 0
                }
                print(f"❌ {api_name}: {str(e)}")
        
        return results

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
        
        # Only collect from healthy APIs
        health_results = self.run_health_checks()
        healthy_apis = [api for api, result in health_results.items() if result['status'] == 'healthy']
        
        print(f"Collecting from healthy APIs: {healthy_apis}")
        
        for api_name in healthy_apis:
            try:
                print(f"Collecting jobs from {api_name}...")
                # Collect more data for job collection vs health check
                if api_name == 'adzuna':
                    api_data = self.api_integrator.get_api_data(api_name, limit=100)
                elif api_name == 'reed':
                    api_data = self.api_integrator.get_api_data(api_name, limit=150)
                else:
                    api_data = self.api_integrator.get_api_data(api_name, limit=50)
                
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
            'collection_stats': collection_stats,
            'health_status': health_results
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
    print("🔄 Service will test all 6 APIs and provide real health data")
    app.run(host='localhost', port=5679, debug=True)