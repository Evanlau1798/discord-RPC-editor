Discord豐富狀態編輯器
=====================

相信各位一定有用過Discord與朋友聊天過吧 那各位是否有注意過
當遊戲開啟後，DC會幫你顯示目前正在遊玩的遊戲
對於時常一起開黑的朋友們是個相當方便的功能
我寫的這個軟體，就是幫你自定義Discord的"所有"豐富狀態!

特色:

-  存取所有DC豐富狀態的所有內容
-  存檔功能
-  針對遊戲玩家優化，使用超低資源

介面說明:
---------

|image|

1.設定狀態主標題 2.設定狀態副標題 3.設定當滑鼠移至大圖片上方時顯示的文字
4.設定要使用哪張大圖片 5.設定當滑鼠移至小圖片上方時顯示的文字
6.設定要使用哪張小圖片 7,10:設定按鈕的名稱 8,11:設定按鈕的連結網址
9,12:開啟/關閉自訂按鈕 13.時間設定 : 從零開始/經過時間/剩餘時間 功能切換
14.時間設定 : 模式為"經過時間/剩餘時間"時，設定時間
15.重設14.的時間為電腦目前的時間 16.勾選以開啟"經過時間"計時功能
17.以不同的檔案名稱儲存目前狀態設定檔
18.直接儲存所有目前已設定的狀態資料，下次打開修改器時會自動帶入所有已儲存資料至輸入框內
19.啟動discord自訂狀態 20.將修改器關閉至後台運行
21.目前已啟用的設定檔(若使用Discord App ID開啟時會顯示該App
ID的數字，另存新檔後會套用新名稱 22.重新啟動狀態修改器並選擇新存檔
23.前往discord developers applications網站，會根據前面輸入的App
ID前往該網站 24.目前顯示在discord的狀態 25.顯示修改器目前狀態

初始視窗
--------

|image|\  |image|\  在此輸入您的Discord Developers Applications中的App
ID 或是選擇已儲存的存檔 輸入完後按Enter或按下確定即可開啟狀態設定視窗
若是使用自己創建的App
ID，在狀態設定視窗按下"另存新檔"後，此狀態設定檔也會一併儲存
並於下次開啟時根據您輸入的檔案名稱自動載入存檔

存檔功能
--------

|image|\  "另存新檔" 可以額外儲存一份同App ID的檔案
可以自訂存檔標題，儲存後的狀態設定檔會存於\ ``data``\ 資料夾中
下次再開啟狀態修改器後 初始設定視窗會顯示出之前已存檔的設定檔名稱

*"儲存資料" 為直接將目前格子內的所有狀態寫入至已儲存的檔案內*

背景執行
--------

|image|\  在狀態設定視窗按下「最小化視窗」後 程式會最小化到系統托盤
在該圖示按下右鍵可以呼出菜單 修改器的第二種關閉方式也在這裡
[STRIKEOUT:(當然你想要到工作管理員強制停止也可以)]\ 
當此圖標於系統托盤內時Discord狀態也會持續顯示
並以最低的系統占用保持狀態修改器持續運行

--------------

如何自訂遊戲名稱及圖片?
-----------------------

1. 

首先打開\ `Discord Devloper
Portal <https://discord.com/developers/applications>`__\ ，或是點選修改器中\ ``"點我前往Dc Dev網站"``\ 也可以前往該網站
網站打開後，你會看這個畫面 |image|\ 

2. 

按下右上角的\ ``New Application``\ 按鈕，並輸入欲創建的遊戲名稱
這裡以Apex Legends作為範例 |image|\  輸入完後，按下\ ``Create``\ 
即可創建屬於你自己的遊戲名稱

3. 

創建完成後，會看到這個畫面 |image|\ 
紅框框內的一大串數字就是剛剛創建好的Discord Application ID
可以先複製起來，等等會用到

4. 

依序點選左側的 Rich Presence -> Art Assets
點選紅圈圈中的\ ``Add image(s)``\ 就可以新增圖片囉 |image|\ 

5. 

選好圖片後，可以幫圖片取個好記的名稱 取好後就按下\ ``"Save Changes"``\ 
圖片開始上傳至Discord伺服器
單張圖片約需\ **10~20分鐘**\ 的處理時間，網頁重整後如果圖片已經出現在畫面上，就代表上傳完成囉!
|image|\ 

6. 

開啟Discord狀態修改器，把剛剛第三點提到的Application
ID貼到輸入框框內並按下確定，就可以使用自己的遊戲名稱了 |image|\  Tips.
第一次使用新的的App ID時記得按下\ ``"另存新檔"``\ 
儲存你剛剛辛苦編輯的自訂狀態 名稱可以自訂喜歡的名字
方便下一次使用時快速打開想要使用的檔案 若有同個App ID多開檔案的需求
按下另存新檔後就可以多開囉 |image|\ 

註:之前已下載過舊版修改器的朋友，直接複製data資料夾並取代新版data資料夾即可轉移存檔
下載連結:
`Github <https://github.com/Evanlau1798/discord-RPC-editor/releases/tag/v1.0.0>`__\ 

--------------

注意事項
--------

1.本程式是使用pyinstaller進行exe打包，使用者不需要安裝python便可執行此程式
2.由於pyinstaller打包後非常容易被Windows
Defender誤判為木馬，暫時關閉defender可解決
3.本程式目前還有隱藏的bug尚未被發現，如有發現bug請直接私訊作者的Discord(
Evanlau#0857)
4.請不要讓exe檔與資料夾們分開，data與lib資料夾內為執行所需的必要檔案，如需常用可以建立修改器的捷徑至桌面
5.如您有任何建議，歡迎直接私訊的Discord(Evanlau#0857)

.. |image| image:: https://truth.bahamut.com.tw/s01/202209/02b6e19117037443e81cb81d0695c52c.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/a7eb8edb44d42b30ba1b5fa34368e938.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/ca2db6b0e825fdafc51c430395869f53.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/c37b1e7149e663ac82febbb93f70031c.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/f031cb7b0ed8ddba50ba8de735b2e456.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/9bdd6666a33a3b7737ebcd72967eef6a.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/40a9d68caa0fe38b72a1ec4e9824ae2a.JPG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/a32e6e49bcd246a7279fc8130b60c45f.JPG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/a2f128adcb420d46e598a5dc4ace095e.JPG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/5cae348c0ac1f10aaa740fc8b18ee468.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/82829e1487253954354a3b855abb4c6e.PNG
.. |image| image:: https://truth.bahamut.com.tw/s01/202209/d86ddba9457959bd1739e1f61a75bdd9.PNG
