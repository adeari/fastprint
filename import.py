import json
import mysql.connector

print(f"Start import")
try:
	# Connect Mysql
	mydb = mysql.connector.connect(host="localhost", user="ade", password="1234", database="fastprint")
	mycursor = mydb.cursor()

	# Read from a JSON file
	with open('json/data.json', 'r') as file:
		data = json.load(file)

	list = data.get('data')
	kategoriMap = {}
	statusMap = {}
	for item in list:
		kategori = item.get('kategori')
		if kategori not in kategoriMap:
			sql = "INSERT INTO Kategori (nama_kategori) VALUES (%s)"
			mycursor.execute(sql, (kategori,))
			mydb.commit()
			new_id = mycursor.lastrowid
			kategoriMap[kategori] = new_id

		status = item.get('status')
		if status not in statusMap:			
			sql = "INSERT INTO Status (nama_status) VALUES (%s)"
			mycursor.execute(sql, (status,))
			mydb.commit()
			new_id = mycursor.lastrowid
			statusMap[status] = new_id
		
		sql = "INSERT INTO Produk (nama_produk, harga, kategori_id, status_id) VALUES (%s, %s, %s, %s)"
		mycursor.execute(sql, (item.get('nama_produk'), item.get('harga'), kategoriMap[kategori], statusMap[status]))
		mydb.commit()

except mysql.connector.Error as err:
	print(f"Error: {err}")

finally:
	# Close the cursor and connection
	if 'mycursor' in locals() and mycursor is not None:
		mycursor.close()
	if 'mydb' in locals() and mydb is not None and mydb.is_connected():
		mydb.close()
	print(f"Finish import")
