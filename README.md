**Captchas辨識器**

**Introduction:**

- Captcha是一種全自動的圖靈測試，可以用來區分電腦跟人類使用者。雖然有很多非文字型態的Captcha被開發出來，但市面上最廣泛被使用的還是文字形Captcha。
- Captcha為網站和應用程序中最常見的安全機制，用來防止自動化程式或機器人的惡意操作。通常要求用戶在註冊、登錄或提交表單時輸入文字、數字或圖像中的信息，以驗證其是真正的人類使用者。
- 隨著科技的發展，Captcha的形式不斷演進，包括圖片辨識、聲音確認以及拼圖等各種形式，這些方法都旨在提高安全性並確保網路空間的真實性和可信度。然而Captcha也可能成為用戶體驗的一種障礙，因此許多開發人員正在尋求更具包容性的解決方案，以確保安全性的同時不影響使用者的便利性和體驗。

**動機:**

- 這個專題讓我有機會更深入地理解網路安全的挑戰。尤其是對於數字Captcha辨識的挑戰，這其中可能涉及到圖像處理、機器學習等技術。我希望能挑戰自我，嘗試找到突破點，提高對Captcha的辨識準確率。

**目的:**

- 研究Captcha辨識能改進Captcha辨識的方法和技術。透過深入研究，我希望能夠提高對於數字Captcha的辨識準確性和效率，並嘗試解決這方面的挑戰。
- 透過開發出一個可靠的辨識器，加強網站和應用的安全性。這有助於防止惡意機器人或自動化程式對系統進行攻擊或滲透，保護使用者和數據的安全。
- 透過有效的Captcha辨識器，希望提高真正使用者通過驗證的便利性和流暢度。我的目標是在提高安全性的同時，減少對於正常使用者的不必要干擾和阻礙。

**文獻探討:**

- 我原本只有打算直接使用tesseract做辨識，但發現此作法的準確率極低，因此開始在網上尋找不同preprocesss的方法。網上文獻有多方法可以處理影像。因此我最後選擇了二值化黑白影像，Morphological Transformation(形態學轉換)，goodFeaturesToTrack(角點檢測)，CopyMakeBorder，MedianBlur(中值濾波) 來處理影像。以下將在“你的方法”段說明使用這些方法的優點，以及同樣函示不同參數下的缺點。

**你的方法:**

**CaptchaBreaker.py:**

- **def menu():** Menu介面讓使用者選擇模式

  Captcha辨識

Captcha資料集folder準確率顯示(將每一張圖做Captcha辨識)

Quit退出

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 001](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/1ed8e644-86ca-4b1e-885a-39cd4f6fca0a)


**Load.py:**

- **def get_image(path):** get\_input=str(input) 輸入辨識圖片的路徑

  image, label=get\_image(get\_input) 使用cv2.imread(path)將圖片回傳(若路徑有 “” 在前後，也可以處理)

label為檔案名稱(在使用Show success rate for dataset時拿來比對正確的方式)

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 002](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/d8511582-5c29-4ac9-9ba0-110f9b9a4711)

**Process\_manage.py:**

- **def choose\_process():** 可以決定使用不同欲處理的順序，get\_order並且 return order



- **def process(original\_image,order):** 將原圖片以及指定order輸入，以orginal\_image->images[1]->images[2]->images[3]->images[4]依序處理，並且在最後將images[4]用tesseract\_ocr辨識圖片內的文字。最後return 指定order，images[]，以及text[]
![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 003](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/ac857418-a30f-4f1f-b507-403f4bd8be65)
- **class result:** 用來將前面做好的order, images,text用matplot顯示結果。for迴圈會利用self.order指定順序去決定plt的titles應該為甚麼，再將self.images存入images。最後利用empty建立與original\_images相同大小的全白圖用來當text的背景。
- **def show\_rate():** 用來計算整個資料集執行後的字元正確率以及單張圖片正確率。

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 004](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/e6b996d5-cee7-4a47-9507-70c61cc174b7)

- **def bw(original\_image):** 對圖片進行binarization以及noise removal。使用threshold可以將灰階影像處理成黑白影像回傳。單純使用threshold() 處理灰階影像時需要手動設定臨界值，比較適合單純的影像，遇到這種較複雜的影像，像素與像素間可能都有關聯性，因此使用adaptiveThreshold()。 adaptiveThreshold()可以根據指定大小的區域平均值自動設定灰度臨界值，有時可以產生更好的結果。因此這邊使用t=min(t1,t2,t3,t4)如果t>250則使用adaptiveThreshold()，反之則使用threshold()。

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 005](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/ed6531c8-ad9c-4f45-952a-453eb99335d4)

- **def crop\_image(original\_image):** 使用goodFeaturesToTrack判定四個角，並用這四格角設定圖片邊界。最後用copyMakeBorder複製一張使用新的邊界製作的圖片並回傳。

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 006](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/380df829-9371-4ac5-a672-13f35d3a096b)

- **def morph\_image(original\_image):** morphologyEx使用MORPH\_CLOSE可以將圖片先膨脹(Dilation)再腐蝕(Erosion)，這樣可以消除原圖片中的空洞以及小黑點

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 007](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/1ee6e7eb-f065-43dd-baa5-0d9d077c4373)

- **def blur\_image(original\_image):** 使用medianBlur以kernal 大小3\*3去模糊化圖片

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 008](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/0cbf13b9-442d-4de0-8122-fc8cb77b4ee1)

- **def tesseract(givin\_image):** 使用tesseract將預處理最後的圖片做辨識。
- 可以透過環境變數 `TESSERACT_CMD` 指定 tesseract 執行檔位置，未設定時將由 `pytesseract` 自行搜尋。

**實驗結果:**

- Process image 以1234 order preprocess

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 009](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/44e54142-1f67-416c-adfd-3c59d57c153d)

- Tesseract 處理失敗時

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 010](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/877af4ba-68ca-42f5-9b94-94a76810ec05)

- Tesseract 處理成功時

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 011](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/9616f533-fae7-4279-9ed7-7615839cfb53)

- 將所有order都嘗試後的準確率如下

![Aspose Words a18e4c6e-9999-40b4-af90-b957a83afeea 012](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/080f3b41-bf3b-4372-9e3a-bdd5d5bfc5c4)

- 可以觀察到普遍越多預處理，準確率越高，但也有例外狀況。
- 有1以及3的狀況下也會準確率比較高。
- 有趣的是13以及31的準確率非常高，做多次實驗的結果也是如此，可能是對於這個資料集特別適合的結果，但不能保證適用於所有狀況。
- 可以考慮時間允許的狀況下用預處理後的圖片執行機器學習，這將會有很高的機會提高準確率。

**參考資料:**

What is Captchas: <https://zh.wikipedia.org/zh-tw/%E9%AA%8C%E8%AF%81%E7%A0%81>

可能會用到的函示庫: [Keras: Deep Learning for humans](https://keras.io/)

文字辨識庫: [Home · UB-Mannheim/tesseract Wiki (github.com)](https://github.com/UB-Mannheim/tesseract/wiki)

二值化黑白影像: [二值化黑白影像 - OpenCV 教學 ( Python ) | STEAM 教育學習網 (oxxostudio.tw)](https://steam.oxxostudio.tw/category/python/ai/opencv-threshold.html)

Morphological Transformation(形態學轉換): [OpenCV-Python学习之路-9：Morphological Transformations(形态学转换)_morphology转换-CSDN博客](https://blog.csdn.net/qq_36560894/article/details/107667211)

goodFeaturesToTrack(角點檢測): [【OpenCV3】角点检测——cv::goodFeaturesToTrack()与cv::cornerSubPix()详解-CSDN博客](https://blog.csdn.net/guduruyu/article/details/69537083)

CopyMakeBorder: [OpenCV-Python: cv2.copyMakeBorder()函数详解_copymakeborder函数详解-CSDN博客](https://blog.csdn.net/qq_36560894/article/details/105416273)

MedianBlur(中值濾波): [python-opencv 中值滤波{cv2.medianBlur(src, ksize)}_cv2 中值滤波-CSDN博客](https://blog.csdn.net/A_Z666666/article/details/81324288)

Tesseract\_OCR: [tesseract-ocr/tesseract: Tesseract Open Source OCR Engine](https://github.com/tesseract-ocr/tesseract)













