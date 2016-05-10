# coding= utf-8
import string
import re
import csv
import sys


infile = open('3_IP_publications_2015Aug28-xls(2).csv', 'rb')
reader = csv.reader(infile, dialect='excel', delimiter=',')
readerlist = list(reader)
outfile_1 = open('cleaned_publications.csv', 'wb')
writer = csv.writer(outfile_1, dialect='excel')

#rows: 582 w/ header
#cols: 11

def clean_author(author):
	m = re.search("(,)(\S)", author)
	if m:
		#print("PASS: " + author + " AT: " + "'" + m.group(1)+m.group(2)) + "'"
		changed = re.sub(r"(,)(\S)", r"\1 \2", author)
		#print("CHANGED: " + changed)
		author = changed
	# insert space after comma
	#print author
	m = re.search("([A-Z]\.)\s([A-Z]\.)", author)
	if m:
		#print("PASS: " + author + " AT: " + "'" + m.group(1)+ " " +m.group(2) + "'")
		changed = re.sub(r"([A-Z]\.)\s([A-Z]\.)", r"\1\2", author)
		#print("changed: " + changed)
		author = changed
	# delete spaces in intials
	m = re.search("([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.)\s(de)\s([A-Z]\w+)", author)
	if m:
		#print "PASS: " + author + " AT " + "'" + m.group(1) + " " + m.group(2) + " "  + m.group(3) + "'"
		changed = re.sub(r"([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.)\s(de)\s([A-Z]\w+)", r"\2 \3, \1", author)
		author = changed
		#print "CHANGED: " + changed
	#re-order last names with "de"
	m = re.search("([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.)\s([A-Z]\w+)\s(y)\s([A-Z]\w+)", author)
	if m:
		#print "PASS: " + author + " AT " + "'" + m.group(1) + " " + m.group(2) + " " + m.group(3) + " " + m.group(4) + "'"
		changed = re.sub(r"([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.)\s([A-Z]\w+)\s(y)\s([A-Z]\w+)", r"\2 \3 \4, \1", author)
		author = changed
		#print "CHANGED: " + changed
	#re-order last names with "y"
	match = re.search("([A-Z]\.[A-Z]\.|[A-Z].|[A-Z]\.[A-Z]\.[A-Z]\.)\s(Jr\.|[A-Z][A-Za-z]+)", author, re.UNICODE)
	if match:
 		#print("PASS: " + author + " AT: " + "'" + match.group(1) + " " + match.group(2) + "'")
 		changed = re.sub(r"([A-Z]\.[A-Z]\.|[A-Z].|[A-Z]\.[A-Z]\.[A-Z]\.)\s(Jr\.|[A-Z][A-Za-z]+)", r"\2, \1", author)
 		#print("CHANGED: " + changed)
 		author = changed
 	#names flipped to <lastName, initial>
 	#"Jr" names in correct order need to be escaped
 	if "," not in author and "no agent data" not in author:
 		#print "PASS: " + author
 		x = author.split(" ")
 		#print x
 		if len(x) > 1:
	 		changed = [x[-1] + ","] + x[0:-1]
	 		y = " ".join(changed)
	 		#print "CHANGED: " + y
	 		author = y
	#names without initials
	m = re.search("(\sand)\s", author)
	if m:
		#print author
		#print "PASS: " + author
		changed = re.sub(r"(\sand)", ";", author)
		author = changed
		#print author
	#sub ; for "and"
	if " ed" not in author and " et" not in author:
		m = re.search("([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.),(\s[A-Za-z]\w+)", author)
		if m: 
			#print "PASS: " + author
			changed = re.sub(r"([A-Z]\.[A-Z]\.|[A-Z]\.|[A-Z]\.[A-Z]\.[A-Z]\.),(\s[A-Za-z]\w+)", r"\1;\2", author)
			#print "CHANGED: " + changed
			author = changed
	#semi-colons after initials, before last names
	m = re.search(r";\s([A-Z]\w+)\s([A-Z]\w+)$|;\s([A-Z]\w+)\s([A-Z]\w+);", author)
	if m:
		print "PASS: " + author
		changed = re.sub(r"([A-Z]\w+)\s([A-Z]\w+)", r"\2, \1", author)
		print "CHANGED: " + changed
		author = changed
		#match first name and last name format in list
		#re-order to last name, first name
	return author


def clean_title(title):
	if "<i>" in title:
		#print "PASS: " + title
		changed = title.replace("<i>", "")
		title = changed
	if "</i>" in title:
		changed = title.replace("</i>", "")
		#print "CHANGED: " + changed
		title = changed
	return title

def clean_abbrev(abbrev, dictionary):
	m = re.search("(\.)([A-Za-z])", abbrev)
	if m:
		#print "PASS: " + abbrev + " AT " + m.group(1) + m.group(2)
		changed = re.sub(r"(\.)([A-Za-z])", r"\1 \2", abbrev)
		#print "CHANGED: " + changed
		abbrev = changed
	#insert space after period
	m = re.search("(,)(\S)", abbrev)
	if m:
		#print("PASS: " + abbrev + " AT: " + "'" + m.group(1)+m.group(2)) + "'"
		changed = re.sub(r"(,)(\S)", r"\1 \2", abbrev)
		#print("CHANGED: " + changed)
		abbrev = changed
	# insert space after comma
	#print abbrev
	rc = re.compile('|'.join(map(re.escape, dictionary)))
	def translate(match):
	    return dictionary[match.group(0)]
	changed = re.sub(rc, translate, abbrev)
	#print "ORIGINAL: " + abbrev
	#print "CHANGED: " + changed
	abbrev = changed 
	if abbrev.endswith(".") or abbrev.endswith(","):
		#print "ORGINAL: " + abbrev
		x = abbrev.rstrip(".")
		changed = x.rstrip(",")
		#print "CHANGED: " + changed
		abbrev = changed
	return abbrev

dictionary = { "Jour." : "Journal",
	"J." : "Journal",
	"Univ." : "University",
	"Nat." : "Natural",
	"Am." : "American",
	"Amer." : "American",
	"Bull." : "Bulletin",
	"Bull" : "Bulletin",
	"Quart." : "Quarterly",
	"Geol." : "Geological",
	"Soc." : "Society",
	"Mus." : "Museum",
	"Hist." : "History",
	"Sci." : "Science",
	"Lab." : "Laboratory",
	"Mon." : "Monitor",
	"Rept." : "Report",
	"Rpt." : "Report",
	"Misc." : "Miscellaneous",
	"Acad." : "Academy",
	"Ann." : "Annual",
	"Natl." : "National",
	"Colln." : "Collections",
	"Philos." : "Philosophy",
	"N." :  "North",
	"Proc." : "Proceedings",
	"Paleo.": "Paleontology",
	"Comp." : "Comparative",
	"Leop." : "Leopoldina",
	"Mono." : "Monographs",
	"Mem." : "Memoirs",
	"Geosci." : "Geoscience",
	"Mag." : "Magazine",
	"Pub." : "Publication",
	"U. S." : "U.S.",
	"n. s." : "n.s.",
	"N. Y." : "N.Y.",

}


for row in readerlist:
	author = clean_author(row[1])
	title = clean_title(row[3])
	abbrev = clean_abbrev(row[4], dictionary)
	writer.writerow([row[0], author, row[2], title, abbrev, row[5], row[6], row[7], row[8], row[9], row[10]])
	

infile.close()
outfile_1.close()

#writer.writerow([row[0], author, row[2]], title)

# rownum = 0
# for row in readerlist:
# 	#save header
# 	if rownum == 0:
# 		header = row
# 	else:
# 		colnum = 0
# 		for col in row:
# 			#print '%s: %s' % (header[colnum], col)
# 			#print col
# 			#if colnum == 1:
# 				#print col
# 			colnum += 1
# 	rownum += 1

#print header[2]	


#writes column[1]
#for col in readerlist:
#	writer.writerow([col[1]])


##write header to file
#writer.writerow(header)

#writes entire dataset
#for row in readerlist:
#	writer.writerow(row)

##writes column[1]
#for col in readerlist:
#	writer.writerow([col[1]])


#	row1 = row[1]
#	writer.writerow(row1)

##prints all data in each row separated by /n
#for row in readerlist:
#	print("\n".join(row))

##print column 1 separated by /n
# for row in reader:
# 	print row[1]
# 	print 'test'


##????
# for line in reader.readline():
#     array = line.split(',')
#     first_item = array[0]
# print first_item

    
