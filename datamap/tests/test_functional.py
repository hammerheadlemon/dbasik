import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = "/opt/firefox-quantum/firefox"
    firefox_options.headless = True
    return firefox_options


def test_upload_datamap_form_title(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    assert "Upload datamap" in selenium.title


def test_upload_datamap_form_items(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    assert "Upload datamap" in selenium.title
    assert selenium.find_element_by_id("form-table")
    assert selenium.find_element_by_id("id_file_name")
    assert selenium.find_element_by_id("id_target_datamap")
    assert selenium.find_element_by_id("id_uploaded_file")
    assert selenium.find_element_by_id("id_replace_all_entries")
    assert selenium.find_element_by_id("upload-button")


@pytest.mark.nondestructive
def test_upload_incorrect_csv(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    selenium.find_element_by_id("id_uploaded_file").send_keys("/home/lemon/Documents/bcompiler/source/datamap.csv")
    selenium.find_element_by_id("id_file_name").send_keys("Test file")
    selenium.find_element_by_id("upload-button").click()
    try:
        message = WebDriverWait(selenium, 3).until(EC.presence_of_element_located((By.ID, 'message-test')))
        print("Message found!")
        assert "Incorrect headers in csv file" in message.text
    except TimeoutException:
        print("No... timed out")
