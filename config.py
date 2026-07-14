import os

from dotenv import load_dotenv


load_dotenv()


WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
TEST_WEBHOOK_URL = os.getenv("TEST_WEBHOOK_URL", "")

NEWS_URL = "https://torchlight.xd.com/tw/news/list"
OFFICIAL_SITE_URL = "https://torchlight.starforce.tw/"
OFFICIAL_FACEBOOK_URL = "https://www.facebook.com/TorchlightInfiniteTW"
