#### TESTING 
DELAY <- 2000
UIDS <- 1000
############


rndint <- function(n) round(runif(1)*(n-1),0)
dt_sequence <- function(delay= 2000) {
                   rs <- seq(from =as.POSIXct('2013-01-01 00:00:00',tz = '%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
                   to=as.POSIXct('2014-01-01 00:00:00',tz='%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
                   by=delay)
}

#core functions could be disreagrd
#benchmark(dt_sequence(delay=200),replications = 10)
