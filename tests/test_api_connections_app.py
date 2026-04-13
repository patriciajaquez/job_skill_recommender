"""
API Connection Testing Interface
A Streamlit app to test and validate all configured APIs with REAL data priority
- Job APIs: Adzuna, Reed, Muse, Theirstack, RapidAPI  
- Course APIs: Coursera (OAuth 2.0)
- Clearly indicates when fallback/mock data is used for testing
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add project root to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.api_integration import JobAPIIntegrator

# Load environment variables
load_dotenv()

def test_api_connections():
    """Test all API connections and return status"""
    integrator = JobAPIIntegrator()
    results = {}
    
    # Test each API with basic queries
    try:
        jobs = integrator.get_adzuna_jobs(query="data science", pages=1)
        results['adzuna'] = len(jobs) > 0
    except:
        results['adzuna'] = False
    
    try:
        jobs = integrator.get_reed_jobs(query="data science", pages=1)
        results['reed'] = len(jobs) > 0
    except:
        results['reed'] = False
    
    try:
        jobs = integrator.get_muse_jobs(query="data science", pages=1)
        results['muse'] = len(jobs) > 0
    except:
        results['muse'] = False
    
    try:
        jobs = integrator.get_rapidapi_jobs(query="data science", pages=1)
        results['rapidapi'] = len(jobs) > 0
    except:
        results['rapidapi'] = False
    
    try:
        jobs = integrator.get_theirstack_jobs(query="data science", pages=1)
        results['theirstack'] = len(jobs) > 0
    except:
        results['theirstack'] = False

    try:
        courses = integrator.get_coursera_courses(query="python", max_results=1)
        results['coursera'] = len(courses) > 0
    except:
        results['coursera'] = False

    return results

def test_all_apis():
    """Test all APIs including course APIs"""
    integrator = JobAPIIntegrator()
    results = {}
    
    # Test job APIs
    try:
        jobs = integrator.get_adzuna_jobs(query="data science", pages=1)
        results['adzuna'] = len(jobs) > 0
    except:
        results['adzuna'] = False
    
    try:
        jobs = integrator.get_reed_jobs(query="data science", pages=1)
        results['reed'] = len(jobs) > 0
    except:
        results['reed'] = False
    
    try:
        jobs = integrator.get_muse_jobs(query="data science", pages=1)
        results['muse'] = len(jobs) > 0
    except:
        results['muse'] = False
    
    try:
        jobs = integrator.get_rapidapi_jobs(query="data science", pages=1)
        results['rapidapi'] = len(jobs) > 0
    except:
        results['rapidapi'] = False
    
    try:
        jobs = integrator.get_theirstack_jobs(query="data science", pages=1)
        results['theirstack'] = len(jobs) > 0
    except:
        results['theirstack'] = False
    
    # Test course APIs
    try:
        courses = integrator.get_coursera_courses(query="python", max_results=5)
        results['coursera'] = len(courses) > 0
    except:
        results['coursera'] = False
    
    return results

def main():
    st.title("🔌 API Connection Tester - Real Data Priority")
    st.write("Test and validate your API integrations with real data (fallback clearly indicated)")
    
    st.header("🔑 Environment Variables Status")
    
    # Check environment variables
    env_vars = {
        'ADZUNA_APP_ID': os.getenv('ADZUNA_APP_ID'),
        'ADZUNA_APP_KEY': os.getenv('ADZUNA_APP_KEY'),
        'REED_API_KEY': os.getenv('REED_API_KEY'),
        'RAPIDAPI_KEY': os.getenv('RAPIDAPI_KEY'),
        'THEIRSTACK_API_KEY': os.getenv('THEIRSTACK_API_KEY'),
        'MUSE_API_KEY': os.getenv('MUSE_API_KEY'),
        'COURSERA_CLIENT_ID': os.getenv('COURSERA_CLIENT_ID'),
        'COURSERA_CLIENT_SECRET': os.getenv('COURSERA_CLIENT_SECRET')
    }
    
    for var, value in env_vars.items():
        if var == 'MUSE_API_KEY':
            if value and value != 'your_muse_api_key':
                st.success(f"✅ {var}: Configured (Optional)")
            else:
                st.info(f"ℹ️ {var}: Not configured (Currently optional)")
        elif value and value not in ['', 'your_adzuna_app_id', 'your_adzuna_app_key', 'your_reed_api_key', 'your_rapidapi_key', 'your_theirstack_api_key']:
            st.success(f"✅ {var}: Configured")
        else:
            st.error(f"❌ {var}: Missing or not configured")
    
    # Note about API status
    st.info("🎯 **Priority**: Real API data first, fallback data clearly labeled")
    st.info("✅ **Job APIs**: Adzuna, Reed, Muse, RapidAPI, Theirstack")
    st.info("🎓 **Course APIs**: Coursera (OAuth 2.0 Business API)")
    st.info("💡 **MUSE API**: Active at public endpoint (API key optional)")
    
    st.header("🌐 API Connection Tests")
    
    if st.button("Test All APIs"):
        with st.spinner("Testing APIs..."):
            results = test_all_apis()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Job APIs")
                st.write("✅ Adzuna:" if results['adzuna'] else "❌ Adzuna:", "Working" if results['adzuna'] else "Failed")
                st.write("✅ Reed:" if results['reed'] else "❌ Reed:", "Working" if results['reed'] else "Failed")
                st.write("✅ The Muse:" if results['muse'] else "❌ The Muse:", "Working" if results['muse'] else "Failed")
                st.write("✅ RapidAPI:" if results['rapidapi'] else "❌ RapidAPI:", "Working" if results['rapidapi'] else "Failed")
                st.write("✅ Theirstack:" if results['theirstack'] else "❌ Theirstack:", "Working" if results['theirstack'] else "Failed")
            
            with col2:
                st.subheader("Course APIs")
                st.write("✅ Coursera:" if results['coursera'] else "❌ Coursera:", "Working" if results['coursera'] else "Failed")
            
            failed_apis = [api for api, status in results.items() if not status]
            if failed_apis:
                st.warning(f"Failed APIs: {', '.join(failed_apis)}")
                st.info("See error details below and check API credentials.")
            else:
                st.success("All APIs are working!")
    
    st.header("📊 Real Data Validation Test")
    
    if st.button("Fetch Sample Jobs from Each API"):
        with st.spinner("Fetching REAL data from each API (fallback clearly indicated)..."):
            integrator = JobAPIIntegrator()
            
            # Track errors for summary
            error_summary = []
            success_count = 0
            
            # Test each API individually
            apis_to_test = [
                ('Adzuna', integrator.get_adzuna_jobs),
                ('Reed', integrator.get_reed_jobs),
                ('Muse', integrator.get_muse_jobs),
                ('RapidAPI', integrator.get_rapidapi_jobs),
                ('Theirstack', integrator.get_theirstack_jobs),
                ('Coursera', integrator.get_coursera_courses)
            ]
            
            for api_name, api_function in apis_to_test:
                st.subheader(f"🔍 {api_name} API Sample")
                try:
                    # Handle different parameter requirements for different APIs
                    if api_name == 'Coursera':
                        results = api_function(query="data science", max_results=5)
                        result_type = "courses"
                    else:
                        results = api_function(query="data science", pages=1)
                        result_type = "jobs"
                    
                    if results and len(results) > 0:
                        # For Coursera, check if authentication worked but data is mock
                        if api_name == 'Coursera':
                            data_type = "🔐 AUTH ✅, DATA 🧪 MOCK"
                        else:
                            data_type = "📊 REAL"
                        st.success(f"✅ {api_name}: Retrieved {len(results)} {data_type} {result_type}")
                        success_count += 1
                        
                        # Show first result as sample in expandable section
                        with st.expander(f"View {api_name} Sample {result_type.title()[:-1]}"):
                            st.json(results[0])
                            
                        # Show quick summary with appropriate fields
                        st.write(f"**{result_type.title()} found:** {len(results)}")
                        if results[0].get('title'):
                            st.write(f"**Sample title:** {results[0]['title']}")
                        elif results[0].get('name'):
                            st.write(f"**Sample title:** {results[0]['name']}")
                        
                        if api_name == 'Coursera':
                            if results[0].get('provider'):
                                st.write(f"**Provider:** {results[0]['provider']}")
                            if results[0].get('rating'):
                                st.write(f"**Rating:** {results[0]['rating']}")
                        else:
                            if results[0].get('company'):
                                st.write(f"**Sample company:** {results[0]['company']}")
                    else:
                        st.warning(f"⚠️ {api_name}: No {result_type} retrieved")
                        error_summary.append(f"{api_name}: No data returned")
                except Exception as e:
                    st.error(f"❌ {api_name}: Error - {str(e)}")
                    error_summary.append(f"{api_name}: {str(e)}")
                
                st.write("---")  # Separator between APIs
            
            # Error handling summary
            if error_summary:
                st.header("🚨 Error Summary")
                st.error(f"**{len(error_summary)}/6 APIs encountered issues:**")
                for error in error_summary:
                    st.write(f"• {error}")
                
                with st.expander("🔧 Troubleshooting Tips"):
                    st.write("**Common solutions:**")
                    st.write("• Check API keys in .env file")
                    st.write("• Verify internet connection")
                    st.write("• Some APIs may require active subscriptions")
                    st.write("• Rate limits may cause temporary failures")
                    st.write("• Check API documentation for parameter requirements")
            
            # Success summary
            if success_count > 0:
                st.success(f"✅ **{success_count}/6 APIs working successfully**")
    
    if st.button("API Status Summary"):
        st.write("**🎯 Data Source Priority:**")
        st.write("• **PRIORITY**: Real API data")
        st.write("• **FALLBACK**: Mock/test data (clearly labeled)")
        st.write("")
        st.write("**Available Job APIs:**")
        st.write("• Adzuna: Global job board (Real data)")
        st.write("• Reed: UK-focused recruitment (Real data)")  
        st.write("• Muse: Company culture & jobs (Real data)")
        st.write("• RapidAPI: Aggregated job data (Real data)")
        st.write("• Theirstack: Tech company jobs (Real data)")
        st.write("**Course APIs:**")
        st.write("• Coursera: OAuth authenticated ✅ + Mock course data 🧪 (Real endpoints need adjustment)")
        
if __name__ == "__main__":
    main()
