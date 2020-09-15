import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

source = "[Source](https://github.com/GoblinHater/sauceNAOcheckbot)"
FAQ = "[FAQ](https://www.reddit.com/r/sauceNAOcheckbot/comments/iocsj9/saucenaocheckbot_faq/)"


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
            # To see if a title exists

            titlename = "Sauce: " + str(titlename.text) + "\n\n"
            # print(len(titlename))
            content = driver.find_element_by_class_name("resultcontentcolumn")
            print(content.text)
            content = str(content.text) + "\n\n"
            if "pixiv" in content.lower() or "da id" in content.lower() or "seiga" in content.lower() or "nijie" in content.lower():
                print(driver.find_element_by_css_selector("div.resultcontentcolumn > a").get_attribute('href'))
                content ="[Sauce link]"+str("(") + str(driver.find_element_by_css_selector("div.resultcontentcolumn > a").get_attribute('href'))+str(")\n\n")
            similarity = driver.find_element_by_class_name("resultsimilarityinfo")
            # print("Similarity = " + str(similarity.text))
            # print(str(similarity.text)[0:2]+" This is a test")
            similarity = "Similarity = " + str(similarity.text) + "\n" + "\n"
            footer = "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater ||" + source + " || " + FAQ
            reply = titlename + content + similarity + footer
            driver.quit()
            return reply
        else:
            # If title does not exist it means that there was no result
            
            print("No result")
            replyNeg = "Sorry I was not able to find the sauce.\n\nI did not check the low similarity options\n\n"
            replyNeg = replyNeg + "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater ||" + source + " || " + FAQ
            driver.quit()
            return replyNeg
    except:
        # If the page has not loaded

        print("No result")
        replyNeg = "Sorry I was not able to find the sauce.\n\nI did not check the low similarity options\n\n"
        replyNeg = replyNeg + "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater ||" + source + " || " + FAQ
        driver.quit()
        return replyNeg


# For giving source on posts on PASSEDSUBREDDIT
# Slightly modified the function for quality checks and hyperlinks
def getSauceSubreddit(url):
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
            # To see if a title exists

            titlename = "Sauce: " + str(titlename.text) + "\n\n"
            # print(len(titlename))
            content = driver.find_element_by_class_name("resultcontentcolumn")
            print(content.text)
            content = str(content.text) + "\n\n"

            # To get links to artwork
            try:
                if "pixiv" in content.lower() or "da id" in content.lower() or "seiga" in content.lower() or "nijie" in content.lower():
                    print(driver.find_element_by_css_selector("div.resultcontentcolumn > a").get_attribute('href'))
                    content = "[Sauce link]" + str("(") + str(driver.find_element_by_css_selector("div.resultcontentcolumn > a").get_attribute('href')) + str(")\n\n")
            except:
                pass

            similarity = driver.find_element_by_class_name("resultsimilarityinfo")
            # print("Similarity = " + str(similarity.text))

            # Check if similarity is more than 60%
            if int(str(similarity.text)[0:2]) >= 60:
                print("Similarity>60")
                similarity = "Similarity = " + str(similarity.text) + "\n" + "\n"
                footer = "^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater || [Source](https://github.com/GoblinHater/sauceNAOcheckbot) || [FAQ](https://www.reddit.com/r/sauceNAOcheckbot/comments/iocsj9/saucenaocheckbot_faq/)"
                reply = titlename + content + similarity + footer
                driver.quit()
                return reply
            else:
                print("Low similarity")
                driver.quit()

        else:
            # If title does not exist it means that there was no result
            driver.quit()
            print("No result")
            pass

    except:
        # If the page has not loaded
        driver.quit()
        print("No result")
