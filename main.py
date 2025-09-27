# Created by safe-acid
import os
import time
from conf import Conf

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


BG_TEMPLATE = """
chrome.webRequest.onAuthRequired.addListener(
  function (details) {
    return {
      authCredentials: {
        username: "__USERNAME__",
        password: "__PASSWORD__"
      }
    };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
""".lstrip()


def write_background_js(plugin_dir: str, username: str, password: str) -> str:
    #Generate background.js with injected proxy credentials
    os.makedirs(plugin_dir, exist_ok=True)
    bg_path = os.path.join(plugin_dir, "background.js")
    with open(bg_path, "w", encoding="utf-8") as f:
        f.write(
            BG_TEMPLATE
            .replace("__USERNAME__", username)
            .replace("__PASSWORD__", password)
        )
    return bg_path


def build_options(plugin_dir: str) -> webdriver.ChromeOptions:
    """Build Chrome options; proxy address via flag, credentials via extension."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=200,600")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-features=DisableLoadExtensionCommandLineSwitch")

    if Conf.proxy:
        options.add_argument(f"--proxy-server=http://{Conf.proxyIP}:{Conf.proxyPort}")
        options.add_argument(f"--load-extension={plugin_dir}")
    return options


def main() -> None:
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(script_dir, "proxy_auth")

    # Generate background.js with credentials
    write_background_js(plugin_dir, Conf.proxyUsername, Conf.proxyPassword)

    # Launch Chrome
    options = build_options(plugin_dir)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Check current IP 
    driver.get("https://api.ipify.org/?format=text")
    ip = driver.find_element(By.TAG_NAME, "body").text
    print(f"🛡 Current IP: {ip}")

    # Open target site
    driver.get("https://nekto.me/audiochat#/")
    time.sleep(5)

    # option
    # driver.quit()


if __name__ == "__main__":
    main()
