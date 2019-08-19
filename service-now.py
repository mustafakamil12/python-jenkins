from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.chrome.options import Options


import time
import pw
import json

# Define the radio buttons

os = {
        1: "Windows Server 2016",
        2: "Windows Server 2012 R2",
        3: "SuSE Linux 12 SP3",
        4: "SuSE Linux 12 SP2",
        5: "SuSE Linux 12 SP1",
        6: "Red Hat Linux 7"
}

location = {
    1: "Ashburn",
    2: "Richardson"
}

domain = {
    1: "abc.amerisourcebergen.com",
    2: "npd.amerisourcebergen.com",
    3: "cfd.amerisourcebergen.com",
    4: "absg.net (Legacy)",
    5: "clt.lash.loc (Legacy)",
    6: "dmz.absg.com (Legacy)",
    7: "abcs.loc (Legacy)",
    8: "corp.absc.local (Legacy)",
    9: "cfdmz.dmz (Legacy)"
}

servertype = {
    1: "Cluster",
    2: "Instance"
}

patching_cycle = {
    1: "Thursday (non-prod) 9pm",
    2: "Saturday 8am",
    3: "Saturday 12 noon",
    4: "Saturday 9pm",
    5: "Saturday/Sunday",
    6: "Tuesday 10pm"
}

tier_level = {
    1: "Production",
    2: "Dev",
    3: "Stage",
    4: "Test"
}

size = {
    1: "Small - 2 CPU, 8GB Memory",
    2: "Medium - 4 CPU, 16GB Memory",
    3: "Large - 8 CPU, 32GB Memory",
    4: "XLarge - 16 CPU, 64GB Memory"
}

compliance_level = {
    1: "PCI",
    2: "PHI",
    3: "None"
}

network_zone = {
    1: "Back End",
    2: "Front End",
    3: "Middle Tier",
    4: "Shared Services"
}

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


def main():
    print("--- Start ---")
    total_start_time = time.time()
    # test_run()
    run_once()
    total_elapsed_time = time.time() - total_start_time
    print("Total Elapsed Time: " + str(total_elapsed_time))
    print("--- Done ---")


def run_once():
    # Run one time for testing
    # Set values as needed. These are indexes into
    # the arrays listed above.
    os_num = 2
    loc_num = 1
    dom_num = 1
    server_num = 1
    patch_num = 6
    tier_num = 2
    size_num = 1
    compliance_num = 1
    net_z_num = 1

    place_order(os_num, loc_num, dom_num, server_num, patch_num,
                tier_num, size_num, compliance_num, net_z_num, "Running with defaults")


def test_run():
    # loop through every checkbox and submit an order
    print("testRun")
    ct = 0
    # Set Defaults
    os_num = 1
    loc_num = 1
    dom_num = 1
    server_num = 1
    patch_num = 1
    tier_num = 1
    size_num = 1
    compliance_num = 1
    net_z_num = 1

    for os1 in range(1, 7):    # OS range
        ct += 1
        place_order(os1, loc_num, dom_num, server_num, patch_num,
                    tier_num, size_num, compliance_num, net_z_num, "OS")

    for lc in range(1, 3):    # Location
        ct += 1
        place_order(os_num, lc, dom_num, server_num, patch_num,
                    tier_num, size_num, compliance_num, net_z_num, "Location")

    for dn in range(1, 10):   # Domain
        ct += 1
        place_order(os_num, loc_num, dn, server_num, patch_num,
                    tier_num, size_num, compliance_num, net_z_num, "Domain")

    for st in range(1, 3):    # Server Type
        ct += 1
        place_order(os_num, loc_num, dom_num, st, patch_num,
                    tier_num, size_num, compliance_num, net_z_num, "Server Type")

    for pc in range(1, 7):    # Patch Cycle
        ct += 1
        place_order(os_num, loc_num, dom_num, server_num, pc,
                    tier_num, size_num, compliance_num, net_z_num, "Patch Cycle")

    for tl in range(1, 5):    # Tier Level
        ct += 1
        place_order(os_num, loc_num, dom_num, server_num, patch_num,
                    tl, size_num, compliance_num, net_z_num, "Tier level")

    for sz in range(1, 5):    # Size
        ct += 1
        place_order(os_num, loc_num, dom_num, server_num, patch_num,
                    tier_num, sz, compliance_num, net_z_num, "Size")

    for cl in range(1, 4):    # Compliance Level
        ct += 1
        place_order(os_num, loc_num, dom_num, server_num, patch_num,
                    tier_num, size_num, cl, net_z_num, "Compliance Level")

    for nz in range(1, 5):    # Network Zone
        ct += 1
        place_order(os_num, loc_num, dom_num, server_num, patch_num,
                    tier_num, size_num, compliance_num, nz, "Network Zone")

    print("Combinations: " + str(ct))


# This is just for testing what is getting passed to place_order
def place_order1(os_num, loc_num, dom_num, server_num, patch_num,
                tier_num, size_num, compliance_num, net_z_num, run_desc):
    print(os.get(os_num))
    print(location.get(loc_num))
    print(domain.get(dom_num))
    print(servertype.get(server_num))
    print(patching_cycle.get(patch_num))
    print(tier_level.get(tier_num))
    print(size.get(size_num))
    print(compliance_level.get(compliance_num))
    print(network_zone.get(net_z_num))
    print(run_desc + "\n--------------------")


# Pass in which checkboxes to select and a description to add to the order
def place_order(os_num, loc_num, dom_num, server_num, patch_num,
                 tier_num, size_num, compliance_num, net_z_num, run_desc):
    start_time = time.time()
    # Create a new instance
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)  # seconds to wait for an element to show up
    driver.set_window_position(0, 0)
    # driver.set_window_size(1920, 1007)
    driver.maximize_window()

    # go to the servicenow home page
    driver.get("https://amerisourcebergentest.service-now.com/com.glideapp.servicecatalog_cat_item_view.do?v=1&sysparm_id=4e42a7c5db0fa70036b716494896196b&sysparm_link_parent=a64cc13b6f52b100e23c77f16a3ee46c&sysparm_catalog=e0d08b13c3330100c8b837659bba8fb4&sysparm_catalog_view=catalog_default")

    # the page is ajaxy so the title is originally this:
    print("Driver Title: " + driver.title)

    time.sleep(5)
    print(driver)

    seq = driver.find_elements_by_tag_name('iframe')
    print("seq: " + str(seq))

    driver.switch_to.frame(0)
        
    print("Enter service name")
    input_element = driver.find_element_by_name('sys_display.IO:8a527781db4fa70036b71649489619fd')
    input_element.click()
    input_element.send_keys("TEST SERVICE NAME")
        
    time.sleep(1)

    input_element = driver.find_element_by_id('IO:d025a7cddbcba70036b7164948961972')
    input_element.click()
    input_element.send_keys("Description: " + run_desc)

    time.sleep(1)

    # Click to select from the popup window
    print("Popup window")
    oldtab = driver.current_window_handle
    input_element = driver.find_element_by_xpath('//a[@id="lookup.IO:def8bb85db4fa70036b71649489619e9"]/span')
    input_element.click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # Enter text
    input_element = driver.find_element_by_xpath('//span/div/div/input')
    input_element.click()
    input_element.send_keys("TEST APPLICATION NAME\n")

    input_element = driver.find_element_by_link_text("TEST APPLICATION NAME")
    input_element.click()

    time.sleep(1)

    print("oldtab: " + oldtab)
    driver.switch_to.window(oldtab)

    for handle in driver.window_handles:
        print("Handle = ", handle)
    driver.switch_to.frame(0)

    print("Click Server OS")
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + os.get(os_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Ashburn/Richardson
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + location.get(loc_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Domain
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + domain.get(dom_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Server Type
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + servertype.get(server_num) + '")]')
    input_element.click()

    time.sleep(1)

    # network zone
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + network_zone.get(net_z_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Patching Cycle
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + patching_cycle.get(patch_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Tier Level
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + tier_level.get(tier_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Avaliability - only do this if its a Production server
    if tier_num == 1:
        try:
            input_element = driver.find_element_by_xpath('//label[contains(.,"HA Storage")]')
            input_element.click()
        except:
            print("Didn't find the availability element")

    time.sleep(1)

    # Size
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + size.get(size_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Compliance Level
    input_element = driver.find_element_by_xpath('//label[contains(.,"' + compliance_level.get(compliance_num) + '")]')
    input_element.click()

    time.sleep(1)

    # Click to order
    input_element = driver.find_element_by_css_selector('#order_now .text_cell')
    input_element.click()
    time.sleep(15)
    driver.close()
    elapsed_time = time.time() - start_time
    print("Elapsed Time: " + str(elapsed_time))


if __name__ == "__main__":
    main()
