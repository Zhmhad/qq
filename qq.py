import 'package:flutter/material.dart';

void main() => runApp(const KomikApp());

class KomikApp extends StatelessWidget {
  const KomikApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF222222),
      ),
      home: const KomikPage(),
    );
  }
}

class KomikItem {
  final String title;
  final String flag;
  final List<Color> colors;
  final String latestChapter;
  final String latestTime;
  final String previousChapter;
  final String previousTime;

  const KomikItem({
    required this.title,
    required this.flag,
    required this.colors,
    required this.latestChapter,
    required this.latestTime,
    required this.previousChapter,
    required this.previousTime,
  });
}

class KomikPage extends StatelessWidget {
  const KomikPage({super.key});

  static const List<KomikItem> items = [
    KomikItem(
      title: 'MookHyang: Darklady',
      flag: '🇰🇷',
      colors: [Color(0xFFE8D9A8), Color(0xFF6A4A7C), Color(0xFF2A1F3D)],
      latestChapter: 'Chapter 300',
      latestTime: '21 hours ago',
      previousChapter: 'Chapter 299',
      previousTime: '15 Sep 26',
    ),
    KomikItem(
      title: 'It Starts With a King Account',
      flag: '🇨🇳',
      colors: [Color(0xFF3B5BA8), Color(0xFFE6A23C), Color(0xFF1B1B3A)],
      latestChapter: 'Chapter 337',
      latestTime: '21 hours ago',
      previousChapter: 'Chapter 336',
      previousTime: '2 days ago',
    ),
    KomikItem(
      title: 'Reincarnator',
      flag: '🇰🇷',
      colors: [Color(0xFF8A4FFF), Color(0xFF3A1F6B), Color(0xFF14102B)],
      latestChapter: 'Chapter 120',
      latestTime: '1 day ago',
      previousChapter: 'Chapter 119',
      previousTime: '3 days ago',
    ),
    KomikItem(
      title: 'Great Ancestor',
      flag: '🇨🇳',
      colors: [Color(0xFFBFD3E0), Color(0xFF3C4A8A), Color(0xFF14142B)],
      latestChapter: 'Chapter 88',
      latestTime: '2 days ago',
      previousChapter: 'Chapter 87',
      previousTime: '4 days ago',
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const BrowserBar(),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: items.length,
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 20,
          childAspectRatio: 0.45,
        ),
        itemBuilder: (context, index) => KomikCard(item: items[index]),
      ),
    );
  }
}

class BrowserBar extends StatelessWidget implements PreferredSizeWidget {
  const BrowserBar({super.key});

  @override
  Size get preferredSize => const Size.fromHeight(64);

  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFF1F2023),
      child: SafeArea(
        bottom: false,
        child: SizedBox(
          height: 64,
          child: Row(
            children: [
              IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () {},
              ),
              IconButton(
                icon: const Icon(Icons.keyboard_arrow_down,
                    color: Colors.white, size: 32),
                onPressed: () {},
              ),
              const Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'MGKOMIK | ...',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Text(
                      'id.mgkomik.cc',
                      style: TextStyle(color: Colors.white70, fontSize: 13),
                    ),
                  ],
                ),
              ),
              IconButton(
                icon: const Icon(Icons.share_outlined, color: Colors.white),
                onPressed: () {},
              ),
              IconButton(
                icon: const Icon(Icons.bookmark_border, color: Colors.white),
                onPressed: () {},
              ),
              IconButton(
                icon: const Icon(Icons.more_vert, color: Colors.white),
                onPressed: () {},
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class KomikCard extends StatelessWidget {
  final KomikItem item;

  const KomikCard({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AspectRatio(
          aspectRatio: 0.6,
          child: Stack(
            children: [
              Positioned.fill(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: item.colors,
                    ),
                  ),
                  alignment: Alignment.bottomLeft,
                  padding: const EdgeInsets.all(12),
                  child: Text(
                    item.title,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                ),
              ),
              Positioned(
                top: 10,
                right: 10,
                child: Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(item.flag, style: const TextStyle(fontSize: 18)),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        Text(
          item.title,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 10),
        ChapterRow(chapter: item.latestChapter, time: item.latestTime),
        const SizedBox(height: 10),
        ChapterRow(chapter: item.previousChapter, time: item.previousTime),
      ],
    );
  }
}

class ChapterRow extends StatelessWidget {
  final String chapter;
  final String time;

  const ChapterRow({super.key, required this.chapter, required this.time});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFF3A3A3C),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            chapter,
            style: const TextStyle(
              color: Colors.white70,
              fontSize: 16,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          time,
          style: const TextStyle(color: Colors.white38, fontSize: 15),
        ),
      ],
    );
  }
}
