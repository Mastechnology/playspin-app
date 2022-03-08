import 'package:flutter/material.dart';
import 'dart:math';
//burad kutuphanelerimiz cagiriyoruz.

String dropdownValue = 'Tek Zar';
String dropdownValueOld = 'Tek Zar';
String producedValue = "Bekleniyor!";
//bunlar kullanacagimiz degiskenlerimiz.

void main() {
  runApp(MyApp()); //buradan projemizi baslatiyoruz.
}

class MyApp extends StatelessWidget{

  final _messangerKey = GlobalKey<ScaffoldMessengerState>();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        scaffoldMessengerKey: _messangerKey,

        home: Scaffold( //ekranin tumunu kapliyor bu
        appBar: AppBar( //baslik kismi burasi
          backgroundColor: Colors.blueGrey,
          centerTitle: true,
          title: Text("Playspin"),
        ),
        body: AnaEkran(), // burada ekranda olacaklari bir fonksiyona aldik.
        floatingActionButton: FloatingActionButton(
          onPressed: () { //bu buton sayesinde ekranda bilgirim nasil gosterilir onu goruyoruz.
            _messangerKey.currentState!.showSnackBar(SnackBar(content: Text('Bu uygulama mfgstudio tarafından yazılmıştır.\nDaha fazlası için mfgstudiosblog.com\'a bekleriz.', style: TextStyle(fontSize: 20, color: Colors.blueGrey))));
          },
          backgroundColor: Colors.blueGrey,
          child: const Icon(Icons.info),
        ),
      )
    );
  }
}

class AnaEkran extends StatefulWidget {
  const AnaEkran({Key? key}) : super(key: key);

  @override
  _AnaEkranState createState() => _AnaEkranState();
}

class _AnaEkranState extends State<AnaEkran> {

  @override
  Widget build(BuildContext context) {
    final ButtonStyle style = ElevatedButton.styleFrom(textStyle: const TextStyle(fontSize: 20));

    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Padding( //secim yap dedigimiz yer
            padding: const EdgeInsets.all(16.0),
            child: Text("Tür seçimi yapın:", style: TextStyle(fontSize: 12),),
          ),
          DropdownButton<String>(
            value: dropdownValue,
            icon: const Icon(Icons.arrow_downward),
            elevation: 16,
            style: const TextStyle(color: Colors.blueGrey, fontSize: 24,),
            underline: Container(
              height: 2,
              width: 7,
              color: Colors.blueGrey,
            ),
            onChanged: (String? newValue) {
              setState(() {
                dropdownValue = newValue!;
              });
            },
            items: <String>['Tek Zar', 'Çift Zar', 'Türkçe Alfabe', 'İngilizce Alfabe', '1-10', '1-50', '1-100']
                .map<DropdownMenuItem<String>>((String value) {
              return DropdownMenuItem<String>( //burada secim yaptiriyoruz dropdown'dan
                value: value,
                child: Text(value),
              );
            }).toList(),
          ),
          const SizedBox(height: 100), //bosluk birakiyoruz araya.
          Padding(
            padding: const EdgeInsets.all(1.0), //burada en son uretilen degerin ne ile alakali oldugunu gosteriyoruz.
            child: Text("$dropdownValueOld seçimi için üretilen değer:", style: TextStyle(fontSize: 16, color: Colors.blueGrey),),
          ),
          Padding( //burasi uretilen degerimizin gosterilen kismi
            padding: const EdgeInsets.all(1.0),
            child: Text("< $producedValue >", style: TextStyle(fontSize: 64, color: Colors.blueGrey),),
          ),
          const SizedBox(height: 100), //araya bosluk
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
              style: ButtonStyle( //bu buton ile yapacagiz tum islemleri
                minimumSize: MaterialStateProperty.all(const Size(250, 60)),
                textStyle: MaterialStateProperty.all(
                  const TextStyle(fontSize: 20,),
                ),
                shape: MaterialStateProperty.all(
                  RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
              onPressed: () {
                setState(() {
                  dropdownValueOld = dropdownValue;
                  //burada yaptigi secime gore ekrana farkli deger gonderecegiz.
                  if (dropdownValue == "Tek Zar") {
                    producedValue = (Random().nextInt(6) + 1).toString();
                  }
                  else if (dropdownValue == "Çift Zar") {
                    int zar1 = Random().nextInt(6) + 1;
                    int zar2 = Random().nextInt(6) + 1;
                    String sonuc = "$zar1 > < $zar2";
                    producedValue = sonuc;
                  }
                  else if (dropdownValue == "Türkçe Alfabe"){
                    var turkishAlphabet = ['A','B','C','Ç','D','E','F','G','Ğ','H','I','İ','J','K','L','M','N','O','Ö','P','R','S','Ş','T','U','Ü','V','Y','Z'];
                    int rand = Random().nextInt(turkishAlphabet.length-1);
                    producedValue = turkishAlphabet[rand];
                  }
                  else if (dropdownValue == "İngilizce Alfabe"){
                    var englishAlphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
                    int rand = Random().nextInt(englishAlphabet.length-1);
                    producedValue = englishAlphabet[rand];
                  }
                  else if (dropdownValue == "1-10") {
                    producedValue = (Random().nextInt(10) + 1).toString();
                  }
                  else if (dropdownValue == "1-50") {
                    producedValue = (Random().nextInt(50) + 1).toString();
                  }
                  else if (dropdownValue == "1-100") {
                    producedValue = (Random().nextInt(100) + 1).toString();
                  }
                  //genel olarak basit zaten anlatacak bisey bulamadim iceride.
                });
              },
              child: const Text('Yeni değer üret!'), //buton ismi de boyle.
            ),
          ),
        ],
      ),
    );
  }
}
