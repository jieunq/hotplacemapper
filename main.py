from selenium import webdriver
import time
import getpass
from selenium.webdriver.common.by import By


class Post:
    location = ""
    date = ""

    def setLocation(self, location):
        self.location = location

    def setDate(self, date):
        self.date = date

    def getPost(self):
        print("location: " + self.location)
        print("date: " + self.date)


def crawler(email, password, url):
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    options.add_argument('user-agent=' + user_agent)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.instagram.com")
    time.sleep(10)

    input_id = driver.find_elements(By.TAG_NAME, "input")[0]
    input_id.clear()
    input_id.send_keys(email)

    input_pw = driver.find_elements(By.TAG_NAME, "input")[1]
    input_pw.clear()
    input_pw.send_keys(password)

    input_pw.submit()

    time.sleep(7)
    driver.get(url)

    time.sleep(30)

    first_post_elements = driver.find_elements(By.CSS_SELECTOR, "div._aagw")
    if len(first_post_elements) > 0:
        first_post = first_post_elements[0]
        first_post.click()
        time.sleep(15)
        i = 1
        count = 0

        while count < 500:
            post = Post()

            try:
                location_elements = driver.find_elements(By.CSS_SELECTOR, "div._aaqm")
                if len(location_elements) > 0:
                    location = location_elements[0].text
                    post.setLocation(location)
            except:
                continue

            time.sleep(1)
            date_elements = driver.find_elements(By.CSS_SELECTOR, 'time._aaqe')
            if len(date_elements) > 0:
                date = date_elements[0].get_attribute("datetime")[5:7]
                post.setDate(date)
                print(str(location) + "," + str(date))

                # 장소와 날짜를 텍스트 파일에 저장
                with open("locations.txt", "a") as file:
                    file.write(f"Location: {location}\n")
                    file.write(f"Date: {date}\n\n")

                count += 1

            time.sleep(1)

            if i == 1:
                next_post_elements = driver.find_elements(By.CSS_SELECTOR, "button._abl-")
                if len(next_post_elements) > 0:
                    next_post = next_post_elements[0]
            else:
                next_post_elements = driver.find_elements(By.CSS_SELECTOR, "button._abl-")
                if len(next_post_elements) > 1:
                    next_post = next_post_elements[1]

            if next_post:
                next_post.click()
                time.sleep(3)
                i += 1
            else:
                # 다음 링크로 이동
                break

        # 다음 링크로 이동
        next_link_elements = driver.find_elements(By.CSS_SELECTOR, "a.coreSpriteRightPaginationArrow")
        if len(next_link_elements) > 0:
            next_link = next_link_elements[0]
            next_link.click()
            time.sleep(3)

    driver.quit()


urlList = [
    # "https://www.instagram.com/explore/locations/178094996400669/jamwon-hangang-park/",
    # "https://www.instagram.com/explore/locations/122895854963617/-cafe-knotted-cheongdam/",
    # "https://www.instagram.com/explore/locations/239485922/alver/",
    "https://www.instagram.com/explore/locations/132780913928216/-downtowner-cheongdam/",
    "https://www.instagram.com/explore/locations/421578965117914/andaz-seoul-gangnam-/",
    "https://www.instagram.com/explore/locations/229531766/jw-marriott-hotel-seoul/",
    "https://www.instagram.com/explore/locations/111748813803643/mondrian-seoul-itaewon/",
    "https://www.instagram.com/p/Csn78Y8vP_a/",
    "https://www.instagram.com/explore/locations/109430270864707/daily-cheongdam/",
    "https://www.instagram.com/explore/locations/818710853/blue-square-seoul-south-korea/",
    "https://www.instagram.com/explore/locations/101307075338041/"
]

email = input('이메일: ')
password = getpass.getpass('비밀번호: ')

for url in urlList:
    crawler(email, password, url)
    time.sleep(10)
