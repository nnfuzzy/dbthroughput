(ns throughput_clojure.throughput
  (require [monger.core :as mg :only [connect get-db]]
    [monger.collection :as mc :only [drop find-maps upsert ensure-index]]
    [monger.operators :refer :all]
    [clj-time.periodic :as time-period]
    [clj-time.core :as tcore :only [seconds date-time]]
    [clj-time.format :as tf]
    [clj-time.coerce :as tc :only [from-long to-long]]
    ;[clojure.core.reducers :as r]
    [clojure.tools.cli :as cli]
    [taoensso.carmine :as car :refer (wcar)])
  (:gen-class :main true))


(def server1-conn)
(defmacro wcar* [& body] `(car/wcar server1-conn ~@body))


(defn time-range
  [start end step]
  (let [inf-range (time-period/periodic-seq start step)
        below-end? (fn [t] (tcore/within? (tcore/interval start end)
                             t))]
    (take-while below-end? inf-range)))



(defn dtsequence [delay] (time-range (tcore/date-time 2013 01 01)
                           (tcore/date-time 2014 01 01)
                           (tcore/seconds delay)))

(defn setid [int] (rand-int int))
(defn trans [day] (tc/to-long day))
(def abbr-day (tf/formatter "E"))
(defn get_dt [ts] (tc/from-long ts))
(defn get_timeslot [dt] (str (tf/unparse abbr-day dt) "_" (tcore/hour dt)))


(defn prepare_data_mongodb [map] (hash-map :dt (get_timeslot
                                                 (get_dt
                                                   (get map :ts)
                                                   )) :id (get map :id)))


(defn insert_timestamp_values_mongodb [database collection dtsequence uids]
  (let [conn (mg/connect)
        db (mg/get-db conn database)
        coll collection]
    (mc/drop db coll)
    (doseq [item dtsequence] (mc/insert db coll {:id (setid uids) :ts (trans item)}))))


(defn insert_timestamp_values_redis [dtsequence uids]
  (wcar* (car/flushdb))
  (doseq [item dtsequence] (wcar* (car/hset (format "%s:%s" 'src (setid uids)) (trans item) nil))))


(defn prepare_data_redis [tstamp]
  (get_timeslot
    (get_dt tstamp
      )))


(defn -main [& args]
  (let [[opts args banner] (cli/cli args
                             ["-h" "--help" "Print this help" :default false :flag true]
                             ["-d" "--delay" "delay in seconds" :default 2000 :parse-fn #(Integer. %)]
                             ["-u" "--uids" "number of uids" :default 1000 :parse-fn #(Integer. %)]
                             ["-i" "--inserts_mongodb" "insert in mongodb" :default false :flag true]
                             ["-a" "--aggregate_mongodb" "aggregate in mongodb" :default false :flag true]
                             ["-r" "--inserts_redis" "insert in redis" :default false :flag true]
                             ["-s" "--aggregate_redis" "aggregate in redis" :default false :flag true]
                             )]

    (when (:help opts)
      (println banner))
    (when (:inserts_mongodb opts)
      (let [conn (mg/connect)
            db (mg/get-db conn "throughput")
            src "clojure_throughput_src"
            agg "clojure_throughput_agg"]
        (mc/drop db src))

      (insert_timestamp_values_mongodb "throughput" "clojure_throughput_src" (dtsequence (:delay opts)) (:uids opts)))

    (when (:aggregate_mongodb opts)
      (let [conn (mg/connect)
            db (mg/get-db conn "throughput")
            src "clojure_throughput_src"
            agg "clojure_throughput_agg"]
        (mc/drop db agg)
        (mc/ensure-index db agg (array-map :id 1) {:name "id_1"})
        (doseq [item (mc/find-maps db src {})]
          (let [doc (prepare_data_mongodb item)]
            (mc/upsert db agg {:id (get doc :id)} {$inc {(symbol (get doc :dt)) 1}})
            )
          )
        ))
    (when (:inserts_redis opts)
      (insert_timestamp_values_redis (dtsequence (:delay opts)) (:uids opts))
      )
    (when (:aggregate_redis opts)
      (doseq [item (get_keys "src*")]
        (let [uid (last (str/split item #":"))]
          (doseq [ts (wcar* (car/hkeys item))]
            (wcar* (car/hincrby (str/join ":" ["agg" uid])
                     (prepare_data_redis (read-string ts)) 1)))))
      )
    ))


