from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os


def main():
    
    dashBoard = 'https://www.chegg.com/my/expertqa'
    expertPage = 'https://expert.chegg.com/'
    
    chrome_options = Options()
    chrome_options.add_argument('user-data-dir='+os.path.join(os.path.expanduser("~"),'.config/google-chrome'))
    
    browser = webdriver.Chrome(options=chrome_options, executable_path=os.path.join(os.path.expanduser("~"),'chromedriver'))
    browser.get(dashBoard)
    
    k = input("Ready to Onboard? (exit-0) :::: ")
    if(k=='0'):
    	browser.close()
    	return 0
    
    browser.get(expertPage)

    while(True):
        k = input("Skip? (exit-0) :::: ")
        if(k=='0'):break
        try:
            xpath_for_skip_button = "//div[@data-test-id='question-skip-button']/button/span[contains(.,'Skip')]"
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_for_skip_button)))
            browser.execute_script("arguments[0].click();",element)
            
            xpath_for_skip_reason = "//div[@data-test-id='skip-question-modal']/label[text()=\"I don't have the subject knowledge\"]"
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_for_skip_reason)))
            browser.execute_script("arguments[0].click();",element)
            
            xpath_drop_1 = "//div[@data-test-id='granular-list']/div/div/span[contains(.,'What topic should it be?')]"
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_drop_1)))
            browser.execute_script("arguments[0].click();",element)
            
            xpath_drop_2 = "//div[@data-test-id='granular-list']/div/ul/li[@data-name='Other Computer Science']"
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_drop_2)))
            browser.execute_script("arguments[0].click();",element)
            
            xpath_submit = "//div[@data-test='modalContent']/div/button/span[contains(.,'Submit')]"
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_submit)))
            browser.execute_script("arguments[0].click();",element)
        except:
            browser.get(expertPage)
            continue
        
    browser.close()


if __name__ == "__main__":
    main()






