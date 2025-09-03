import json, os
import glob
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
from colorama import Fore, init
init()
from time import sleep
import keyboard
import threading
import shutil
import gdown
from PIL import Image
from pillow_heif import register_heif_opener
import re 
import rich
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.style import Style
from rich.text import Text

with open("config.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
    q_portrait = config["form_questions"]["portrait"]
    q_signature = config["form_questions"]["signature"]
    q_firstname = config["form_questions"]["first name"]
    q_middlename = config["form_questions"]["middle name"]
    q_lastname = config["form_questions"]["last name"]
    q_dob = config["form_questions"]["dob"]
    q_eyecolor = config["form_questions"]["eye color"]
    q_haircolor = config["form_questions"]["hair color"]
    q_address = config["form_questions"]["address"]
    q_city = config["form_questions"]["city"]
    q_zip = config["form_questions"]["zip"]
    q_gender = config["form_questions"]["gender"]
    q_glasses = config["form_questions"]["glasses"]
    q_organdonor = config["form_questions"]["organ donor"]
    q_state = config["form_questions"]["state"]

def login(driver):
    
    url = "https://idplug.su/usercenter/usercenter"
    driver.uc_open_with_reconnect(url, 4)
    # ^ Bypasses Cloudflare Captcha ^
    logcheck = WebDriverWait(driver=driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"container_body\"]/div/div/div[2]/div/div[3]/div[1]/input")))

    if logcheck.is_displayed():
        pass_for_login = driver.find_element(By.XPATH, "//*[@id=\"container_body\"]/div/div/div[2]/div/div[3]/div[2]/input")
        print(Fore.LIGHTYELLOW_EX, "[/] Logging In...")
        logcheck.send_keys(config["login"]['email'])
        pass_for_login.send_keys(config["login"]['password'])
        logbutton = driver.find_element(By.XPATH, "//*[@id=\"container_body\"]/div/div/div[2]/div/div[3]/div[5]/button")
        logbutton.click()
        print("[+] Logged In")
    else:
        print("[-] Error")

    sleep(1)
    return

def upload_photos(driver, order_name, item):
    keyboard = Controller()
    cwd = os.getcwd()

    if item[q_portrait].startswith('http'):
        fullname = item[q_firstname] + item[q_lastname]
    else:
        fullname = os.path.basename(item[q_portrait])
        fullname = fullname.split('.')[0]

    os.chdir("./idphotos")
    fullphotopath = str(os.path.abspath(glob.glob(f"{fullname}.*")[0]))

    os.chdir(cwd) 
    os.chdir("./sigphotos")

    fullsigpath = str(os.path.abspath(glob.glob(f"{fullname}.*")[0]))
    os.chdir(cwd)

    try:
        photoupload = driver.find_element(By.CSS_SELECTOR, "#_img1").click()
        sleep(0.6)
        keyboard.type(fullphotopath)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        photoupload = driver.find_element(By.CSS_SELECTOR, "#_img1").click()
        sleep(0.6)
        keyboard.type(fullphotopath)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        WebDriverWait(driver, 100).until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id=\"_img1\"]/div[2]"), "100"))
        sleep(0.2)
    except:
        print(f"[-] Photo Upload Failed - {fullname}")
        pass

    try:
        sigupload = driver.find_element(By.CSS_SELECTOR, "#_img2").click()
        sleep(0.6)
        keyboard.type(fullsigpath)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        sigupload = driver.find_element(By.CSS_SELECTOR, "#_img2").click()
        sleep(0.6)
        keyboard.type(fullsigpath)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        WebDriverWait(driver, 100).until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id=\"_img2\"]/div[2]"), "100"))
        sleep(0.3)
        addtocart = driver.find_element(By.XPATH, "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[4]/div[2]/button[2]").click()
        sleep(0.2)
        agebox = driver.find_element(By.XPATH, "//*[@id=\"layui-layer8\"]/div[3]/a[1]")
        if agebox.is_displayed():
            agebox.click()
        state = item[q_state]
        print(Fore.LIGHTYELLOW_EX, f"[+] Added | {fullname} | {state}")
    except:
        print(f"[-] Signature Upload Failed - {fullname}")
        pass
    sleep(0.5)
    return

def add_to_cart(driver, order_name):
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
        q_firstname = config["form_questions"]["first name"]
        q_middlename = config["form_questions"]["middle name"]
        q_lastname = config["form_questions"]["last name"]
        q_dob = config["form_questions"]["dob"]
        q_eyecolor = config["form_questions"]["eye color"]
        q_haircolor = config["form_questions"]["hair color"]
        q_height = config["form_questions"]["height"]
        q_address = config["form_questions"]["address"]
        q_city = config["form_questions"]["city"]
        q_zip = config["form_questions"]["zip"]
        q_gender = config["form_questions"]["gender"]
        q_glasses = config["form_questions"]["glasses"]
        q_organdonor = config["form_questions"]["organ donor"]
        q_state = config["form_questions"]["state"]
        q_weight = config["form_questions"]["weight"]

    e_value = {
    "first_name": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[1]/input",
    "middle_name": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[2]/input",
    "last_name": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[3]/input",
    "dob": "//*[@id=\"personial_information_date_6\"]",
    "weight": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[9]/input",
    "address": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[10]/input",
    "city": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[11]/input",
    "zip_code": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[12]/input"
    },

    gender_value = {
        "gender_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div/div",
        "male": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div/div/ul/li[2]",
        "female": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div/div/ul/li[3]"
    },

    height_value = {
        "height_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div",
        "5-00": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[2]",
        "5-01": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[3]",
        "5-02": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[4]",
        "5-03": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[5]",
        "5-04": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[6]",
        "5-05": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[7]",
        "5-06": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[8]",
        "5-07": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[9]",
        "5-08": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[10]",
        "5-09": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[11]",
        "5-10": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[12]",
        "5-11": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[13]",
        "6-00": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[14]",
        "6-01": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[15]",
        "6-02": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[16]",
        "6-03": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[17]",
        "6-04": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[18]",
        "6-05": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[19]",
        "6-06": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[20]",
        "6-07": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[21]",
        "6-08": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[22]",
        "6-09": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[23]",
        "6-10": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[24]",
        "6-11": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[25]",
        "6-12": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[8]/div/div/ul/li[26]"
    },

    eyes_value = {
        "eyes_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div",
        "Brown" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[2]",
        "Green" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[3]",
        "Hazel" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[4]",
        "Blue" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[5]",
        "Black" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[6]",
        "Grey" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[7]",
        "Sandy" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[8]",
        "Multicolor" : "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[5]/div/div/ul/li[9]"
    },

    hair_value = {
        "hair_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div",
        "Black": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[2]",
        "Brown": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[3]",
        "Red": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[4]",
        "Bald": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[5]",
        "Blonde": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[6]",
        "Gray": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[2]/div/div/div/div/div[6]/div/div/ul/li[7]"
    },

    glasses_value = {
        "glasses_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[3]/div/div",
        "no": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[3]/div/div/ul/li[2]",
        "yes": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[3]/div/div/ul/li[3]"
    },

    organ_donor_value = {
        "organ_donor_main": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[4]/div/div",
        "yes": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[4]/div/div/ul/li[3]",
        "no": "//*[@id=\"container_body\"]/div/div[1]/div[4]/div[3]/div/div/div/div/div[4]/div/div/ul/li[3]"
    }

    login(driver)
    cookies = driver.get_cookies()
    with open("cookies.json", 'w') as f:
        json.dump(cookies, f)
    

    with open(f"./orders/{order_name}") as f:
        data = json.load(f)
        maximum = 0
        for item in data:
            maximum += 1
        print(Fore.LIGHTYELLOW_EX, f"[+] {maximum} Customers Found")
        for item in data:
            state = item[q_state]
            link = config["links"][state]
            driver.get(link)
            
            sleep(1)
            driver.maximize_window()
            driver.execute_script("window.scrollTo(1300, 450)")

            # Open Gender Dropdown
            genderbutton = driver.find_element(By.XPATH, gender_value[0]["gender_main"])
            driver.execute_script("arguments[0].click();", genderbutton)

            # Click Gender
            genderxpath = item[q_gender]
            genderxpath2 = gender_value[0][genderxpath]
            gender = driver.find_element(By.XPATH, genderxpath2)
            driver.execute_script("arguments[0].click();", gender)

            # Open Height Dropdown
            heightbutton = driver.find_element(By.XPATH, height_value[0]["height_main"])
            driver.execute_script("arguments[0].click();", heightbutton)

            # Click Height
            heightxpath = item[q_height]
            heightxpath2 = height_value[0][heightxpath]
            height = driver.find_element(By.XPATH, heightxpath2)
            driver.execute_script("arguments[0].click();", height)

            # Open Eyes Dropdown
            eyesbutton = driver.find_element(By.XPATH, eyes_value[0]["eyes_main"])
            driver.execute_script("arguments[0].click();", eyesbutton)

            # Click Eyes
            eyesxpath = item[q_eyecolor]
            eyesxpath2 = eyes_value[0][eyesxpath]
            eyes = driver.find_element(By.XPATH, eyesxpath2)
            driver.execute_script("arguments[0].click();", eyes)

            # Open Hair Dropdown
            hairbutton = driver.find_element(By.XPATH, hair_value[0]["hair_main"])
            driver.execute_script("arguments[0].click();", hairbutton)

            # Click Hair
            hairxpath = item[q_haircolor]
            hairxpath2 = hair_value[0][hairxpath]
            hair = driver.find_element(By.XPATH, hairxpath2)
            driver.execute_script("arguments[0].click();", hair)

            # Open Glasses Dropdown
            glassesbutton = driver.find_element(By.XPATH, glasses_value[0]["glasses_main"])
            driver.execute_script("arguments[0].click();", glassesbutton)

            # Click Glasses
            glassesxpath = item[q_glasses]
            glassesxpath2 = glasses_value[0][glassesxpath]
            glasses = driver.find_element(By.XPATH, glassesxpath2)
            driver.execute_script("arguments[0].click();", glasses)

            # Open Organ Donor Dropdown
            organbutton = driver.find_element(By.XPATH, organ_donor_value["organ_donor_main"])
            driver.execute_script("arguments[0].click();", organbutton)

            # Click Organ Donor
            organxpath = item[q_organdonor]
            organxpath2 = organ_donor_value[organxpath]
            organdonor = driver.find_element(By.XPATH, organxpath2)
            driver.execute_script("arguments[0].click();", organdonor)

            ### Dropdowns Done,
            ### Rest of page   

            firstname = driver.find_element(By.XPATH, e_value[0]["first_name"]).send_keys(item[q_firstname])
            if item[q_middlename].lower() == "n/a" or item[q_middlename].lower() == "na":
                middlename = None
            elif item[q_middlename] is not None:
                middlename = driver.find_element(By.XPATH, e_value[0]["middle_name"]).send_keys(item[q_middlename])
            lastname = driver.find_element(By.XPATH, e_value[0]["last_name"]).send_keys(item[q_lastname])
            dob = driver.find_element(By.XPATH, e_value[0]["dob"]).send_keys(item[q_dob])
            weight = driver.find_element(By.XPATH, e_value[0]["weight"]).send_keys(item[q_weight])
            address = driver.find_element(By.XPATH, e_value[0]["address"]).send_keys(item[q_address])
            city = driver.find_element(By.XPATH, e_value[0]["city"]).send_keys(item[q_city])
            zipcode = driver.find_element(By.XPATH, e_value[0]["zip_code"]).send_keys(item[q_zip])

            upload_photos(driver, order_name, item)

    print(f"[+] Order Added!")
    sleep(1)
    start()

    menu = input("> ")
    if menu == "1":
        pass

    if menu == "2":
        pass

    if menu == "3":
        pass

def curate():
    register_heif_opener()
    photo_path = os.path.abspath("./idphotos")
    signature_path = os.path.abspath("./sigphotos")

    
    for file in os.listdir(photo_path):
        file_for_edit = f"./idphotos/{file}"
        
                     
    # Convert HEIC
        if file.lower().endswith(".heic"):
            with Image.open(file_for_edit) as image:
                filename = file_for_edit[:-4] + "jpeg"
                image = image.convert("RGB")
                image.save(filename, "JPEG")
                os.remove(file_for_edit)

    # Convert JPG to JPEG
        elif file.lower().endswith(".jpg"):
            name = file[:-3] + "jpeg"
            os.rename(os.path.join(photo_path, file), os.path.join(photo_path, name))
    
    # Resize
    for photo in os.listdir(photo_path):
        with Image.open(file_for_edit) as img:
            width, height = img.size
            if width + height < 1024:
                    img.resize((512, 512)).save(f"./idphotos/{photo}")

    for file in os.listdir(signature_path):
        file_for_edit = f"./sigphotos/{file}"
        
    # Convert HEIC
        if file.lower().endswith(".heic"):
            with Image.open(file_for_edit) as image:
                filename = file_for_edit[:-4] + "jpeg"
                image = image.convert("RGB")
                image.save(filename, "JPEG")
                os.remove(file_for_edit)
    # Convert JPG to JPEG
        elif file.lower().endswith(".jpg"):
                name = file[:-3] + "jpeg"
                os.rename(os.path.join(signature_path, file), os.path.join(signature_path, name))
    
    # Resize
    for photo in os.listdir(signature_path):
        with Image.open(file_for_edit) as img:
            width, height = img.size
            if width + height < 1024:
                    img.resize((512, 512)).save(f"./sigphotos/{photo}")

def rename(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        file = os.path.abspath(file)
        try:
            newname = file.rsplit("-")[-1].replace(" ", "")
            print(newname)
            os.rename(folder_path + file, folder_path + newname)
        except:
            pass

def download_photos(order):

    with open(f"./orders/{order}") as f:
        data = json.load(f)

    count = 0
    cwd = os.getcwd()
    idphotos = cwd + "\\idphotos"
    sigphotos = cwd + "\\sigphotos"
    
    for item in data:
        url1 = str(data[count][q_portrait])
        url2 = str(data[count][q_signature])
        output = data[count][q_firstname] + data[count][q_lastname]
        filename1 = os.path.join(idphotos, output)
        filename2 = os.path.join(sigphotos, output)

        os.chdir(idphotos)
        if url1.startswith("https://drive.google.com"):
            if not glob.glob(f"{filename1}.*"):
                if url1 == None:
                    continue

                file = gdown.download(url=url1, fuzzy=True)

                if file.lower().endswith(".jpeg"):
                    os.rename(os.path.join(idphotos, file), os.path.join(idphotos, output + ".jpeg"))

                elif file.lower().endswith("png"):
                    os.rename(os.path.join(idphotos, file), os.path.join(idphotos, output + ".png"))

                elif file.lower().endswith(".jpg"):
                        os.rename(file, os.path.join(idphotos, output + ".jpeg"))
                
                elif file.lower().endswith((".heif", ".heic")):
                    register_heif_opener()
                    with Image.open(file) as image:
                        image = image.convert("RGB")
                        image.save(output + ".jpeg", "JPEG")
                        os.remove(file)
            else:
                print(f"skipping portrait download, {output} already exists.")


        os.chdir(cwd)

        os.chdir("./sigphotos")
        if url2.startswith("https://drive.google.com"):
            if not glob.glob(f"{filename2}.*") and filename2 != None:

                file = gdown.download(url=url2, fuzzy=True)

                if file.lower().endswith(".jpeg"):
                    os.rename(os.path.join(sigphotos, file), os.path.join(sigphotos, output + ".jpeg"))

                elif file.lower().endswith("png"):
                    os.rename(os.path.join(sigphotos, file), os.path.join(sigphotos, output + ".png"))

                elif file.lower().endswith(".jpg"):
                        os.rename(file, os.path.join(sigphotos, output + ".jpeg"))
                
                elif file.lower().endswith((".heif", ".heic")):
                    register_heif_opener()
                    with Image.open(file) as image:
                        image = image.convert("RGB")
                        image.save(output + ".jpeg", "JPEG")
                        os.remove(file)
            else:
                print(f"skipping signature download, {output} already exists.")
        count +=1
    os.chdir(cwd)
    start()


def check_form_q(order):
    with open(f"./orders/{order}", "r") as f:
        data = json.load(f)
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
        q_portrait = config["form_questions"]["portrait"]
        q_height = config["form_questions"]["height"]
        q_signature = config["form_questions"]["signature"]
        q_firstname = config["form_questions"]["first name"]
        q_middlename = config["form_questions"]["middle name"]
        q_lastname = config["form_questions"]["last name"]
        q_dob = config["form_questions"]["dob"]
        q_weight = config["form_questions"]["weight"]
        q_eyecolor = config["form_questions"]["eye color"]
        q_haircolor = config["form_questions"]["hair color"]
        q_address = config["form_questions"]["address"]
        q_city = config["form_questions"]["city"]
        q_zip = config["form_questions"]["zip"]
        q_gender = config["form_questions"]["gender"]
        q_glasses = config["form_questions"]["glasses"]
        q_organdonor = config["form_questions"]["organ donor"]
        q_state = config["form_questions"]["state"]
    dict = {
    'portrait': q_portrait in data[0],
    'signature': q_signature in data[0],
    'first name': q_firstname in data[0],
    'middle name': q_middlename in data[0],
    'last name': q_lastname in data[0],
    'date of birth': q_dob in data[0],
    'eye color': q_eyecolor in data[0],
    'hair color': q_haircolor in data[0],
    'address': q_address in data[0],
    'city': q_city in data[0],
    'zip': q_zip in data[0],
    'gender': q_gender in data[0],
    'glasses': q_glasses in data[0],
    'organ_donor': q_organdonor in data[0],
    'state': q_state in data[0]
}
    all_good = True
    false_values = []
    for key, value in dict.items():
        if not value:
            false_values.append(key)
    
    if false_values:
        print(Fore.RED+f"\n[-] Question Names Do Not Match\nFix:")
        for s in false_values:
            print(s)
        if input(Fore.GREEN + "\n[BETA] Attempt to Autofix? (y/n): ").lower() == "y":
            keywords = {
            "state": q_state,
            "signature": q_signature,
            "idphoto": q_portrait,
            "first": q_firstname,
            "middle": q_middlename,
            "last": q_lastname,
            "address": q_address,
            "street": q_address,
            "city": q_city,
            "zip": q_zip,
            "birth": q_dob,
            "date": q_dob,
            "dob": q_dob,
            "eye": q_eyecolor,
            "hair": q_haircolor,
            "height": q_height,
            "feet": q_height,
            "gender": q_gender,
            "sex": q_gender,
            "glasses": q_glasses,
            "organ donor": q_organdonor,
            }

            count = 0
            for item in data:
                print(Fore.BLUE + f"\n---=== Checking #{str(count)} ===---")
                for key in list(item.keys()):
                    for word, value in keywords.items():
                        if value.lower() != key.lower():
                            if word in key.lower():
                                item[value] = item.pop(key)
                                print(Fore.GREEN+f"\n[+] Changed: \"{key}\"\n[+] To: \"{value}\"\n[+] Based on Keyword: {word}\n[+] In Order: {order}\n")
                        else:
                            print(Fore.BLUE + f"[+] Matches: {key}")
                count += 1

            with open(f'./orders/{order}', 'w') as file:
                json.dump(data, file, indent=4)   

            print(Fore.GREEN+"\n[+] Autofix Complete\n[/] Checking Config..."+Fore.RESET)
            check_form_q(order)
        else:
            return False
    else:
        print(Fore.GREEN + "[+] All Questions Match.")
        return True

def start():
    os.system("cls")
    console = Console()
    for file in os.listdir("./orders"):
        filepath = os.path.join(os.path.abspath("./orders"), file)
        if file.endswith(".json"):
            with open(filepath) as f:
                data = json.load(f)
            
            table = Table(title=Text(f"╔═══ {file} ═══╗", style="Bold Magenta"), border_style="magenta", box=rich.box.ROUNDED)
            table.add_column("#", style="bold magenta", header_style="yellow")
            table.add_column("Name", style="bold magenta", width=25, header_style="yellow")
            table.add_column("State", style="bold magenta", width=20, header_style="yellow")
            table.add_column("ID Photo", justify="center", style="yellow", header_style="yellow")
            table.add_column("Signature", justify="center", style="yellow", header_style="yellow")
            count = 1

            for item in data:
                ## Check Photos
                idphoto = "No"
                sigphoto = "No"

                if item[q_portrait].startswith('http'):
                    fullname = item[q_firstname] + item[q_lastname]
                else:
                    fullname = os.path.basename(item[q_portrait])
                    fullname = fullname.split('.')[0]
                #print(fullname)

                fullphotopath = os.getcwd() + "\\idphotos\\" + fullname + ".jpeg"
                fullsigpath = os.getcwd() + "\\sigphotos\\" + fullname + ".jpeg"
                
                #print(fullphotopath)

                if os.path.isfile(fullphotopath):
                    idphoto = "Yes"
                else:
                    fullphotopath = os.getcwd() + "\\idphotos\\" + fullname + ".png"
 
                if os.path.isfile(fullsigpath):
                    sigphoto = "Yes"
                else:
                    fullsigpath = os.getcwd() + "\\sigphotos\\" + fullname + ".png"
                    if os.path.isfile(fullsigpath):
                        sigphoto = "Yes"   

                with open("config.json", 'r') as f:
                    data = json.load(f)
                    
                firstname = item[q_firstname]
                lastname = item[q_lastname]
                state = item[q_state]
                
                if idphoto == "Yes": idphoto = "[green]Yes"
                elif idphoto == "No": idphoto = "[red]No"
                
                if sigphoto == "Yes": sigphoto = "[green]Yes"
                elif sigphoto == "No": sigphoto = "[red]No"
                
                table.add_row(str(count), f"{firstname} {lastname}", state, idphoto, sigphoto)

                count += 1
                
            console.print(table)

    console.print("""[bold magenta]╔═════════════════════════════════════════════════════════╗
║[bold yellow]                            d8b                       [magenta]   ║
║[bold yellow]                            88P                       [magenta]   ║
║[bold yellow]                            d88                       [magenta]   ║
║[bold yellow]    ?88   d8P d8888b?88,.d88b,888  ?88   d8P d888b8b  [magenta]   ║
║[bold yellow]    d88   88 d8P' `P`?88'  ?88?88  d88   88 d8P' ?88  [magenta]   ║
║[bold yellow]    ?8(  d88 88b      88b  d8P 88b ?8(  d88 88b  ,88b [magenta]   ║
║[bold yellow]    `?88P'?8b`?888P'  888888P'  88b`?88P'?8b`?88P'`88b[magenta]   ║ 
║[bold yellow]                    88P'                         )88  [magenta]   ║
║[bold yellow]                    d88                          ,88P [magenta]   ║
║[bold yellow]                    ?8P                      `?8888P  [magenta]   ║
║[bold yellow]    By spx                                            [magenta]   ║
╚═╦═══════════════════════════════════════════════════════╝
  ║ 1 > [bold magenta]Add To Cart[magenta]
  ║ 2 > [bold magenta]Download Photos[magenta]
  ║ 3 > [bold magenta]Check Config Compatability[magenta]      
  ║""")
    
    print(Fore.LIGHTMAGENTA_EX+"══╝ > ", end="")

    selection = input()
    if selection == "1":
        order = input("Add To Cart | Order?: ")
        if order.endswith(".json"):
            pass
        else:
            order = order + ".json"
        
        if not os.path.exists(os.path.abspath(f"./orders/{order}")):
            print("Invalid Order Name.")
            sleep(0.5)
            start()
        
        response = check_form_q(order=order)
        if response == True:
            
            from pyvirtualdisplay import Display
            with Display(visible=1, size=(1920, 1080)):
                driver = Driver(uc=True)
                add_to_cart(order_name=order, driver=driver)
        else:
            start()

    elif selection == ("2"):
        order = input("Download Photos > Order Name?: ")
        if order.endswith(".json"):
            pass
        else:
            order = order + ".json"

        if not os.path.exists(os.path.abspath(f"./orders/{order}")):
            print("Invalid Order Name.")
            sleep(0.5)
            start()
        print("\n[/] Ensure Google Drive Folder Privacy is Set To \"Anyone With The Link\" For Both Folders. If they arent, the program will crash. \n[ENTER] to continue")
        keyboard.wait("enter")
        download_photos(order)
        os.system("cls")
        start()

    elif selection == "3":
        order = input("Check Config Compatability | Order Name?: ")
        if order.endswith(".json"):
            pass
        else:
            order = order + ".json"
        if not os.path.exists(os.path.abspath(f"./orders/{order}")):
            print("Invalid Order Name.")
            sleep(0.5)
            start()
        check_form_q(order)
        sleep(0.5)
        os.system("cls")
        start()

    else:
        os.system("cls")
        start()

start()