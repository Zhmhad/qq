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

// Reusable widget: badge bendera negara (digambar manual agar tampil di Windows)
class CountryBadge extends StatelessWidget {
  final String country;

  const CountryBadge({super.key, required this.country});

  @override
  Widget build(BuildContext context) {
    final bool isKorea = country == 'KR';

    return Container(
      width: 34,
      height: 22,
      decoration: BoxDecoration(
        color: isKorea ? Colors.white : const Color(0xFFDE2910),
        borderRadius: BorderRadius.circular(5),
      ),
      alignment: Alignment.center,
      child: isKorea
          ? ClipOval(
              child: SizedBox(
                width: 14,
                height: 14,
                child: Column(
                  children: [
                    Expanded(child: Container(color: const Color(0xFFCD2E3A))),
                    Expanded(child: Container(color: const Color(0xFF0047A0))),
                  ],
                ),
              ),
            )
          : const Align(
              alignment: Alignment.topLeft,
              child: Padding(
                padding: EdgeInsets.only(left: 3, top: 1),
                child: Icon(Icons.star, size: 11, color: Color(0xFFFFDE00)),
              ),
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
          borderRadius: BorderRadius.circular(14),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: const Color(0xFF3A3A3C),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              chapter,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: Colors.white70,
              ),
            ),
          ),
        ),
        const SizedBox(height: 3),
        Padding(
          padding: const EdgeInsets.only(left: 2),
          child: Text(
            time,
            style: const TextStyle(fontSize: 11, color: Colors.white38),
          ),
        ),
      ],
    );
  }
}

// Reusable widget: kartu manga
class MangaCard extends StatelessWidget {
  final Manga manga;

  const MangaCard({super.key, required this.manga});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Cover + badge negara
        Expanded(
          child: Stack(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: SizedBox.expand(
                  child: Image.network(
                    manga.coverUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        color: const Color(0xFF2C2C2E),
                        child: const Center(
                          child: Icon(
                            Icons.image_not_supported_outlined,
                            size: 32,
                            color: Colors.white38,
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
              Positioned(
                top: 6,
                right: 6,
                child: CountryBadge(country: manga.country),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),

        // Judul
        Text(
          manga.title,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w700,
            color: Colors.white70,
          ),
        ),
        const SizedBox(height: 6),

        // Chapter terbaru
        ChapterTile(
          chapter: manga.latestChapter,
          time: manga.latestTime,
        ),
        const SizedBox(height: 6),

        // Chapter sebelumnya
        ChapterTile(
          chapter: manga.previousChapter,
          time: manga.previousTime,
        ),
      ],
    );
  }
}

class MangaListPage extends StatefulWidget {
  const MangaListPage({super.key});

  @override
  State<MangaListPage> createState() => _MangaListPageState();
}

class _MangaListPageState extends State<MangaListPage> {
  final ScrollController _scrollController = ScrollController();

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
    Manga(
      title: 'Solo Max-Level Newbie',
      coverUrl: 'https://picsum.photos/seed/manga5/400/560',
      country: 'KR',
      latestChapter: 'Chapter 210',
      latestTime: '3 days ago',
      previousChapter: 'Chapter 209',
      previousTime: '20 Sep 26',
    ),
    Manga(
      title: 'Martial Peak Legacy',
      coverUrl: 'https://picsum.photos/seed/manga6/400/560',
      country: 'CN',
      latestChapter: 'Chapter 512',
      latestTime: '4 days ago',
      previousChapter: 'Chapter 511',
      previousTime: '25 Sep 26',
    ),
    Manga(
      title: 'The Beginning After The End',
      coverUrl: 'https://picsum.photos/seed/manga7/400/560',
      country: 'KR',
      latestChapter: 'Chapter 188',
      latestTime: '5 days ago',
      previousChapter: 'Chapter 187',
      previousTime: '22 Sep 26',
    ),
    Manga(
      title: 'Battle Through Heavens',
      coverUrl: 'https://picsum.photos/seed/manga8/400/560',
      country: 'CN',
      latestChapter: 'Chapter 420',
      latestTime: '6 days ago',
      previousChapter: 'Chapter 419',
      previousTime: '21 Sep 26',
    ),
  ];

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToTop() {
    _scrollController.animateTo(
      0,
      duration: const Duration(milliseconds: 400),
      curve: Curves.easeOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const Icon(Icons.close),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'MGKOMIK | ...',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            Text(
              'id.mgkomik.cc',
              style: TextStyle(fontSize: 11, color: Colors.white54),
            ),
          ],
        ),
        actions: const [
          Icon(Icons.share_outlined),
          SizedBox(width: 16),
          Icon(Icons.bookmark_border),
          SizedBox(width: 16),
          Icon(Icons.more_vert),
          SizedBox(width: 12),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1100),
          child: GridView.builder(
            controller: _scrollController,
            padding: const EdgeInsets.all(16),
            itemCount: _mangaList.length,
            gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
              maxCrossAxisExtent: 190,
              mainAxisExtent: 360,
              crossAxisSpacing: 16,
              mainAxisSpacing: 20,
            ),
            itemBuilder: (context, index) {
              return MangaCard(manga: _mangaList[index]);
            },
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.small(
        onPressed: _scrollToTop,
        backgroundColor: const Color(0xFF3A3A3C),
        foregroundColor: Colors.white,
        child: const Icon(Icons.arrow_upward),
      ),
    );
  }
}
```