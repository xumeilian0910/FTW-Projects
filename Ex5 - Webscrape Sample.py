from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
# ...import your database module here
import pymysql

conn = pymysql.connect(host='127.0.0.1',user='root', passwd = 'mysql@r00t', db = 'mysql',
charset = 'utf8')
cur = conn.cursor()
cur.execute("USE scraperdb")
def store(id, date, stars, title, content):
    # finish this mysql query
   cur.execute('INSERT INTO reviews (reviewId, title, stars, reviewDate, content) VALUES ''("%s","%s","%s","%s","%s")', (id, title, stars, date, content))
   cur.connection.commit()

dirpath = os.getcwd()
filepath = dirpath + '/chromedriver'
print('Path to Driver: ' + filepath)
browser = webdriver.Chrome(executable_path = filepath)
browser.get('https://www.amazon.com/dp/B01MECVTDY?aaxitk=w4dL3-w.fkh.eaGplMGdNQ&pd_rd_i=B01MECVTDY&pf_rd_p=3fade48a-e699-4c96-bf08-bb772ac0e242&hsa_cr_id=9358540660701&sb-ci-n=productDescription&sb-ci-v=NutraChamps%20Korean%20Red%20Panax%20Ginseng%201000mg%20-%20120%20Vegan%20Capsules%20Extra%20Strength%20Root%20Extract%20Powder%20Supplement%20w%2FHigh%20Ginsenosides%20for%20Energy%2C%20Performance%20%26%20Focus%20Pills%20for%20Men%20%26%20Women')

try:
    # Wait as long as required, or maximum of 5 sec for element to appear
    # If successful, retrieves the element
    element = WebDriverWait(browser,5).until(
         EC.presence_of_element_located((By.XPATH, '//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]/span/input')))

    element.click()

    element = WebDriverWait(browser,5).until(
         EC.presence_of_element_located((By.XPATH, '//*[@id="acrCustomerReviewText"]')))

    element.click()

    reviewsElement = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="cm-cr-dp-review-list"]')))
    
    reviewChildren = reviewsElement.find_elements_by_class_name("review")
    for review in reviewChildren:
        reviewId = review.get_attribute('id')
        date = review.find_element_by_class_name('review-date').get_attribute('innerHTML')
        stars = review.find_element_by_class_name('a-link-normal').get_attribute('title')
        title = review.find_element_by_xpath('.//div[2]/a[2]/span').get_attribute('innerHTML')
        reviewContent = review.find_element_by_xpath('.//div[4]/span/div/div[1]/span').get_attribute('innerHTML')
        print(reviewId)
        print(title)
        print(date)
        print(stars)
        print(reviewContent).encode('utf8')
        print('#############')
        # call your database insert function here
        store(reviewId, date, stars, title, reviewContent)

except TimeoutException:
    print("Failed to load search bar at www.google.com")
finally:
    browser.quit()


