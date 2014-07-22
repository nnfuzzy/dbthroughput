(ns Throughput)
(require  '[monger.core :as mg]
          '[monger.collection :as mc]
          '[monger.operators :refer :all]
          '[clj-time.periodic :as time-period]
          '[clj-time.core :as tcore]
          '[clj-time.local :as tl]
          '[clj-time.format :as tf]
          '[clj-time.coerce :as tc]
          '[clj-time.periodic :as tp]
          '[clojure.core.reducers :as r]
)

(:use [clojure.tools.cli :only (cli)])
(:gen-class :main true)



(defmacro pdoseq
  "Run over a sequence in parallel (like pmap)"
  [seq-exprs & body]
  (let [pairs (partition 2 seq-exprs)]
    `(do (doall (pmap (fn ~(vec (map first pairs)) ~@body) ~@(map
                                                               second pairs))) nil)))



(defmacro dopar [seq-expr & body]
  (assert (= 2 (count seq-expr)) "single pair of forms in sequence expression")
  (let [[k v] seq-expr]
    `(apply await
       (for [k# ~v]
         (let [a# (agent k#)]
           (send a# (fn [~k] ~@body))
           a#)))))


(defn time-range
  [start end step]
  (let [inf-range (time-period/periodic-seq start step)
        below-end? (fn[t] (tcore/within? (tcore/interval start end)
                            t))]
    (take-while below-end? inf-range)))


(defn setid [int] (rand-int int))
(defn trans [day] (tc/to-long day))

(def dtsequence (time-range (tcore/date-time 2013 01 01)
            (tcore/date-time 2014 01 01)
           (tcore/seconds 200)))


(defn insert_timestamp_values [database collection]
  (let [conn (mg/connect)
        db   (mg/get-db conn database)
        coll collection ]
   (mc/drop db coll)
  (doseq [item dtsequence]  (mc/insert db coll {:id (setid 1000) :ts (trans item)}))))


(time(insert_timestamp_values "throughput" "clojure_throughput_src"))



(def abbr-day (tf/formatter "E"))
(defn get_dt [ts] (tc/from-long ts))
(defn get_timeslot [dt] (str (tf/unparse abbr-day dt) "_" (tcore/hour dt)))

(defn prepare_data [map] (hash-map :dt
  (get_timeslot
    (get_dt
      (get map :ts)
      )) :id (get map :id)))



(time (let [conn (mg/connect)
            db (mg/get-db conn "throughput")
            src "clojure_throughput_src"
            agg "clojure_throughput_agg"]
        (mc/drop db agg)
        (mc/ensure-index db agg (array-map :id 1) {:name "id_1"})
        (doseq [item (mc/find-maps db src {})]
          (let [doc (prepare_data item)]
            (mc/upsert db agg {:id (get doc :id)} {$inc {(symbol (get doc :dt)) 1}})
            )
          )
        )
  )

