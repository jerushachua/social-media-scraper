import time
import simplejson
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SocialMediaScraper():

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
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

    # search for users by #tag and #related_tags and return all users
    def related_tags_search(self, tag, pics_per_tag=10):
        # get insta usernames by searching for tag, and by how many pics to go through
        related_tags = []
        insta_users, related_tags = scraper.get_usernames(tag, pics_per_tag)

        # log the #tags we are visiting
        file = open("output.txt", "w")
        simplejson.dump(related_tags, file)
        file.close()

        new_user_li, new_related_tags = [], []
        for edge in related_tags:
            new_user_li, new_related_tags = scraper.get_usernames(edge, 5)

            # combine the lists with no dups
            new_user_set = set(new_user_li)
            old_users = set(insta_users)
            insta_users = insta_users + list(new_user_set - old_users)

        return insta_users

    # return a list of users who post top #tagged posts
    def get_usernames(self, tag, pics_per_tag=10):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)

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
        driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while pics_per_tag > 0:
            actions = ActionChains(driver)
            aa_tags = driver.find_elements_by_xpath("//div[1]/div[1]/a")

            # scrape all <a> tags to find the href attribute
            # 6th element from this array is the poster of the image
            # once found, break and go to next image
            # we only want the poster, not all commenters
            for aa in aa_tags:
                href = aa.get_attribute("href")
                if href:
                    # only keep username URLs
                    tok = 0
                    for char in href:
                        if char == '/':
                            tok += 1
                    if tok <= 4:
                        if href not in outarr:
                            outarr.append(href)
                            break

            # move right
            actions.send_keys(Keys.RIGHT).perform()
            time.sleep(1)
            pics_per_tag -= 1

        return outarr, related_tags

    # search for users by #tag and #related_tags and return user's whose post has enough likes
    def related_tags_search_by_likes(self, tag, pics_per_tag=10):
        # get insta usernames by searching for tag, and by how many pics to go through
        related_tags = []
        insta_users, related_tags = scraper.get_usernames_by_likes(
            tag, pics_per_tag)

        # log the #tags we are visiting
        filename = str(tag) + ".txt"
        file = open(filename, "w")
        simplejson.dump(related_tags, file)
        file.close()

        new_user_li, new_related_tags = [], []
        for edge in related_tags:
            new_user_li, new_related_tags = scraper.get_usernames_by_likes(
                edge, pics_per_tag)

            # combine the lists with no dups
            new_user_set = set(new_user_li)
            old_users = set(insta_users)
            insta_users = insta_users + list(new_user_set - old_users)

        return insta_users

    # return a list of users who post top #tagged posts if it has > num_likes
    def get_usernames_by_likes(self, tag, pics_per_tag=10, num_likes=1000):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)

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
            time.sleep(2)
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while pics_per_tag >= 0:
            actions = ActionChains(driver)
            aa_tags = driver.find_elements_by_xpath("//div[1]/div[1]/a")

            # scrape all <a> tags to find the href attribute
            # 6th element from this array is the poster of the image
            # once found, break and go to next image
            # we only want the poster, not all commenters
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
                                print(likes_str)
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

    # search for users by #tag and #related_tags and return user's whose post is sponsered
    def related_tags_search_paid_promo(self, tag, pics_per_tag=10):
        # get insta usernames by searching for tag, and by how many pics to go through
        related_tags = []
        insta_users, related_tags = scraper.get_usernames_by_paid_promo(
            tag, pics_per_tag)

        # log the #tags we are visiting
        file = open("output.txt", "w")
        simplejson.dump(related_tags, file)
        file.close()

        new_user_li, new_related_tags = [], []
        for edge in related_tags:
            new_user_li, new_related_tags = scraper.get_usernames_by_paid_promo(
                edge, pics_per_tag)

            # combine the lists with no dups
            new_user_set = set(new_user_li)
            old_users = set(insta_users)
            insta_users = insta_users + list(new_user_set - old_users)

        return insta_users

    # return a list of users who post top #tagged posts if it has > num_likes
    def get_usernames_by_paid_promo(self, tag, pics_per_tag=10):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)

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
            time.sleep(2)
            driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while pics_per_tag >= 0:
            actions = ActionChains(driver)
            aa_tags = driver.find_elements_by_xpath("//div[1]/div[1]/a")

            # scrape all <a> tags to find the href attribute
            # 6th element from this array is the poster of the image
            # once found, break and go to next image
            # we only want the poster, not all commenters
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

        return outarr, related_tags

    # default cut off for number of followers to define content creator is 10,000
    def get_content_creators_by_followage(self, follower_threshold=10000, users=[]):
        content_creators = []

        for user in users:
            driver = self.driver
            profile_url = str(user)
            driver.get(profile_url)

            # see if user hits our metrics to define them a content creator
            aa_tags = driver.find_elements_by_xpath("//a/span")

            for elem in aa_tags:
                num_followers = elem.get_attribute("title")
                if num_followers:
                    if int(num_followers.replace(",", "")) > follower_threshold:
                        print(num_followers)
                        content_creators.append(user)

            time.sleep(1)

        return content_creators

    def write_arr_to_file(self, tag, arr):
        filename = str(tag) + ".txt"
        with open(filename, "a") as f:
            for item in arr:
                f.write("%s\n" % item)
        f.close()


if __name__ == "__main__":

    # tag to search
    tag = ["leagueoflegends", "esports", "twitch", "apexlegends",
           "xbox", "playstation", "games", "contentcreator"]

    for tt in tag:

        # set up scraper
        scraper = SocialMediaScraper()
        scraper.setUp()
        scraper.login("bountifulapps", "jamesharden2020")

        insta_users = scraper.related_tags_search_by_likes(tt, 10)
        scraper.write_arr_to_file(tt, insta_users)

        scraper.tearDown()
