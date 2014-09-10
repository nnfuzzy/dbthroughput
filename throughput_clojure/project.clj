(defproject mongothroughput_clojure "1.0.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [clj-time "0.7.0"]
                 [com.novemberain/monger "2.0.0-rc1"]
                 [iota "1.1.2"]
                 [cheshire "5.3.1"]
                 [com.taoensso/carmine "2.7.0" :exclusions [org.clojure/clojure]]
                 [korma "0.3.0"]
                 [org.clojure/tools.cli "0.3.1"]
                 [org.clojure/java.jdbc "0.3.5"]
                 [org.xerial/sqlite-jdbc "3.7.15-M1"]
                 [lein-swank "1.4.5"]]


  :plugins [[lein-bin "0.3.4"]]
  :main throughput_clojure.throughput
 )
