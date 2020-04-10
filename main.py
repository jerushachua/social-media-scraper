import sys

import instagram_scraper


# tag to search
tag_dict = {
    "ad": ["ad"],
    "gaming": ["leagueoflegends", "esports", "twitch", "apexlegends", "xbox", "playstation", "games", "fortnite"],
    "food": ["instafood", "baking", "sourdough", "thefeedfeed", "pasta", "foodtography", "buzzfeast", "beautifulcuisines"],
    "travel": ["travel", "sanfrancisco", "nyc", "japan", "usa", "roadtrip", "downtown", "city"], 
    "insta": ["instagram", "youtube", "sponsor", "influencer", "tiktok", "blogger", "goodvides", "ootd"],
    "lifestyle": ["lifestyle", "home", "architecture", "minimalism", "throwback", "decor", "interior", "art"], 
    "rand": ["stayhome", "random", "spring", "summer", "fall", "winter", "fitness", "family"]
}

# file parameters
if len(sys.argv) < 3:
    print("Incorrect arguments. ")
    print("Make sure you have all arguments: username, password, and tag genre. ")
    print("Example command: `python selenium_driver.py username password tag`")
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
scraper = instagram_scraper.InstagramScraper()
scraper.setUp()
scraper.login(username, password)

tag = tag_dict.get(tag_genre, ["instagram"])

if tag_genre == "ad":
    insta_users = scraper.related_tags_search_paid_promo("ad")
    scraper.write_arr_to_file("ad", insta_users)
elif tag_genre == "emails": 
    dirname = input("directory name: ")
    scraper.get_insta_profile_emails(dirname)
else:
    for tt in tag:
        insta_users = scraper.related_tags_search_by_likes(tt)

        # sometimes api limits the scraping. try again
        if len(insta_users) <= 1:
            insta_users = scraper.related_tags_search_by_likes(tt)

        scraper.write_arr_to_file(tt, insta_users)

scraper.tearDown()
