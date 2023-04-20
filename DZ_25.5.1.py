import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:\Users\2668a\Документы\project\chromedriver.exe')
    # Переход на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.implicitly_wait(10) #Неявное ожидание
    pytest.driver.find_element(By.ID, 'email').send_keys('marsochka@gmail.com')
    pytest.driver.find_element(By.ID,'pass').send_keys('Cataract123') # Вводим пароль
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что находимся на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Явные ожидания
    images = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))



    for i in range(len(names)): #Перебор всех элементов
        assert images[i].get_attribute('src') != '', #Есть фотография
        assert names[i].text != '', #Есть имя
        assert descriptions[i].text != '', #Поле не пустое
        assert ', ' in descriptions[i] #Есть запятая
        parts = descriptions[i].text.split(", ") #Разделение строки на части
        assert len(parts[0]) > 0 #Проверка наличия вида в первой части
        assert len(parts[1]) > 0 #Проверка наличия возраста во второй части
