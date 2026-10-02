```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const SeminarApp());
}

class SeminarApp extends StatelessWidget {
  const SeminarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Seminar Teknologi',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: Colors.white,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          foregroundColor: Colors.black87,
          elevation: 0,
        ),
      ),
      home: const SeminarPage(),
    );
  }
}

// Reusable widget untuk identitas pembicara
class SpeakerCard extends StatelessWidget {
  final String imageUrl;
  final String name;
  final String role;
  final IconData badgeIcon;
  final String badgeLabel;
  final double avatarRadius;
  final double nameFontSize;
  final double detailFontSize;
  final double iconSize;
  final double leftPadding;

  const SpeakerCard({
    super.key,
    required this.imageUrl,
    required this.name,
    required this.role,
    required this.badgeIcon,
    required this.badgeLabel,
    this.avatarRadius = 26,
    this.nameFontSize = 13,
    this.detailFontSize = 9,
    this.iconSize = 14,
    this.leftPadding = 8,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Padding(
        padding: EdgeInsets.only(left: leftPadding),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            CircleAvatar(
              radius: avatarRadius,
              backgroundImage: NetworkImage(imageUrl),
              backgroundColor: Colors.black12,
            ),
            const SizedBox(height: 10),
            Text(
              name,
              style: TextStyle(
                fontSize: nameFontSize,
                fontWeight: FontWeight.w500,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              role,
              style: TextStyle(
                fontSize: detailFontSize,
                color: Colors.black54,
              ),
            ),
            const SizedBox(height: 8),
            Icon(badgeIcon, size: iconSize, color: Colors.black87),
            const SizedBox(height: 2),
            Text(
              badgeLabel,
              style: TextStyle(
                fontSize: detailFontSize,
                color: Colors.black54,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class SeminarPage extends StatelessWidget {
  const SeminarPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Seminar Teknologi',
          style: TextStyle(fontSize: 18),
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image banner
            Image.network(
              'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200',
              width: double.infinity,
              height: 110,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) {
                return Container(
                  width: double.infinity,
                  height: 110,
                  color: Colors.grey.shade300,
                  child: const Icon(
                    Icons.landscape,
                    size: 48,
                    color: Colors.black38,
                  ),
                );
              },
            ),

            Container(
              width: double.infinity,
              color: Colors.white,
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 16),

                  // Judul
                  const Text(
                    'Seminar Teknologi 2026',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w500,
                      color: Colors.black87,
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Subjudul
                  const Text(
                    'Membangun Masa Depan Digital dengan Artificial Intelligence',
                    style: TextStyle(fontSize: 12, color: Colors.black54),
                  ),
                  const SizedBox(height: 24),

                  // RichText: tanggal
                  RichText(
                    text: const TextSpan(
                      style: TextStyle(fontSize: 12, color: Colors.black54),
                      children: [
                        TextSpan(
                          text: 'Tanggal: ',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                        TextSpan(text: '15 Oktober 2026'),
                      ],
                    ),
                  ),
                  const SizedBox(height: 2),

                  // RichText: waktu
                  RichText(
                    text: const TextSpan(
                      style: TextStyle(fontSize: 12, color: Colors.black54),
                      children: [
                        TextSpan(
                          text: 'Waktu: ',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                        TextSpan(text: '09.00 - 15.00 WIB'),
                      ],
                    ),
                  ),
                  const SizedBox(height: 2),

                  // RichText: lokasi
                  RichText(
                    text: const TextSpan(
                      style: TextStyle(fontSize: 12, color: Colors.black54),
                      children: [
                        TextSpan(
                          text: 'Lokasi: ',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                        TextSpan(text: 'Aula Universitas Mikroskil'),
                      ],
                    ),
                  ),
                  const SizedBox(height: 28),

                  // Judul section pembicara
                  const Text(
                    'Pembicara',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w500,
                      color: Colors.black87,
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Pembicara 1
                  const SpeakerCard(
                    imageUrl:
                        'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300',
                    name: 'Dr. Budi Santoso',
                    role: 'AI Researcher',
                    badgeIcon: Icons.star,
                    badgeLabel: 'Keynote Speaker',
                    avatarRadius: 32,
                    nameFontSize: 15,
                    detailFontSize: 10,
                    iconSize: 18,
                    leftPadding: 8,
                  ),
                  const SizedBox(height: 28),

                  // Pembicara 2
                  const SpeakerCard(
                    imageUrl:
                        'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=300',
                    name: 'Siti Rahma',
                    role: 'Data Scientist',
                    badgeIcon: Icons.groups,
                    badgeLabel: 'Guest Speaker',
                    avatarRadius: 24,
                    nameFontSize: 12,
                    detailFontSize: 9,
                    iconSize: 14,
                    leftPadding: 12,
                  ),
                  const SizedBox(height: 28),

                  // Pembicara 3
                  const SpeakerCard(
                    imageUrl:
                        'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=300',
                    name: 'Andi Pratama',
                    role: 'Software Engineer',
                    badgeIcon: Icons.code,
                    badgeLabel: 'Industry Speaker',
                    avatarRadius: 26,
                    nameFontSize: 13,
                    detailFontSize: 9,
                    iconSize: 14,
                    leftPadding: 4,
                  ),
                  const SizedBox(height: 32),

                  // Ajakan
                  const Text(
                    'Jangan lewatkan kesempatan ini!',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                      color: Colors.black87,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // RichText: ajakan daftar
                  RichText(
                    text: const TextSpan(
                      style: TextStyle(fontSize: 11, color: Colors.black54),
                      children: [
                        TextSpan(text: 'Daftarkan diri Anda sekarang dan dapatkan '),
                        TextSpan(
                          text: 'pengalaman belajar bersama para praktisi teknologi.',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Icon kalender
                  const Align(
                    alignment: Alignment.centerRight,
                    child: Padding(
                      padding: EdgeInsets.only(right: 24),
                      child: Icon(
                        Icons.event_available,
                        size: 24,
                        color: Colors.black87,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```