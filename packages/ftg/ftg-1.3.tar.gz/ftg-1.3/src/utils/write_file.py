def write_file(loc, cont):
	f = open(loc, "w+")
	f.write(cont)
	f.close()