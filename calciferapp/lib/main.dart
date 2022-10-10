import 'dart:convert';
import 'package:flutter/material.dart';

import 'package:http/http.dart' as http;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

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

class Image1 extends StatefulWidget {
  @override
  State<Image1> createState() => _Image1State();
}

class _Image1State extends State<Image1> {
  bool detected = false;
  Stream<String> fetchFirstCam() async* {
    while (true) {
      var result = await http
          .get(Uri.parse("http://192.168.0.204:5000/get_first_camera"));
      await Future.delayed(const Duration(milliseconds: 500));
      yield jsonDecode(result.body)['detected'].toString();
      setState(() {
        detected = jsonDecode(result.body)['detected'].toString() == 'True'
            ? true
            : false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<String>(
      stream: fetchFirstCam(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return SizedBox(
            child: detected
                ? Card(
                    color: Colors.yellow[700],
                    child: ListTile(
                      title: const Text(
                        "위험이 감지되었습니다.",
                        textScaleFactor: 1.5,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              'http://192.168.0.204:5000/',
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  )
                : Card(
                    color: Colors.white,
                    child: ListTile(
                      title: const Text(
                        "감지된 위험이 없습니다.",
                        textScaleFactor: 1.0,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              'http://192.168.0.204:5000/',
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
          );
        }
        return SizedBox(
          child: Card(
            color: Colors.grey[400],
            child: const ListTile(
              title: Text(
                "아직 카메라 1이 켜지지 않은 것 같습니다.",
                textScaleFactor: 1.0,
              ),
            ),
          ),
        );
      },
    );
  }
}

class Image2 extends StatefulWidget {
  @override
  State<Image2> createState() => _Image2State();
}

class _Image2State extends State<Image2> {
  bool detected = false;
  Stream<String> fetchFirstCam() async* {
    while (true) {
      var result = await http
          .get(Uri.parse("http://192.168.0.204:5000/get_first_camera"));
      await Future.delayed(const Duration(milliseconds: 500));
      yield jsonDecode(result.body)['detected'].toString();
      setState(() {
        detected = jsonDecode(result.body)['detected'].toString() == 'True'
            ? true
            : false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<String>(
      stream: fetchFirstCam(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return SizedBox(
            child: detected
                ? Card(
                    color: Colors.yellow[700],
                    child: ListTile(
                      title: const Text(
                        "주변에서 위험이 감지되었습니다.",
                        textScaleFactor: 1.5,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              'http://192.168.0.204:5000',
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  )
                : Card(
                    color: Colors.white,
                    child: ListTile(
                      title: const Text(
                        "주변에 감지된 위험이 없습니다.",
                        textScaleFactor: 1.5,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              'http://192.168.0.204:5000',
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
          );
        }
        return SizedBox(
          child: Card(
            color: Colors.grey[400],
            child: const ListTile(
              title: Text(
                "아직 카메라 2가 켜지지 않은 것 같습니다.",
                textScaleFactor: 1.5,
              ),
            ),
          ),
        );
      },
    );
  }
}

class Scene1 extends StatefulWidget {
  @override
  State<Scene1> createState() => _Scene1State();
}

class _Scene1State extends State<Scene1> {
  bool detected = false;
  String scene = "None";
  Stream<String> fetchFirstCam() async* {
    while (true) {
      var result = await http
          .get(Uri.parse("http://192.168.0.204:5000/get_first_camera"));
      await Future.delayed(const Duration(milliseconds: 500));
      yield jsonDecode(result.body)['detected'].toString();
      setState(() {
        detected = jsonDecode(result.body)['detected'].toString() == 'True'
            ? true
            : false;
      });
      if (detected) {
        var sceneUri =
            await http.get(Uri.parse("http://192.168.0.204:5000/scene"));
        await Future.delayed(const Duration(milliseconds: 500));
        yield jsonDecode(sceneUri.body)['gifs'].toString();
        setState(() {
          scene = jsonDecode(sceneUri.body)['gifs'].toString();
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<String>(
      stream: fetchFirstCam(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return SizedBox(
            child: detected
                ? Card(
                    color: Colors.white,
                    child: ListTile(
                      title: const Text(
                        "지난 여행의 풍경을 확인해 보세요.",
                        textScaleFactor: 1.0,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              scene,
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  )
                : Card(
                    color: Colors.grey[400],
                    child: ListTile(
                      title: const Text(
                        "아직 저장된 풍경이 없어요.",
                        textScaleFactor: 1.0,
                      ),
                      subtitle: Column(
                        children: [
                          Card(
                            child: Image.network(
                              'http://192.168.0.204:5000',
                              width: 640,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
          );
        }
        return SizedBox(
          child: Card(
            color: Colors.grey[400],
            child: const ListTile(
              title: Text(
                "아직 저장된 풍경이 없어요.",
                textScaleFactor: 1.5,
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
            // Scene1(),
            // Scene2(),
            // Scene3(),
            // Scene4(),
            Image1(),
            // Image2(),
          ],
        ),
      ),
    );
  }
}
