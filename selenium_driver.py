import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SocialMediaScraper():

    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')

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

    # search related tags if not yet visited
    # combine and return a list of all usernames from tags and related tags
    def related_tags_search(self, tag, thresh=100):
        # get insta usernames by searching for tag, and by how many pics to go through
        related_tags = []
        insta_users, related_tags = scraper.get_usernames(tag, 7)
        print(insta_users, related_tags)

        new_user_li, new_related_tags = [], []
        for edge in related_tags:
            new_user_li, new_related_tags = scraper.get_usernames(edge, 7)

            # combine the lists with no dups
            new_user_set = set(new_user_li)
            old_users = set(insta_users)
            insta_users = insta_users + list(new_user_set - old_users)
        
        return insta_users

    # search for trending posts by hashtag
    # find related tags and return a list
    # find all usernames of posters and also return another list
    def get_usernames(self, tag, thresh=100):
        outarr = [u'https://www.instagram.com/']
        driver = self.driver
        URL = "https://www.instagram.com/explore/tags/" + tag
        driver.get(URL)

        # xpath definitions
        all_images_xpath = "/html/body/div[1]/section/main/article/div[1]/div/div[1]/div/div"

        # find the related tags and also return
        related_tags = []
        related_tags_xpath = "//span[2]/div/a"
        related = driver.find_elements_by_xpath("//span[2]/div/a")
        for hashtag in related:
            clean_tag = hashtag.text
            clean_tag = clean_tag.replace("#", "")
            related_tags.append(clean_tag)

        # insta feeds on desktop render 3 rows, with 3 images each
        # iterate through each image by right arrow key
        driver.find_elements_by_xpath(all_images_xpath)[0].click()
        while thresh > 0:
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
            thresh -= 1

        return outarr, related_tags

    # default cut off for number of followers to define content creator is 10,000
    def get_content_creators(self, follower_threshold=10000, users=[]):
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

if __name__ == "__main__":

    # tag to search
    tag = "cook"

    # set up scraper
    scraper = SocialMediaScraper()
    scraper.setUp()
    scraper.login("bountifulapps", "jamesharden2020")

    # insta_users = scraper.related_tags_search(tag, 7)
    insta_users = [u'https://www.instagram.com/lotusinaseaoffire/', u'https://www.instagram.com/ciccio.lauretta_/', u'https://www.instagram.com/burcunun__mutfagi/', u'https://www.instagram.com/the.exquisite/', u'https://www.instagram.com/locosxlaparrillaa/', u'https://www.instagram.com/mariacorreae/', u'https://www.instagram.com/5a1bull/', u'https://www.instagram.com/alex_marquez02/', u'https://www.instagram.com/the_nutritionguy/', u'https://www.instagram.com/nishcooks/', u'https://www.instagram.com/chefspringerish/', u'https://www.instagram.com/lysimachos_drakos/', u'https://www.instagram.com/guysinnott/', u'https://www.instagram.com/thestaffcanteen/', u'https://www.instagram.com/rachaeljfrancis/', u'https://www.instagram.com/chefclaysmith/', u'https://www.instagram.com/taleitalei/', u'https://www.instagram.com/fit_for_plate/', u'https://www.instagram.com/_liyun_y/', u'https://www.instagram.com/hungryhoggers/', u'https://www.instagram.com/tineshawijesuriya/', u'https://www.instagram.com/evripidis_apostolidis/', u'https://www.instagram.com/malloryhopes/', u'https://www.instagram.com/omyazeed_123/', u'https://www.instagram.com/stefanocbz/', u'https://www.instagram.com/acooknamedmatt/', u'https://www.instagram.com/pierre.le.chef/', u'https://www.instagram.com/armand_hasanpapaj/', u'https://www.instagram.com/notorious_foodie/', u'https://www.instagram.com/makeup_aybuke/', u'https://www.instagram.com/ileniagreco1985/', u'https://www.instagram.com/cozinhandopara2ou1/', u'https://www.instagram.com/inventaricette/', u'https://www.instagram.com/753mk/', u'https://www.instagram.com/yantykitchen/', u'https://www.instagram.com/noodleworship/', u'https://www.instagram.com/bhukkadiyer/', u'https://www.instagram.com/thegreeneggeffect/', u'https://www.instagram.com/petealwayseats/', u'https://www.instagram.com/igmeals/', u'https://www.instagram.com/mutfakdahayatvar/', u'https://www.instagram.com/foodychimp/', u'https://www.instagram.com/florentmargaillan/', u'https://www.instagram.com/donnguyenknives/', u'https://www.instagram.com/rickmatharu/', u'https://www.instagram.com/thebestchefawards/', u'https://www.instagram.com/kitchenrayofficial/', u'https://www.instagram.com/chef.field/', u'https://www.instagram.com/nathalie.aranda.12/', u'https://www.instagram.com/_artonaplate/', u'https://www.instagram.com/diaryofakitchenlover/', u'https://www.instagram.com/frankie_corrado/', u'https://www.instagram.com/juandavidcocina/', u'https://www.instagram.com/keiko.kitchen/', u'https://www.instagram.com/sweatnetnashville/', u'https://www.instagram.com/chefjoegatto/', u'https://www.instagram.com/thenigirishow/', u'https://www.instagram.com/dccheapeats/', u'https://www.instagram.com/flyingfoodie.ff/', u'https://www.instagram.com/pbnfood/', u'https://www.instagram.com/thrillist/', u'https://www.instagram.com/thefeastkings/']
    
    # visit each user and filter those with > 2000 followers
    content_creators = scraper.get_content_creators(2000, insta_users)
    print(content_creators)

    scraper.tearDown()
