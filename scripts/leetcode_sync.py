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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

class LeetCodeSync:
    def __init__(self):
        self.username = os.environ.get('LEETCODE_USERNAME')
        self.password = os.environ.get('LEETCODE_PASSWORD')
        self.base_dir = 'leetcode-solutions'
        self.metadata_file = 'metadata/submissions.json'
        self.session = requests.Session()
        
        # Ensure directories exist
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs('metadata', exist_ok=True)
        
    def setup_driver(self):
        """Setup Chrome driver with headless options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        return driver
    
    def login_leetcode(self, driver):
        """Login to LeetCode"""
        try:
            driver.get('https://leetcode.com/accounts/login/')
            
            # Wait for login form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'login'))
            )
            
            # Fill login form
            username_field = driver.find_element(By.NAME, 'login')
            password_field = driver.find_element(By.NAME, 'password')
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Submit form
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()
            
            # Wait for redirect to dashboard
            WebDriverWait(driver, 10).until(
                lambda driver: 'leetcode.com' in driver.current_url and 'login' not in driver.current_url
            )
            
            print("Successfully logged in to LeetCode")
            return True
            
        except Exception as e:
            print(f"Failed to login: {e}")
            return False
    
    def get_recent_submissions(self, driver):
        """Get recent accepted submissions"""
        try:
            # Navigate to submissions page
            driver.get('https://leetcode.com/submissions/')
            
            # Wait for submissions to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="submission-item"]'))
            )
            
            submissions = []
            submission_elements = driver.find_elements(By.CSS_SELECTOR, '[data-cy="submission-item"]')
            
            for element in submission_elements[:10]:  # Get last 10 submissions
                try:
                    status = element.find_element(By.CSS_SELECTOR, '[data-cy="submission-status"]').text
                    if 'Accepted' in status:
                        title_element = element.find_element(By.CSS_SELECTOR, '[data-cy="submission-title"] a')
                        problem_title = title_element.text
                        problem_url = title_element.get_attribute('href')
                        
                        timestamp_element = element.find_element(By.CSS_SELECTOR, '[data-cy="submission-time"]')
                        timestamp = timestamp_element.text
                        
                        submissions.append({
                            'title': problem_title,
                            'url': problem_url,
                            'timestamp': timestamp,
                            'status': 'Accepted'
                        })
                except Exception as e:
                    print(f"Error parsing submission: {e}")
                    continue
            
            return submissions
            
        except Exception as e:
            print(f"Failed to get submissions: {e}")
            return []
    
    def get_submission_code(self, driver, submission_url):
        """Get the actual code from submission"""
        try:
            driver.get(submission_url)
            
            # Wait for code to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'code'))
            )
            
            # Get the code content
            code_element = driver.find_element(By.CSS_SELECTOR, 'code')
            code = code_element.text
            
            # Get language from the page
            language_element = driver.find_element(By.CSS_SELECTOR, '[data-cy="lang-select"] span')
            language = language_element.text.lower()
            
            return code, language
            
        except Exception as e:
            print(f"Failed to get submission code: {e}")
            return None, None
    
    def load_existing_metadata(self):
        """Load existing submissions metadata"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
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
        
        print(f"Created: {filepath}")
        return filepath
    
    def sync_solutions(self):
        """Main sync function"""
        print("Starting LeetCode sync...")
        
        driver = self.setup_driver()
        
        try:
            if not self.login_leetcode(driver):
                return
            
            # Get recent submissions
            submissions = self.get_recent_submissions(driver)
            print(f"Found {len(submissions)} accepted submissions")
            
            # Load existing metadata
            existing_metadata = self.load_existing_metadata()
            
            new_solutions = 0
            
            for submission in submissions:
                problem_key = f"{submission['title']}_{submission['timestamp']}"
                
                # Skip if already processed
                if problem_key in existing_metadata:
                    continue
                
                print(f"Processing: {submission['title']}")
                
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
            
            # Save updated metadata
            self.save_metadata(existing_metadata)
            
            print(f"Sync completed. Added {new_solutions} new solutions.")
            
        finally:
            driver.quit()

if __name__ == "__main__":
    sync = LeetCodeSync()
    sync.sync_solutions()