import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)


def getSauce(url):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://saucenao.com")

    # ActionChains(driver).click(driver.find_element_by_class_name("style7")).perform()
    expand = driver.find_element_by_link_text("~advanced options~")
    expand.click()
    search = driver.find_element_by_name("url")
    search.send_keys(url)
    search.send_keys(Keys.RETURN)
    driver.implicitly_wait(8)
    # time.sleep(8)
    try:
        titlename = driver.find_element_by_class_name("resulttitle")
        print(titlename.text)
        # print(len(titlename.text))
        if len(titlename.text) > 0:
            titlename = "Sauce: " + str(titlename.text) + "\n\n"
            # print(len(titlename))
            content = driver.find_element_by_class_name("resultcontentcolumn")
            print(content.text)
            content = str(content.text) + "\n\n"
            similarity = driver.find_element_by_class_name("resultsimilarityinfo")
            # print("Similarity = " + str(similarity.text))
            similarity = "Similarity = " + str(similarity.text) + "\n" + "\n"
            footer = "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater"
            reply = titlename + content + similarity + footer
            driver.quit()
            return reply
        else:
            print("No result")
            replyNeg = "Sorry I was not able to find the sauce.\n\nI did not check the low similarity options\n\n"
            replyNeg = replyNeg + "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater"
            driver.quit()
            return replyNeg
    except:
        print("No result")
        replyNeg = "Sorry I was not able to find the sauce.\n\nI did not check the low similarity options\n\n"
        replyNeg = replyNeg + "^I ^am ^a ^bot. ^Give ^feedback ^to u/GoblinHater"
        driver.quit()
        return replyNeg