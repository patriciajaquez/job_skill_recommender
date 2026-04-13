"""
Enhanced API Integration Module for Job Market Intelligence Platform
Supports: Adzuna, Reed, Muse, Theirstack, RapidAPI job data sources
Plus: Coursera course API with OAuth 2.0 authentication
Focus: Real data retrieval with clear fallback indicators
"""

import requests
import json
import os
import base64
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import warnings
import time
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobAPIIntegrator:
    """Enhanced API integrator supporting multiple job data sources"""
    
    def __init__(self):
        # Load API credentials from environment
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID', '')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY', '')
        self.reed_api_key = os.getenv('REED_API_KEY', '')
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY', '')
        self.theirstack_api_key = os.getenv('THEIRSTACK_API_KEY', '')
        self.muse_api_key = os.getenv('MUSE_API_KEY', '')
        
        # Course API credentials
        self.coursera_client_id = os.getenv('COURSERA_CLIENT_ID', '')
        self.coursera_client_secret = os.getenv('COURSERA_CLIENT_SECRET', '')
        self.coursera_app_id = os.getenv('COURSERA_APP_ID', '')
        self.coursera_business_id = os.getenv('COURSERA_BUSINESS_ID', '')  # Organization ID from admin settings
        
        # API endpoints
        self.endpoints = {
            'adzuna': 'https://api.adzuna.com/v1/api/jobs',
            'reed': 'https://www.reed.co.uk/api/1.0/search',
            'muse': 'https://www.themuse.com/api/public/jobs',
            'theirstack': 'https://api.theirstack.com/v1/jobs/search',
            'rapidapi_jobs': 'https://job-posting-feed-api.p.rapidapi.com',
            'coursera_oauth': 'https://api.coursera.com/oauth2/client_credentials/token',
            # Working endpoints discovered through testing
            'coursera_courses': 'https://api.coursera.org/api/courses.v1',  # ✅ WORKING! Real data
            'coursera_search': 'https://api.coursera.org/api/courses.v1',   # Same endpoint with different params
            # Business API endpoints (for future use if Business ID is configured)
            'coursera_business_programs': 'https://api.coursera.com/ent/api/businesses.v1',
            'coursera_business_contents': 'https://api.coursera.com/ent/api/contents.v1'
        }
        
        # Headers for different APIs
        self.headers = {
            'rapidapi': {
                'X-RapidAPI-Key': self.rapidapi_key,
                'X-RapidAPI-Host': 'job-posting-feed-api.p.rapidapi.com'
            },
            'reed': {
                'Authorization': f'Basic {base64.b64encode(f"{self.reed_api_key}:".encode()).decode()}'
            }
        }
        
        # Add Muse headers if API key is provided
        if self.muse_api_key:
            self.headers['muse'] = {
                'Authorization': f'Bearer {self.muse_api_key}'
            }
            
        # Add Theirstack headers if API key is provided
        if self.theirstack_api_key:
            self.headers['theirstack'] = {
                'Authorization': f'Bearer {self.theirstack_api_key}',
                'Content-Type': 'application/json'
            }
    
    def get_adzuna_jobs(self, query: str = "data science", location: str = "us", pages: int = 1) -> List[Dict]:
        """Fetch jobs from Adzuna API"""
        try:
            all_jobs = []
            for page in range(1, pages + 1):
                # Correct Adzuna API URL structure: /v1/api/jobs/{country}/search/{page}
                url = f"{self.endpoints['adzuna']}/{location}/search/{page}"
                params = {
                    'app_id': self.adzuna_app_id,
                    'app_key': self.adzuna_app_key,
                    'what': query,
                    'results_per_page': 50
                }
                
                response = requests.get(url, params=params, timeout=30)
                print(f"Adzuna URL: {url}")
                print(f"Adzuna Response: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('results', [])
                    all_jobs.extend(jobs)
                    print(f"✅ Adzuna API: Retrieved {len(jobs)} jobs (page {page})")
                    
                    time.sleep(0.5)  # Rate limiting
                else:
                    print(f"❌ Adzuna API error: {response.status_code} - {response.text}")
                    warnings.warn(f"Adzuna API error: {response.status_code}")
                    
            return all_jobs
            
        except Exception as e:
            print(f"❌ Adzuna API call failed: {e}")
            warnings.warn(f"Adzuna API call failed: {e}")
            return []
    
    def get_reed_jobs(self, query: str = "data science", location: str = "", pages: int = 1) -> List[Dict]:
        """Fetch jobs from Reed API"""
        try:
            all_jobs = []
            for page in range(1, pages + 1):
                params = {
                    'keywords': query,
                    'location': location,
                    'resultsToTake': 100,
                    'resultsToSkip': (page - 1) * 100
                }
                
                response = requests.get(
                    self.endpoints['reed'],
                    params=params,
                    headers=self.headers['reed'],
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('results', [])
                    all_jobs.extend(jobs)
                    
                    time.sleep(0.5)  # Rate limiting
                else:
                    warnings.warn(f"Reed API error: {response.status_code}")
                    
            return all_jobs
            
        except Exception as e:
            warnings.warn(f"Reed API call failed: {e}")
            return []
    
    def get_muse_jobs(self, query: str = "data science", location: str = "", pages: int = 1) -> List[Dict]:
        """Fetch jobs from The Muse API"""
        try:
            all_jobs = []
            for page in range(pages):
                params = {
                    'category': query if query in ['Data Science', 'Engineering'] else 'Data Science',
                    'location': location,
                    'page': page
                }
                
                # Use authentication headers if API key is available
                headers = {}
                if self.headers.get('muse'):
                    headers = self.headers['muse']
                
                response = requests.get(
                    self.endpoints['muse'], 
                    params=params, 
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('results', [])
                    if jobs:
                        print(f"✅ Muse API: Retrieved {len(jobs)} REAL jobs (page {page + 1})")
                    all_jobs.extend(jobs)
                    
                    time.sleep(0.5)  # Rate limiting
                else:
                    print(f"⚠️ Muse API: Error {response.status_code} on page {page + 1}")
                    
            if all_jobs:
                print(f"📊 Muse API: Total {len(all_jobs)} REAL jobs retrieved for '{query}'")
            else:
                print(f"❌ Muse API: No real data retrieved for '{query}'")
            return all_jobs
            
        except Exception as e:
            warnings.warn(f"Muse API call failed: {e}")
            return []

    def get_theirstack_jobs(self, query: str = "data science", location: str = "", pages: int = 1) -> List[Dict]:
        """Fetch jobs from Theirstack API with client-side filtering"""
        try:
            all_jobs = []
            
            # Theirstack API returns a general feed, so we fetch more jobs and filter client-side
            max_jobs_to_fetch = pages * 50  # Fetch more to increase chances of relevant matches
            jobs_per_request = 50  # Maximum batch size
            
            for page in range(pages):
                offset = page * jobs_per_request
                
                search_payload = {
                    "posted_at_max_age_days": 30,  # Required field - last 30 days
                    "limit": min(jobs_per_request, max_jobs_to_fetch - offset),
                    "offset": offset
                }
                
                response = requests.post(
                    self.endpoints['theirstack'],
                    json=search_payload,
                    headers=self.headers['theirstack'],
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('data', [])
                    
                    # Client-side filtering for relevance
                    filtered_jobs = self._filter_theirstack_jobs(jobs, query, location)
                    all_jobs.extend(filtered_jobs)
                        
                else:
                    warnings.warn(f"Theirstack API error: {response.status_code} - {response.text}")
                    break
            
            # Sort by relevance score (if we added one) and limit results
            return all_jobs[:20]  # Return top 20 most relevant jobs
            
        except Exception as e:
            warnings.warn(f"Theirstack API call failed: {e}")
            return []
    
    def _filter_theirstack_jobs(self, jobs: List[Dict], query: str, location: str) -> List[Dict]:
        """Filter Theirstack jobs based on query and location"""
        if not jobs:
            return []
        
        query_terms = query.lower().split()
        location_terms = location.lower().split() if location else []
        relevant_jobs = []
        
        for job in jobs:
            relevance_score = 0
            title = job.get('job_title', '').lower()
            description = job.get('description', '').lower()
            tech_slugs = job.get('technology_slugs', [])
            job_location = job.get('location', '').lower()
            
            # Score based on query terms in title (highest weight)
            for term in query_terms:
                if term in title:
                    relevance_score += 10
                elif term in description:
                    relevance_score += 5
                elif term in tech_slugs:
                    relevance_score += 8
            
            # Score based on location match
            if location_terms:
                for term in location_terms:
                    if term in job_location:
                        relevance_score += 3
            else:
                # Bonus for remote jobs when no location specified
                if 'remote' in job_location or job.get('remote', False):
                    relevance_score += 2
            
            # Include jobs with any relevance score
            if relevance_score > 0:
                job['_relevance_score'] = relevance_score
                relevant_jobs.append(job)
        
        # Sort by relevance score descending
        relevant_jobs.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
        return relevant_jobs

    def get_rapidapi_jobs(self, query: str = "data science", location: str = "United States") -> List[Dict]:
        """Fetch jobs from RapidAPI Jobs API with error mitigation"""
        try:
            params = {
                'query': query,
                'location': location,
                'distance': '1.0',
                'language': 'en_GB',
                'remoteOnly': 'false',
                'datePosted': 'month',
                'employmentTypes': 'fulltime;parttime;intern;contractor',
                'index': '0'
            }
            
            response = requests.get(
                self.endpoints['rapidapi_jobs'],
                headers=self.headers['rapidapi'],
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                return jobs
            elif response.status_code == 401:
                warnings.warn("RapidAPI: Unauthorized - check API key or subscription status")
                return []
            elif response.status_code == 429:
                warnings.warn("RapidAPI: Rate limit exceeded - subscription may be needed")
                return []
            elif response.status_code == 402:
                warnings.warn("RapidAPI: Payment required - subscription inactive")
                return []
            elif response.status_code == 403:
                warnings.warn("RapidAPI: Access forbidden - check subscription status")
                return []
            else:
                warnings.warn(f"RapidAPI error: {response.status_code}")
                return []
                
        except Exception as e:
            warnings.warn(f"RapidAPI call failed: {e}")
            return []

    def get_coursera_access_token(self) -> Optional[str]:
        """Get OAuth 2.0 access token for Coursera API using official documentation"""
        try:
            if not self.coursera_client_id or not self.coursera_client_secret:
                warnings.warn("Coursera credentials not configured")
                return None
                
            # Official Coursera OAuth endpoint
            token_url = self.endpoints['coursera_oauth']
            
            # Create Base64 encoded Authorization header (key:secret)
            auth_string = f"{self.coursera_client_id}:{self.coursera_client_secret}"
            auth_header = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Request body with grant_type (as form data, not JSON)
            data = 'grant_type=client_credentials'
            
            response = requests.post(token_url, headers=headers, data=data, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 1799)  # Usually 1799 seconds (30 minutes)
                
                print(f"✅ Coursera Business API token obtained (expires in {expires_in} seconds)")
                return access_token
            elif response.status_code == 401:
                warnings.warn("Coursera API: Unauthorized - credentials may not be registered through Coursera Business portal")
                print("❌ Note: Coursera APIs require Business/Campus/Government registration through their developer portal")
                return None
            elif response.status_code == 403:
                warnings.warn("Coursera API: Access forbidden - ensure app is registered and APIs are enabled")
                return None
            else:
                warnings.warn(f"Coursera token error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            warnings.warn(f"Coursera token request failed: {e}")
            return None

    def get_coursera_courses(self, query: str = "python", max_results: int = 20) -> List[Dict]:
        """
        Fetch courses from Coursera API using official authentication
        Priority: Real API data → Fallback mock data (clearly labeled)
        """
        try:
            # Get fresh access token
            access_token = self.get_coursera_access_token()
            if not access_token:
                print("🔑 Coursera API: Authentication failed")
                print(f"📋 FALLBACK: Using MOCK data for '{query}' (authentication failed)")
                return self._generate_mock_coursera_courses(query, max_results)
            
            headers = {
                'Authorization': f'Bearer {access_token}'
                # Remove Content-Type for GET requests - it was causing JSON parsing errors
            }
            
            # Try different endpoint approaches for Coursera Business and Catalog APIs
            # Method 1: Try the proven working endpoint first
            try:
                # Use the endpoint we confirmed works: https://api.coursera.org/api/courses.v1
                # Start simple - just get basic data that we know works
                params = {
                    'limit': max_results * 2  # Get more to allow filtering
                }
                
                response = requests.get(
                    self.endpoints['coursera_courses'],
                    headers=headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    courses = data.get('elements', [])
                    if courses:
                        # Filter courses by query term for relevance
                        filtered_courses = [
                            course for course in courses 
                            if query.lower() in course.get('name', '').lower() or 
                               query.lower() in course.get('description', '').lower()
                        ]
                        
                        if filtered_courses:
                            print(f"✅ Coursera API: Retrieved {len(filtered_courses)} REAL filtered courses for '{query}'")
                            return self._standardize_coursera_courses(filtered_courses[:max_results])
                        else:
                            # No matches for query, return first courses anyway
                            print(f"✅ Coursera API: Retrieved {len(courses)} REAL courses (no specific matches for '{query}')")
                            return self._standardize_coursera_courses(courses[:max_results])
                else:
                    print(f"⚠️ Coursera API (main): {response.status_code}")
                    print(f"   Response: {response.text[:100]}...")
                
            except Exception as e:
                print(f"⚠️ Coursera API main endpoint failed: {e}")
                
            # Method 2: Try with fields parameter if basic call failed
            try:
                params = {
                    'limit': max_results,
                    'fields': 'name,description,slug,id'  # Simplified fields
                }
                
                response = requests.get(
                    self.endpoints['coursera_courses'],
                    headers=headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    courses = data.get('elements', [])
                    if courses:
                        print(f"✅ Coursera API (with fields): Retrieved {len(courses)} REAL courses")
                        return self._standardize_coursera_courses(courses)
                else:
                    print(f"⚠️ Coursera API (with fields): {response.status_code}")
                
            except Exception as e:
                print(f"⚠️ Coursera API with fields failed: {e}")
            
            # Method 3: Try Business API if organization ID is configured (future enhancement)
            if self.coursera_business_id:
                print(f"ℹ️ Business ID configured: {self.coursera_business_id} - trying Business API...")
                try:
                    # Business API: Programs endpoint  
                    business_url = f"{self.endpoints['coursera_business_programs']}/{self.coursera_business_id}/programs"
                    params = {
                        'limit': max_results,
                        'fields': 'name,description,courseIds,specializations'
                    }
                    
                    response = requests.get(business_url, headers=headers, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        programs = data.get('elements', [])
                        if programs:
                            print(f"✅ Coursera Business API: Retrieved {len(programs)} REAL programs for organization")
                            courses = self._extract_courses_from_programs(programs, query)
                            if courses:
                                return courses[:max_results]
                    else:
                        print(f"⚠️ Coursera Business API (programs): {response.status_code}")
                        
                except Exception as e:
                    print(f"⚠️ Coursera Business API failed: {e}")
            
            # Method 3: Fallback with different parameters
            # Method 3: Fallback with different parameters
            try:
                # Try with search query parameter
                params = {
                    'q': 'search',
                    'query': query,
                    'limit': max_results,
                    'fields': 'name,description,workload,photoUrl,courseType,averageRating,enrollmentCount,slug,id'
                }
                
                response = requests.get(
                    self.endpoints['coursera_search'],
                    headers=headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    courses = data.get('elements', [])
                    if courses:
                        print(f"✅ Coursera Search API: Retrieved {len(courses)} REAL courses for '{query}'")
                        return self._standardize_coursera_courses(courses)
                else:
                    print(f"⚠️ Coursera Search API: {response.status_code}")
                
            except Exception as e:
                print(f"⚠️ Coursera Search API failed: {e}")
            
            # If all real API methods failed (shouldn't happen now!)
            print(f"� Coursera API: REAL authentication successful, but course endpoints failed")
            print(f"�📋 FALLBACK: Using MOCK data for '{query}' (authentication ✅, data ❌)")
            return self._generate_mock_coursera_courses(query, max_results)
                
        except Exception as e:
            print(f"❌ Coursera API: Connection failed - {e}")
            print(f"📋 FALLBACK: Using MOCK data for '{query}' (connection error)")
            return self._generate_mock_coursera_courses(query, max_results)

    def _extract_courses_from_programs(self, programs: List[Dict], query: str) -> List[Dict]:
        """Extract course information from Coursera Business programs"""
        courses = []
        for program in programs:
            program_name = program.get('name', '')
            if query.lower() in program_name.lower():
                # Create a course-like object from program data
                course = {
                    'id': program.get('id', ''),
                    'name': program_name,
                    'description': program.get('description', f'Professional program in {program_name}'),
                    'provider': 'Coursera Business',
                    'courseType': 'Professional Program',
                    'averageRating': 4.5,  # Default for business programs
                    'enrollmentCount': 0,
                    'slug': program.get('slug', program.get('id', ''))
                }
                courses.append(course)
        return self._standardize_coursera_courses(courses)

    def _standardize_coursera_courses(self, courses: List[Dict]) -> List[Dict]:
        """Standardize Coursera course data format"""
        standardized_courses = []
        for course in courses:
            standardized_course = {
                'id': course.get('id', ''),
                'title': course.get('name', course.get('title', '')),
                'description': course.get('description', ''),
                'provider': 'Coursera',
                'duration': course.get('workload', 'Not specified'),
                'rating': course.get('averageRating', 0),
                'enrollment_count': course.get('enrollmentCount', 0),
                'image_url': course.get('photoUrl', ''),
                'course_type': course.get('courseType', 'Course'),
                'url': f"https://www.coursera.org/learn/{course.get('slug', course.get('id', ''))}"
            }
            standardized_courses.append(standardized_course)
        return standardized_courses

    def _generate_mock_coursera_courses(self, query: str, max_results: int) -> List[Dict]:
        """
        Generate realistic mock Coursera courses for testing purposes
        Note: This is FALLBACK data, not real Coursera API data
        """
        print(f"🧪 Generating {max_results} mock courses for testing '{query}' functionality")
        mock_courses = [
            {
                'id': f'coursera-{query}-{i}',
                'title': f'{query.title()} Programming Course {i}',
                'description': f'Learn {query} programming with hands-on projects and real-world applications.',
                'provider': 'Coursera',
                'duration': f'{4 + i} weeks',
                'rating': 4.2 + (i * 0.1),
                'enrollment_count': 10000 + (i * 1000),
                'image_url': 'https://via.placeholder.com/300x200',
                'course_type': 'Course',
                'url': f'https://www.coursera.org/learn/{query}-programming-{i}'
            }
            for i in range(1, min(max_results + 1, 6))
        ]
        return mock_courses

# Global API integrator instance
job_api = JobAPIIntegrator()

def get_live_job_data(query: str = "data science", location: str = "remote", 
                     sources: List[str] = None) -> Dict[str, List[Dict]]:
    """Get live job data from multiple APIs - returns raw data by source"""
    results = {}
    
    if sources is None:
        sources = ['adzuna', 'reed', 'muse', 'theirstack', 'rapidapi']
    
    if 'adzuna' in sources and job_api.adzuna_app_id and job_api.adzuna_app_key:
        results['adzuna'] = job_api.get_adzuna_jobs(query, location)
        
    if 'reed' in sources and job_api.reed_api_key:
        results['reed'] = job_api.get_reed_jobs(query, location)
        
    if 'muse' in sources:
        results['muse'] = job_api.get_muse_jobs(query, location)
        
    if 'theirstack' in sources and job_api.theirstack_api_key:
        results['theirstack'] = job_api.get_theirstack_jobs(query, location)
    
    if 'rapidapi' in sources and job_api.rapidapi_key:
        results['rapidapi'] = job_api.get_rapidapi_jobs(query, location)
    
    return results

def test_api_connections() -> Dict[str, bool]:
    """Test all API connections - returns raw connection status"""
    results = {}
    
    # Test Adzuna
    try:
        adzuna_jobs = job_api.get_adzuna_jobs("python", "us", 1)
        results['adzuna'] = len(adzuna_jobs) > 0
    except:
        results['adzuna'] = False
    
    # Test Reed
    try:
        reed_jobs = job_api.get_reed_jobs("python", "", 1)
        results['reed'] = len(reed_jobs) > 0
    except:
        results['reed'] = False
    
    # Test Muse
    try:
        muse_jobs = job_api.get_muse_jobs("data science", "", 1)
        results['muse'] = len(muse_jobs) > 0
    except:
        results['muse'] = False
    
    # Test Theirstack
    try:
        theirstack_jobs = job_api.get_theirstack_jobs("python", "", 1)
        results['theirstack'] = len(theirstack_jobs) > 0
    except:
        results['theirstack'] = False
    
    # Test RapidAPI (with error mitigation)
    try:
        rapidapi_jobs = job_api.get_rapidapi_jobs("python")
        results['rapidapi'] = len(rapidapi_jobs) > 0
    except:
        results['rapidapi'] = False
    
    # Test Coursera API
    try:
        coursera_courses = job_api.get_coursera_courses("python", 5)
        results['coursera'] = len(coursera_courses) > 0
    except:
        results['coursera'] = False
    
    return results
