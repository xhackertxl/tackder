load   data
infile '002578.csv'
append   into   table DAY_002578
fields terminated by ','
trailing   nullcols
(
--------------------------------------------------------

    "date" DATE "yyyy-mm-dd",
	"OPEN",
	"HIGH" ,
	"CLOSE" ,
	"LOW" ,
	"VOLUME" ,
	"AMOUNT" ,
	"FACTOR"
)
