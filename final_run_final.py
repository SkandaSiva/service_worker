from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import concurrent.futures
from urllib.parse import urlparse
import jsbeautifier
import time
import requests
import random
import os


def process_website(url):
    url = url.strip("\n")
    uri = url
    url = url.strip()
    url = "http://www." + url 
    proper_uri = None

    try:
        response = requests.head(url, allow_redirects=True, timeout=20)
        proper_uri = response.url
        #list_urls.append(proper_uri)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException as e:
        pass
    #print(proper_uri)
    with open(filename2, "a") as k:
        k.write(f"{proper_uri}\n")
        k.flush()
    
    if proper_uri == None:
        pass
    else:
        user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15' ]
        user_agentt = random.choice(user_agent_list)

        # Configure Chrome options
        chrome_options = Options()  
        chrome_options.add_argument(f"user-agent={user_agentt}")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        #driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        #print(user_agentt)
        # Navigate to the website
        #print(website_url)
        try:
            #print("5")
            driver.get(proper_uri)
        except Exception as e:
            print("error occured", proper_uri)
        #print("9")
        #driver.set_script_timeout(5)
        #driver.implicitly_wait(5)
        #print("10")

        # overriding the cosole.log function to capture the logs needed
        driver.execute_script("console.log = function(message) {window._consoleLog = message; };")

        javascript_code = """  
        try 
            {
            if ('serviceWorker' in navigator) 
            {
                navigator.serviceWorker.getRegistrations().then(function(registrations) 
                {
                    if (registrations.length > 0) 
                    {
                    var serviceWorker_found = registrations[0].active;
                    if (serviceWorker_found)
                        {
                        var serviceWorkerURL = serviceWorker_found.scriptURL;
                        console.log('Service Worker URL: ',serviceWorkerURL)
                        }
                    console.log(serviceWorkerURL);
                    } 
                    else 
                    {
                    console.log('No service worker found.');
                    }
                });
            } 
            else 
            {
                console.log('Service workers are not supported in this browser.');
            }
        } 
        catch (error) 
        {
            console.log('An error occurred:', error);
        }
        """
        # 'Service worker is deployed. ', 
        # Execute the JS code
        driver.execute_script(javascript_code)

        # Retrieve the captured log value
        captured_log = driver.execute_script("return window._consoleLog;")

        parsed_url = urlparse(captured_log)
        domain = parsed_url.netloc.split(':')[0]

        if captured_log.startswith("http"):
           response = requests.get(captured_log)
           filename = f"{filename4}/{domain}.js"
           #filename = f"service_worker_scripts/swscript.js"
           #print(filename)
           if response.status_code == 200:
               with open(filename, 'wb') as file:
                   file.write(response.content)
                #    c = response.content
                #    #print(c)
                #    #contents = file.read()
                #    content1 = jsbeautifier.beautify(c)
                #    sw_beauty = f"sw_beautified/{uri}.js"
                #    print(sw_beauty)
                #    with open(sw_beauty, "wb") as l:
                #        l.write(content1)
            
           else:
              print("failed to capture SW", parsed_url)

        else:
           captured_log = None
           #print("no service worker to capture")

        #return captured_log
        with open(filename3, "a") as g:
            g.write(f"{url},{proper_uri},{captured_log}\n")
            g.flush()           
        print(proper_uri, captured_log)



if __name__ == "__main__":    
    start_time = time.time()
    filename1 = "unprocessed.txt"    
    #filename1 = "1000_urls.txt"
    filename2 = "proper_uri_unprocessed.txt"
    filename3 = "updated_sw_check_unprocessed.csv"
    filename4 = "service_worker_scripts_unprocessed"
    filename5 = "sw_beautified"
    full_list=[]

    with open(filename1, "r") as h:
        list_urls = h.readlines()

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_to_url = {executor.submit(process_website, url) for url in list_urls}


    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in list_urls:
            full_list.append(url)
            if len(full_list)%100 == 0:
                time.sleep(30)
                between_time = time.time()
                elapsed_time = between_time - start_time
                elapsed_time_in_mins = elapsed_time/60
                print(f"Elapsed time for {len(full_list)} urls is {elapsed_time_in_mins} minutes")
                print("Waiting ========================================================================================================")       
            elif len(full_list)%1000 == 0:
                time.sleep(120)
                between_time = time.time()
                elapsed_time = between_time - start_time
                elapsed_time_in_mins = elapsed_time/60
                print(f"Elapsed time for {len(full_list)} urls is {elapsed_time_in_mins} minutes")
                print("Waiting ========================================================================================================")         
            elif len(full_list)%10000 == 0:
                time.sleep(300)
                between_time = time.time()
                elapsed_time = between_time - start_time
                elapsed_time_in_mins = elapsed_time/60
                print(f"Elapsed time for {len(full_list)} urls is {elapsed_time_in_mins} minutes")
                print("Waiting ========================================================================================================")              
            else:
                future_to_url = executor.submit(process_website, url) 


    # for fn in os.listdir(filename4):
    #     #print(fn)
    #     file_path = os.path.join(filename4,fn)
    #     print(file_path)
    #     with open(file_path, "r") as f:
    #         contents = f.read()
    #         print(contents)
    #         content1 = jsbeautifier.beautify(contents)
    #         #print(content1)
    #         sw_beauty = f"sw_beautified/{fn}"
    #         #sw_beauty = f"sw_beautified/{uri}.js"
    #         with open(sw_beauty, "w") as l:                
    #             l.write(content1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_in_mins = elapsed_time/60
    #print("Elapsed time: ", elapsed_time_in_mins) 
    print(f"Elapsed time for all urls is {elapsed_time_in_mins} minutes")


