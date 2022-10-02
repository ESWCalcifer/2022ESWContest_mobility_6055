import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'firebase_options.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_flutter_web/webview_flutter_web.dart';

void main() async {
  WebView.platform = WebWebViewPlatform();
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

FirebaseFirestore firestore = FirebaseFirestore.instance;

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calcifer',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
      ),
      home: const MyHomePage(title: '쓰담'),
    );
  }
}

class Image1 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      child: Card(
        child: ListTile(
          title: const Text(
            "주변의 위험을 확인해보세요",
            textScaleFactor: 1.5,
          ),
          subtitle: Card(
            child: Image.network(
              'http://192.168.0.6:5000',
              width: 640,
            ),
          ),
        ),
      ),
    );
  }
}

class COInformation extends StatefulWidget {
  @override
  _COInformationState createState() => _COInformationState();
}

class _COInformationState extends State<COInformation> {
  final Stream<QuerySnapshot> _usersStream =
      FirebaseFirestore.instance.collection('co_ppm').snapshots();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot>(
      stream: _usersStream,
      builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.hasError) {
          return const Text('Something went wrong');
        }

        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Text("Loading");
        }

        return SizedBox(
          height: 120,
          child: Card(
            child: ListTile(
              title: const Text(
                "현재 차량 내 일산화탄소 농도",
                textScaleFactor: 1.5,
              ),
              subtitle: ListView(
                children: snapshot.data!.docs.map(
                  (DocumentSnapshot document) {
                    Map<dynamic, dynamic> data =
                        document.data()! as Map<dynamic, dynamic>;
                    return Card(
                      child: ListTile(
                        title: Text(
                          data['ppm'] + "ppm",
                          textScaleFactor: 1.5,
                        ),
                      ),
                    );
                  },
                ).toList(),
              ),
            ),
          ),
        );
      },
    );
  }
}

class VideosInformation extends StatefulWidget {
  @override
  _VideosInformationState createState() => _VideosInformationState();
}

class _VideosInformationState extends State<VideosInformation> {
  final Stream<QuerySnapshot> _usersStream =
      FirebaseFirestore.instance.collection('video').snapshots();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot>(
      stream: _usersStream,
      builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.hasError) {
          return const Text('Something went wrong');
        }

        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Text("Loading");
        }

        return SizedBox(
          height: 200,
          child: Card(
            child: ListTile(
              title: const Text(
                "지난 여행의 풍경들을 확인해 보세요.",
                textScaleFactor: 1.5,
              ),
              subtitle: ListView(
                children: snapshot.data!.docs.map(
                  (DocumentSnapshot document) {
                    Map<dynamic, dynamic> data =
                        document.data()! as Map<dynamic, dynamic>;
                    return Card(
                      child: ListTile(
                        title: Text(data['video_date']),
                        subtitle: Text(data['video_url']),
                      ),
                    );
                  },
                ).toList(),
              ),
            ),
          ),
        );
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            VideosInformation(),
            COInformation(),
            Image1(),
          ],
        ),
      ),
    );
  }
}
