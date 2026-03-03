🔐 XORLocker v2 - أداة تشفير الملفات
<div align="center">

English | العربية | Français

https://img.shields.io/badge/version-2.0-blue
https://img.shields.io/badge/license-MIT-green
https://img.shields.io/badge/python-3.8+-yellow
</div>

<a name="english"></a>
📘 English
Overview

XORLocker v2 is a powerful file encryption tool with a user-friendly GUI interface. It allows you to encrypt files on fixed drives and USB flash drives using multiple encryption algorithms.
✨ Features

    🖥️ User-friendly GUI interface

    💾 Support for all drive types (Fixed, USB, External)

    🔐 Multiple encryption algorithms: MD5, SHA-1, SHA-256, AES-256

    🔑 Secure password system with encrypted storage

    📁 File encryption using XOR + Base64

    🔍 Automatic detection of encrypted files

    📊 File and drive statistics

    🚀 Portable version - no installation required

    🖱️ Drag & Drop support

    ⚡ Fast encryption mode

    🌐 Multi-language support (Arabic, English, French)

🛠️ Requirements

    Windows 7/8/10/11

    Python 3.8+ (optional - portable version available)

    Required libraries:

        psutil (for drive management)

        pycryptodome (for AES encryption)

        tkinterdnd2 (for Drag & Drop)

📥 Installation
Quick Install
bash

# Clone repository
git clone https://github.com/Liptoid/XORLockerv2.git
cd XORLockerv2

# Install requirements
pip install -r requirements.txt

# Run the program
python xorlocker.py

Portable Version

    Download the latest release

    Extract to any folder

    Run XORLocker.exe

🚀 How to Use
1️⃣ Encrypt Files

    Run XORLocker.exe or python xorlocker.py

    Select drives from the list or drag & drop files

    Enter password (min 4 characters)

    Choose encryption type (MD5, SHA-1, SHA-256, AES-256)

    Click "🔒 Encrypt Files & Save Password"

    Confirm - all files will be encrypted

2️⃣ Decrypt Files

    Run the program again

    It will automatically detect pass.ded file

    Enter your password

    Click "🔓 Decrypt"

📁 File Structure
text

XORLockerv2/
│
├── 📄 xorlocker.py          # Main program
├── 📄 run.bat               # Quick launcher
├── 📄 requirements.txt      # Dependencies
├── 📄 README.md             # This file
├── 📄 CHANGELOG.md          # Version history
│
├── 📁 docs/                  # Documentation
└── 📁 examples/              # Example files

🔒 Security Features

    ✅ Password stored as SHA-256 hash

    ✅ pass.ded file automatically hidden in Windows

    ✅ Multi-layer encryption (XOR + Base64 + AES)

    ✅ Automatic system file skipping

    ✅ Backup creation before encryption

👨‍💻 Developer

    Main Developer: LIPTOID

    Email: iotclol313@gmail.com

    GitHub: https://github.com/Liptoid

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<a name="arabic"></a>
📘 العربية
نظرة عامة

XORLocker v2 هي أداة قوية لتشفير الملفات بواجهة رسومية سهلة الاستخدام. تتيح لك تشفير الملفات على الأقراص الثابتة والفلاشات USB باستخدام خوارزميات تشفير متعددة.
✨ المميزات

    🖥️ واجهة رسومية سهلة الاستخدام

    💾 دعم جميع أنواع الأقراص (ثابتة، USB، خارجية)

    🔐 خوارزميات تشفير متعددة: MD5, SHA-1, SHA-256, AES-256

    🔑 نظام كلمات مرور آمن مع تخزين مشفر

    📁 تشفير الملفات باستخدام XOR + Base64

    🔍 كشف تلقائي للملفات المشفرة

    📊 إحصائيات الملفات والأقراص

    🚀 نسخة محمولة - بدون تثبيت

    🖱️ دعم السحب والإفلات

    ⚡ وضع التشفير السريع

    🌐 دعم لغات متعددة (عربية، إنجليزية، فرنسية)

🛠️ المتطلبات

    نظام Windows 7/8/10/11

    Python 3.8+ (اختياري - توجد نسخة محمولة)

    المكتبات المطلوبة:

        psutil (لإدارة الأقراص)

        pycryptodome (لتشفير AES)

        tkinterdnd2 (للسحب والإفلات)

📥 التثبيت
تثبيت سريع
bash

# نسخ المستودع
git clone https://github.com/Liptoid/XORLockerv2.git
cd XORLockerv2

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل البرنامج
python xorlocker.py

النسخة المحمولة

    حمل أحدث إصدار

    فك الضغط في أي مجلد

    شغل XORLocker.exe

🚀 طريقة الاستخدام
1️⃣ تشفير الملفات

    شغل XORLocker.exe أو python xorlocker.py

    اختر الأقراص من القائمة أو اسحب وأفلت الملفات

    أدخل كلمة المرور (4 أحرف على الأقل)

    اختر نوع التشفير (MD5, SHA-1, SHA-256, AES-256)

    اضغط "🔒 تشفير الملفات وحفظ كلمة المرور"

    أكد - سيتم تشفير جميع الملفات

2️⃣ فك التشفير

    شغل البرنامج مرة أخرى

    سيكتشف تلقائياً ملف pass.ded

    أدخل كلمة المرور

    اضغط "🔓 فك التشفير"

📁 هيكل الملفات
text

XORLockerv2/
│
├── 📄 xorlocker.py          # البرنامج الرئيسي
├── 📄 run.bat               # مشغل سريع
├── 📄 requirements.txt      # المتطلبات
├── 📄 README.md             # هذا الملف
├── 📄 CHANGELOG.md          # سجل التغييرات
│
├── 📁 docs/                  # وثائق
└── 📁 examples/              # ملفات أمثلة

🔒 مميزات أمنية

    ✅ كلمة المرور مخزنة بصيغة Hash (SHA-256)

    ✅ ملف pass.ded مخفي تلقائياً في Windows

    ✅ تشفير متعدد الطبقات (XOR + Base64 + AES)

    ✅ تخطي الملفات النظامية تلقائياً

    ✅ إنشاء نسخة احتياطية قبل التشفير

👨‍💻 المطور

    المطور الرئيسي: LIPTOID

    البريد الإلكتروني: iotclol313@gmail.com

    الموقع: https://github.com/Liptoid

📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف LICENSE للتفاصيل

<a name="french"></a>
📘 Français
Aperçu

XORLocker v2 est un outil puissant de cryptage de fichiers avec une interface graphique conviviale. Il vous permet de crypter des fichiers sur les disques fixes et les clés USB en utilisant plusieurs algorithmes de cryptage.
✨ Fonctionnalités

    🖥️ Interface graphique intuitive

    💾 Support de tous types de disques (fixes, USB, externes)

    🔐 Algorithmes de cryptage multiples : MD5, SHA-1, SHA-256, AES-256

    🔑 Système de mots de passe sécurisé avec stockage crypté

    📁 Cryptage de fichiers avec XOR + Base64

    🔍 Détection automatique des fichiers cryptés

    📊 Statistiques des fichiers et disques

    🚀 Version portable - sans installation

    🖱️ Support du glisser-déposer

    ⚡ Mode cryptage rapide

    🌐 Support multilingue (Arabe, Anglais, Français)

🛠️ Prérequis

    Windows 7/8/10/11

    Python 3.8+ (optionnel - version portable disponible)

    Bibliothèques requises :

        psutil (gestion des disques)

        pycryptodome (cryptage AES)

        tkinterdnd2 (glisser-déposer)

📥 Installation
Installation Rapide
bash

# Cloner le dépôt
git clone https://github.com/Liptoid/XORLockerv2.git
cd XORLockerv2

# Installer les dépendances
pip install -r requirements.txt

# Lancer le programme
python xorlocker.py

Version Portable

    Téléchargez la dernière version

    Extrayez dans n'importe quel dossier

    Lancez XORLocker.exe

🚀 Utilisation
1️⃣ Crypter des Fichiers

    Lancez XORLocker.exe ou python xorlocker.py

    Sélectionnez les disques ou glissez-déposez des fichiers

    Entrez le mot de passe (min 4 caractères)

    Choisissez le type de cryptage (MD5, SHA-1, SHA-256, AES-256)

    Cliquez sur "🔒 Crypter et sauvegarder"

    Confirmez - tous les fichiers seront cryptés

2️⃣ Décrypter

    Relancez le programme

    Détection automatique du fichier pass.ded

    Entrez votre mot de passe

    Cliquez sur "🔓 Décrypter"

📁 Structure des Fichiers
text

XORLockerv2/
│
├── 📄 xorlocker.py          # Programme principal
├── 📄 run.bat               # Lanceur rapide
├── 📄 requirements.txt      # Dépendances
├── 📄 README.md             # Ce fichier
├── 📄 CHANGELOG.md          # Historique
│
├── 📁 docs/                  # Documentation
└── 📁 examples/              # Exemples

🔒 Sécurité

    ✅ Mot de passe stocké en hash SHA-256

    ✅ Fichier pass.ded caché automatiquement

    ✅ Cryptage multi-couches (XOR + Base64 + AES)

    ✅ Ignore automatiquement les fichiers système

    ✅ Sauvegarde avant cryptage

👨‍💻 Développeur

    Développeur principal : LIPTOID

    Email : iotclol313@gmail.com

    GitHub : https://github.com/Liptoid

📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.
📞 Support

    Email: iotclol313@gmail.com

    GitHub Issues: https://github.com/Liptoid/XORLockerv2/issues

⭐ Remerciements

Merci à tous les contributeurs et utilisateurs qui soutiennent ce projet !
<div align="center">

⭐ Si vous aimez ce projet, n'oubliez pas de mettre une étoile sur GitHub ! ⭐

Signaler un bug · Proposer une fonctionnalité
</div>
