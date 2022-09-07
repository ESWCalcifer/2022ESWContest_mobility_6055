// File generated by FlutterFire CLI.
// ignore_for_file: lines_longer_than_80_chars, avoid_classes_with_only_static_members
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Default [FirebaseOptions] for use with your Firebase apps.
///
/// Example:
/// ```dart
/// import 'firebase_options.dart';
/// // ...
/// await Firebase.initializeApp(
///   options: DefaultFirebaseOptions.currentPlatform,
/// );
/// ```
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return web;
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      case TargetPlatform.macOS:
        return macos;
      case TargetPlatform.windows:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for windows - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      case TargetPlatform.linux:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for linux - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not supported for this platform.',
        );
    }
  }

  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'AIzaSyDNiV9Mjff91LB4KvpeInFJ71btCuEqghM',
    appId: '1:117390220505:web:8987b7053ce978980172c8',
    messagingSenderId: '117390220505',
    projectId: 'calcifer-react',
    authDomain: 'calcifer-react.firebaseapp.com',
    databaseURL: 'https://calcifer-react-default-rtdb.firebaseio.com',
    storageBucket: 'calcifer-react.appspot.com',
    measurementId: 'G-VKYZWYCKE2',
  );

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyCQoppNITyFv7fof9qvxXMnOua82adzv4U',
    appId: '1:117390220505:android:0d3f5a9dba4ed4560172c8',
    messagingSenderId: '117390220505',
    projectId: 'calcifer-react',
    databaseURL: 'https://calcifer-react-default-rtdb.firebaseio.com',
    storageBucket: 'calcifer-react.appspot.com',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'AIzaSyDpsXGwTgEy7IRLshH9B1l50r9Tc66GYTc',
    appId: '1:117390220505:ios:5cd859be03ca7ec60172c8',
    messagingSenderId: '117390220505',
    projectId: 'calcifer-react',
    databaseURL: 'https://calcifer-react-default-rtdb.firebaseio.com',
    storageBucket: 'calcifer-react.appspot.com',
    iosClientId: '117390220505-o30ubjajj44mkkdkji4f5ac2jkuni6ka.apps.googleusercontent.com',
    iosBundleId: 'com.example.calciferapp',
  );

  static const FirebaseOptions macos = FirebaseOptions(
    apiKey: 'AIzaSyDpsXGwTgEy7IRLshH9B1l50r9Tc66GYTc',
    appId: '1:117390220505:ios:5cd859be03ca7ec60172c8',
    messagingSenderId: '117390220505',
    projectId: 'calcifer-react',
    databaseURL: 'https://calcifer-react-default-rtdb.firebaseio.com',
    storageBucket: 'calcifer-react.appspot.com',
    iosClientId: '117390220505-o30ubjajj44mkkdkji4f5ac2jkuni6ka.apps.googleusercontent.com',
    iosBundleId: 'com.example.calciferapp',
  );
}
