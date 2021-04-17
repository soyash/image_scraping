from bs4 import BeautifulSoup as bs
import os
import urllib.request #for opening and reading URLs
import urllib.parse #for parsing URLs
import urllib.error #containing the exceptions raised by urllib.request
from urllib.request import urlretrieve

class ScrapperImage:
    
    ## Create  Image URl
    def createImageUrl(searchterm):
        searchterm=searchterm.split()
        searchterm="+".join(searchterm)
        web_url="https://www.google.co.in/search?q=" + searchterm + "&source=lnms&tbm=isch"
        return web_url
    
   # get Raw HTML
    def scrap_html_data(url,header):
        request=urllib.request.Request(url,headers=header)
        response = urllib.request.urlopen(request)
        responseData = response.read()
        html = bs(responseData, 'html.parser')
        return html
    
    # contains the link for Large original images, type of  image
    def getimageUrlList(rawHtml):
        imageUrlList = []
        for a in rawHtml.find_all("img", {"class=":"rg_i Q4LuWd"}):
            link = a['src']
            imageUrlList.append(link)

        print("there are total", len(imageUrlList), "images")
        return imageUrlList
    
    def downloadImagesFromURL(imageUrlList,image_name, header):
        masterListOfImages = []
        count=0
        ###print images
        imageFiles = []
        image_counter=0
        for i, (img) in enumerate(imageUrlList):
            try:
                if (count > 5):
                    break
                else:
                    count = count + 1
                req = urllib.request.Request(img, headers=header)
                try:
                    urllib.request.urlretrieve(img,"./static/"+image_name+str(image_counter)+".jpg")
                    image_counter=image_counter+1
                except Exception as e:
                    print("Image write failed:  ",e)
                    image_counter = image_counter + 1
                respData = urllib.request.urlopen(req)
                raw_img = respData.read()
                # soup = bs(respData, 'html.parser')

                imageFiles.append(raw_img)

            except Exception as e:
                print("could not load : " + img)
                print(e)
                count = count + 1
        masterListOfImages.append(imageFiles)

        return masterListOfImages
    
    def delete_downloaded_images(self,list_of_images):
        for self.image in list_of_images:
            try:
                os.remove("./static/"+self.image)
            except Exception as e:
                print('error in deleting:  ',e)
        return 0