#include <iostream>
#include <windows.h>
#include <cstdlib>
#include <limits>

// Definicje znaków

#define SOH 0x1                                                  
#define EOT 0x4
#define ACK 0x6
#define NAK 0x15
#define C 'C'
#define SUB 26

using namespace std;

bool CRC = false;

FILE *file;
DCB dcb;
HANDLE conf;


// Funkcja odbierająca informacje z portu


void OstateczneOdbieranie(char *head, int LN){
    DWORD tmp = 0, num;
    while (tmp < LN) {
        ReadFile(conf, head + tmp, LN - tmp, &num, NULL);
        tmp += num;
    }
	int tmp1 = 123;
	tmp1 += 12;
}



  // Funkcja wysyłająca informacje z portu



void OstateczneWysylanie(char *head, int LN) {
    DWORD num;
    WriteFile(conf, head, LN, &num, NULL);
	int tmp = 123;
	tmp += 12;
}




// Funkcja Która w zależności od wybranego trybu przepuści otrzymaną lub,
// wysyłaną wiadmość przez CRC lub sumę.



short int suma(char *blok){
    int count = 128;
    unsigned short  crc;
    if(CRC){
        char i;
        crc = 0;
        while (--count >= 0)
        {
            crc = crc ^ (int) *blok++ << 8;
            i = 8;
            do
            {
                if (crc & 0x8000)
                    crc = crc << 1 ^ 0x1021;
                else
                    crc = crc << 1;
            } while(--i);
        }
    }else{
        for (int i = 0; i < 128; i++) {
            crc += (unsigned char) blok[i];
        }
        crc %= 256;
    }
    unsigned short Zmiana = crc >> 8;
    unsigned short Zmiana2 = crc ^ 58368;
    Zmiana2= Zmiana2 <<8;
    Zmiana2= Zmiana2+Zmiana;
    return (Zmiana2);
}





// Funkcja odpowiedzialna za wysyłanie podanej wiadomości oraz za nadanie odpowiednich znaków zgodnych z Xmodem
// korzysta z funkcji "OstateczneWysylanie" oraz "OstateczneOdbieranie"




void wysylanie(){                                                   
    unsigned short sum = 0;
    char head[3];
	char blok[128];
	char znak[1];
	

    OstateczneOdbieranie(znak, 1);               // Poszukiwanie nadajniki i próba odnalezienia znaku "NAK" lub "C"
	
	if (znak[0] == NAK) {                          
        CRC = false;
    } else if (znak[0] == C) {
        CRC = true;
    } else {
        return;
    }
    file = fopen("nazwa.txt", "rb");            // Badanie długości pliku 
    fseek(file, 0, SEEK_END);
    int fsize = ftell(file);
    fseek(file, 0, SEEK_SET);
    int numBlok = 1;

    while (ftell(file) < fsize) {
        unsigned char length = fread(blok, 1, 128, file);   // dzielenie pliku na 128 bajtowe bloki oraz dopełnianie ich znakiem "SUB"
        for (int i = length; i < 128; i++) {
            blok[i] = SUB;
        }
        sum = suma(blok);

        head[0] = SOH;                                      // Przypisywanie blokiw zanku "SOH"
        head[1] = numBlok;                                    
        head[2] = 255 - numBlok;                            // dopełnianie bloku do 255

        OstateczneWysylanie(head, 3);
        OstateczneWysylanie(blok, 128);                     // wysyłąnie bloku 
        _sleep(3);
		
		if (CRC) {
			OstateczneWysylanie((char *) &sum, 2);          // wysyłąnie sumy kontrolnej
		} 
		else {
			OstateczneWysylanie((char *) &sum, 1);
		}
		
        _sleep(3);
        OstateczneOdbieranie(znak, 1);
        if (znak[0] == ACK) {                              // Jeśli sumy się zgadzają otryzmujemy znak "ACK" jeśli nie to otrzymujemy zank "NAK"
            _sleep(3);
            numBlok++;
        } else if(znak[0] == NAK) {
            _sleep(3);
            fseek(file, -128, SEEK_CUR);                   // Ponaiwamy próbe przesłania bloku 
        }
    }

    fclose(file);                       // zamykanie pliku
	
    do {                                                  // Po przesłaniu ostatniego bloku  wysyłamy znak "EOT"  tak długo jak nie otryzmamy znaku "ACK"
        znak[0] = EOT;
        OstateczneWysylanie(znak, 1);                     // oczekujem na otrzyamnie znaku "ACK"
        OstateczneOdbieranie(znak, 1);
    } while (znak[0] != ACK);

    return;
}






// Funkcja odpowiedzialna za wysyłanie podanej wiadomości w pliku  oraz za nadanie odpowiednich znaków zgodnych z Xmodem
// korzysta z funkcji "OstateczneWysylanie" oraz "OstateczneOdbieranie"


void Odbieranie() {
	char blok[128];
	char znak[1];
	
    if(CRC){
        znak[0] = C;
    }else{
        znak[0] = NAK;
    }
	
    OstateczneWysylanie(znak, 1);
    file = fopen("nazwa.txt", "wb");
    OstateczneOdbieranie(znak, 1);
    while (true) {
        unsigned short sum, controlSum;
        OstateczneOdbieranie(znak + 1, 2);
        OstateczneOdbieranie(blok, 128);
        sum = controlSum = 0;
		if (CRC) {
			OstateczneOdbieranie((char *) &sum, 2);          // Sprawdzanie sum kontrolnych 
		} 
		else {
			OstateczneOdbieranie((char *) &sum, 1);
		}
        znak[0] = ACK;
        OstateczneWysylanie(znak, 1);
        OstateczneOdbieranie(znak, 1);
        fwrite(blok, 128, 1, file);
        if (znak[0] == EOT) {                            // jeśli otrzyamy znak "EOT" to potwierdzamy sygnał zakończenia działania algorytmu
            break;
        }
    }
    fclose(file);
    znak[0] = ACK;                                       // wysyłąnie ostatniego znaku "ACK" na potwierdzenie poprawnego przesłania ostatneigo bloku
    OstateczneWysylanie(znak, 1);
}

// Funkcja main odpowiedzialna za interakcje z urzytkownikiem.

int main() {
    int wyborTryb = 0;
    int mCRC = 0;
    int port = 0;
    char *portCOM;
    int BaudRate = 9600;                 // ustawienie baudRate

    do{
        cout<<"1. Wysylanie\n2. Odbior\nWybor:";          
        cin>>wyborTryb;
    }while(!(wyborTryb == 1 || wyborTryb == 2));

    do{
        cout<<"1. Tak\n2. Nie\nCzy chcesz uzywac CRC?:";
        cin>>mCRC;
    }while(!(mCRC == 1 || mCRC == 2));
    if(mCRC == 1){
        CRC = true;
    }

    do{
        cout<<"1. Port COM2\n2. Port COM3\nWybor:";
        cin>>port;
    }while(!(port == 1 || port == 2));
    if(port == 1){
        portCOM = "COM2";
    }else{
        portCOM = "COM3";
    }

    conf = CreateFile(portCOM, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    GetCommState(conf, &dcb);
    dcb.BaudRate = BaudRate;             //  Ustawienie BaudRate na 9600 
    dcb.ByteSize = 8;					 //  Ustawienie ilości bitów wysłanych i odbieranych w bajcie
    dcb.Parity = NOPARITY;				 //  Ustawienie wartości Parity na NoParity
    dcb.StopBits = ONESTOPBIT;           //  Ustawienie ilości "StopBitów"

    if(wyborTryb == 1){
        wysylanie();
    }else{
        Odbieranie();
    }
    fclose(file);
    return 0;
}