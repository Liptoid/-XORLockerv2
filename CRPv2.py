import os
import base64
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import string
import random
from pathlib import Path
import json
import sys
import time
import zlib

# محاولة استيراد مكتبة السحب والإفلات
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️ مكتبة السحب والإفلات غير مثبتة. سيتم تعطيل هذه الميزة.")
    print("📦 للتثبيت: pip install tkinterdnd2")

# محاولة استيراد مكتبة AES
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False
    print("⚠️ مكتبة AES غير مثبتة. سيتم تعطيل تشفير AES-256.")
    print("📦 للتثبيت: pip install pycryptodome")

class BitLockerClone:
    def __init__(self, root):
        self.root = root
        self.root.title("BitLocker Clone - تشفير الملفات")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # متغيرات
        self.selected_drives = []
        self.encryption_type = tk.StringVar(value="SHA-256")  # تغيير الافتراضي إلى SHA-256
        self.password = tk.StringVar()
        self.encryption_key = None
        self.current_drive = None
        self.password_file = "pass.ded"
        self.language = tk.StringVar(value="ar")
        self.fast_mode = tk.BooleanVar(value=False)
        self.compress_mode = tk.BooleanVar(value=False)
        self.dragged_files = []
        
        # ترجمة النصوص
        self.translations = self.load_translations()
        
        # التحقق من وجود كلمة مرور مخزنة
        self.check_stored_password()
        
        # إنشاء الواجهة
        self.setup_ui()
        
        # تحديث قائمة الأقراص
        self.refresh_drives()
        
        # إعداد السحب والإفلات إذا كانت المكتبة متوفرة
        if DRAG_DROP_AVAILABLE:
            self.setup_drag_drop()
    
    def load_translations(self):
        """تحميل الترجمات"""
        return {
            'ar': {
                'title': 'BitLocker Clone - تشفير الملفات',
                'drives': 'الأقراص المتوفرة',
                'fixed_drives': 'الأقراص الثابتة:',
                'removable_drives': 'الأقراص القابلة للإزالة (USB):',
                'refresh': 'تحديث القائمة',
                'encryption_settings': 'إعدادات التشفير',
                'password': 'كلمة المرور:',
                'encryption_type': 'نوع التشفير:',
                'fast_mode': 'وضع التشفير السريع',
                'compress': 'ضغط الملفات قبل التشفير',
                'encrypt_save': '🔒 تشفير الملفات وحفظ كلمة المرور',
                'decrypt': '🔓 فك التشفير',
                'statistics': '📊 إحصائيات',
                'drag_drop': '📁 اختر الملفات يدوياً',
                'log': 'سجل العمليات',
                'status': 'الحالة',
                'ready': '✅ جاهز للتشفير',
                'encrypting': '🔐 جاري التشفير...',
                'decrypting': '🔓 جاري فك التشفير...',
                'success': '✅ اكتمل بنجاح',
                'error': '❌ خطأ',
                'warning': '⚠️ تحذير',
                'confirm': 'تأكيد',
                'cancel': 'إلغاء',
                'files_found': 'ملف سيتم تشفيرها',
                'password_required': 'الرجاء إدخال كلمة المرور',
                'password_length': 'كلمة المرور يجب أن تكون 4 أحرف على الأقل',
                'select_drive': 'الرجاء اختيار قرص واحد على الأقل',
                'no_files': 'لا توجد ملفات للتشفير',
                'stats_message': 'إحصائيات الملفات:\n\n• الملفات القابلة للتشفير: {}\n• الملفات المشفرة: {}\n• ملف كلمة المرور: {}\n• إجمالي الملفات: {}',
                'clear_dragged': 'مسح القائمة',
                'selected_files': 'الملفات المختارة:'
            },
            'en': {
                'title': 'BitLocker Clone - File Encryption',
                'drives': 'Available Drives',
                'fixed_drives': 'Fixed Drives:',
                'removable_drives': 'Removable Drives (USB):',
                'refresh': 'Refresh List',
                'encryption_settings': 'Encryption Settings',
                'password': 'Password:',
                'encryption_type': 'Encryption Type:',
                'fast_mode': 'Fast Mode',
                'compress': 'Compress files before encryption',
                'encrypt_save': '🔒 Encrypt & Save Password',
                'decrypt': '🔓 Decrypt',
                'statistics': '📊 Statistics',
                'drag_drop': '📁 Select Files Manually',
                'log': 'Log',
                'status': 'Status',
                'ready': '✅ Ready',
                'encrypting': '🔐 Encrypting...',
                'decrypting': '🔓 Decrypting...',
                'success': '✅ Completed',
                'error': '❌ Error',
                'warning': '⚠️ Warning',
                'confirm': 'Confirm',
                'cancel': 'Cancel',
                'files_found': 'files will be encrypted',
                'password_required': 'Please enter password',
                'password_length': 'Password must be at least 4 characters',
                'select_drive': 'Please select at least one drive',
                'no_files': 'No files to encrypt',
                'stats_message': 'File Statistics:\n\n• Encryptable files: {}\n• Encrypted files: {}\n• Password file: {}\n• Total files: {}',
                'clear_dragged': 'Clear List',
                'selected_files': 'Selected Files:'
            },
            'fr': {
                'title': 'BitLocker Clone - Cryptage de fichiers',
                'drives': 'Lecteurs disponibles',
                'fixed_drives': 'Lecteurs fixes:',
                'removable_drives': 'Lecteurs amovibles (USB):',
                'refresh': 'Actualiser',
                'encryption_settings': 'Paramètres de cryptage',
                'password': 'Mot de passe:',
                'encryption_type': 'Type de cryptage:',
                'fast_mode': 'Mode rapide',
                'compress': 'Compresser avant cryptage',
                'encrypt_save': '🔒 Crypter et sauvegarder',
                'decrypt': '🔓 Décrypter',
                'statistics': '📊 Statistiques',
                'drag_drop': '📁 Sélectionner des fichiers',
                'log': 'Journal',
                'status': 'Statut',
                'ready': '✅ Prêt',
                'encrypting': '🔐 Cryptage...',
                'decrypting': '🔓 Décryptage...',
                'success': '✅ Terminé',
                'error': '❌ Erreur',
                'warning': '⚠️ Attention',
                'confirm': 'Confirmer',
                'cancel': 'Annuler',
                'files_found': 'fichiers seront cryptés',
                'password_required': 'Veuillez entrer le mot de passe',
                'password_length': 'Le mot de passe doit contenir au moins 4 caractères',
                'select_drive': 'Veuillez sélectionner au moins un lecteur',
                'no_files': 'Aucun fichier à crypter',
                'stats_message': 'Statistiques:\n\n• Fichiers cryptables: {}\n• Fichiers cryptés: {}\n• Fichier mot de passe: {}\n• Total: {}',
                'clear_dragged': 'Effacer la liste',
                'selected_files': 'Fichiers sélectionnés:'
            }
        }
    
    def get_text(self, key):
        """الحصول على النص باللغة المحددة"""
        return self.translations[self.language.get()].get(key, key)
    
    def setup_drag_drop(self):
        """إعداد ميزة السحب والإفلات"""
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
            self.drag_label.config(text=self.get_text('drag_drop') + " (اسحب وأفلت الملفات هنا)")
        except:
            self.drag_label.config(text=self.get_text('drag_drop'))
    
    def handle_drop(self, event):
        """معالجة الملفات المسحوبة"""
        try:
            files = self.root.tk.splitlist(event.data)
            for file in files:
                # تنظيف المسار من الأقواس إذا وجدت
                file = file.strip('{}')
                if os.path.exists(file):
                    self.dragged_files.append(file)
                    self.log(f"📁 تم إضافة: {os.path.basename(file)}")
            
            self.update_dragged_files_list()
        except Exception as e:
            self.log(f"❌ خطأ في معالجة الملفات المسحوبة: {str(e)}")
    
    def update_dragged_files_list(self):
        """تحديث قائمة الملفات المختارة"""
        if hasattr(self, 'files_listbox'):
            self.files_listbox.delete(0, tk.END)
            for file in self.dragged_files[:10]:  # عرض أول 10 ملفات فقط
                self.files_listbox.insert(tk.END, os.path.basename(file))
            
            if len(self.dragged_files) > 10:
                self.files_listbox.insert(tk.END, f"... و {len(self.dragged_files) - 10} ملف آخر")
        
        self.drag_label.config(text=f"📦 {len(self.dragged_files)} {self.get_text('selected_files')}")
    
    def setup_ui(self):
        """إنشاء عناصر الواجهة"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار اللغة
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(lang_frame, text="Language / اللغة:").pack(side=tk.LEFT)
        languages = [("🇸🇦 العربية", "ar"), ("🇬🇧 English", "en"), ("🇫🇷 Français", "fr")]
        for lang_text, lang_code in languages:
            ttk.Radiobutton(lang_frame, text=lang_text, variable=self.language, 
                          value=lang_code, command=self.update_language).pack(side=tk.LEFT, padx=5)
        
        # عنوان البرنامج
        self.title_label = ttk.Label(main_frame, text=self.get_text('title'), 
                                     font=('Arial', 16, 'bold'))
        self.title_label.pack(pady=10)
        
        # إطار حالة التشفير
        status_frame = ttk.LabelFrame(main_frame, text=self.get_text('status'), padding="5")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text=self.get_text('ready'), 
                                      font=('Arial', 10))
        self.status_label.pack()
        
        # إطار اختيار الملفات
        files_frame = ttk.LabelFrame(main_frame, text=self.get_text('drag_drop'), padding="10")
        files_frame.pack(fill=tk.X, pady=5)
        
        file_buttons_frame = ttk.Frame(files_frame)
        file_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.drag_label = ttk.Label(file_buttons_frame, text=self.get_text('drag_drop'), 
                                   font=('Arial', 10))
        self.drag_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(file_buttons_frame, text="🗂️ " + self.get_text('drag_drop'), 
                  command=self.select_files).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(file_buttons_frame, text="🗑️ " + self.get_text('clear_dragged'), 
                  command=self.clear_dragged_files).pack(side=tk.LEFT, padx=5)
        
        # قائمة الملفات المختارة
        self.files_listbox = tk.Listbox(files_frame, height=3)
        self.files_listbox.pack(fill=tk.X, pady=5)
        
        # إطار الأقراص
        drives_frame = ttk.LabelFrame(main_frame, text=self.get_text('drives'), padding="5")
        drives_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # قائمة الأقراص
        list_frame = ttk.Frame(drives_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # قائمة الأقراص الثابتة
        ttk.Label(list_frame, text=self.get_text('fixed_drives'), 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.fixed_drives_listbox = tk.Listbox(list_frame, height=2, selectmode=tk.MULTIPLE)
        self.fixed_drives_listbox.pack(fill=tk.X, pady=2)
        
        # قائمة الأقراص القابلة للإزالة
        ttk.Label(list_frame, text=self.get_text('removable_drives'), 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(5,0))
        self.removable_drives_listbox = tk.Listbox(list_frame, height=2, selectmode=tk.MULTIPLE)
        self.removable_drives_listbox.pack(fill=tk.X, pady=2)
        
        # زر تحديث
        ttk.Button(drives_frame, text=self.get_text('refresh'), 
                  command=self.refresh_drives).pack(pady=5)
        
        # إطار التشفير
        encrypt_frame = ttk.LabelFrame(main_frame, text=self.get_text('encryption_settings'), padding="5")
        encrypt_frame.pack(fill=tk.X, pady=5)
        
        # كلمة المرور
        pass_frame = ttk.Frame(encrypt_frame)
        pass_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pass_frame, text=self.get_text('password')).pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(pass_frame, textvariable=self.password, show="*", width=25)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # نوع التشفير
        type_frame = ttk.Frame(encrypt_frame)
        type_frame.pack(fill=tk.X, pady=2)
        ttk.Label(type_frame, text=self.get_text('encryption_type')).pack(side=tk.LEFT)
        
        encryption_types = ["MD5", "SHA-1", "SHA-256"]
        if AES_AVAILABLE:
            encryption_types.append("AES-256")
        
        for enc_type in encryption_types:
            ttk.Radiobutton(type_frame, text=enc_type, variable=self.encryption_type, 
                          value=enc_type).pack(side=tk.LEFT, padx=5)
        
        # خيارات إضافية
        options_frame = ttk.Frame(encrypt_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(options_frame, text=self.get_text('fast_mode'), 
                       variable=self.fast_mode).pack(side=tk.LEFT, padx=10)
        
        ttk.Checkbutton(options_frame, text=self.get_text('compress'), 
                       variable=self.compress_mode).pack(side=tk.LEFT, padx=10)
        
        # إطار الأزرار الرئيسية
        main_button_frame = ttk.Frame(main_frame)
        main_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(main_button_frame, text=self.get_text('encrypt_save'), 
                  command=self.encrypt_and_save_password, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        ttk.Button(main_button_frame, text=self.get_text('decrypt'), 
                  command=self.start_decryption).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        ttk.Button(main_button_frame, text=self.get_text('statistics'), 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # إطار تقدم التشفير
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        # إطار السجل
        log_frame = ttk.LabelFrame(main_frame, text=self.get_text('log'), padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = ScrolledText(log_frame, height=6, width=70)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def clear_dragged_files(self):
        """مسح قائمة الملفات المختارة"""
        self.dragged_files = []
        self.update_dragged_files_list()
        self.log("🗑️ تم مسح قائمة الملفات")
    
    def update_language(self):
        """تحديث واجهة المستخدم عند تغيير اللغة"""
        self.root.title(self.get_text('title'))
        self.title_label.config(text=self.get_text('title'))
        self.status_label.config(text=self.get_text('ready'))
        self.drag_label.config(text=self.get_text('drag_drop'))
        # يمكن إضافة المزيد من التحديثات
    
    def select_files(self):
        """اختيار ملفات للتشفير"""
        files = filedialog.askopenfilenames(title=self.get_text('drag_drop'))
        for file in files:
            self.dragged_files.append(file)
            self.log(f"📁 تم إضافة: {os.path.basename(file)}")
        
        self.update_dragged_files_list()
    
    def aes_encrypt(self, data, key):
        """تشفير AES-256"""
        if not AES_AVAILABLE:
            return self.xor_encrypt(data, key)
        
        # توليد مفتاح AES من كلمة المرور
        key = hashlib.sha256(key).digest()
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        return cipher.iv + ct_bytes
    
    def aes_decrypt(self, data, key):
        """فك تشفير AES-256"""
        if not AES_AVAILABLE:
            return self.xor_encrypt(data, key)
        
        key = hashlib.sha256(key).digest()
        iv = data[:AES.block_size]
        ct = data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size)
    
    def encrypt_file(self, file_path, key):
        """تشفير ملف واحد مع دعم AES والخيارات المتقدمة"""
        try:
            # تخطي ملف pass.ded
            if os.path.basename(file_path) == self.password_file:
                return True, file_path
            
            # قراءة الملف
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # ضغط إذا كان مفعلاً
            if self.compress_mode.get():
                file_data = zlib.compress(file_data)
            
            # تشفير حسب النوع المختار
            if self.encryption_type.get() == "AES-256" and AES_AVAILABLE:
                encrypted_data = self.aes_encrypt(file_data, key)
            else:
                # XOR للتشفيرات الأخرى
                encrypted_data = self.xor_encrypt(file_data, key)
            
            # تشفير Base64 إضافي
            b64_encoded = base64.b64encode(encrypted_data)
            
            # اسم الملف المشفر
            if self.encryption_type.get() == "AES-256" and AES_AVAILABLE:
                new_path = file_path + ".aes_locked"
            else:
                new_path = file_path + ".locked"
            
            # كتابة الملف المشفر
            with open(new_path, 'wb') as f:
                f.write(b64_encoded)
            
            # حذف الملف الأصلي
            os.remove(file_path)
            
            return True, new_path
        except Exception as e:
            return False, str(e)
    
    def encrypt_folder(self, folder_path, key):
        """تشفير مجلد كامل"""
        encrypted_files = []
        failed_files = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                success, result = self.encrypt_file(file_path, key)
                
                if success:
                    encrypted_files.append(result)
                else:
                    failed_files.append(file_path)
        
        return encrypted_files, failed_files
    
    def encrypt_files_thread(self, files):
        """خيط تشفير الملفات مع دعم الوضع السريع"""
        try:
            self.progress_bar.start()
            self.status_label.config(text=self.get_text('encrypting'))
            
            total_files = len(files)
            self.log(f"🔐 بدء تشفير {total_files} ملف...")
            
            # توليد المفتاح
            key = self.generate_key_from_password(self.password.get(), self.encryption_type.get())
            
            success_count = 0
            fail_count = 0
            
            for i, file_path in enumerate(files):
                self.log(f"📁 تشفير: {os.path.basename(file_path)}")
                
                # تشفير الملف
                success, result = self.encrypt_file(file_path, key)
                
                if success:
                    success_count += 1
                else:
                    fail_count += 1
                    self.log(f"❌ فشل التشفير: {file_path} - {result}")
                
                # تحديث التقدم
                progress = int((i + 1) / total_files * 100)
                self.progress_label.config(text=f"{progress}%")
                
                if i % 5 == 0:
                    self.root.update()
            
            self.progress_bar.stop()
            self.status_label.config(text=self.get_text('success'))
            self.progress_label.config(text="100%")
            
            self.log(f"🎯 اكتمل التشفير: {success_count} نجاح، {fail_count} فشل")
            messagebox.showinfo(self.get_text('success'), 
                              f"تم تشفير {success_count} ملف بنجاح")
            
        except Exception as e:
            self.progress_bar.stop()
            self.status_label.config(text=self.get_text('error'))
            self.log(f"❌ خطأ عام: {str(e)}")
            messagebox.showerror(self.get_text('error'), f"حدث خطأ: {str(e)}")
    
    def encrypt_and_save_password(self):
        """تشفير الملفات وحفظ كلمة المرور"""
        if not self.validate_inputs():
            return
        
        # استخدام الملفات المسحوبة أو الأقراص المحددة
        if self.dragged_files:
            files = self.dragged_files
            drives = []
        else:
            # الحصول على الأقراص المحددة
            selected_fixed = [self.fixed_drives_listbox.get(i) for i in self.fixed_drives_listbox.curselection()]
            selected_removable = [self.removable_drives_listbox.get(i) for i in self.removable_drives_listbox.curselection()]
            selected_drives = selected_fixed + selected_removable
            
            if not selected_drives:
                messagebox.showwarning(self.get_text('warning'), self.get_text('select_drive'))
                return
            
            files = self.get_files_to_encrypt(selected_drives)
            drives = selected_drives
        
        if not files:
            messagebox.showinfo(self.get_text('warning'), self.get_text('no_files'))
            return
        
        result = messagebox.askyesno(self.get_text('confirm'), 
            f"{len(files)} {self.get_text('files_found')}\n"
            f"هل أنت متأكد من الاستمرار؟")
        
        if result:
            # حفظ كلمة المرور في الأقراص
            if drives:
                for drive in drives:
                    drive_path = drive.split(' - ')[0]
                    self.save_password_to_drive(drive_path, self.password.get(), self.encryption_type.get())
            
            # بدء التشفير
            thread = threading.Thread(target=self.encrypt_files_thread, args=(files,))
            thread.daemon = True
            thread.start()
    
    def generate_key_from_password(self, password, method):
        """توليد مفتاح التشفير من كلمة المرور"""
        if method == "MD5":
            return hashlib.md5(password.encode()).digest()
        elif method == "SHA-1":
            return hashlib.sha1(password.encode()).digest()
        else:  # SHA-256 أو AES-256
            return hashlib.sha256(password.encode()).digest()
    
    def xor_encrypt(self, data, key):
        """تشفير XOR بسيط"""
        key_length = len(key)
        return bytes([data[i] ^ key[i % key_length] for i in range(len(data))])
    
    def check_stored_password(self):
        """التحقق من وجود كلمة مرور مخزنة"""
        try:
            import psutil
            for partition in psutil.disk_partitions():
                drive_path = partition.mountpoint
                password_file_path = os.path.join(drive_path, self.password_file)
                
                if os.path.exists(password_file_path):
                    with open(password_file_path, 'r', encoding='utf-8') as f:
                        stored_data = json.load(f)
                        self.current_drive = drive_path
                        
                        # عرض نافذة إدخال كلمة المرور
                        self.show_password_dialog(stored_data)
                    break
        except:
            pass
    
    def show_password_dialog(self, stored_data):
        """عرض نافذة إدخال كلمة المرور"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.get_text('password'))
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.lift()
        dialog.focus_force()
        
        ttk.Label(dialog, text=self.get_text('password_required'), 
                 font=('Arial', 12)).pack(pady=20)
        
        password_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=password_var, show="*", 
                 width=30, font=('Arial', 11)).pack(pady=10)
        
        def verify_password():
            entered_password = password_var.get()
            if entered_password:
                hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
                
                if hashed_password == stored_data.get('password_hash'):
                    self.password.set(entered_password)
                    self.encryption_type.set(stored_data.get('encryption_type', 'SHA-256'))
                    dialog.destroy()
                    self.log("✅ تم التحقق من كلمة المرور بنجاح")
                    
                    self.show_decryption_options()
                else:
                    messagebox.showerror(self.get_text('error'), "كلمة المرور غير صحيحة")
        
        ttk.Button(dialog, text=self.get_text('confirm'), command=verify_password, 
                  style="Accent.TButton").pack(pady=20)
        
        ttk.Button(dialog, text=self.get_text('cancel'), command=dialog.destroy).pack()
    
    def show_decryption_options(self):
        """عرض خيارات فك التشفير"""
        result = messagebox.askyesno(self.get_text('decrypt'), 
            "تم العثور على ملفات مشفرة. هل تريد فك تشفيرها الآن؟")
        
        if result:
            locked_files = []
            for root, dirs, files in os.walk(self.current_drive):
                for file in files:
                    if file.endswith('.locked') or file.endswith('.aes_locked'):
                        locked_files.append(os.path.join(root, file))
            
            if locked_files:
                thread = threading.Thread(target=self.decrypt_files_thread, args=(locked_files,))
                thread.daemon = True
                thread.start()
            else:
                messagebox.showinfo(self.get_text('warning'), "لا توجد ملفات .locked في هذا القرص")
    
    def save_password_to_drive(self, drive_path, password, encryption_type):
        """حفظ كلمة المرور المشفرة في القرص"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            password_data = {
                'password_hash': password_hash,
                'encryption_type': encryption_type,
                'drive_id': drive_path,
                'created': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            password_file_path = os.path.join(drive_path, self.password_file)
            with open(password_file_path, 'w', encoding='utf-8') as f:
                json.dump(password_data, f, indent=4, ensure_ascii=False)
            
            # إخفاء الملف في Windows
            if os.name == 'nt':
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(password_file_path, 2)
            
            return True
        except Exception as e:
            self.log(f"❌ خطأ في حفظ كلمة المرور: {str(e)}")
            return False
    
    def refresh_drives(self):
        """تحديث قائمة الأقراص"""
        try:
            import psutil
        except ImportError:
            self.log("❌ يرجى تثبيت مكتبة psutil: pip install psutil")
            return
        
        self.fixed_drives_listbox.delete(0, tk.END)
        self.removable_drives_listbox.delete(0, tk.END)
        
        for partition in psutil.disk_partitions():
            try:
                drive_letter = partition.device
                usage = psutil.disk_usage(partition.mountpoint)
                
                has_password = "🔑 " if os.path.exists(os.path.join(partition.mountpoint, self.password_file)) else ""
                
                if 'removable' in partition.opts:
                    self.removable_drives_listbox.insert(tk.END, 
                        f"{drive_letter} - {self.get_size_string(usage.total)} - {has_password}قابل للإزالة")
                else:
                    self.fixed_drives_listbox.insert(tk.END, 
                        f"{drive_letter} - {self.get_size_string(usage.total)} - {has_password}ثابت")
            except:
                continue
        
        self.log("✅ تم تحديث قائمة الأقراص")
    
    def get_size_string(self, size):
        """تحويل الحجم إلى نص مقروء"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def get_files_to_encrypt(self, drives):
        """الحصول على قائمة الملفات في الأقراص المحددة"""
        files = []
        extensions_to_skip = ['.exe', '.dll', '.sys', '.locked', '.aes_locked']
        
        for drive in drives:
            drive_path = drive.split(' - ')[0]
            try:
                for root, dirs, filenames in os.walk(drive_path):
                    for filename in filenames:
                        if filename == self.password_file:
                            continue
                        
                        file_path = os.path.join(root, filename)
                        ext = os.path.splitext(filename)[1].lower()
                        if ext not in extensions_to_skip and not filename.startswith('.'):
                            files.append(file_path)
            except Exception as e:
                self.log(f"⚠️ خطأ في قراءة {drive_path}: {str(e)}")
        
        return files
    
    def decrypt_file(self, file_path, key):
        """فك تشفير ملف واحد مع دعم AES"""
        try:
            with open(file_path, 'rb') as f:
                encrypted_b64 = f.read()
            
            encrypted_data = base64.b64decode(encrypted_b64)
            
            # فك التشفير حسب نوع الملف
            if file_path.endswith('.aes_locked') and AES_AVAILABLE:
                decrypted_data = self.aes_decrypt(encrypted_data, key)
                original_path = file_path.replace('.aes_locked', '')
            else:
                decrypted_data = self.xor_encrypt(encrypted_data, key)
                original_path = file_path.replace('.locked', '')
            
            # فك الضغط إذا كان مضغوطاً
            try:
                decrypted_data = zlib.decompress(decrypted_data)
            except:
                pass  # ليس ملفاً مضغوطاً
            
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            os.remove(file_path)
            
            return True, original_path
        except Exception as e:
            return False, str(e)
    
    def decrypt_files_thread(self, files):
        """خيط فك تشفير الملفات"""
        try:
            self.progress_bar.start()
            self.status_label.config(text=self.get_text('decrypting'))
            
            total_files = len(files)
            self.log(f"🔓 بدء فك تشفير {total_files} ملف...")
            
            key = self.generate_key_from_password(self.password.get(), self.encryption_type.get())
            
            success_count = 0
            fail_count = 0
            
            for i, file_path in enumerate(files):
                self.log(f"📁 فك تشفير: {os.path.basename(file_path)}")
                success, result = self.decrypt_file(file_path, key)
                
                if success:
                    success_count += 1
                    self.log(f"✅ تم فك التشفير: {result}")
                else:
                    fail_count += 1
                    self.log(f"❌ فشل فك التشفير: {file_path} - {result}")
                
                progress = int((i + 1) / total_files * 100)
                self.progress_label.config(text=f"{progress}%")
                self.root.update()
            
            self.progress_bar.stop()
            self.status_label.config(text=self.get_text('success'))
            self.progress_label.config(text="100%")
            
            self.log(f"🎯 اكتمل فك التشفير: {success_count} نجاح، {fail_count} فشل")
            messagebox.showinfo(self.get_text('success'), 
                              f"تم فك تشفير {success_count} ملف بنجاح")
            
        except Exception as e:
            self.progress_bar.stop()
            self.status_label.config(text=self.get_text('error'))
            self.log(f"❌ خطأ عام: {str(e)}")
            messagebox.showerror(self.get_text('error'), f"حدث خطأ: {str(e)}")
    
    def start_decryption(self):
        """بدء عملية فك التشفير"""
        if not self.validate_inputs():
            return
        
        # استخدام الملفات المسحوبة أو البحث في الأقراص
        if self.dragged_files:
            locked_files = [f for f in self.dragged_files if f.endswith(('.locked', '.aes_locked'))]
        else:
            selected_fixed = [self.fixed_drives_listbox.get(i) for i in self.fixed_drives_listbox.curselection()]
            selected_removable = [self.removable_drives_listbox.get(i) for i in self.removable_drives_listbox.curselection()]
            selected_drives = selected_fixed + selected_removable
            
            locked_files = []
            for drive in selected_drives:
                drive_path = drive.split(' - ')[0]
                for root, dirs, files in os.walk(drive_path):
                    for file in files:
                        if file.endswith(('.locked', '.aes_locked')):
                            locked_files.append(os.path.join(root, file))
        
        if not locked_files:
            messagebox.showinfo(self.get_text('warning'), "لا توجد ملفات مشفرة")
            return
        
        result = messagebox.askyesno(self.get_text('confirm'), 
            f"سيتم فك تشفير {len(locked_files)} ملف. هل أنت متأكد؟")
        
        if result:
            thread = threading.Thread(target=self.decrypt_files_thread, args=(locked_files,))
            thread.daemon = True
            thread.start()
    
    def validate_inputs(self):
        """التحقق من المدخلات"""
        if not self.password.get():
            messagebox.showwarning(self.get_text('warning'), self.get_text('password_required'))
            return False
        
        if len(self.password.get()) < 4:
            messagebox.showwarning(self.get_text('warning'), self.get_text('password_length'))
            return False
        
        return True
    
    def show_statistics(self):
        """عرض إحصائيات الملفات"""
        try:
            # إحصائيات الملفات المسحوبة
            if self.dragged_files:
                files = self.dragged_files
                locked_files = [f for f in files if f.endswith(('.locked', '.aes_locked'))]
                normal_files = [f for f in files if not f.endswith(('.locked', '.aes_locked'))]
                
                has_password = "نعم" if any('pass.ded' in f for f in files) else "لا"
            else:
                selected_fixed = [self.fixed_drives_listbox.get(i) for i in self.fixed_drives_listbox.curselection()]
                selected_removable = [self.removable_drives_listbox.get(i) for i in self.removable_drives_listbox.curselection()]
                selected_drives = selected_fixed + selected_removable
                
                if not selected_drives:
                    messagebox.showwarning(self.get_text('warning'), self.get_text('select_drive'))
                    return
                
                normal_files = self.get_files_to_encrypt(selected_drives)
                locked_files = []
                
                for drive in selected_drives:
                    drive_path = drive.split(' - ')[0]
                    for root, dirs, files_in_dir in os.walk(drive_path):
                        for file in files_in_dir:
                            if file.endswith(('.locked', '.aes_locked')):
                                locked_files.append(os.path.join(root, file))
                
                has_password = "نعم" if any(os.path.exists(os.path.join(drive.split(' - ')[0], self.password_file)) 
                                           for drive in selected_drives) else "لا"
            
            stats = self.get_text('stats_message').format(
                len(normal_files), len(locked_files), has_password, 
                len(normal_files) + len(locked_files)
            )
            
            # إضافة إحصائيات AES
            aes_files = len([f for f in locked_files if f.endswith('.aes_locked')])
            if aes_files > 0:
                stats += f"\n• ملفات AES-256: {aes_files}"
            
            messagebox.showinfo(self.get_text('statistics'), stats)
            
        except Exception as e:
            messagebox.showerror(self.get_text('error'), f"حدث خطأ: {str(e)}")
    
    def log(self, message):
        """إضافة رسالة إلى سجل العمليات"""
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

def create_launcher():
    """إنشاء ملف لتشغيل البرنامج"""
    launcher_content = '''@echo off
title BitLocker Clone
color 0A
echo ========================================
echo    BitLocker Clone - تشغيل البرنامج
echo ========================================
echo.
echo جاري تشغيل البرنامج...
python "CRPv2.py"
pause
'''
    
    with open("run.bat", "w") as f:
        f.write(launcher_content)
    
    print("✅ تم إنشاء ملف التشغيل run.bat")

def install_requirements():
    """تثبيت المتطلبات"""
    requirements = [
        "psutil",
        "pycryptodome"
    ]
    
    print("📦 جاري تثبيت المتطلبات...")
    for req in requirements:
        os.system(f"pip install {req}")
    
    # محاولة تثبيت tkinterdnd2 (اختياري)
    try:
        os.system("pip install tkinterdnd2")
    except:
        pass
    
    print("✅ تم تثبيت المتطلبات")

def main():
    # التحقق من وجود وسائط سطر الأوامر
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create-launcher":
            create_launcher()
            return
        elif sys.argv[1] == "--install":
            install_requirements()
            return
    
    # استخدام TkinterDnD إذا كان متاحاً
    if DRAG_DROP_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    # تطبيق الثيم
    style = ttk.Style()
    style.theme_use('clam')
    
    # تخصيص الأزرار
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    app = BitLockerClone(root)
    root.mainloop()

if __name__ == "__main__":
    main()