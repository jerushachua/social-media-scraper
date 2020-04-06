import glob
import csv
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import progressbar


class InstagramScraper():

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(
            "./chromedriver.exe", chrome_options=chrome_options)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)

        userInput = driver.find_element_by_name("username")
        passInput = driver.find_element_by_name("password")

        userInput.send_keys(username)
        passInput.send_keys(password)
        passInput.send_keys(Keys.ENTER)
        time.sleep(2)

        # verify 
    
    # search for users by #tag and #related_tags and return user's whose post has enough likes
    def related_tags_search_by_likes(self, tag):
        insta_users = {}
        related_tags = self.get_related_tags(tag)

        # start the log
        filename = time.strftime("%Y-%m-%d") + "-" + str(tag) + ".csv"
        with open(filename, mode='w') as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in related_tags:
                writer.writerow([item])

        # first tag
        insta_users.fromkeys(self.get_usernames_by_likes(tag), 1)

        # related tags
        for edge in related_tags:
            # see if user is already in dict
            new_users_dict = self.get_usernames_by_likes(edge)
            for new_user in new_users_dict.keys():
                if new_user not in insta_users.keys():
                    insta_users[new_user] = 1

        return insta_users

    # get list of related #tags
    def get_related_tags(self, tag):
        related_tags = []
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)
        time.sleep(1)

        related_tags_xpath = "//span[2]/div/a"
        related = driver.find_elements_by_xpath("//span[2]/div/a")
        for hashtag in related:
            clean_tag = hashtag.text
            clean_tag = clean_tag.replace("#", "")
            related_tags.append(clean_tag)

        return related_tags

    def get_usernames_by_likes(self, tag, num_likes=1000):
        outarr = {u'https://www.instagram.com/': 1}
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        pics_per_tag = 9
        all_images_xpath = "/html/body/div[1]/section/main/article/div[1]/div/div[1]/div/div"

        # start search and progress bar 
        bar = progressbar.ProgressBar(maxval=10,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start() 
        print("Searching through " + str(tag))
        bb = 0

        # iterate through each image by right arrow key
        # if the #tag has an emoji, the DOM changes slightly.
        try:
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        except:
            driver.get(URL)
            time.sleep(2)
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while pics_per_tag >= 0:
            actions = ActionChains(driver)
            aa_tags = driver.find_elements_by_xpath("//div[1]/div[1]/a")

            # scrape all <a> tags to find the href attribute
            # 6th element from this array is the poster of the image
            for aa in aa_tags:
                href = aa.get_attribute("href")
                if href:
                    # only keep username URLs
                    tok = 0
                    for char in href:
                        if char == '/':
                            tok += 1
                    if tok <= 4:

                        # append to array if photo has at least num_likes
                        if href not in outarr.keys():
                            try:
                                likes_str = driver.find_element_by_xpath(
                                    "//div/div/button/span").text
                                likes_int = int(likes_str.replace(",", ""))
                                if likes_int >= num_likes:
                                    outarr[href] = 1
                                break
                            except:
                                pass

            # move right
            actions.send_keys(Keys.RIGHT).perform()
            time.sleep(1)
            pics_per_tag -= 1
            bb += 1
            bar.update(bb)

        return outarr

    # search for users by #ad and return users whose post is sponsered
    def related_tags_search_paid_promo(self, tag):
        insta_users = {}

        # start the log
        filename = time.strftime("%Y-%m-%d") + "-" + str(tag) + ".csv"
        with open(filename, mode='w') as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([tag])

        insta_users = insta_users.fromkeys(
            self.get_usernames_by_paid_promo(tag), 1)
        return insta_users

    def get_usernames_by_paid_promo(self, tag):
        outarr = {u'https://www.instagram.com/': 1}
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)
        pics_per_tag = 1024
        all_images_xpath = "/html/body/div[1]/section/main/article/div[1]/div/div[1]/div/div"

        # start search and progress bar
        print("Searching through " + str(tag))
        bar = progressbar.ProgressBar(maxval=1025,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        ii = 0

        # iterate through each image by right arrow key
        # if the #tag has an emoji, the DOM changes slightly.
        try:
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        except:
            driver.get(URL)
            time.sleep(2)
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while pics_per_tag >= 0:
            actions = ActionChains(driver)
            aa_tags = driver.find_elements_by_xpath("//div[1]/div[1]/a")

            # scrape all <a> tags to find the href attribute
            # 6th element from this array is the poster of the image
            for aa in aa_tags:
                href = aa.get_attribute("href")
                if href:
                    # only keep username URLs
                    tok = 0
                    for char in href:
                        if char == '/':
                            tok += 1
                    if tok <= 4:

                        # append to array if photo is a paid promotion
                        if href not in outarr.keys():
                            try:
                                promo_str = "Paid partnership with "
                                likes_str = driver.find_element_by_xpath(
                                    "//*[contains(text(),'" + promo_str + "')]")
                                outarr[href] = 1
                                break
                            except:
                                pass

            # move right
            actions.send_keys(Keys.RIGHT).perform()
            time.sleep(1)
            pics_per_tag -= 1
            ii += 1
            bar.update(ii)

        return outarr

    # read instagram profiles in given directory
    def get_insta_profile_emails(self, dirname):
        driver = self.driver
        filenames = glob.glob(str(dirname) + "/*")
        business_emails = {}
        profile_text_xpath = "//section/div[2]/span"
        
        # read in file in the given directory and extract profile urls
        for name in filenames:
            with open(name, mode="r") as file:
                profile_urls = file.readlines()[10:]

                print(profile_urls)

                # visit each profile url
                for url in profile_urls:
                    if url == "https://www.instagram.com/\n":
                        continue
                    driver.get(url)
                    time.sleep(1)
                    try:
                        profile_text = driver.find_element_by_xpath(
                            profile_text_xpath).text
                        print("match xpath 1")
                    except:
                        print("Cannot find profile text. ")
                        continue
                        profile_text_xpath = "//section/main/div/div[1]/span"
                        profile_text = driver.find_element_by_xpath(profile_text_xpath).text
                    email = re.search('\S+@\S+', profile_text)
                    if email:
                        print(email.group(0))
                        business_emails[email.group(0)] = 1

            file.close()
            break
        return business_emails

    # write the array to a text file
    def write_arr_to_file(self, tag, arr):
        filename = time.strftime("%Y-%m-%d") + "-" + str(tag) + ".csv"
        with open(filename, mode='a') as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in arr.keys():
                writer.writerow([item])
        file.close()
