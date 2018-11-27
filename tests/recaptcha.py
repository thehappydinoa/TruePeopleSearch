from random import randint
from time import sleep

from fake_useragent import UserAgent
from selenium.common.exceptions import (NoSuchWindowException,
                                        WebDriverException)
from splinter import Browser
from splinter.exceptions import ElementDoesNotExis


def rand_sleep(a, b):
    sleep(randint(a, b))


def solve_captcha(url):
    ua = UserAgent()
    browser = Browser("firefox", user_agent=ua.random)
    browser.visit(url)

    try:
        iframe_name = browser.find_by_xpath("//iframe").first["name"]
        with browser.get_iframe(iframe_name) as iframe:
            checkbox = iframe.find_by_xpath(
                '//*[@id="recaptcha-anchor"]').first
            if iframe.is_text_present("I'm not a robot"):
                print("Captcha Loaded")
                print("Waiting....")
                rand_sleep(1, 5)
                print("Mouse Over")
                checkbox.mouse_over()
                rand_sleep(0, 1)
                print("Click")
                checkbox.click()

        while not browser.is_text_present("You are verified"):
            sleep(0.5)

        submit = browser.find_by_xpath("/html/body/form/button").first
        submit.click()

        if "InternalCaptcha" in browser.url:
            print("Failed")
        browser.quit()
    except ElementDoesNotExist:
        print("Failed")
        browser.quit()
    except NoSuchWindowException:
        print("Browser Closed")
        exit(1)
    except WebDriverException:
        print("Browser Broke")
        exit(1)


if __name__ == "__main__":
    solve_captcha(
        "https://www.truepeoplesearch.com/InternalCaptcha?returnUrl=%2fresults%3fname%3dAdam%2520M%2520Leighton%26personid%3dpxrr2492ulurl862r9ul4%26rid%3d0x0")
