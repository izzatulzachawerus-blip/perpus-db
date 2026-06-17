from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    stok = models.IntegerField(default=0)
    pengarang = models.CharField(max_length=255, null=True, blank=True)
    tahun_terbit = models.CharField(max_length=50, null=True, blank=True)
    kategori = models.CharField(max_length=100, null=True, blank=True)
    penerbit = models.CharField(max_length=100, null=True, blank=True)
    rak = models.CharField(max_length=50, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)


class Siswa(models.Model):
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class Peminjam(models.Model):
    nama_peminjam = models.CharField(max_length=255)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)


class Peminjaman(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.TextField()
    status = models.CharField(max_length=50)