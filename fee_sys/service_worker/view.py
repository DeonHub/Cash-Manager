import os
from django.http import HttpResponse
from django.views import View
from pathlib import Path

from fee_sys.settings import BASE_URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(f'Base directory: {BASE_DIR}')

class ServiceWorkerView(View):
    content_type = "application/x-javascript"
    DIR_NAME = [f"{BASE_DIR}/superuser/static", f"{BASE_DIR}/login/static", f"{BASE_DIR}/client/static"]
    
    exclude_map_file = "js.map"
    exclude_map_file2 = "css.map"
    exclude_map_file3 = "min.map"
    exclude_manifest_file = "manifest.webmanifest"
    exclude_service_worker_file = "service_worker.js"

    def get(self, request):

        

        SERVICE_WORKER = open(f"{BASE_DIR}/fee_sys/service_worker/service_worker.js",
            "rb").read().decode('UTF-8')
        service_worker = f"{SERVICE_WORKER}"

        CACHEABLE_FILES = ""
        for dir_name in self.DIR_NAME:
            CACHEABLE_FILES += self.getCacheableFiles(dir_name, dir_name)[:-1]

        CACHEABLE_URLS = self.getCacheableUrls()
        cacheables = f"const ASSETS = [{CACHEABLE_URLS} {CACHEABLE_FILES}\n];\n"
        service_worker = service_worker.replace(
            "const ASSETS = [];", cacheables)

        UNCACHEABLE_URLS = self.getUnCacheableUrls()
        uncacheables = f"const UNCACHEABLE_URLS = [{UNCACHEABLE_URLS}\n];\n"
        service_worker = service_worker.replace(
            "const UNCACHEABLE_URLS = [];", uncacheables)

        return HttpResponse(service_worker, headers={"Content-Type": self.content_type})
    
    def getCacheableFiles(self, dirname:str, main_dirname: str):
        """return  [
            "files you want to cache",
            "E.g, css, js, image files, yes"
        ]"""
        allFiles = ""

        # get a list of files in a directory 
        listOfFiles = os.listdir(dirname)
        # print({"listOfFiles": listOfFiles})

        for entry in listOfFiles:
            fullPath = os.path.join(dirname, entry)
            # print({"fullPath-fullPath": fullPath})
            if os.path.isdir(fullPath):
                # check if path is a directory, if it is call `getCacheableFiles`
                allFiles = allFiles + self.getCacheableFiles(fullPath, main_dirname)
            else:
                if fullPath.__contains__(self.exclude_manifest_file):
                    pass
                elif fullPath.__contains__(self.exclude_service_worker_file):
                    pass
                elif fullPath.__contains__(self.exclude_map_file):
                    pass
                elif fullPath.__contains__(self.exclude_map_file2):
                    pass
                elif fullPath.__contains__(self.exclude_map_file3):
                    pass
                else:
                    fullPath = fullPath.replace(main_dirname, f"{BASE_URL}static").replace("\\", "/")
                    allFiles += f"\n'{fullPath}',"

        return allFiles
    
    

    def getCacheableUrls(self,):
        """
        List of urls you want to cache , eg, login url, registration urls .
        """
        URLS = [ 
            f'{BASE_URL}',

            f'{BASE_URL}superuser',
            
            f'{BASE_URL}superuser/create-fee-type/', 
            f'{BASE_URL}superuser/view-fee-type/',
            f'{BASE_URL}superuser/create-fee-items/',
            f'{BASE_URL}superuser/view-fee-items/', 
            f'{BASE_URL}superuser/create-fee-description/',
            f'{BASE_URL}superuser/view-fee-description/',
            f'{BASE_URL}superuser/create-currency/', 
            f'{BASE_URL}superuser/view-currency/', 
            f'{BASE_URL}superuser/set-invoice-details/',
            f'{BASE_URL}superuser/view-invoice-details/', 
            f'{BASE_URL}superuser/create-invoice/',
            f'{BASE_URL}superuser/view-invoice/', 
            f'{BASE_URL}superuser/view-payment-details/', 
            f'{BASE_URL}superuser/view-members/',
            f'{BASE_URL}superuser/activity-log/',
            f'{BASE_URL}superuser/view-payments/', 
            f'{BASE_URL}superuser/profile/',

        ]

        allUrls = ""

        # Add the list of urls into a str
        for url in URLS:
            allUrls += f"\n'{url}',"

        return allUrls

    def getUnCacheableUrls(self,):
        """
        List of urls you do not want to cache, e.g api, 
        if you dont do this api calls will always return cached data
        """
        URLS = [
            f'{BASE_URL}api/',
        ]
        allUrls = ""

        # Add the list of urls into a str
        for url in URLS:
            allUrls += f"\n'{url}',"

        return allUrls

