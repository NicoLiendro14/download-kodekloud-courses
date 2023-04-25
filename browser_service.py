import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from undetected_chromedriver import ChromeOptions


def get_courses_url():
    options = ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Users\Nicolas\Desktop\UpWork Projects\pythonProject7\data_browser")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://kodekloud.com/courses/')
    all_links = driver.find_elements(By.TAG_NAME, "a")
    matching_links = []
    for link in all_links:
        try:
            if "https://kodekloud.com/courses/" in link.get_attribute("href"):
                classes = link.get_attribute("class")
                if "bb-cover-wrap" in classes.split():
                    matching_links.append(link.get_attribute("href"))
        except:
            pass
    # Cierra el navegador
    with open("enlaces.txt", "w") as archivo:
        # Escribimos cada enlace en una línea separada
        for enlace in matching_links:
            archivo.write(enlace + "\n")
    driver.quit()
    return matching_links


