## OS project 1 組別1

1. 設計
   將程式分成三個部分，分別為main.c、scheduler.c、process.c。

   main.c：讀取input資料和確定是選取哪個CPU排程演算法，並將資料傳給schehuler.c執行。

   scheduler.c：模擬作業系統的排程的情況，先將process按照ready time大小從小排到大，根據排程演算法以及process的ready time，決定現在可以使用cpu的是哪個process，並且執行process，直到所有process執行完畢。

   process.c：主要是提供四個函式給scheduler.c使用，分別為
   ​			proc_assign_cpu：指派cpu給process使用。
   ​			proc_exec：模擬process實際執行。
   ​			proc_block：將指定的process放入等待佇列。
   ​			proc_wakeup：將指定的process放入準備佇列。

2. 執行範例測資的結果

3. 比較實際結果與理論結果，並解釋造成差異的原因


   因為在切換process時，實際上還會有context switch的時間，所以如果是比較頻繁切換process的演算法，就會花費比較多context switch的代價。
   另外在程式中，我們的方法是假設scheduler跑完一個unit的時間和process跑完一個unit的時間差不多，但實際上因為兩者是不同的程式並且放在不同CPU上執行，所以也會造成差異。

4. 各組員的貢獻
