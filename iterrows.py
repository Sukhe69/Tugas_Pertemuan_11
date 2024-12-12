import pandas as pd

# Path file Excel yang akan dibaca
file_path = "data_jabar.xlsx"  # Ganti dengan path file Anda

# Membaca file Excel ke dalam DataFrame
data_sampah = pd.read_excel(file_path)

# Mengganti nama kolom untuk mempermudah analisis
data_sampah.rename(columns={
    "nama_kabupaten_kota": "Kabupaten/Kota",
    "jumlah_produksi_sampah": "Jumlah Produksi Sampah (Ton)",
    "tahun": "Tahun Pencatatan"
}, inplace=True)

# Memilih hanya kolom yang relevan
filter_data_sampah = data_sampah[["Kabupaten/Kota", "Jumlah Produksi Sampah (Ton)", "Tahun Pencatatan"]]

# Menampilkan beberapa baris awal untuk verifikasi
print("Data jumlah produksi sampah berdasarkan Kabupaten/Kota di Jawa Barat:")
print(filter_data_sampah.head())

# SOAL 2: Dari DataFrame yang telah dibuat, hitunglah total produksi sampah di seluruh Kabupaten/Kota di Jawa Barat untuk tahun tertentu.
tahun_tertentu = 2015  # Ganti dengan tahun yang diinginkan
total_sampah_tahun = filter_data_sampah[filter_data_sampah["Tahun Pencatatan"] == tahun_tertentu]["Jumlah Produksi Sampah (Ton)"].sum()
print(f"\nTotal produksi sampah di seluruh Kabupaten/Kota di Jawa Barat pada tahun {tahun_tertentu}: {total_sampah_tahun} ton")

# SOAL 3: Jumlahkan Data Per Tahun
print("\nJumlah produksi sampah per tahun:")
jumlah_per_tahun = {}
for tahun, data in filter_data_sampah.groupby("Tahun Pencatatan"):
    total_tahun = data["Jumlah Produksi Sampah (Ton)"].sum()
    jumlah_per_tahun[tahun] = total_tahun
    print(f"Tahun {tahun}: {total_tahun} ton")

# SOAL 4: Jumlahkan data per Kota/Kabupaten per tahun
print("\nJumlah produksi sampah per Kota/Kabupaten per tahun:")
jumlah_per_kota_per_tahun = {}
for _, row in filter_data_sampah.iterrows():
    kota = row["Kabupaten/Kota"]
    tahun = row["Tahun Pencatatan"]
    jumlah = row["Jumlah Produksi Sampah (Ton)"]
    if (kota, tahun) not in jumlah_per_kota_per_tahun:
        jumlah_per_kota_per_tahun[(kota, tahun)] = 0
    jumlah_per_kota_per_tahun[(kota, tahun)] += jumlah

for (kota, tahun), total in jumlah_per_kota_per_tahun.items():
    print(f"{kota}, Tahun {tahun}: {total} ton")

# Export hasil ke CSV
csv_output_path = "jumlah_produksi_sampah.csv"
excel_output_path = "jumlah_produksi_sampah.xlsx"

# Membuat DataFrame untuk ekspor
jumlah_per_tahun_df = pd.DataFrame(list(jumlah_per_tahun.items()), columns=["Tahun", "Jumlah Produksi Sampah (Ton)"])
jumlah_per_kota_per_tahun_df = pd.DataFrame(list(jumlah_per_kota_per_tahun.items()), columns=["Kota/Tahun", "Jumlah Produksi Sampah (Ton)"])
jumlah_per_kota_per_tahun_df[["Kabupaten/Kota", "Tahun Pencatatan"]] = pd.DataFrame(jumlah_per_kota_per_tahun_df["Kota/Tahun"].tolist(), index=jumlah_per_kota_per_tahun_df.index)
jumlah_per_kota_per_tahun_df.drop(columns="Kota/Tahun", inplace=True)

# Ekspor ke file CSV
jumlah_per_tahun_df.to_csv(csv_output_path, index=False)
jumlah_per_kota_per_tahun_df.to_csv(csv_output_path.replace(".csv", "_kota_per_tahun.csv"), index=False)

# Ekspor ke file Excel
with pd.ExcelWriter(excel_output_path) as writer:
    jumlah_per_tahun_df.to_excel(writer, sheet_name="Per Tahun", index=False)
    jumlah_per_kota_per_tahun_df.to_excel(writer, sheet_name="Per Kota Per Tahun", index=False)

print(f"\nHasil telah diekspor ke file:\n- {csv_output_path}\n- {csv_output_path.replace('.csv', '_kota_per_tahun.csv')}\n- {excel_output_path}")