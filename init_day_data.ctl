load   data
infile '000666.csv'
append   into   table DAY_000666
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
