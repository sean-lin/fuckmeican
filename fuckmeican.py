#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

USER = ""
PASSWD = "123456"
ADDRESS_KEYWORD = '1903'
CROP_NAMES = {
    u'广州简悦午餐':  u'支竹牛腩饭',
    u'广州简悦晚餐':  u'麻辣牛辗饭',
}

browser = webdriver.Firefox()


def login(user, password):
    browser.find_element_by_id("email").send_keys(user)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_id("signin").click()


def is_switch_done(d):
    c = d.find_element_by_xpath('/html/body').get_attribute('class')
    return 'masked' not in c


def select(crop):
    browser.find_element_by_id("more_tab").click()
    crops = \
        browser.find_elements_by_css_selector(
            '.tab_tipsy_table >tbody > tr .tab_name > a')
    for i in crops:
        if i.text.find(crop) != -1:
            i.click()
            WebDriverWait(
                browser, 10).until(is_switch_done)
            return
    raise Exception('select')


def is_search_done(d):
    return d.find_element_by_css_selector('#regular_dish_revision_list')


def order(foodname):
    browser.find_element_by_id(
        "search_box").send_keys(foodname + Keys.RETURN)
    WebDriverWait(browser, 10).until(is_search_done)

    foods = browser.find_elements_by_css_selector(".name_outer .name")
    print len(foods)
    for i in foods:
        if i.text.find(foodname) != -1:
            i.click()
            return
    raise Exception('order')


def set_address(address_keyword):
    WebDriverWait(browser, 10).until(
        lambda x: x.find_element_by_id('cart').is_displayed())
    browser.find_element_by_id("cart").click()
    WebDriverWait(browser, 10).until(
        lambda x: x.find_element_by_id('corp_add_order_btn').is_displayed())
    locations = \
        browser.find_elements_by_css_selector("#corp_pick_up_location > div")
    for i in locations:
        if i.text.find(address_keyword) != -1:
            i.click()
            return
    raise Exception('set_address')


def submit():
    browser.find_element_by_id('corp_add_order_btn').click()
    WebDriverWait(browser, 10).until(
        lambda x: x.find_element_by_id('corp_order_actions').is_displayed())


def main():
    browser.get('http://meican.com/login')
    login(USER, PASSWD)
    for k in CROP_NAMES:
        browser.get('http://meican.com')
        select(k)
        order(CROP_NAMES[k])
        set_address(ADDRESS_KEYWORD)
        submit()

    browser.quit()

if __name__ == '__main__':
    main()
