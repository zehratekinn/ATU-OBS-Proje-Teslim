import os
import subprocess
import sys

# OTOMATİK KÜTÜPHANE KONTROL VE YÜKLEME
try:
    import customtkinter as ctk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

from tkinter import messagebox

# ==========================================================
# 1. MODEL KATMANI (Orijinal Yapı)
# ==========================================================
class Course:
    def __init__(self, name, day, time, avg, prof, mail, office):
        self.name = name
        self.day = day
        self.time = time
        self.avg = avg
        self.prof = prof
        self.mail = mail
        self.office = office

class Grade:
    def __init__(self, course_name, midterm, final, but=None):
        self.course_name = course_name
        self.midterm = midterm
        self.final = final
        self.but = but

class Attendance:
    def __init__(self, course_name, percent):
        self.course_name = course_name
        self.percent = percent

# ==========================================================
# 2. ANA UYGULAMA (Pembe Şık Dashboard)
# ==========================================================
class ModernSMS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ATÜ ÖĞRENCİ BİLGİ SİSTEMİ")
        self.geometry("1300x950")
        
        ctk.set_appearance_mode("light")
        self.primary = "#db2777"  # Pembe Tema
        self.bg_color = "#fff1f2"

        # SİSTEM HAFIZASI
        self.published_announcements = []
        self.saved_grades_log = []
        self.attendance_log = {} 

        # ÖĞRENCİ VERİLERİ
        self.user_name = "Zehra Tekin"
        self.student_id = "220202048"
        self.department = "Management Information Systems"

        self.student_list = ["Ahmet Yılmaz", "Mehmet Demir", "Ayşe Kaya", "Fatma Çelik", "Mustafa Şahin", "Emine Yıldız", "Ali Öztürk", "Zeynep Aydın", "Hüseyin Özkan", "Elif Arslan", "İbrahim Doğan", "Meryem Kılıç", "Murat Aslan", "Gamze Çetin", "Ömer Toprak", "Hatice Aksoy", "Gökhan Yiğit", "Seda Güneş", "Burak Bulut", "Zehra Tekin"]

        self.courses = [
            Course("Software Engineering", "Pazartesi", "09:15 - 12:00", 55, "Dr. Öğr. Üyesi Nihal Menzi Çetin", "nmenzi@atu.edu.tr", "A Blok - 204"),
            Course("Research Methods", "Salı", "09:30 - 12:00", 65, "Doç. Dr. Bilge Aksay", "baksay@atu.edu.tr", "B Blok - 105"),
            Course("MIS Fundamentals", "Çarşamba", "13:15 - 16:00", 45, "Prof. Dr. Cihan Çetinkaya", "ccetinkaya@atu.edu.tr", "C Blok - 302"),
            Course("Data Structures", "Cuma", "09:15 - 12:00", 48, "Dr. Öğr. Ahmet Büyükeke", "abuyukeke@atu.edu.tr", "A Blok - 110")
        ]

        self.grades = [Grade("Software Engineering", 85, 75), Grade("Research Methods", 70, 60), Grade("MIS Fundamentals", 50, 45), Grade("Data Structures", 40, 30, but=65)]

        self.show_role_selection()

    # HARF NOTU HESAPLAMA
    def calculate_letter_grade(self, vize, final):
        sonuc = (vize * 0.4) + (final * 0.6)
        if sonuc >= 90: return "AA"
        elif sonuc >= 85: return "BA"
        elif sonuc >= 80: return "BB"
        elif sonuc >= 75: return "CB"
        elif sonuc >= 70: return "CC"
        elif sonuc >= 65: return "DC"
        elif sonuc >= 60: return "DD"
        elif sonuc >= 50: return "FD"
        else: return "FF"

    # --- ROL SEÇİM EKRANI ---
    def show_role_selection(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=self.primary)
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=35, width=500, height=450)
        card.place(relx=0.5, rely=0.5, anchor="center")
        logo_bg = ctk.CTkFrame(card, fg_color="#fbcfe8", width=100, height=100, corner_radius=50)
        logo_bg.place(relx=0.5, rely=0.15, anchor="center")
        ctk.CTkLabel(logo_bg, text="ATÜ", text_color=self.primary, font=("Inter", 28, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text="ATÜ ÖĞRENCİ BİLGİ SİSTEMİ", text_color=self.primary, font=("Inter", 20, "bold")).place(relx=0.5, rely=0.32, anchor="center")
        ctk.CTkButton(card, text="ÖĞRENCİ GİRİŞİ", command=lambda: self.show_login("Öğrenci"), fg_color=self.primary, width=300, height=60, corner_radius=15, font=("Inter", 16, "bold")).place(relx=0.5, rely=0.55, anchor="center")
        ctk.CTkButton(card, text="AKADEMİSYEN GİRİŞİ", command=lambda: self.show_login("Akademisyen"), fg_color="#4b5563", width=300, height=60, corner_radius=15, font=("Inter", 16, "bold")).place(relx=0.5, rely=0.78, anchor="center")

    def show_login(self, role):
        self.current_role = role
        for w in self.winfo_children(): w.destroy()
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=35, width=480, height=620)
        card.place(relx=0.5, rely=0.5, anchor="center")
        logo_bg = ctk.CTkFrame(card, fg_color="#fbcfe8", width=120, height=120, corner_radius=60)
        logo_bg.place(relx=0.5, rely=0.18, anchor="center")
        ctk.CTkLabel(logo_bg, text="ATÜ", text_color=self.primary, font=("Inter", 32, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text=f"{role.upper()} GİRİŞİ", text_color=self.primary, font=("Inter", 22, "bold")).place(relx=0.5, rely=0.35, anchor="center")
        
        self.user_e = ctk.CTkEntry(card, placeholder_text="Kullanıcı Adı", width=320, height=55, corner_radius=15)
        self.user_e.place(relx=0.5, rely=0.52, anchor="center")
        self.pw_e = ctk.CTkEntry(card, placeholder_text="Şifre", show="*", width=320, height=55, corner_radius=15)
        self.pw_e.place(relx=0.5, rely=0.65, anchor="center")

        if role == "Öğrenci":
            self.user_e.insert(0, "220202048"); self.pw_e.insert(0, "12345")
        else:
            self.user_e.insert(0, "Nihalmenziçetin"); self.pw_e.insert(0, "nihal123")
        
        ctk.CTkButton(card, text="GİRİŞ YAP", command=self.login, fg_color=self.primary, width=320, height=55, corner_radius=15).place(relx=0.5, rely=0.82, anchor="center")
        ctk.CTkButton(card, text="Geri Dön", command=self.show_role_selection, fg_color="transparent", text_color="gray").place(relx=0.5, rely=0.92, anchor="center")

    def login(self):
        u, p = self.user_e.get(), self.pw_e.get()
        if self.current_role == "Öğrenci" and u == "220202048" and p == "12345": self.show_student_main()
        elif self.current_role == "Akademisyen" and u == "Nihalmenziçetin" and p == "nihal123": self.show_prof_main()
        else: messagebox.showerror("Hata", "Bilgiler yanlış!")

    # --- AKADEMİSYEN PANELİ ---
    def show_prof_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=self.bg_color)
        sidebar = ctk.CTkFrame(self, fg_color="white", width=280, corner_radius=0); sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="ATÜ - HOCA PANEL", text_color=self.primary, font=("Inter", 24, "bold")).pack(pady=40)
        menu = [("📊 Not Girişi", self.prof_grade_entry), ("🚶 Devamsızlık Takibi", self.prof_attendance_entry), ("📢 Duyuru Yayınla", self.prof_announcement), ("🔒 Güvenli Çıkış", self.show_role_selection)]
        for text, cmd in menu:
            ctk.CTkButton(sidebar, text=text, fg_color="transparent", text_color="#334155", anchor="w", hover_color="#fbcfe8", height=45, font=("Inter", 14), command=cmd).pack(fill="x", padx=20, pady=2)
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent"); self.content_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        self.prof_grade_entry()

    def prof_grade_entry(self):
        self.clear_content(); self.section_title("Öğrenci Not Yönetimi")
        f_entry = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f_entry.pack(fill="x", pady=10)
        self.student_combo = ctk.CTkComboBox(f_entry, values=self.student_list, width=300); self.student_combo.grid(row=0, column=0, padx=20, pady=20)
        v_ent = ctk.CTkEntry(f_entry, placeholder_text="Vize", width=60); v_ent.grid(row=0, column=1, padx=5)
        f_ent = ctk.CTkEntry(f_entry, placeholder_text="Final", width=60); f_ent.grid(row=0, column=2, padx=5)
        def save_grade():
            v, fn = int(v_ent.get() or 0), int(f_ent.get() or 0)
            harf = self.calculate_letter_grade(v, fn)
            color = "#dc2626" if v < 50 or fn < 50 or harf == "FF" else "#16a34a"
            status = " -> [BÜT]" if color == "#dc2626" else ""
            res = (f"{self.student_combo.get()} | V: {v} F: {fn} | Harf: {harf}{status}", color)
            self.saved_grades_log.append(res); self.prof_grade_entry()
        ctk.CTkButton(f_entry, text="Kaydet", command=save_grade, fg_color=self.primary).grid(row=0, column=3, padx=20)
        for log, clr in self.saved_grades_log: ctk.CTkLabel(self.content_frame, text=f"✅ {log}", font=("Inter", 12, "bold"), text_color=clr).pack(anchor="w", padx=20, pady=5)

    def prof_attendance_entry(self):
        self.clear_content(); self.section_title("Devamsızlık Takibi (Sınır: 8 Saat)")
        f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f.pack(fill="x", pady=10)
        self.att_combo = ctk.CTkComboBox(f, values=self.student_list, width=300); self.att_combo.grid(row=0, column=0, padx=20, pady=20)
        hour_ent = ctk.CTkEntry(f, placeholder_text="Saat", width=60); hour_ent.grid(row=0, column=1, padx=10)
        def add_att():
            name = self.att_combo.get()
            self.attendance_log[name] = self.attendance_log.get(name, 0) + int(hour_ent.get() or 0)
            self.prof_attendance_entry()
        ctk.CTkButton(f, text="Ekle", command=add_att, fg_color=self.primary).grid(row=0, column=2, padx=10)
        for name, hours in self.attendance_log.items():
            clr = "#dc2626" if hours > 8 else "#16a34a"
            row = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10); row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{name} - {hours} Saat / 8 Saat", text_color=clr, font=("Inter", 12, "bold")).pack(padx=20)

    def prof_announcement(self):
        self.clear_content(); self.section_title("Duyuru Yayınla")
        f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f.pack(fill="x", pady=10)
        t_e = ctk.CTkEntry(f, placeholder_text="Başlık", width=500); t_e.pack(padx=20, pady=10)
        b_e = ctk.CTkTextbox(f, width=500, height=100); b_e.pack(padx=20, pady=10)
        def pub(): self.published_announcements.append((t_e.get(), b_e.get("1.0", "end-1c"))); self.prof_announcement()
        ctk.CTkButton(f, text="Yayınla", command=pub, fg_color=self.primary).pack(pady=10)
        for t, b in self.published_announcements:
            box = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15); box.pack(fill="x", pady=5)
            ctk.CTkLabel(box, text=t, font=("Inter", 13, "bold"), text_color=self.primary).pack(anchor="w", padx=15, pady=5)
            ctk.CTkLabel(box, text=b, font=("Inter", 11)).pack(anchor="w", padx=15, pady=5)

    # --- ÖĞRENCİ PANELİ ---
    def show_student_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=self.bg_color)
        sidebar = ctk.CTkFrame(self, fg_color="white", width=280, corner_radius=0); sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="ATÜ - SMS", text_color=self.primary, font=("Inter", 26, "bold")).pack(pady=40)
        profile = ctk.CTkFrame(sidebar, fg_color="#fff1f2", corner_radius=15); profile.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(profile, text=self.user_name, font=("Inter", 14, "bold"), text_color=self.primary).pack(pady=10)
        menu = [("🏠 Dashboard", self.view_dashboard), ("📊 Notlarım", self.view_grades), ("👨‍🏫 Hoca Rehberi", self.view_profs), ("📅 Ders Programı", self.view_timetable), ("🍽️ Yemekhane", self.view_campus), ("🗓️ Akademik Takvim", self.view_academic_calendar), ("🔒 Güvenli Çıkış", self.show_role_selection)]
        for text, cmd in menu:
            ctk.CTkButton(sidebar, text=text, fg_color="transparent", text_color="#334155", anchor="w", hover_color="#fbcfe8", height=45, font=("Inter", 14), command=cmd).pack(fill="x", padx=20, pady=2)
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent"); self.content_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        self.view_dashboard()

    def view_dashboard(self):
        self.clear_content(); self.section_title("Akademik & Kampüs Özeti")
        stats = ctk.CTkFrame(self.content_frame, fg_color="transparent"); stats.pack(fill="x", pady=(0, 20))
        self.create_card(stats, "GPA Ortalama", "3.82", self.primary).pack(side="left", padx=(0, 20))
        self.create_card(stats, "Kütüphane Doluluk", "%74", "#0ea5e9").pack(side="left", padx=(0, 20))
        self.create_card(stats, "Kalan Kredi", "116", "#059669").pack(side="left")
        
        self.section_title("📢 Üniversite Duyuruları")
        news = [("📢 DERS DUYURUSU", "Bugün yapılacak olan Software Engineering dersi, Nihal Hoca'nın rahatsızlığı nedeniyle iptal edilmiştir.", "Bugün"),
                ("🚀 TANIŞMA TOPLANTISI!", "ATÜ Kültür ve Sanat Topluluğu olarak yeni dönemi açıyoruz! Saat: 15:30 Kantin.", "Bugün"),
                ("⚠️ ÖNEMLİ HATIRLATMA", "Data Structure dersinin ödev teslimi için son saat bugün 17:00'dir. LMS'ye yüklemeyi unutmayın.", "Bugün")]
        for t, b, d in news:
            f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15); f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=t, font=("Inter", 14, "bold"), text_color=self.primary).pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkLabel(f, text=b, font=("Inter", 12), wraplength=700).pack(anchor="w", padx=20, pady=5)

    def view_grades(self):
        self.clear_content(); self.section_title("📊 Detaylı Not Takibi")
        f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f.pack(fill="x")
        for g in self.grades:
            row = ctk.CTkFrame(f, fg_color="transparent"); row.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(row, text=g.course_name, font=("Inter", 13, "bold"), width=200, anchor="w").pack(side="left")
            val = f"Vize: {g.midterm} | Final: {g.final}" + (f" | Büt: {g.but}" if g.but else "")
            ctk.CTkLabel(row, text=val).pack(side="right")

    def view_profs(self):
        self.clear_content(); self.section_title("👨‍🏫 Hoca Bilgi Sistemi")
        for c in self.courses:
            card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20, border_width=1, border_color="#fbcfe8")
            card.pack(fill="x", pady=10)
            ctk.CTkLabel(card, text=c.prof, font=("Inter", 15, "bold"), text_color=self.primary).pack(anchor="w", padx=20, pady=(15, 5))
            ctk.CTkLabel(card, text=f"📧 {c.mail} | 🏢 {c.office}").pack(anchor="w", padx=20, pady=(0, 15))

    def view_campus(self):
        self.clear_content(); self.section_title("🍽️ Aralık Ayı Son Hafta Yemek Menüsü")
        f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f.pack(fill="x", pady=10)
        menu = [("Pazartesi", "Mercimek Çorbası, Pirinç Pilavı, Et Sote, Ayran"), ("Salı", "Ezogelin Çorbası, Bulgur Pilavı, İzmir Köfte, Meyve"), ("Çarşamba", "Yayla Çorbası, Soslu Makarna, Tavuk Baget, Salata"), ("Perşembe", "Tarhana Çorbası, Nohut Yemeği, Şehriyeli Pilav, Cacık"), ("Cuma", "Domates Çorbası, Tas Kebabı, Mantı, Revani Tatlısı")]
        for gun, yemek in menu:
            row = ctk.CTkFrame(f, fg_color="transparent"); row.pack(fill="x", padx=20, pady=12)
            ctk.CTkLabel(row, text=gun, font=("Inter", 13, "bold"), text_color=self.primary, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=yemek, font=("Inter", 12)).pack(side="left", padx=10)

    def view_timetable(self):
        self.clear_content(); self.section_title("📅 Haftalık Ders Programı & Saatler")
        f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); f.pack(fill="x")
        for c in self.courses:
            row = ctk.CTkFrame(f, fg_color="transparent"); row.pack(fill="x", padx=20, pady=12)
            ctk.CTkLabel(row, text=f"{c.day}:", text_color=self.primary, font=("Inter", 13, "bold"), width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"{f'{c.name} ({c.time})'}").pack(side="left")

    def view_academic_calendar(self):
        self.clear_content()
        self.section_title("📅 Güz Yarıyılı (Detaylı)")
        g_f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); g_f.pack(fill="x", pady=(0, 20))
        g_ev = [("Kayıt Yenileme (Danışman Onaylı)", "15-19 Eylül 2025"), ("Derslerin Başlaması", "22 Eylül 2025"), ("Ders Ekleme/Bırakma", "29 Eylül-03 Ekim 2025"), ("Ara Sınavlar (Vize)", "10-21 Kasım 2025"), ("Derslerin Kesilmesi", "02 Ocak 2026"), ("Final Sınavları", "05-16 Ocak 2026"), ("Bütünleme Sınavları", "26-31 Ocak 2026")]
        for a, d in g_ev:
            r = ctk.CTkFrame(g_f, fg_color="transparent"); r.pack(fill="x", padx=20, pady=6)
            ctk.CTkLabel(r, text=f"• {a}").pack(side="left"); ctk.CTkLabel(r, text=d, font=("Inter", 12, "bold")).pack(side="right")
        self.section_title("📅 Bahar Yarıyılı (Detaylı)")
        b_f = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20); b_f.pack(fill="x")
        b_ev = [("Derslerin Başlaması", "09 Şubat 2026"), ("Ara Sınavlar (Vize)", "06-17 Nisan 2026"), ("23 Nisan Bayram Tatili", "23 Nisan 2026"), ("Derslerin Bitimi", "22 Mayıs 2026"), ("Final Sınavları", "01-12 Haziran 2026"), ("Bütünleme Sınavları", "22-27 Haziran 2026"), ("Tek Ders Sınavı", "17 Temmuz 2026")]
        for a, d in b_ev:
            r = ctk.CTkFrame(b_f, fg_color="transparent"); r.pack(fill="x", padx=20, pady=6)
            ctk.CTkLabel(r, text=f"• {a}").pack(side="left"); ctk.CTkLabel(r, text=d, font=("Inter", 12, "bold")).pack(side="right")

    def create_card(self, master, title, val, color):
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=20, width=220, height=110); card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, text_color="gray", font=("Inter", 12)).pack(pady=(20, 0))
        ctk.CTkLabel(card, text=val, text_color=color, font=("Inter", 24, "bold")).pack(); return card

    def section_title(self, text):
        ctk.CTkLabel(self.content_frame, text=text, font=("Inter", 20, "bold"), text_color="#1e1b4b").pack(anchor="w", pady=(10, 15))

    def clear_content(self):
        for w in self.content_frame.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = ModernSMS()
    app.mainloop()