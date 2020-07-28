from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bidi.algorithm import get_display
import time


def get_article_talkbacks(url):
    options = Options()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(
        executable_path=r"./chromedriver.exe", options=options)
    driver.get(url)

    # load comments section
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)

    # load additional comments
    try:
        driver.execute_script('document.querySelector("#block-system-main > div > div.center-wrapper > div.panel-col-first.panel-panel > div > div.panel-pane.pane-spotim-comments > div > div:nth-child(4) > div:nth-child(6) > div").shadowRoot.querySelector("#spotim-specific-conversation > div > div.spcv_conversation > div.spcv_loadMoreCommentsContainer > div").click()')
        time.sleep(3)
    except:
        print("No additional comments to load")

    try:
        all_comments = driver.execute_script('return document.querySelector("#block-system-main > div > div.center-wrapper > div.panel-col-first.panel-panel > div > div.panel-pane.pane-spotim-comments > div > div:nth-child(4) > div:nth-child(6) > div").shadowRoot.querySelectorAll(".spcv_message-container")')
        for comment in all_comments:
            try:
                comment_by = driver.execute_script('return arguments[0].querySelector(".spcv_username").innerText', comment)
                try:
                    comment_to = driver.execute_script('return arguments[0].querySelector(".spcv_reply-username").innerText', comment)
                except:
                    pass

                text = driver.execute_script(
                    'return arguments[0].querySelector(".spcv_message-entities").innerText', comment)
                try:
                    likes = driver.execute_script(
                        'return arguments[0].querySelectorAll(".spcv_likes-count")[0].innerText', comment)
                except:
                    pass

                try:
                    dislikes = driver.execute_script(
                        'return arguments[0].querySelectorAll(".spcv_likes-count")[1].innerText', comment)
                except:
                    pass

                print("Comment by: " + get_display(comment_by))
                try:
                    print("Comment to: " + get_display(comment_to))
                except:
                    pass
                print("Comment text: " + get_display(text))
                try:
                    print("Likes: " + get_display(likes))
                except:
                    print("No likes for this comment")
                try:
                    print("Dislikes: " + get_display(dislikes))
                except:
                    print("No dislikes for this comment")
                print("--------------------------------------------------------")
            except:
                print("Rejected message has been deleted")
    except:
        print("No comments found")
    driver.quit()

url = "https://www.israelhayom.co.il/article/784471"
get_article_talkbacks(url)
