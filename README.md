# Hand Target – El Hareketleriyle Hedef Vurma Oyunu

## Proje Hakkında

Bu proje, Bilgisayarlı Görü dersi kapsamında Python, OpenCV ve MediaPipe kütüphaneleri kullanılarak geliştirilmiş, el hareketleriyle kontrol edilen bir hedef vurma oyunudur.

Uygulama, bilgisayar kamerasından alınan görüntüler üzerinden kullanıcının elini gerçek zamanlı olarak tespit eder. İşaret parmağının konumu kullanılarak ekrandaki nişangâh kontrol edilir. Başparmak ve işaret parmağının birbirine yaklaştırılmasıyla ateş etme işlemi gerçekleştirilir.

Oyuncunun amacı, belirlenen süre içerisinde ekranda rastgele konumlarda oluşan hedefleri vurarak mümkün olduğunca yüksek puan elde etmektir.

## Kullanılan Teknolojiler

- **Python:** Uygulamanın geliştirilmesi ve oyun algoritmalarının oluşturulması.
- **OpenCV:** Kamera görüntüsünün alınması, işlenmesi ve oyun arayüzünün oluşturulması.
- **MediaPipe:** El tespiti ve el üzerindeki 21 landmark noktasının belirlenmesi.
- **Random:** Hedeflerin rastgele konumlarda oluşturulması.
- **Time:** Oyun süresinin hesaplanması ve kontrol edilmesi.

## Projenin Çalışma Mantığı

1. OpenCV ile bilgisayar kamerasından canlı görüntü alınır.
2. Görüntü, MediaPipe modelinin işleyebileceği formata dönüştürülür.
3. MediaPipe kullanılarak elin 21 landmark noktası tespit edilir.
4. İşaret parmağının uç noktası (Landmark 8) kullanılarak ekrandaki nişangâhın konumu belirlenir.
5. Başparmak (Landmark 4) ile işaret parmağı arasındaki Öklid mesafesi hesaplanır.
6. Parmaklar arasındaki mesafe belirlenen eşik değerinin altına düştüğünde ateş etme işlemi gerçekleştirilir.
7. Nişangâhın hedefe olan uzaklığı hesaplanarak isabet kontrolü yapılır.
8. Başarılı atışlarda oyuncunun skoru 10 puan artırılır ve hedef rastgele yeni bir konuma taşınır.
9. Belirlenen süre sona erdiğinde oyun durur ve yeni atışlar kabul edilmez.

## Oyun Kontrolleri

- **İşaret Parmağı:** Nişangâhı hareket ettirir.
- **Başparmak + İşaret Parmağı:** Parmaklar birleştirildiğinde ateş edilir.
- **S Tuşu:** Oyunu başlatır veya süre dolduktan sonra yeniden başlatır.
- **Q Tuşu:** Oyundan çıkış yapar.

## Oyun Özellikleri

- Gerçek zamanlı el ve parmak takibi
- El hareketleriyle nişan alma ve ateş etme
- Öklid mesafesiyle hareket ve isabet kontrolü
- Tek parmak birleştirme hareketinde tek atış gerçekleştirme
- Rastgele konumlanan hedefler
- Başarılı atışlarda puan kazanma
- Süreye karşı oynanış
- Anlık skor ve kalan süre göstergesi
- Oyun sonunda yeniden başlatma

## Kurulum ve Çalıştırma

Projenin çalıştırılması için Python ve gerekli kütüphanelerin bilgisayarda kurulu olması gerekmektedir.

Gerekli bağımlılıklar `requirements.txt` dosyası üzerinden yüklenebilir.

Uygulamada kullanılan `hand_landmarker.task` model dosyasının `main.py` ile aynı dizinde bulunması gerekmektedir.

Kurulum tamamlandıktan sonra `main.py` dosyası çalıştırılarak oyun başlatılabilir.

## Sonuç

Bu projede MediaPipe tarafından sağlanan el tespit verileri, OpenCV ve Python kullanılarak etkileşimli bir oyun mekanizmasına dönüştürülmüştür.

Proje sayesinde gerçek zamanlı görüntü işleme, landmark koordinatlarının kullanılması, Öklid mesafesi hesaplama, hareket tanıma, isabet kontrolü ve temel oyun algoritmaları uygulamalı olarak gerçekleştirilmiştir.