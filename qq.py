```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MangaApp());
}

class MangaApp extends StatelessWidget {
  const MangaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MGKOMIK',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF1C1C1E),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF1C1C1E),
          foregroundColor: Colors.white,
          elevation: 0,
        ),
      ),
      home: const MangaListPage(),
    );
  }
}

// Model data
class Manga {
  final String title;
  final String coverUrl;
  final String country; // 'KR' atau 'CN'
  final String latestChapter;
  final String latestTime;
  final String previousChapter;
  final String previousTime;

  const Manga({
    required this.title,
    required this.coverUrl,
    required this.country,
    required this.latestChapter,
    required this.latestTime,
    required this.previousChapter,
    required this.previousTime,
  });
}

// Reusable widget: badge bendera negara
class CountryBadge extends StatelessWidget {
  final String country;

  const CountryBadge({super.key, required this.country});

  @override
  Widget build(BuildContext context) {
    final bool isKorea = country == 'KR';

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: isKorea ? Colors.white : const Color(0xFFDE2910),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        isKorea ? '🇰🇷' : '🇨🇳',
        style: const TextStyle(fontSize: 16),
      ),
    );
  }
}

// Reusable widget: tombol chapter + waktu rilis
class ChapterTile extends StatelessWidget {
  final String chapter;
  final String time;
  final VoidCallback? onTap;

  const ChapterTile({
    super.key,
    required this.chapter,
    required this.time,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(20),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF3A3A3C),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              chapter,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Colors.white70,
              ),
            ),
          ),
        ),
        const SizedBox(height: 6),
        Padding(
          padding: const EdgeInsets.only(left: 2),
          child: Text(
            time,
            style: const TextStyle(fontSize: 12, color: Colors.white38),
          ),
        ),
      ],
    );
  }
}

// Reusable widget: kartu manga
class MangaCard extends StatelessWidget {
  final Manga manga;
  final double width;

  const MangaCard({super.key, required this.manga, required this.width});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Cover + badge negara
          Stack(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: AspectRatio(
                  aspectRatio: 3 / 4.2,
                  child: Image.network(
                    manga.coverUrl,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        color: const Color(0xFF2C2C2E),
                        child: const Center(
                          child: Icon(
                            Icons.image_not_supported_outlined,
                            size: 40,
                            color: Colors.white38,
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
              Positioned(
                top: 8,
                right: 8,
                child: CountryBadge(country: manga.country),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Judul (dipotong dengan ellipsis)
          Text(
            manga.title,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w700,
              color: Colors.white70,
            ),
          ),
          const SizedBox(height: 10),

          // Chapter terbaru
          ChapterTile(
            chapter: manga.latestChapter,
            time: manga.latestTime,
          ),
          const SizedBox(height: 10),

          // Chapter sebelumnya
          ChapterTile(
            chapter: manga.previousChapter,
            time: manga.previousTime,
          ),
        ],
      ),
    );
  }
}

class MangaListPage extends StatelessWidget {
  const MangaListPage({super.key});

  static const List<Manga> _mangaList = [
    Manga(
      title: 'MookHyang: Dark Lady',
      coverUrl: 'https://picsum.photos/seed/manga1/400/560',
      country: 'KR',
      latestChapter: 'Chapter 300',
      latestTime: '21 hours ago',
      previousChapter: 'Chapter 299',
      previousTime: '15 Sep 26',
    ),
    Manga(
      title: 'It Starts With a King Account',
      coverUrl: 'https://picsum.photos/seed/manga2/400/560',
      country: 'CN',
      latestChapter: 'Chapter 337',
      latestTime: '21 hours ago',
      previousChapter: 'Chapter 336',
      previousTime: '2 days ago',
    ),
    Manga(
      title: 'Reincarnator',
      coverUrl: 'https://picsum.photos/seed/manga3/400/560',
      country: 'KR',
      latestChapter: 'Chapter 120',
      latestTime: '1 day ago',
      previousChapter: 'Chapter 119',
      previousTime: '3 days ago',
    ),
    Manga(
      title: 'Great Yuan Dynasty',
      coverUrl: 'https://picsum.photos/seed/manga4/400/560',
      country: 'CN',
      latestChapter: 'Chapter 85',
      latestTime: '2 days ago',
      previousChapter: 'Chapter 84',
      previousTime: '4 days ago',
    ),
  ];

  @override
  Widget build(BuildContext context) {
    const double horizontalPadding = 16;
    const double spacing = 16;
    final double screenWidth = MediaQuery.of(context).size.width;
    final double cardWidth =
        (screenWidth - (horizontalPadding * 2) - spacing) / 2;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'MGKOMIK',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        actions: const [
          Icon(Icons.share_outlined),
          SizedBox(width: 16),
          Icon(Icons.bookmark_border),
          SizedBox(width: 16),
          Icon(Icons.more_vert),
          SizedBox(width: 8),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(horizontalPadding),
        child: Wrap(
          spacing: spacing,
          runSpacing: 28,
          children: _mangaList
              .map((manga) => MangaCard(manga: manga, width: cardWidth))
              .toList(),
        ),
      ),
    );
  }
}
```