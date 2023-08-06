# Ipython ODBC SQL Magic

IPython Magic untuk menjalankan SQL menggunakan ODBC secara langsung pada notebook cell.

## Pemasangan

```bash
$ pip3 install ipython-dawet-sql
```

## Penggunaan

### Load Ekstensi
Untuk dapat menggunakan, ekstensi harus di *load* terlebih dahulu ke notebook yang sedang digunakan.
```
In [ ]: %load_ext dawetsql
```

### Database Connection

#### Membuka Koneksi
```
In [ ]: %dawetsql
```
Setelah line magic dieksekusi, selanjutnya isi form sesuai dengan konfigurasi ODBC. Username dan password optional jika sudah diset di konfigurasi ODBC sistem.

![query builder](img/login.PNG)

Untuk me-restart koneksi, cukup klik `connect`, `dawetsql` akan otomatis menutup koneksi terlebih dahulu sebelum membuka koneksi baru lagi.


#### Menutup Koneksi

```
In [ ]: %dawetsqlclose
```

### Menjalankan SQL

```
In [ ]: %%dawetsql
        SELECT * FROM tables
        WHERE somecolumn = 'somevalue'
```
Preview hasil query ditampilkan menggunakan `pandas.DataFrame` dengan default limit 10 baris.

Available arguments

Arguments | Type | Default | Descriptions
---|---|---|---
`-l --limit` | Integer | 10 | Set limit query untuk preview
`-o --output` | String | `_` | Nama output hasil query.

### Contoh Penggunaan

#### Menyimpan Hasil query ke Python Variable

```
In [ ]: %%dawetsql --ouput variablename
        SELECT * FROM tables
        WHERE somecolumn = 'somevalue'
```

#### Menyimpan Hasil Query ke File
Cell Magic `%%dawetsql` akan otomatis menyimpan hasil query kedalam file jika nama output memiliki ekstensi `.csv`, `.pkl`, dan `.xlsx`
```
In [ ]: %%dawetsql --output filename.csv
        SELECT * FROM tables
        WHERE somecolumn = 'somevalue'
```

### Akses Python Variable dari SQL Query
Untuk mengakses variable dari local namespace, gunakan format `?namavariable` sebagai placeholder pada SQL Query. Tanda petik (`'`) akan otomatis ditambahkan jika tipe variable bukan `int` atau `float`.

```
In [1]: low = 1
        high = 100
        other_column_name = "something"
```

pada magic cell

```
In [2]: %%dawetsql
        SELECT 
            *
        FROM
            TABLE
        WHERE
            SOME_COLUMN BETWEEN ?low AND ?high
            AND OTHER_COLUMN = ?other_column_name
```
SQL Query akan dikonversi menjadi 
```
SELECT 
    *
FROM
    TABLE
WHERE
    SOME_COLUMN BETWEEN 1 AND 100
    AND OTHER_COLUMN = 'something'
```

### Widgets

#### Schema Explorer Widget

Widget ini digunakan untuk meng-explore skema, tabel, kolom, dan tipe kolom pada database.

```
%explorer [-f --force]
```

**Table Detail**


![table detail](img/widget01.JPG)

**Query Builder**


![query builder](img/widget02.JPG)

**Table Data Preview**


![query builder](img/widget03.JPG)

### Settings

File konfigurasi `dawetsql` tersimpan pada direktori `~/.dawetsql`.

### Lain-lain

#### SQL Autocomplete
Cell magic `%%dawetsql` mendukung SQL Autocomplete. Fitur ini masih bersifat eksperimental. Autocomplete untuk nama tabel dan kolom tersedia setelah pengguna menjalankan magic `%explore`. Untuk pengguna lama, jalankan `%explorer -f`, lalu restart notebook.

## Legal
Package ini dirilis di bawah lisensi MIT.
