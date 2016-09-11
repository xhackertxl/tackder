load   data
infile '000029.csv'
append   into   table DAY_000029
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
