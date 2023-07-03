from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def add_to_cart(driver, price):
    """adds the products to the cart and return number of items added"""
    for amount in price:
        driver.find_element(By.XPATH,f"//*[contains(text(),'{amount}')]"
                                     f"/following-sibling::button").click()
    cart_item = driver.find_element(By.ID,"cart").text
    if cart_item == "1 item":
        print("Added 1 items, redirecting to cart")
    else:
        print("Kindly add 1 items to proceed to cart")

def get_product(temp):
    """returns the product and types of items depending on the temperature value"""
    product = ""
    items = list()
    if temp < 30:
        product = "moisturizer" 
        items = ["Almond"or"Aloe"]
    elif temp > 30:
        product = "sunscreen"
        items = ["SPF-30"or"SPF-50"]
    return product,items

def get_temperature(driver):
    """returns the temperature on the landing page"""
    temp = driver.find_element(By.XPATH,"//span[contains(@id,'temperature')]")
    # Slice only the temperature value
    temp = int(temp.text[:-2])
    return temp

def click_on_buy(driver, product):
    """go to product page based on the temperature value"""
    driver.find_element(By.XPATH,f"//button[contains(.,'Buy {product}s')]").click()


def take_me_to_product_page(driver):
    """takes from landing page to product page"""
    temperature = get_temperature(driver)
    product,items = get_product(temperature)
    click_on_buy(driver, product)
    return items

def min_price(driver, items):
    """Returns the price of the least expensive aloe and almond products"""
    price = list()
    for item in items:
        item_list = driver.find_elements(By.XPATH,f"//*[contains(text(),'{item}') or "
                                                  f"contains(text(),'{item.lower()}')]"
                                                  f"/following-sibling::p")
        price_list = [item_list[i-1].text for i in range(len(item_list))]
        price_only = [price[-3:] for price in price_list]
        price.append(int(min(price_only)))
    return price

def take_me_to_cart(driver):
    """takes from landing page to cart page"""
    items = take_me_to_product_page(driver)
    cheap_products = min_price(driver, items)
    add_to_cart(driver, cheap_products)
    click_on_cart(driver)
    return cheap_products

def click_on_cart(driver):
    """go to cart page"""
    driver.find_element(By.ID,"cart").click()

def cart_page():
    """takes you to the cart page"""
    # create webdriver instance and navigate to main page
    driver = webdriver.Firefox()
    # navigate to main page
    driver.get("https://weathershopper.pythonanywhere.com/")
    # go to product page depending on the temperature
    items = take_me_to_product_page(driver)
    time.sleep(3)
    # find the least expensive products
    cheap_products = min_price(driver,items)
    # add them to cart
    add_to_cart(driver,cheap_products)
    # go to cart
    click_on_cart(driver)
    time.sleep(100)
    driver.quit()
if __name__ == "__main__":
    cart_page()
