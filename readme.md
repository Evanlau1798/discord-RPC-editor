相信各位一定有用過Discord與朋友聊天過吧
那各位是否有注意過
當遊戲開啟後，Dc會幫你顯示目前正在遊玩的遊戲
對於時常一起開黑的朋友們是個相當方便的功能
那我可不可以自己決定要顯示甚麼呢?
繼續把這篇文章看下去就對了!

我寫的這個軟體，就是幫你自定義Discord的"所有"豐富狀態!
2019年時有位大大寫了一個核心功能跟我一樣的軟體
點我前往該文章
那為什麼我要再寫一個呢?
除了該軟體已經停止維護以外
Discord所推出的豐富狀態也越來越強大
它在今日已無法充分發揮DC強大的功能
那到底是少了那些功能呢?



使用前須知
使用前請到discord developers applications網站創建App
創建完後即可獲得App id
關於如何創建App的詳細資訊請參考這位大大的文章
https://forum.gamer.com.tw/C.php?page=1&bsn=60076&snA=5075796
(在此感謝happy819tw詳細的解說QwQb)

介面及功能講解

1.設定狀態主標題
2.設定狀態副標題
3.設定當滑鼠移至大圖片上方時顯示的文字
4.設定要使用哪張大圖片
5.設定當滑鼠移至小圖片上方時顯示的文字
6.設定要使用哪張小圖片
7,10:設定按鈕的名稱
8,11:設定按鈕的連結網址
9,12:開啟/關閉自訂按鈕
13.時間設定 : 從零開始/經過時間/剩餘時間 功能切換
14.時間設定 : 模式為"經過時間/剩餘時間"時，設定時間
15.重設14.的時間為電腦目前的時間
16.勾選以開啟"經過時間"計時功能
17.以不同的檔案名稱儲存目前狀態設定檔
18.直接儲存所有目前已設定的狀態資料，下次打開修改器時會自動帶入所有已儲存資料至輸入框內
19.啟動discord自訂狀態
20.將修改器關閉至後台運行
21.目前已啟用的設定檔(若使用discord app id開啟時會顯示該app id的數字，另存新檔後會套用新名稱
22.重新啟動狀態修改器並選擇新存檔
23.前往discord developers applications網站，會根據前面輸入的app id前往該網站
24.目前顯示在discord的狀態
25.顯示修改器目前狀態

初始視窗


在此輸入您的discord developers applications中的App id
或是選擇已儲存的存檔
輸入完後按Enter或按下確定即可開啟狀態設定視窗
若是使用自己創建的app id，在狀態設定視窗按下"另存新檔"後，此狀態設定檔也會一併儲存
並於下次開啟時根據您輸入的檔案名稱自動載入存檔

存檔功能

存檔時可以自訂存檔標題，儲存後的狀態設定檔會存於data資料夾中
下次再開啟狀態修改器後
初始設定視窗會顯示出之前已存檔的設定檔名稱

背景執行

在狀態設定視窗按下「最小化視窗」後
程式會最小化到系統托盤
在該圖示按下右鍵可以呼出菜單
修改器的第二種關閉方式也在這裡
(當然你想要到工作管理員強制停止也可以)
當此圖標於系統托盤內時discord狀態也會持續顯示
並以最低的系統占用保持狀態修改器持續運行


精彩範例
可以試著用這些狀態騙騙朋友uwub
1.osu
第一個是正牌的osu
第二個是修改器的osu

自訂義按鈕的功能終於做出來啦~~~(灑花🎉
跟原版的一模一樣呢XD

2.Hexa Hysteria

手機沒辦法用Discord豐富狀態?那就自己動手創造一個屬於自己且獨一無二的遊戲名稱和狀態吧 !

3.人生模擬器

向朋友們展示自己正在爆肝(X

4.Apex

Apex不支援豐富狀態?那就幫它創造一個吧!

5.Sword Art Online

一堆人敲碗的星爆，終於可以自訂啦!

現在就趕緊下載來豐富你的discord狀態吧!

註:之前已下載過舊版修改器的朋友，直接複製data資料夾並取代新版data資料夾即可轉移存檔
下載連結: Github
Discord狀態修改器 Discord-RPC-editor v1.0更新資訊
新增時間相關設定
新增按鈕相關設定
新增"更換存檔"按鈕
"儲存資料"按鈕改為快捷儲存
新增另存新檔按鈕
另存新檔後，"目前設定檔"會套用新名稱
舊版/data資料夾中的檔案可以完美相容於新版本，只需直接取代新版資料夾
所有視窗皆使用黑暗模式
UI重新設計
若以新的app id啟動狀態修改器，需先另存新檔才能使用快捷儲存按鈕
所有視窗改為使用pyqt呈現
執行檔大小優化
初始設定視窗新增"點我前往Dc Dev網站"按鈕
初始設定視窗新增"確定"按鈕
另存新檔視窗新增"確定"按鈕
本程式已在Github上開源，有興趣參考的人歡迎前去查看
https://github.com/Evanlau1798/discord-RPC-editor
README會在近日更新上去
若有程式上的建議也歡迎私訊我( Evanlau#0857 )
注意事項
1.本程式是使用pyinstaller進行exe打包，使用者不需要安裝python便可執行此程式
2.由於pyinstaller打包後非常容易被Windows Defender誤判為防毒軟體，暫時關閉defender的解決方法在這
3.本程式目前還有隱藏的bug尚未被發現，如有發現bug請直接私訊我的Discord( Evanlau#0857 )
4.請不要讓exe檔與資料夾們分開，data與lib資料夾內為執行所需的必要檔案，如需常用可以建立修改器的捷徑至桌面
5.如您遇到bug或是有任何建議，歡迎直接私訊我的Discord(Evanlau#0857)
6.小弟我是第一次發文，用詞不好請各位見諒QQ