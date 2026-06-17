from django.db import connection
from django.shortcuts import render, redirect

def dashboard(request):
    with connection.cursor() as cursor:
        # TOTAL BUKU (jumlah stok semua)
        cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM core_buku")
        total_buku = cursor.fetchone()[0]

        # TOTAL JUDUL
        cursor.execute("SELECT COUNT(*) FROM core_buku")
        total_judul = cursor.fetchone()[0] or 0

        # SEDANG DIPINJAM
        cursor.execute("SELECT COUNT(*) FROM core_peminjaman WHERE status='dipinjam'")
        sedang_dipinjam = cursor.fetchone()[0] or 0

        # SUDAH DIKEMBALIKAN
        cursor.execute("SELECT COUNT(*) FROM core_peminjaman WHERE status='kembali'")
        sudah_kembali = cursor.fetchone()[0] or 0

        # DISTRIBUSI STOK
        cursor.execute("SELECT judul, stok FROM core_buku")
        stok_data = cursor.fetchall()

    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_kembali': sudah_kembali,
        'stok_data': stok_data,
    }
    return render(request, 'dashboard.html', context)

# ================= BUKU =================
def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_buku")
        data = cursor.fetchall()
    return render(request, 'buku/list.html', {'data': data})

def buku_create(request):
    if request.method == "POST":
        judul = request.POST['judul']
        pengarang = request.POST['pengarang']
        kategori = request.POST['kategori']
        penerbit = request.POST['penerbit']
        tahun = request.POST['tahun']
        rak = request.POST['rak']
        stok = request.POST['stok']
        deskripsi = request.POST['deskripsi']

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO core_buku 
                (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, [judul, pengarang, kategori, penerbit, tahun, rak, stok, deskripsi])
        return redirect('buku_list')

    return render(request, 'buku/create.html')

def buku_edit(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id, judul, pengarang, kategori, penerbit,
                tahun_terbit, rak, stok, deskripsi
            FROM core_buku WHERE id=%s
        """, [id])
        buku = cursor.fetchone()

    if request.method == "POST":
        judul = request.POST['judul']
        pengarang = request.POST['pengarang']
        kategori = request.POST['kategori']
        penerbit = request.POST['penerbit']
        tahun = request.POST['tahun']
        rak = request.POST['rak']
        stok = request.POST['stok']
        deskripsi = request.POST['deskripsi']

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE core_buku SET
                    judul=%s,
                    pengarang=%s,
                    kategori=%s,
                    penerbit=%s,
                    tahun_terbit=%s,
                    rak=%s,
                    stok=%s,
                    deskripsi=%s
                WHERE id=%s
            """, [judul, pengarang, kategori, penerbit, tahun, rak, stok, deskripsi, id])
        return redirect('buku_list')

    return render(request, 'buku/edit.html', {'buku': buku})

def buku_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_buku WHERE id = %s", [id])
        buku = cursor.fetchone()

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_buku WHERE id = %s", [id])
        return redirect('buku_list')

    return render(request, 'buku/delete.html', {'buku': buku})

def buku_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id, judul, pengarang, kategori, penerbit,
                tahun_terbit, rak, stok, deskripsi
            FROM core_buku WHERE id=%s
        """, [id])
        row = cursor.fetchone()

    if not row:
        return redirect('buku_list')

    buku = {
        'id': row[0],
        'judul': row[1],
        'pengarang': row[2],
        'kategori': row[3],
        'penerbit': row[4],
        'tahun': row[5],
        'rak': row[6],
        'stok': row[7],
        'deskripsi': row[8],
    }
    return render(request, 'buku/detail.html', {'buku': buku})        

# ================= SISWA =================
def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_siswa")
        data = cursor.fetchall()
    return render(request, 'siswa/list.html', {'data': data})

def siswa_create(request):
    if request.method == "POST":
        nama = request.POST['nama']
        kelas = request.POST['kelas']
        nis = request.POST['nis']
        is_active = request.POST.get('is_active') == 'on'

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO core_siswa (nama, kelas, nis, is_active)
                VALUES (%s,%s,%s,%s)
            """, [nama, kelas, nis, is_active])
        return redirect('siswa_list')

    return render(request, 'siswa/create.html')

def siswa_edit(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_siswa WHERE id=%s", [id])
        siswa = cursor.fetchone()

    if request.method == "POST":
        nama = request.POST['nama']
        kelas = request.POST['kelas']
        nis = request.POST['nis']
        is_active = request.POST.get('is_active') == 'on'

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE core_siswa 
                SET nama=%s, kelas=%s, nis=%s, is_active=%s
                WHERE id=%s
            """, [nama, kelas, nis, is_active, id])
        return redirect('siswa_list')

    return render(request, 'siswa/edit.html', {'siswa': siswa})

def siswa_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_siswa WHERE id=%s", [id])
    return redirect('siswa_list')

def siswa_detail(request, id):
    with connection.cursor() as cursor:
        # ambil data siswa
        cursor.execute("""
            SELECT id, nama, kelas, nis, is_active
            FROM core_siswa WHERE id=%s
        """, [id])
        siswa = cursor.fetchone()

        if not siswa:
            return redirect('siswa_list')

        # total peminjaman
        cursor.execute("""
            SELECT COUNT(*) FROM core_peminjaman WHERE siswa_id=%s
        """, [id])
        total_pinjam = cursor.fetchone()[0] or 0

        # peminjaman aktif
        cursor.execute("""
            SELECT COUNT(*) FROM core_peminjaman
            WHERE siswa_id=%s AND status='dipinjam'
        """, [id])
        aktif = cursor.fetchone()[0] or 0

    data = {
        'id': siswa[0],
        'nama': siswa[1],
        'kelas': siswa[2],
        'nis': siswa[3],
        'is_active': siswa[4],
        'total_pinjam': total_pinjam,
        'aktif': aktif,
    }
    return render(request, 'siswa/detail.html', {'siswa': data})

# ================= PEMINJAMAN =================
def peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.id, s.nama, b.judul, p.tanggal_pinjam,
                p.jatuh_tempo, p.keperluan, 'admin', p.status
            FROM core_peminjaman p
            JOIN core_siswa s ON p.siswa_id = s.id
            JOIN core_buku b ON p.buku_id = b.id
        """)
        data = cursor.fetchall()
    return render(request, 'peminjaman/list.html', {'data': data})

def pinjam_tambah(request):
    if request.method == "POST":
        siswa_id = request.POST.get('siswa')
        buku_id = request.POST.get('buku')
        tgl_pinjam = request.POST.get('tgl_pinjam')
        jatuh_tempo = request.POST.get('jatuh_tempo')
        keperluan = request.POST.get('keperluan')

        with connection.cursor() as cursor:
            # cek stok dulu
            cursor.execute("SELECT stok FROM core_buku WHERE id=%s", [buku_id])
            stok = cursor.fetchone()[0]

            if stok <= 0:
                return render(request, 'peminjaman/form.html', {'error': 'Stok buku habis!'})

            # insert peminjaman
            cursor.execute("""
                INSERT INTO core_peminjaman
                (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s,%s,%s,%s,%s,'dipinjam')
            """, [siswa_id, buku_id, tgl_pinjam, jatuh_tempo, keperluan])

            # kurangi stok
            cursor.execute("""
                UPDATE core_buku SET stok = stok - 1 WHERE id=%s
            """, [buku_id])

        return redirect('peminjaman')

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM core_siswa")
        siswa = cursor.fetchall()

        cursor.execute("SELECT id, judul, stok FROM core_buku")
        buku = cursor.fetchall()

    return render(request, 'peminjaman/form.html', {'siswa': siswa, 'buku': buku})

def ubah_status(request, id):
    with connection.cursor() as cursor:
        # ambil buku_id dulu
        cursor.execute("SELECT buku_id FROM core_peminjaman WHERE id=%s", [id])
        buku_id = cursor.fetchone()[0]

        # ubah status
        cursor.execute("""
            UPDATE core_peminjaman SET status='kembali' WHERE id=%s
        """, [id])

        # kembalikan stok
        cursor.execute("""
            UPDATE core_buku SET stok = stok + 1 WHERE id=%s
        """, [buku_id])

    return redirect('peminjaman')