import pytest
from py._xmlgen import html

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("测试人: 龙雄")])