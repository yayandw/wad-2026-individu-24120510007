📌 **PANDUAN TUGAS INDIVIDU: FASTAPI ENDPOINT**

Buat 1 endpoint FastAPI di repo pribadi (dari template starter). Pilih 1 topik dari tabel berikut:

**Pilihan Topik & Validasi Khusus:**

* **T1 | Buku**: `isbn` (13 digit), `tahun_terbit` (1900–2026)
* **T2 | Tiket**: `kode_tiket` (pola EVT-XXXX), `kuota` (> 0)
* **T3 | Pengiriman**: `no_resi` (pola JKT0000000), `berat_kg` (<= 50)
* **T4 | Menu**: `sku` (pola KOPI-000), `kategori` (kopi / non-kopi / makanan)

---

✅ **CHECKLIST DEFINITION OF DONE (DoD):**

1. **Repo Setup:**
* Nama repo: `wad-2026-individu-<NIM>` (Public, dari template).
* README.md jelas dan dapat diikuti.


2. **Endpoint Specs:**
* `POST /api/<entitas>` -> Status 201 Created + Header `Location`.
* `GET /api/<entitas>` -> Status 200 OK (dukung `?skip`, `?limit`, `?search`).
* `GET /api/<entitas>/{id}` -> Status 404 jika ID tidak ada.


3. **Data & Validation:**
* Input invalid -> Status 422 Unprocessable Entity.
* Skema Input != Skema Output (`id` dibuat oleh server).


4. **Workflow & Verification:**
* Dikerjakan di branch `feature/endpoint-individu`, PR ke `main`, lalu merge sendiri.
* Pengujian `python verify.py --individu` berstatus hijau (PASS).



---