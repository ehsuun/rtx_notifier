from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import random
from pushbullet import Pushbullet
import io
from IPython.display import clear_output
import time
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import datetime
import sys

# your pushbullet API key
api_key = "########################"
pb = Pushbullet(api_key)

newegg_email = "###@###.###"
newegg_password = "###############"
cc_number = "###############"
cc_cvv = "####"


# Update the search term for each of the vendors. the css class to look for. should be fine for a while. currenly setup for 3080 
vendict = {"newegg" : (0,"https://www.newegg.com/p/pl?d=3080&N=100007709%20601357247&isdeptsrh=1","item-cell","add to cart",2),
          "nvidia" : (0,"https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080/","content-table","add to cart",5),
          "bestbuy" : (0,"https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080","sku-item","add to cart",5),
          "asus": (0,"https://store.asus.com/us/search?q=3080&s_c=1","item","buy now",30),
          "zotac": (0,"https://store.zotac.com/zotac-gaming-geforce-rtx-3080-trinity-zt-a30800d-10p","product-essential","add to cart",20),
          "amazon":(0,"https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82","style__item__3gM_7","add to cart",5), 
          "evga": (0,"https://www.evga.com/products/ProductList.aspx?type=0&family=GeForce+30+Series+Family","list-item","qty",3),
          "bh" : (0,"https://www.bhphotovideo.com/c/products/Graphic-Cards/ci/6567/N/3668461602?filters=fct_nvidia-geforce-series_5011%3Ageforce-rtx-3080","product_19pae40ejOyj6V7StHfjYz","add to cart",30)
         }


driver = webdriver.Firefox()
shouldexit = False

def restart():
    global driver
    driver.close()
    driver = webdriver.Firefox()


def orderItem_newegg(item):
    global shouldexit
    btn = item.find_elements_by_class_name("btn-primary")[0]
    btn.click()
    time.sleep(0.5)
    driver.get("https://secure.newegg.com/Shopping/ShoppingCart.aspx")
    time.sleep(0.5)
    driver.get("javascript:attachDelegateEvent((function(){Biz.GlobalShopping.ShoppingCart.checkOut('True')}));")
    time.sleep(3)
    
    emailinput = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
    emailinput.send_keys(newegg_email)

    loginbtn = driver.find_elements_by_class_name("btn-orange")[0]
    loginbtn.click()
    time.sleep(2)
    pswd = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "labeled-input-password")))
    pswd.send_keys(newegg_password)

    loginbtn = driver.find_elements_by_class_name("btn-orange")[0]
    loginbtn.click()
    time.sleep(5)

    driver.get("javascript:Biz.GlobalShopping.CheckOut.continueToBilling();")
    time.sleep(2)

    inp = driver.find_elements_by_id("ReEnterCardNum182697655")
    if len(inp)>0 and inp[0].is_displayed():
        inp[0].send_keys(cc_number)

    inp = driver.find_elements_by_id("creditCardCVV2")
    if len(inp)>0 and inp[0].is_displayed():
        inp[0].send_keys(cc_cvv)

    driver.get("javascript:Biz.GlobalShopping.CheckOut.continueToReview(1);")
    time.sleep(2)

    driver.get("javascript:Biz.Shopping.CheckAddress.useInteractionRequired('Shippingusedsuggestedaddress');")
    time.sleep(2)

    driver.find_element_by_id("term").click()
    driver.get("javascript:Biz.GlobalShopping.CheckOut.submitOrder();")
    shouldexit = True

vendor = sys.argv[1]

showimage=False
def showitem(item,showimage=False):
    print(item.text+"\n")
    if not showimage:
        return

index = 0
while True:
    if index >100:
        restart()
        index=0
    index+=1
    delay = random.random()*10+vendict[vendor][4]
    print(vendor+"\n")
    #driver.switch_to.window(vendict[vendor][0])
    try:
        driver.get(vendict[vendor][1])
        time.sleep(3)
        try:
            items = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, vendict[vendor][2])))
            for item in items:
                now = datetime.datetime.now()
                print ("Time : ")
                print (now.strftime("%Y-%m-%d %H:%M:%S \n"))
                print(vendor+"\n")
                showitem(item,showimage)

                if item.text.lower().find(vendict[vendor][3])>-1:
                    for device in pb.devices:
                        pb.push_note("item available at "+vendor,item.text,device)
                    if vendor =="newegg":
                        orderItem_newegg(item)
                        break
        except TimeoutException as ex:
            print("site did not respond")
            delay+=15
    except WebDriverException as ex:
        print("site did not respond")
        delay+=15
    if shouldexit:
        pb.push_note("Done ordering and now exiting",pb.devices[0])
    time.sleep(delay)