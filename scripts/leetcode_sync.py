#!/usr/bin/env python3
# scripts/leetcode_sync.py

import os
import json
import time
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import re
import sys

class LeetCodeSync:
    def __init__(self):
        self.username = os.environ.get('LEETCODE_USERNAME')
        self.password = os.environ.get('LEETCODE_PASSWORD')
        self.base_dir = 'leetcode-solutions'
        self.metadata_file = 'metadata/submissions.json'
        
        print(f"🔐 Username loaded: {'✅' if self.username else '❌'}")
        print(f"🔐 Password loaded: {'✅' if self.password else '❌'}")
        
        if not self.username or not self.password:
            print("❌ Missing credentials! Check your GitHub secrets.")
            sys.exit(1)
        
        # Ensure directories exist
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs('metadata', exist_ok=True)
        print(f"📁 Created directories: {self.base_dir}, metadata")
        
    def setup_driver(self):
        """Setup Chrome driver with headless options"""
        print("🚀 Setting up Chrome driver...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            # Try to use system Chrome
            driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver setup successful")
            return driver
        except Exception as e:
            print(f"❌ Chrome driver setup failed: {e}")
            raise
    
    def login_leetcode(self, driver):
        """Login to LeetCode"""
        print("🔑 Attempting to login to LeetCode...")
        
        try:
            driver.get('https://leetcode.com/accounts/login/')
            print("📄 Loaded login page")
            
            # Wait for login form - try multiple selectors
            print("⏳ Waiting for login form...")
            
            username_field = None
            password_field = None
            
            # Try different selectors for username field
            username_selectors = [
                'input[name="login"]',
                'input[name="username"]', 
                'input[type="email"]',
                'input[placeholder*="username"]',
                'input[placeholder*="email"]'
            ]
            
            for selector in username_selectors:
                try:
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    username_field = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Found username field with: {selector}")
                    break
                except:
                    continue
            
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]'
            ]
            
            for selector in password_selectors:
                try:
                    password_field = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Found password field with: {selector}")
                    break
                except:
                    continue
            
            if not username_field or not password_field:
                print("❌ Could not find login form fields")
                return False
            
            username_field.clear()
            username_field.send_keys(self.username)
            
            password_field.clear()
            password_field.send_keys(self.password)
            
            print("📝 Filled login credentials")
            time.sleep(1)
            
            print("🔍 Looking for submit button...")
            submit_selectors = [
                '//button[@type="submit"]',
                '//button[contains(text(), "Sign In")]',
                '//button[contains(text(), "Log In")]',
                '//button[contains(@class, "btn-login")]',
                '//input[@type="submit"]',
                'button[data-cy="sign-in-btn"]',
                '.btn-signin',
                '.signin-btn'
            ]
            
            login_button = None
            for selector in submit_selectors:
                try:
                    if selector.startswith('//'):
                        login_button = driver.find_element(By.XPATH, selector)
                    else:
                        login_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Found submit button with: {selector}")
                    break
                except:
                    continue
            
            if not login_button:
                print("❌ Could not find submit button, trying Enter key...")
                try:
                    password_field.send_keys(Keys.RETURN)
                    print("🚀 Submitted using Enter key")
                except:
                    print("❌ Enter key method also failed")
                    return False
            else:
                # Use JS click for reliability
                driver.execute_script("arguments[0].click();", login_button)
                print("🚀 Submitted login form")
            
            # Wait for either successful login or error message
            print("⏳ Waiting for login redirect or error message...")
            time.sleep(5)
            
            # Check for error message
            error_selectors = [
                'div[class*="error"]',
                '.error-message',
                'div[role="alert"]'
            ]
            for err_selector in error_selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, err_selector)
                if elems:
                    error_text = elems[0].text
                    if error_text.strip():
                        print(f"❌ Login error message: {error_text}")
                        return False

            current_url = driver.current_url
            print(f"📍 Current URL after login: {current_url}")
            
            # Try to detect if logged in by presence of user avatar or dashboard
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.avatar, div[data-cy='user-info']"))
                )
                print("✅ Successfully logged in to LeetCode (user info detected)")
                return True
            except TimeoutException:
                print("❌ Login appears to have failed - still on login page or missing user info")
                return False
            
        except TimeoutException as e:
            print(f"⏰ Login timeout: {e}")
            return False
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def get_recent_submissions(self, driver):
        """Get recent accepted submissions"""
        print("📋 Fetching recent submissions...")
        
        try:
            # Navigate to submissions page
            driver.get('https://leetcode.com/submissions/') 
            print("📄 Loaded submissions page")
            
            # Wait for submissions to load - try multiple selectors
            print("⏳ Waiting for submissions to load...")
            
            # Try different possible selectors
            selectors = [
                '[data-cy="submission-item"]',
                '.submission-row',
                '.ReactVirtualized__Table__row',
                'tbody tr'
            ]
            
            submission_elements = []
            for selector in selectors:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    submission_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if submission_elements:
                        print(f"✅ Found submissions using selector: {selector}")
                        break
                except TimeoutException:
                    continue
            
            if not submission_elements:
                print("❌ No submissions found with any selector")
                return []
            
            submissions = []
            print(f"🔍 Processing {len(submission_elements)} submission elements...")
            
            for i, element in enumerate(submission_elements[:10]):  # Get last 10 submissions
                try:
                    print(f"Processing submission {i+1}...")
                    
                    # Try to get status - multiple approaches
                    status = None
                    status_selectors = [
                        '[data-cy="submission-status"]',
                        '.status-accepted',
                        'td:nth-child(3)',
                        '.text-green-s'
                    ]
                    
                    for status_selector in status_selectors:
                        try:
                            status_elem = element.find_element(By.CSS_SELECTOR, status_selector)
                            status = status_elem.text
                            break
                        except:
                            continue
                    
                    if not status or 'Accepted' not in status:
                        continue
                    
                    # Try to get problem title and URL
                    title_element = None
                    title_selectors = [
                        '[data-cy="submission-title"] a',
                        'td:nth-child(2) a',
                        '.title-cell a'
                    ]
                    
                    for title_selector in title_selectors:
                        try:
                            title_element = element.find_element(By.CSS_SELECTOR, title_selector)
                            break
                        except:
                            continue
                    
                    if not title_element:
                        print(f"⚠️ Could not find title for submission {i+1}")
                        continue
                    
                    problem_title = title_element.text
                    problem_url = title_element.get_attribute('href')
                    
                    # Try to get timestamp
                    timestamp = "unknown"
                    timestamp_selectors = [
                        '[data-cy="submission-time"]',
                        'td:nth-child(4)',
                        '.time-cell'
                    ]
                    
                    for timestamp_selector in timestamp_selectors:
                        try:
                            timestamp_element = element.find_element(By.CSS_SELECTOR, timestamp_selector)
                            timestamp = timestamp_element.text
                            break
                        except:
                            continue
                    
                    submissions.append({
                        'title': problem_title,
                        'url': problem_url,
                        'timestamp': timestamp,
                        'status': 'Accepted'
                    })
                    
                    print(f"✅ Found accepted submission: {problem_title}")
                    
                except Exception as e:
                    print(f"⚠️ Error parsing submission {i+1}: {e}")
                    continue
            
            print(f"📊 Found {len(submissions)} accepted submissions")
            return submissions
            
        except Exception as e:
            print(f"❌ Failed to get submissions: {e}")
            return []
    
    def get_submission_code(self, driver, submission_url):
        """Get the actual code from submission"""
        print(f"📄 Getting code from: {submission_url}")
        
        try:
            driver.get(submission_url)
            
            # Wait for code to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'code, pre, .view-lines'))
            )
            
            # Try different selectors for code
            code_selectors = [
                'code',
                'pre',
                '.view-lines',
                '.monaco-editor .view-lines'
            ]
            
            code = None
            for selector in code_selectors:
                try:
                    code_element = driver.find_element(By.CSS_SELECTOR, selector)
                    code = code_element.text
                    if code.strip():
                        break
                except:
                    continue
            
            if not code or not code.strip():
                print("❌ No code content found")
                return None, None
            
            # Try to get language
            language = "unknown"
            language_selectors = [
                '[data-cy="lang-select"] span',
                '.language-select',
                '.select-language'
            ]
            
            for lang_selector in language_selectors:
                try:
                    language_element = driver.find_element(By.CSS_SELECTOR, lang_selector)
                    language = language_element.text.lower()
                    break
                except:
                    continue
            
            print(f"✅ Found code in {language}")
            return code, language
            
        except Exception as e:
            print(f"❌ Failed to get submission code: {e}")
            return None, None
    
    def load_existing_metadata(self):
        """Load existing submissions metadata"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_metadata(self, metadata):
        """Save submissions metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def sanitize_filename(self, title):
        """Sanitize problem title for filename"""
        # Remove problem number and special characters
        title = re.sub(r'^\d+\.\s*', '', title)
        title = re.sub(r'[^\w\s-]', '', title)
        title = re.sub(r'[-\s]+', '-', title)
        return title.lower().strip('-')
    
    def get_language_extension(self, language):
        """Get file extension based on language"""
        extensions = {
            'python': '.py',
            'python3': '.py',
            'java': '.java',
            'cpp': '.cpp',
            'c++': '.cpp',
            'c': '.c',
            'javascript': '.js',
            'typescript': '.ts',
            'go': '.go',
            'rust': '.rs',
            'kotlin': '.kt',
            'scala': '.scala',
            'ruby': '.rb',
            'swift': '.swift',
            'php': '.php'
        }
        return extensions.get(language, '.txt')
    
    def create_solution_file(self, problem_title, code, language, problem_url):
        """Create solution file with code and metadata"""
        filename = self.sanitize_filename(problem_title)
        extension = self.get_language_extension(language)
        
        # Create language-specific directory
        lang_dir = os.path.join(self.base_dir, language)
        os.makedirs(lang_dir, exist_ok=True)
        
        filepath = os.path.join(lang_dir, f"{filename}{extension}")
        
        # Create file header comment
        header = f"""/*
Problem: {problem_title}
URL: {problem_url}
Language: {language}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Accepted
*/

"""
        
        # Adjust comment style based on language
        if language in ['python', 'python3']:
            header = f'''"""
Problem: {problem_title}
URL: {problem_url}
Language: {language}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Accepted
"""

'''
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + code)
        
        print(f"📁 Created: {filepath}")
        return filepath
    
    def sync_solutions(self):
        """Main sync function"""
        print("🚀 Starting LeetCode sync...")
        
        driver = None
        try:
            driver = self.setup_driver()
            
            if not self.login_leetcode(driver):
                print("❌ Login failed, exiting")
                return
            
            # Get recent submissions
            submissions = self.get_recent_submissions(driver)
            print(f"📊 Found {len(submissions)} accepted submissions")
            
            if not submissions:
                print("ℹ️ No accepted submissions found")
                return
            
            # Load existing metadata
            existing_metadata = self.load_existing_metadata()
            
            new_solutions = 0
            
            for submission in submissions:
                problem_key = f"{submission['title']}_{submission['timestamp']}"
                
                # Skip if already processed
                if problem_key in existing_metadata:
                    print(f"⏭️ Skipping already processed: {submission['title']}")
                    continue
                
                print(f"🔄 Processing: {submission['title']}")
                
                # Get submission code
                code, language = self.get_submission_code(driver, submission['url'])
                
                if code and language:
                    # Create solution file
                    filepath = self.create_solution_file(
                        submission['title'],
                        code,
                        language,
                        submission['url']
                    )
                    
                    # Update metadata
                    existing_metadata[problem_key] = {
                        'title': submission['title'],
                        'language': language,
                        'filepath': filepath,
                        'url': submission['url'],
                        'timestamp': submission['timestamp'],
                        'created_at': datetime.now().isoformat()
                    }
                    
                    new_solutions += 1
                    
                    # Add small delay to avoid rate limiting
                    time.sleep(2)
                else:
                    print(f"⚠️ Could not extract code for: {submission['title']}")
            
            # Save updated metadata
            self.save_metadata(existing_metadata)
            
            print(f"✅ Sync completed. Added {new_solutions} new solutions.")
            
        except Exception as e:
            print(f"❌ Sync failed with error: {e}")
            raise
        finally:
            if driver:
                driver.quit()
                print("🔚 Browser closed")

if __name__ == "__main__":
    try:
        sync = LeetCodeSync()
        sync.sync_solutions()
    except Exception as e:
        print(f"💥 Script failed: {e}")
        sys.exit(1)