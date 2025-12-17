def main():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    # selenium driver path
    service = Service(
        executable_path=r'C:\Users\Tesla\Downloads\chromedriver-win64\chromedriver.exe',
    )
    options = webdriver.ChromeOptions()

    # provide the profile name with which we want to open browser
    # options.add_argument(r"--profile-directory=Profile 1")

    # provide location where chrome stores profiles
    options.add_argument(  # type:ignore
        r'--user-data-dir=C:\Users\Tesla\AppData\Local\Google\Chrome for Testing\User Data'
    )
    # provide the profile name with which we want to open browser
    options.add_argument(r'--profile-directory=Default')  # type:ignore
    # chrome executable
    options.binary_location = (
        r'C:\Users\Tesla\Downloads\chrome-win64\chrome-win64\chrome.exe'
    )
    # initialize driver
    driver = webdriver.Chrome(service=service, options=options)
    response = driver.get('https://example.com')
    print(response.title)
    print(response.current_url)
    driver.quit()


if __name__ == '__main__':
    import os

    os.system('cls')
    main()
