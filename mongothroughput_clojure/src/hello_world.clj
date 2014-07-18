(ns my.service.server
  (:require [monger.core :as mg]
            [monger.collection :as mc]
            [clj-time.periodic :as time-period]
           '[clj-time.core :as t]
           '[clj-time.local :as tl]
           '[clj-time.format :as tf]
           '[clj-time.coerce :as tc]
           '[clj-time.periodic :as tp]))


(tc/to-date (t/now))
(tc/to-long (t/now))


(defn time-range
  "Return a lazy sequence of DateTimes from start to end,
  incremented by step units of time"
  [start end step]
  (let [inf-range (tp/periodic-seq start step)
        below-end? (fn [t] (t/within? (t/interval start end)
                             t))]
    (take-while below-end? inf-range))
)



;;(let [conn (mg/connect)
;;      db   (mg/get-db conn "monger-test")
;;      coll "documents"]

;;(repeat 1000  (mc/insert db coll {:first_name "John"  :last_name "Lennon"})))




;;(time-range '2014 05 01' '2014 06 01' 1)

;;(mc/insert db coll {:first_name "Ringo" :last_name "Starr"})
;;(mc/insert-batch db coll (map hash-map (repeat :a) (range 8000)))
;;(time (mc/insert-batch db coll (doall (map hash-map (repeat :a) (range 1000000)))))
;;(mc/find db coll {:first_name "Ringo"}))

;(defn hello-world [a]
;  (println a))
;
;(println (hello-world "a\n100"))
;
;(def dt (t/date-time 1986 10 14))
;
;(println(t/day dt))
;
;(println 'test)


