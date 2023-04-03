# SQ-ASR-autoTest2

* How to run?

```bash
pytest Test_case_Login.py 
pytest Test_case_ergodic.py
```
* Or you can run in GUI mode

```bash
gui_test_runner.py
```

* Here are some common methods that you might use in tests:

```python
self.open(URL)  # Navigate to the web page
self.click(SELECTOR)  # Click a page element
self.type(SELECTOR, TEXT)  # Type text (Add "\n" to text for pressing enter/return.)
self.assert_element(SELECTOR)  # Assert element is visible
self.assert_text(TEXT)  # Assert text is visible (has optional SELECTOR arg)
self.assert_title(PAGE_TITLE)  # Assert page title
self.assert_no_404_errors()  # Assert no 404 errors from files on the page
self.assert_no_js_errors()  # Assert no JavaScript errors on the page (Chrome-ONLY)
self.execute_script(JAVASCRIPT)  # Execute JavaScript code
self.go_back()  # Navigate to the previous URL
self.get_text(SELECTOR)  # Get text from a selector
self.get_attribute(SELECTOR, ATTRIBUTE)  # Get a specific attribute from a selector
self.is_element_visible(SELECTOR)  # Determine if an element is visible on the page
self.is_text_visible(TEXT)  # Determine if text is visible on the page (optional SELECTOR)
self.hover_and_click(HOVER_SELECTOR, CLICK_SELECTOR)  # Mouseover element & click another
self.select_option_by_text(DROPDOWN_SELECTOR, OPTION_TEXT)  # Select a dropdown option
self.switch_to_frame(FRAME_NAME)  # Switch webdriver control to an iframe on the page
self.switch_to_default_content()  # Switch webdriver control out of the current iframe
self.switch_to_window(WINDOW_NUMBER)  # Switch to a different window/tab
self.save_screenshot(FILE_NAME)  # Save a screenshot of the current page
```

