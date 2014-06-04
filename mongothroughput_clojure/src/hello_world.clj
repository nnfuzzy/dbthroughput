(require '[clj-time.core :as t])


(defn hello-world [a]
  (println a))

(println (hello-world "a\n100"))

(def dt (t/date-time 1986 10 14))

(println(t/day dt))

(println 'test)

