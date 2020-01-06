# Web Application Instruction

## 1/ Homepage

![Homepage](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/homepage.png)

Brief introduction of the web app.

## 2/ By SKU No.

![findsku](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/skufind.png)

This page takes a single input as SKU number (e.g. 192268M212019) that  can be under product name on the page of the product on SSENSE
and returns **three** recommendations with their images, SKU numbers, brands, names, and current lowest prices. Clicking on a recommended SKU number
will take users to search result of that particular SKU.

![bysku](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/by_sku.png)

## 3/ By Product Text

This page takes multiple inputs for details of products that are not available on SSENSE but on other sites like [Farfetch](https://www.farfetch.com),
[END. Clothing](https://www.endclothing.com), and [Mr. Porter](https://www.mrporter.com). 

**Example**: [A jacket from END.](https://www.endclothing.com/ca/barbour-ashby-wax-jacket-mwx0339ol71.html)
![findtext](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/textfind.png)

* **Category**: e.g. Jacket
* **Brand**: e.g. Barbou
* **Product Name**: e.g. ASHBY WAX JACKET
* **Color**: e.g. Olive
* **Product Description**: e.g. the Ashby reworks one of the brand’s original waxed styles for the modern man. Lined with...
* **Material Composition**: e.g. 100% Cotton 
* **Sizes**: e.g. XS, S
  * Note: enter multiple sizes by placing comma "," in between. If the product has only one size (i.e. bags), enter "One Size" 
* **Full Price**: e.g. 319
* **Sale Price**: e.g. 235
  * Note: enter same number as full price if the product is not on sale
* **Country of Origin**: e.g. Other
  * Note: select "Other" from the drop-down list if the country is not listed
  
Similar to SKU, this page returns **three** recommendations with their images, SKU numbers, brands, names, and current lowest prices. Clicking on a recommended SKU number
will take users to search result of that particular SKU.

![bytext](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/by_text.png)
