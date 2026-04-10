class KBS:
    def __init__(self):
        # قاعدة المعرفة: استهلاك الأجهزة بالكيلوواط في الساعة لكل ساعة تشغيل
        self.Base_system = {
            "مكيف الهواء": 2.5,
            "الثلاجة": 0.15,
            "السخان الكهربائي": 3.0,
            "الغسالة": 0.5,
            "الإضاءة (LED)": 0.01,
            "الإضاءة (فلوريسنت)": 0.05,
            "التلفاز": 0.1,
            "الكمبيوتر": 0.2
        }
        self.Recomendation = []

    def Account_consumption(self, الأجهزة):
        total_consumption = 0
        for device, (count, hours) in الأجهزة.items():
            if device in self.Base_system:
                device_consumption = self.Base_system[device] * count * hours
                total_consumption += device_consumption
                if device_consumption > 5:
                    self.Recomendation.append(f"🔹 {device} يستهلك طاقة عالية، حاول تقليل تشغيله.")

        return total_consumption

    def git_recomendation(self):
        if not self.Recomendation:
            return "✅ استهلاكك للطاقة ضمن النطاق الطبيعي. استمر في ذلك!"
        else:
            return "\n".join(self.Recomendation)


# 🛠️ تجربة النظام
Power_system = KBS()

# إدخال بيانات الأجهزة (عدد الأجهزة وساعات تشغيلها يوميًا)
Input_devices = {
    "مكيف الهواء": (2, 8),
    "الثلاجة": (1, 24),
    "السخان الكهربائي": (1, 3),
    "الغسالة": (1, 2),
    "الإضاءة (LED)": (10, 5),
    "التلفاز": (1, 6),
    "الكمبيوتر": (2, 8)
}

# حساب الاستهلاك
totaltotal_consumption = Power_system.Account_consumption(Input_devices)
system_recomendation = Power_system.git_recomendation()
# عرض النتائج
print(f"🔹 إجمالي استهلاك الطاقة اليومي: {totaltotal_consumption:.2f} كيلوواط في الساعة")
print(system_recomendation)