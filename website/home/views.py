import json

from django.db import connections

from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

def viewResult(sql, request):
    with connections['mysql'].cursor() as cursor:
        cursor.execute("SELECT id_kategori, nama_kategori FROM Kategori")
        kategories = cursor.fetchall()
		
        cursor.execute("SELECT id_status, nama_status FROM Status")
        statuses = cursor.fetchall()
		
        cursor.execute(sql)
        produks = cursor.fetchall()

    kategoriOptions = ''
    for item in kategories:
        kategoriOptions += '<option value="' + str(item[0]) + '">' + item[1] + '</option>'

    statusOptions = ''
    for item in statuses:
        statusOptions += '<option value="' + str(item[0]) + '">' + item[1] + '</option>'
    
    results = ''
    for item in produks:
    	results += '<tr><td>' + str(item[0]) + '</td><td>' + item[1] + '</td><td>' + str(item[2]) + '</td><td>' + item[3] + '</td><td>' + item[4] + '</td><td><button onclick="edit(' + str(item[0]) + ', \'' + item[1] + '\', ' + str(item[2]) + ', ' + str(item[5]) + ', ' + str(item[6]) + ')">Edit</button> <button onclick="hapus(' + str(item[0]) + ', \'' + item[1] + '\')">Hapus</button></td></tr>'

    context = {
        'kategoriOptions': kategoriOptions,
        'statusOptions': statusOptions,
        'results': results
    }
    
    return context
    

# Show all Produk
def index(request):
    context = viewResult('SELECT id_produk, nama_produk, harga, Kategori.nama_kategori, Status.nama_status, kategori_id, status_id FROM Produk JOIN Kategori ON Produk.kategori_id = Kategori.id_kategori JOIN Status ON (Produk.status_id = Status.id_status) ORDER BY id_produk', request)
    context['title'] = 'Produk'

    context['href'] = 'bisadijual'
    context['hrefLabel'] = 'Tampilkan produk yang bisa dijual'

    return render(request, 'home/produk.html', context)

# Show Produk bisa dijual only
def bisadijual(request):
    context = viewResult('SELECT id_produk, nama_produk, harga, Kategori.nama_kategori, Status.nama_status, kategori_id, status_id FROM Produk JOIN Kategori ON Produk.kategori_id = Kategori.id_kategori JOIN Status ON (Produk.status_id = Status.id_status AND Status.nama_status = \'bisa dijual\') ORDER BY id_produk', request)
    context['title'] = 'Produk bisa dijual'

    context['href'] = 'produk'
    context['hrefLabel'] = 'Tampilkan semua produk'

    return render(request, 'home/produk.html', context) 

def simpan(request):	
	data = json.loads(request.body)

	editId = data.get('editId')
	nama_produk = data.get('nama_produk')
	harga = data.get('harga')
	kategori_id = data.get('kategori_id')
	status_id = data.get('status_id')

	with connections['mysql'].cursor() as cursor:
		if editId == -1:
			sql = "INSERT INTO Produk (nama_produk, harga, kategori_id, status_id) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (nama_produk, harga, kategori_id, status_id))
		else:
			sql = "UPDATE Produk SET nama_produk = %s, harga = %s, kategori_id = %s, status_id = %s WHERE id_produk = %s"
			cursor.execute(sql, (nama_produk, harga, kategori_id, status_id, editId))
	
	return HttpResponse('{"status": "success"}')

def hapus(request):	
	data = json.loads(request.body)

	id = data.get('id')

	with connections['mysql'].cursor() as cursor:
		sql = "DELETE FROM Produk WHERE id_produk = %s"
		cursor.execute(sql, (id,))
	
	return HttpResponse('{"status": "success"}')
    
# reference, readme, basic page
def semua(request):
    """Home page view"""
    context = {
        'title': 'Welcome to Django!',
        'message': 'Your first Django project is running.',
        'features': [
            'Fast development',
            'Secure by default',
            'Scalable',
            'Versatile'
        ]
    }
    return render(request, 'home/index.html', context)