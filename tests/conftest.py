import pytest
import allure
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from selene.support.shared import browser

import project
import Full_setup_tests_todomvc.helpers.allure.gherkin


def pytest_addoption(parser):
    project.Config.register(parser)


@pytest.fixture
def config(request):
    if not project.config:
        project.config = project.Config(request)
    return project.config


@pytest.fixture(scope='function', autouse=True)
def browser_management(config):
    browser.config.timeout = config.timeout
    browser.config.save_page_source_on_failure \
        = config.save_page_source_on_failure
    yield

    browser.quit()


prev_test_screenshot = None
prev_test_page_source = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    yield

    global prev_test_screenshot
    prev_test_screenshot = browser.config.last_screenshot
    global prev_test_page_source
    prev_test_page_source = browser.config.last_page_source


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    result = outcome.get_result()

    if Full_setup_tests_todomvc.helpers.allure.gherkin.when == 'call' and result.failed:
        last_screenshot = browser.config.last_screenshot
        if last_screenshot and not last_screenshot == prev_test_screenshot:
            allure.attach.file(source=last_screenshot,
                               name='screenshot',
                               attachment_type=allure.attachment_type.PNG)

        last_page_source = browser.config.last_page_source
        if last_page_source and not last_page_source == prev_test_page_source:
            allure.attach.file(source=last_page_source,
                               name='page source',
                               attachment_type=allure.attachment_type.HTML)
