import csv
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class SocialMediaScraper():

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            "./chromedriver.exe", chrome_options=chrome_options)

    def tearDown(self):
        self.driver.close()

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

    # search for users by #tag and #related_tags and return user's whose post has enough likes
    def related_tags_search_by_likes(self, tag):
        # get insta usernames by searching for tag, and by how many pics to go through
        related_tags = []
        insta_users, related_tags = scraper.get_usernames_by_likes(tag)

        # log the #tags we are visiting
        filename = str(tag) + ".csv"
        with open(filename, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in related_tags: 
                writer.writerow([item])

        new_user_li, new_related_tags = [], []
        for edge in related_tags:
            new_user_li, new_related_tags = scraper.get_usernames_by_likes(edge)

            # combine the lists with no dups
            new_user_set = set(new_user_li)
            old_users = set(insta_users)
            insta_users = insta_users + list(new_user_set - old_users)

        return insta_users

    def get_usernames_by_likes(self, tag, num_likes=1000):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)
        pics_per_tag = 9 

        # start search
        print("Searching through " + str(tag))

        # xpath definitions
        all_images_xpath = "/html/body/div[1]/section/main/article/div[1]/div/div[1]/div/div"

        # get list of related #tags
        related_tags = []
        related_tags_xpath = "//span[2]/div/a"
        related = driver.find_elements_by_xpath("//span[2]/div/a")
        for hashtag in related:
            clean_tag = hashtag.text
            clean_tag = clean_tag.replace("#", "")
            related_tags.append(clean_tag)

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
                        if href not in outarr:
                            try:
                                likes_str = driver.find_element_by_xpath(
                                    "//div/div/button/span").text
                                likes_int = int(likes_str.replace(",", ""))
                                if likes_int >= num_likes:
                                    outarr.append(href)
                            except:
                                print("This photo has no likes. ")
                            break

            # move right
            actions.send_keys(Keys.RIGHT).perform()
            time.sleep(1)
            pics_per_tag -= 1

        return outarr, related_tags

    # search for users by #ad and return users whose post is sponsered
    def related_tags_search_paid_promo(self, tag):
        # get insta usernames by searching for tag, and by how many pics to go through
        insta_users = scraper.get_usernames_by_paid_promo(tag)

        # log the #tags we are visiting
        filename = str(tag) + ".csv"
        with open(filename, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([tag])
        
        return insta_users

    def get_usernames_by_paid_promo(self, tag):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)
        pics_per_tag = 1024

        # start search
        print("Searching through " + str(tag))

        # xpath definitions
        all_images_xpath = "/html/body/div[1]/section/main/article/div[1]/div/div[1]/div/div"

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
                        if href not in outarr:
                            try:
                                promo_str = "Paid partnership with "
                                likes_str = driver.find_element_by_xpath(
                                    "//*[contains(text(),'" + promo_str + "')]")
                                outarr.append(href)
                                print("This photo is a paid promotion. ")
                                break
                            except:
                                pass

            # move right
            actions.send_keys(Keys.RIGHT).perform()
            time.sleep(1)
            pics_per_tag -= 1

        return outarr

    # write the array to a text file
    def write_arr_to_file(self, tag, arr):
        filename = str(tag) + ".csv"
        with open(filename, mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in arr: 
                writer.writerow([item])
        file.close()

if __name__ == "__main__":

    # file parameters
    if len(sys.argv) < 3: 
        print("Incorrect arguments. ")
        print("Make sure you have all arguments: username, password, and tag genre. ")
        print("Example command: ")
        print("python selenium_driver.py twsizzle ****** travel")
        username = input("username: ")
        password = input("password: ")
        tag_genre = input("tag genre: ") 
    else: 
        username = str(sys.argv[1])
        password = str(sys.argv[2])
        try: 
            tag_genre = str(sys.argv[3])
        except:
            tag_genre = ""

    # set up scraper
    scraper = SocialMediaScraper()
    scraper.setUp()
    scraper.login(username, password)

    # tag to search
    tag_dict = {
        "ad": ["ad"], 
        "gaming": ["leagueoflegends", "esports", "twitch", "apexlegends", "xbox", "playstation", "games", "fortnite"], 
        "food": ["instafood", "baking", "sourdough", "thefeedfeed", "pasta", "foodtography", "buzzfeast", "beautifulcuisines"], 
        "rand": ["random", "spring", "summer", "fall", "winter", "goodvibes", "fitness", "blogger"], 
        "travel": ["travel", "sanfrancisco", "nyc", "japan", "usa", "roadtrip", "downtown", "city"]
    }

    tag = tag_dict.get(tag_genre, ["instagram"])

    if tag_genre == "ad": 
        for tt in tag:
            insta_users = scraper.related_tags_search_paid_promo(tt)

    else: 
        for tt in tag:
            insta_users = scraper.related_tags_search_paid_promo(tt)

            # sometimes api limits the scraping. try again
            if len(insta_users) <= 1:
                insta_users = scraper.related_tags_search_by_likes(tt)

    
    scraper.write_arr_to_file(tt, insta_users)

    scraper.tearDown()
