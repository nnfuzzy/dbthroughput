(defproject mongothroughput_clojure "1.0.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [clj-time "0.7.0"]
                 [com.novemberain/monger "2.0.0-rc1"]
                 [iota "1.1.2"]
                 [cheshire "5.3.1"]
                 [com.taoensso/carmine "2.6.2"]
                 [org.clojure/tools.cli "0.3.1"]]

  :plugins [[lein-bin "0.3.4"]]
  :main throughput_clojure.throughput
 )