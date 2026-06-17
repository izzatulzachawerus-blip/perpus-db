from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # BUKU
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/create/', views.buku_create, name='buku_create'),
    path('buku/edit/<int:id>/', views.buku_edit, name='buku_edit'),
    path('buku/delete/<int:id>/', views.buku_delete, name='buku_delete'),
    path('buku/<int:id>/', views.buku_detail, name='buku_detail'),

    # SISWA
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/create/', views.siswa_create, name='siswa_create'),
    path('siswa/edit/<int:id>/', views.siswa_edit, name='siswa_edit'),
    path('siswa/delete/<int:id>/', views.siswa_delete, name='siswa_delete'),
    path('siswa/detail/<int:id>/', views.siswa_detail, name='siswa_detail'),

    # PEMINJAMAN
    path('peminjaman/', views.peminjaman, name='peminjaman'),
    path('peminjaman/tambah/', views.pinjam_tambah, name='pinjam_tambah'),
    path('peminjaman/ubah/<int:id>/', views.ubah_status, name='ubah_status'),

    path('admin/', admin.site.urls),
]