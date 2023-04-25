import os
import json
import VimeoDownloader
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import unquote

class ScriptDownloader():
    def __init__(self):
        self.url = "https://pro.codely.tv/auth/sign-in/"
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        self.driver = webdriver.Chrome(desired_capabilities=caps)
        self.email = "nicolasliendro0697@gmail.com"
        self.password = "nicocentra7"
        self.list_courses = []
        self.links_sections = []

    def get_into_webpage(self):
        print("Abriendo CodelyTV PRO")
        self.driver.get(self.url)

    def wait_for_webpage(self, path_component):
        delay = 15
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, path_component)))
        except TimeoutException:
            print ("Loading took too much time!")

    def fill_login_input(self):
        email_input_path = "/html/body/div[2]/div/div[1]/div/div/div[2]/div/form/div/div[1]/div[1]/div/div/input"
        email_input = self.driver.find_element(By.XPATH, email_input_path)
        email_input.clear()
        email_input.send_keys(self.email)
        password_input_path = "/html/body/div[2]/div/div[1]/div/div/div[2]/div/form/div/div[2]/div[1]/div[1]/div/input"
        password_input = self.driver.find_element(By.XPATH, password_input_path)
        password_input.clear()
        password_input.send_keys(self.password)

    def click_button_login(self):
        button_accept_path = "/html/body/div[2]/div/div[1]/div/div/div[2]/div/form/footer/div/button"
        button_accept = self.driver.find_element(By.XPATH, button_accept_path)
        ActionChains(self.driver).click(button_accept).perform()

    def get_list_links_courses(self):
        class_courses_list = 'hdUQvy'
        courses_list = self.driver.find_element_by_class_name(class_courses_list)
        class_link_course = 'kvoVKQ'
        for child in courses_list.find_elements_by_class_name(class_link_course):
            course_link = child.get_attribute('href')
            self.list_courses.append(course_link)

    def go_thorough_courses(self):
        for course in self.list_courses:
            self.driver.get(course)
            time.sleep(3)
            list_show_button = self.driver.find_elements_by_class_name('ccMvAH')
            print("Obteniendo los links de cada video...")
            for show_button in list_show_button:
                if "Show" in show_button.text:
                    ActionChains(self.driver).click(show_button).perform()
                    time.sleep(1)
            self.get_link_courses()
            self.download_course()

    def get_link_courses(self):
        class_section = 'PathStepDetails__Link'
        list_sections = self.driver.find_elements_by_class_name(class_section)
        for element_link in list_sections:
            self.links_sections.append(element_link.get_attribute("href"))

    def download_course(self):
        index = 0
        for link in self.links_sections:
            index = index + 1
            self.driver.get(link)
            time.sleep(5)
            course_name = self.decode_title(self.driver.title)
            download_course_directory = self.create_directory(course_name)
            url_video = self.get_video()
            title_video = self.driver.find_element_by_class_name('PathStepDetails__Title').text
            title_video_decoded = self.decode_title(title_video)
            self.download_video(url_video, course_name, index)
            self.get_doc(title_video_decoded, download_course_directory)
            
    def create_directory(self, course_title):
        actual_directory = os.getcwd()
        download_course_directory = actual_directory + '\Downloads\\' + course_title
        if not os.path.isdir(download_course_directory):
            os.mkdir(download_course_directory)
        return download_course_directory
    
    def get_video(self):
        url_videos = []
        try:
            Resources = self.driver.execute_script("return window.performance.getEntries();")
            is_vimeo_on_network = False
            for resource in Resources:
                if "vimeo" in resource['name']:
                    is_vimeo_on_network = True
                    url = resource['name']
                    url_videos.append(url)
            if is_vimeo_on_network == False:
                iframe_video = self.driver.find_elements_by_tag_name('iframe')
                for iframe in iframe_video:
                    src_iframe = iframe.get_attribute('src')
                    if "vimeo" in src_iframe or "youtube" in src_iframe:
                        url = src_iframe
                        url_videos.append(url)
        except:
            print("Esta pagina no contiene video.")
        finally:
            return url_videos

    def decode_title(self, string_title):
        string_title = string_title.encode('ascii', 'ignore').decode('ascii')
        string_title = string_title.lstrip()
        characters_to_remove = "\/:*?\"<>|"
        for character in characters_to_remove:
            string_title = string_title.replace(character, "")  
        return string_title

    def download_video(self, url_videos, course_name, index):
        for url in url_videos:
            vimeo_downloader = VimeoDownloader.VimeoDownloader(course_name, index)
            if "vimeo" in url:
                video_id = vimeo_downloader.get_video_id(url)
                if video_id == url:
                    vimeo_downloader.download_video(video_id, url)
                vimeo_downloader.download_video(video_id)
            if "youtube" in url:
                url_youtube = vimeo_downloader.get_url_youtube(url)
                vimeo_downloader.download_video_youtube(url_youtube)

    def get_doc(self, title_video, download_course_directory):
        try:
            html_doc = self.driver.find_element_by_class_name('ContentText').get_attribute('outerHTML')
            soup = BeautifulSoup(html_doc, 'html.parser')
            title_html_file = title_video + '.html'
            download_course_directory_notes = download_course_directory + '\\' + title_html_file
            with open(download_course_directory_notes, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
        except:
                print("Este video no posee notas.")

if __name__ == "__main__":
    script_downloader = ScriptDownloader()
    script_downloader.get_into_webpage()
    login_path = "/html/body/div[2]/div/div[1]/div/div/div[2]/div/form/div/div[1]/div[1]/div/div/input"
    script_downloader.wait_for_webpage(login_path)
    script_downloader.fill_login_input()
    script_downloader.click_button_login()
    main_path = "/html/body/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/ul/li[1]/div"
    script_downloader.wait_for_webpage(main_path)
    script_downloader.get_list_links_courses()
    script_downloader.go_thorough_courses()
