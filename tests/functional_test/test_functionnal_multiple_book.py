import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.fixture(scope="class")
def driver_init(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(path=r"drivers").install()))
    request.cls.driver = driver
    driver.implicitly_wait(20)
    driver.maximize_window()
    yield
    driver.close()
    driver.quit()


@pytest.mark.usefixtures("driver_init")
class TestMultipleBook:

    def test_multiple_book_ko(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.find_element(By.ID, "email").send_keys("john@simplylift.co")
        self.driver.find_element(By.ID, "button_register").click()
        self.driver.find_element(By.ID, "url_book_CompetitionTest1").click()
        self.driver.find_element(By.ID, "nb_places").send_keys("11")
        self.driver.find_element(By.ID, "book_button").click()
        self.driver.find_element(By.ID, "url_book_CompetitionTest1").click()
        self.driver.find_element(By.ID, "nb_places").send_keys("2")
        self.driver.find_element(By.ID, "book_button").click()
        assert "The total of the place for this competition is more than 12" in self.driver.find_element(By.TAG_NAME,
                                                                                                         "li").text

    def test_multiple_book_ok(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.find_element(By.ID, "email").send_keys("kate@shelifts.co.uk")
        self.driver.find_element(By.ID, "button_register").click()
        self.driver.find_element(By.ID, "url_book_CompetitionTest1").click()
        self.driver.find_element(By.ID, "nb_places").send_keys("11")
        self.driver.find_element(By.ID, "book_button").click()
        self.driver.find_element(By.ID, "url_book_CompetitionTest1").click()
        self.driver.find_element(By.ID, "nb_places").send_keys("1")
        self.driver.find_element(By.ID, "book_button").click()
        assert "Already booked: 12" in self.driver.find_element(By.ID, "details_CompetitionTest1").text
        assert "Book Places" not in self.driver.find_element(By.ID, "details_CompetitionTest1").text
