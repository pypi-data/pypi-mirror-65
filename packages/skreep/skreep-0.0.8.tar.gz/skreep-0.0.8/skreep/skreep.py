from selenium import webdriver
from time import sleep

class Skreep:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(executable_path='.\\chromedriver.exe', options=options)
        
    def quit(self):
        self.driver.quit()
        
    def get(self, url, sc=0):
        self.driver.get(url)
        sleep(sc)
        
    def tag(self, *args, set='default', sc=0):
        if 'default' == set:
            tag_name = self.driver.find_element_by_tag_name(args[0])
            sleep(sc)
            return tag_name

        if 'in' == set:
            tag_name = args[0].find_element_by_tag_name(args[1])
            sleep(sc)
            return tag_name
 
    def clas(self, *args, set='default', sc=0):
        if 'default' == set:
            class_name = self.driver.find_element_by_class_name(args[0])
            sleep(sc)
            return class_name

        if 'in' == set:
            class_name = args[0].find_element_by_class_name(args[1])
            sleep(sc)
            return class_name

    def id(self, *args, set='default', sc=0):
        if 'default' == set:
            id_name = self.driver.find_element_by_id(args[0])
            sleep(sc)
            return id_name
        
        if 'in' == set:
            id_name = args[0].find_element_by_id(args[1])
            sleep(sc)
            return id_name

    def path(self, *args, set='default', sc=0):
        if 'default' == set:
            xpath_name = self.driver.find_element_by_xpath('//*[@'+ args[0] +']')
            sleep(sc)
            return xpath_name

        if 'in' == set:
            xpath_name = args[0].find_element_by_xpath('//*[@'+ args[1] +']')
            sleep(sc)
            return xpath_name

    def paths(self, xpath, sc=0):
        xpath_name = self.driver.find_elements_by_xpath('//*[@'+ xpath +']')
        sleep(sc)
        return xpath_name

    def img(self, *args, set="pa", sc=0):
        
        if "pa" == set:
            sleep(sc)
            return [i.get_attribute(args[1]) for i in self.driver.find_elements_by_xpath('//*[@'+ args[0] +']')]

        elif "pta" == set:
            sleep(sc)
            return [i.find_element_by_tag_name(args[1]).get_attribute(args[2]) for i in self.driver.find_elements_by_xpath('//*[@'+ args[0] +']')]

        elif "ota" == set:
            sleep(sc)
            return [i.get_attribute(args[2]) for i in args[0].find_elements_by_tag_name(args[1])]
