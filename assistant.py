def read_file(path):
	''' This function reads the given file line by line and returns an MxN matrix,
	where M - the number of lines and N - the number of columns in the file'''
	with open(path, mode='r') as file:
		data_matrix= []
		for line in file:
			data_row = []
			for record in line.split():
				data_row.append(float(record))
			data_matrix.append(data_row)
	return data_matrix
