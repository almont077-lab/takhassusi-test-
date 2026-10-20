import re
import streamlit as st

st.set_page_config(page_title="تخصصي", page_icon="🎓", layout="wide")

STUDENT_GUIDE_URL = "https://heac.gov.om/admission/first-university-stage"
VOCATIONAL_GUIDE_URLS = {
    "تقنية المعلومات (BTEC)": "https://home.moe.gov.om/ar/topics/1/show/11909?GetLang=ar",
    "ريادة الأعمال (BTEC)": "https://home.moe.gov.om/ar/topics/1/show/11909?GetLang=ar",
    "السفر والسياحة (BTEC)": "https://home.moe.gov.om/ar/topics/16/show/13256?GetLang=ar",
    "هندسة التصنيع الميكانيكية": "https://home.moe.gov.om/ar/library/0/show/1446/",
    "الصيانة الهندسية": "https://home.moe.gov.om/ar/library/0/show/1443/",
    "صيانة المنشآت الصلبة": "https://home.moe.gov.om/ar/library/0/show/1445/",
    "اللحام وتشكيل المعادن": "https://home.moe.gov.om/ar/library/0/show/1444/",
    "عمليات الرفع والتنزيل": "https://home.moe.gov.om/ar/library/0/show/1441/",
    "الصحة والسلامة المهنية": "https://home.moe.gov.om/ar/library/0/show/1442/",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Cairo',sans-serif;}
.stApp {direction:rtl;text-align:right;background:
 radial-gradient(ellipse at 12% 3%,rgba(32,125,104,.24),transparent 31%),
 radial-gradient(ellipse at 92% 30%,rgba(255,77,83,.10),transparent 27%),#0c1118;color:#f4f7f8;}
[data-testid="stAppViewContainer"] {background:transparent;}
[data-testid="stHeader"] {background:rgba(12,17,24,.68);}
.block-container {max-width:1380px;padding-top:2rem;padding-bottom:3rem;}
h1,h2,h3,p,label {text-align:right;}
h1,h2,h3 {letter-spacing:-.3px;}
[data-testid="stSidebar"] {direction:rtl;text-align:right;background:linear-gradient(180deg,#202831,#171d26);border-left:1px solid rgba(255,255,255,.08);}
[data-testid="stSidebar"] > div {background:transparent;}
.assistant-badge {width:54px;height:54px;border-radius:18px;background:linear-gradient(135deg,#1b816e,#36b79a);color:white;
 display:flex;align-items:center;justify-content:center;font-size:27px;margin:4px 0 12px auto;box-shadow:0 8px 24px #0b5d4e55;}
.hero {position:relative;overflow:hidden;padding:2rem 2.2rem;border:1px solid rgba(255,255,255,.12);border-radius:24px;
 background:linear-gradient(115deg,rgba(18,59,54,.97),rgba(23,107,93,.92) 57%,rgba(28,133,111,.9));
 color:white;box-shadow:0 18px 48px rgba(0,0,0,.22);}
.hero:after {content:'✦';position:absolute;left:5%;top:3%;font-size:6rem;color:#ffffff12;transform:rotate(-12deg);}
.hero-kicker {font-size:.9rem;color:#bcefe2;font-weight:700;margin-bottom:.3rem;}
.hero h1 {font-size:2.6rem;margin:.1rem 0 .45rem;}
.hero p {font-size:1.08rem;color:#e6fff7;margin:0;}
.feature-card {height:100%;min-height:116px;padding:1rem 1.1rem;border-radius:18px;
 background:linear-gradient(145deg,rgba(31,42,54,.94),rgba(21,30,40,.94));
 border:1px solid rgba(255,255,255,.09);box-shadow:0 10px 26px rgba(0,0,0,.12);}
.feature-card strong {display:block;font-size:1.03rem;color:#a8ead9;margin:.2rem 0 .35rem;}
.feature-card span {font-size:.88rem;color:#c3ccd3;line-height:1.7;}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:18px!important;border-color:rgba(255,255,255,.14)!important;background:rgba(20,27,36,.58);}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"],[data-testid="stMultiSelect"] {border-radius:12px;}
div.stButton > button {border-radius:12px;border:1px solid rgba(255,255,255,.16);font-weight:700;transition:all .18s ease;}
div.stButton > button:hover {transform:translateY(-1px);border-color:#54c6a8;color:#b6f3e2;box-shadow:0 7px 18px rgba(10,120,95,.18);}
div.stButton > button[kind="primary"] {background:linear-gradient(100deg,#fa4d58,#e83f55);border:0;color:white;}
[data-testid="stProgressBar"] > div > div {background:linear-gradient(90deg,#25a98c,#8be0b9);}
[data-testid="stMetric"] {background:rgba(25,37,47,.7);padding:.8rem 1rem;border-radius:14px;}
hr {border-color:rgba(255,255,255,.12);}
[data-testid="stPopover"] {position:fixed!important;left:18px!important;right:auto!important;bottom:20px!important;top:auto!important;z-index:9999!important;}
[data-testid="stPopoverButton"] button {width:60px!important;height:60px!important;min-height:60px!important;padding:0!important;border-radius:50%!important;
 background:linear-gradient(135deg,#178c75,#35b99a)!important;color:white!important;border:2px solid #c0fff0!important;
 box-shadow:0 8px 28px rgba(0,0,0,.4)!important;font-size:27px!important;}
[data-testid="stPopoverButton"] button:hover {transform:scale(1.06);}
[data-testid="stPopoverContent"] {width:min(92vw,420px)!important;max-height:76vh!important;overflow-y:auto!important;}
@media (max-width: 760px) {
 .block-container {padding: .8rem .8rem 5.5rem!important;}
 .hero {padding:1.25rem 1rem;border-radius:18px;}
 .hero h1 {font-size:1.8rem;}
 .hero p {font-size:.96rem;line-height:1.7;}
 .feature-card {min-height:unset;padding:.8rem .9rem;}
 [data-testid="stHorizontalBlock"] {flex-wrap:wrap!important;gap:.55rem!important;}
 [data-testid="stHorizontalBlock"] > [data-testid="column"] {flex:1 1 100%!important;min-width:100%!important;}
 [data-testid="stTextInput"] input,[data-testid="stNumberInput"] input {font-size:16px!important;min-height:46px;}
 [data-testid="stMultiSelect"] [role="combobox"] {min-height:46px;}
 div.stButton > button {min-height:48px;}
 [data-testid="stPopover"] {left:12px!important;bottom:calc(14px + env(safe-area-inset-bottom))!important;}
 [data-testid="stPopoverButton"] button {width:62px!important;height:62px!important;min-height:62px!important;}
 [data-testid="stPopoverContent"] {width:min(92vw,390px)!important;max-height:70vh!important;}
}
</style>
""", unsafe_allow_html=True)

PROGRAMS = {
    "الكلية العسكرية التقنية – هندسة النظم": {"مواد": ["الرياضيات", "الفيزياء", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "العمل الجماعي", "العمل الميداني"], "متطلبات الدليل": "تشمل برامج مثل MT001 وMT002. يذكر دليل 2026/2027 النجاح في دبلوم التعليم العام و55% في الرياضيات المتقدمة أو الأساسية والفيزياء واللغة الإنجليزية."},
    "الكلية العسكرية التقنية – هندسة نظم المعلومات": {"مواد": ["الرياضيات", "الفيزياء", "تقنية المعلومات", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "التقنية", "البرمجة", "الأمن السيبراني", "العمل الجماعي"], "متطلبات الدليل": "تظهر هندسة نظم المعلومات ضمن برامج عسكرية مقرونة بالتشغيل. راجع رمز البرنامج والحد الأدنى المحدد له في دليل 2026/2027."},
    "الكلية العسكرية التقنية – هندسة الطيران (سلاح الجو)": {"مواد": ["الرياضيات", "الفيزياء", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "الطيران", "العمل الميداني", "العمل الجماعي"], "متطلبات الدليل": "برنامج MT003؛ يذكر دليل 2026/2027 النجاح في دبلوم التعليم العام و60% في الرياضيات المتقدمة أو الأساسية والفيزياء واللغة الإنجليزية. وقد توجد اختبارات ومتطلبات إضافية."},
    "الكلية العسكرية التقنية – هندسة بحرية (البحرية السلطانية)": {"مواد": ["الرياضيات", "الفيزياء", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "العمل الميداني", "العمل الجماعي"], "متطلبات الدليل": "برنامج MT004؛ يذكر دليل 2026/2027 النجاح في دبلوم التعليم العام و55% في الرياضيات المتقدمة أو الأساسية والفيزياء واللغة الإنجليزية. وقد توجد اختبارات ومتطلبات إضافية."},
    "الكلية العسكرية التقنية – هندسة مدنية ومسح الكميات": {"مواد": ["الرياضيات", "الفيزياء", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "الهندسة", "التصميم", "العمل الميداني", "العمل الجماعي"], "متطلبات الدليل": "تتوفر برامج مرتبطة بجهات عسكرية وهندسية؛ يجب مطابقة رمز البرنامج والجهة والحد الأدنى في دليل 2026/2027."},
    "الكلية العسكرية التقنية – هندسة الجيوماتكس": {"مواد": ["الرياضيات", "الفيزياء", "اللغة الإنجليزية"], "اهتمامات": ["القيادة", "الانضباط", "خدمة الوطن", "الهندسة", "التقنية", "العمل الميداني", "العمل الجماعي"], "متطلبات الدليل": "برنامج هندسة جيوماتكس ضمن برامج الكلية العسكرية التقنية؛ راجع شروط البرنامج والجهة المستفيدة في دليل 2026/2027."},
    "الطب – جامعة الخليج العربي (SE818)": {
        "مواد": ["الأحياء", "الكيمياء", "الفيزياء", "الرياضيات", "مهارات اللغة الإنجليزية"],
        "اهتمامات": ["الصحة", "مساعدة الناس", "البحث"],
        "متطلبات الدليل": "منحة خارجية. دليل 2026/2027 يذكر معدلًا عامًا لا يقل عن 95%، و90% في الكيمياء والأحياء والفيزياء والرياضيات المتقدمة، و95% في الإنجليزية.",
        "حدود رسمية": {"معدل": 95, "مواد": {"الكيمياء": 90, "الأحياء": 90, "الفيزياء": 90, "مهارات اللغة الإنجليزية": 95}, "بديل": [], "رياضيات متقدمة": 90},
    },
    "الطب – الكلية الملكية للجراحين في البحرين (SE819)": {
        "مواد": ["الأحياء", "الكيمياء", "الفيزياء", "الرياضيات", "مهارات اللغة الإنجليزية"],
        "اهتمامات": ["الصحة", "مساعدة الناس", "البحث"],
        "متطلبات الدليل": "منحة خارجية. دليل 2026/2027 يذكر معدلًا عامًا لا يقل عن 95%، و90% في الكيمياء والأحياء، و85% في الفيزياء أو الرياضيات المتقدمة، و85% في الإنجليزية.",
        "حدود رسمية": {"معدل": 95, "مواد": {"الكيمياء": 90, "الأحياء": 90, "مهارات اللغة الإنجليزية": 85}, "بديل": [("الفيزياء", 85), ("الرياضيات المتقدمة", 85)]},
    },
    "التمريض": {"مواد": ["الأحياء", "اللغة الإنجليزية"], "اهتمامات": ["الصحة", "مساعدة الناس", "التواصل"]},
    "الصيدلة": {"مواد": ["الكيمياء", "الأحياء"], "اهتمامات": ["الصحة", "الكيمياء", "البحث"]},
    "الهندسة": {"مواد": ["الرياضيات", "الفيزياء"], "اهتمامات": ["التقنية", "التصميم", "حل المشكلات"]},
    "علوم الحاسوب والذكاء الاصطناعي": {"مواد": ["الرياضيات", "تقنية المعلومات", "اللغة الإنجليزية"], "اهتمامات": ["التقنية", "البرمجة", "حل المشكلات"]},
    "الأمن السيبراني": {"مواد": ["الرياضيات", "تقنية المعلومات"], "اهتمامات": ["التقنية", "البرمجة", "حل المشكلات"]},
    "إدارة الأعمال": {"مواد": ["الرياضيات", "اللغة الإنجليزية"], "اهتمامات": ["الأعمال", "القيادة", "التواصل"]},
    "المحاسبة والمالية": {"مواد": ["الرياضيات", "اللغة الإنجليزية"], "اهتمامات": ["الأعمال", "الأرقام", "الاقتصاد"]},
    "القانون": {"مواد": ["اللغة العربية", "اللغة الإنجليزية", "التاريخ والجغرافيا"], "اهتمامات": ["القانون", "القراءة والكتابة", "مساعدة الناس"]},
    "التربية": {"مواد": ["اللغة العربية", "اللغة الإنجليزية"], "اهتمامات": ["التعليم", "مساعدة الناس", "التواصل"]},
    "الإعلام والاتصال": {"مواد": ["اللغة العربية", "اللغة الإنجليزية"], "اهتمامات": ["الإعلام", "الكتابة", "التصميم"]},
    "العلوم البيئية": {"مواد": ["الأحياء", "الكيمياء", "العلوم البيئية", "الرياضيات"], "اهتمامات": ["البيئة", "البحث", "حل المشكلات"]},
    "طب الأسنان": {"مواد": ["الأحياء", "الكيمياء"], "اهتمامات": ["الصحة", "مساعدة الناس", "الدقة"]},
    "الطب البيطري": {"مواد": ["الأحياء", "الكيمياء"], "اهتمامات": ["الصحة", "البحث", "رعاية الحيوانات"]},
    "علوم المختبرات الطبية": {"مواد": ["الأحياء", "الكيمياء"], "اهتمامات": ["الصحة", "البحث", "الدقة"]},
    "الأشعة والتصوير الطبي": {"مواد": ["الفيزياء", "الأحياء"], "اهتمامات": ["الصحة", "التقنية", "مساعدة الناس"]},
    "التغذية وعلوم الغذاء": {"مواد": ["الأحياء", "الكيمياء"], "اهتمامات": ["الصحة", "البحث", "البيئة"]},
    "الهندسة المدنية": {"مواد": ["الرياضيات", "الفيزياء"], "اهتمامات": ["التصميم", "حل المشكلات", "البيئة"]},
    "الهندسة الكهربائية": {"مواد": ["الرياضيات", "الفيزياء", "تقنية المعلومات"], "اهتمامات": ["التقنية", "حل المشكلات", "البحث"]},
    "الهندسة الميكانيكية": {"مواد": ["الرياضيات", "الفيزياء"], "اهتمامات": ["التقنية", "التصميم", "حل المشكلات"]},
    "هندسة النفط والغاز": {"مواد": ["الرياضيات", "الفيزياء", "الكيمياء"], "اهتمامات": ["التقنية", "البحث", "حل المشكلات"]},
    "هندسة البرمجيات": {"مواد": ["الرياضيات", "تقنية المعلومات", "اللغة الإنجليزية"], "اهتمامات": ["التقنية", "البرمجة", "حل المشكلات"]},
    "علم البيانات": {"مواد": ["الرياضيات", "تقنية المعلومات"], "اهتمامات": ["التقنية", "الأرقام", "البحث", "حل المشكلات"]},
    "نظم المعلومات": {"مواد": ["الرياضيات", "تقنية المعلومات", "اللغة الإنجليزية"], "اهتمامات": ["التقنية", "الأعمال", "حل المشكلات"]},
    "الكيمياء التطبيقية": {"مواد": ["الكيمياء", "الرياضيات"], "اهتمامات": ["البحث", "البيئة", "حل المشكلات"]},
    "إدارة التسويق": {"مواد": ["اللغة العربية", "اللغة الإنجليزية", "الرياضيات"], "اهتمامات": ["الأعمال", "التواصل", "التصميم", "الكتابة"]},
    "إدارة الموارد البشرية": {"مواد": ["اللغة العربية", "اللغة الإنجليزية"], "اهتمامات": ["الأعمال", "القيادة", "التواصل", "مساعدة الناس"]},
    "اللوجستيات وسلاسل الإمداد": {"مواد": ["الرياضيات", "تقنية المعلومات", "اللغة الإنجليزية"], "اهتمامات": ["الأعمال", "الأرقام", "التقنية", "حل المشكلات"]},
    "السياحة والضيافة": {"مواد": ["اللغة العربية", "اللغة الإنجليزية", "التاريخ والجغرافيا"], "اهتمامات": ["التواصل", "اللغات", "السفر والسياحة", "الأعمال"]},
    "علم النفس": {"مواد": ["اللغة العربية", "اللغة الإنجليزية", "الأحياء"], "اهتمامات": ["مساعدة الناس", "الصحة", "البحث", "التواصل"]},
    "الترجمة واللغات": {"مواد": ["اللغة العربية", "اللغة الإنجليزية"], "اهتمامات": ["اللغات", "القراءة والكتابة", "التواصل"]},
    "العلاقات الدولية": {"مواد": ["اللغة العربية", "اللغة الإنجليزية", "التاريخ والجغرافيا"], "اهتمامات": ["القيادة", "اللغات", "التواصل", "القراءة والكتابة"]},
}
SCIENCE_SUBJECTS = ["الأحياء", "الكيمياء", "الفيزياء", "العلوم البيئية"]
ELECTIVE_SUBJECTS = [
    "الأحياء", "الكيمياء", "الفيزياء", "العلوم البيئية",
    "مهارات اللغة الإنجليزية", "تقنية المعلومات", "الجغرافيا والتقنيات الحديثة",
    "التاريخ (العالم من حولي)", "اللغة الألمانية", "اللغة الفرنسية", "اللغة الصينية",
    "الرياضة المدرسية", "الفنون التشكيلية", "المهارات الموسيقية",
]
GRADE_SUBJECTS = [
    "الرياضيات", "الفيزياء", "الكيمياء", "الأحياء", "العلوم البيئية",
    "تقنية المعلومات", "مهارات اللغة الإنجليزية", "اللغة العربية",
    "الجغرافيا والتقنيات الحديثة", "التاريخ (العالم من حولي)",
]
SUBJECT_ALIASES = {
    "مهارات اللغة الإنجليزية": "اللغة الإنجليزية",
    "الجغرافيا والتقنيات الحديثة": "التاريخ والجغرافيا",
    "التاريخ (العالم من حولي)": "التاريخ والجغرافيا",
}
VOCATIONAL_RELEVANT_SUBJECTS = {
    "تقنية المعلومات (BTEC)": ["تقنية المعلومات", "الرياضيات", "مهارات اللغة الإنجليزية"],
    "ريادة الأعمال (BTEC)": ["الرياضيات", "مهارات اللغة الإنجليزية", "تقنية المعلومات"],
    "السفر والسياحة (BTEC)": ["مهارات اللغة الإنجليزية", "الجغرافيا والتقنيات الحديثة", "اللغة العربية"],
    "هندسة التصنيع الميكانيكية": ["الرياضيات", "الفيزياء", "تقنية المعلومات"],
    "الصيانة الهندسية": ["الرياضيات", "الفيزياء", "تقنية المعلومات"],
    "صيانة المنشآت الصلبة": ["الرياضيات", "الفيزياء", "تقنية المعلومات"],
    "اللحام وتشكيل المعادن": ["الرياضيات", "الفيزياء"],
    "عمليات الرفع والتنزيل": ["الرياضيات", "الفيزياء", "العلوم البيئية"],
    "الصحة والسلامة المهنية": ["الأحياء", "الكيمياء", "الفيزياء", "العلوم البيئية"],
}
INTERESTS = [
    "الطب", "الصحة", "التمريض", "مساعدة الناس", "علم النفس", "البحث العلمي", "المختبرات",
    "الأحياء", "العلوم الحيوية", "الكيمياء", "الفيزياء", "الرياضيات",
    "التقنية", "الكمبيوتر والحاسوب", "علوم الحاسوب", "تقنية المعلومات", "البرمجة", "الذكاء الاصطناعي", "الأمن السيبراني", "الروبوتات", "الشبكات", "تطوير التطبيقات",
    "الهندسة", "الكهرباء", "الميكانيكا", "الصيانة", "الطيران", "السيارات", "الطاقة",
    "التصميم", "الرسم والفنون", "الهندسة المعمارية", "الكتابة", "القراءة", "الإعلام", "التصوير",
    "التعليم", "اللغات", "الترجمة", "التواصل", "القانون", "التاريخ", "الجغرافيا",
    "الأعمال", "ريادة الأعمال", "التسويق", "المحاسبة", "المالية", "الاقتصاد", "الأرقام",
    "القيادة", "الانضباط", "خدمة الوطن", "العسكرية والأمنية", "إدارة المشاريع", "اللوجستيات", "السياحة والسفر", "الضيافة", "البيئة",
    "الزراعة", "الحيوانات", "الرياضة", "العمل العملي", "حل المشكلات", "الدقة", "التنظيم",
    "العمل الجماعي", "الابتكار", "العمل الميداني",
]


def matching_interest_terms(selected, related, subjects=()):
    """Match custom phrases such as 'القيادة والانضباط' to catalogue interests."""
    def normalize(value):
        value = value.strip().replace("وال", "ال")
        if value.startswith("و") and len(value) > 3:
            value = value[1:]
        if value.startswith("ال"):
            value = value[2:]
        return value.replace(" ", "")

    expansions = {
        "احياء": ["الأحياء", "العلوم الحيوية"],
        "علومحيوية": ["الأحياء", "العلوم الحيوية"],
        "الكيمياء": ["الكيمياء"],
        "الفيزياء": ["الفيزياء"],
        "الرياضيات": ["الرياضيات"],
        "الهندسة": ["الهندسة", "حل المشكلات", "التصميم"],
        "الطب": ["الطب", "الصحة"],
        "الصحة": ["الصحة", "الطب", "التمريض"],
        "المختبرات": ["المختبرات", "البحث العلمي"],
        "البرمجة": ["البرمجة", "التقنية"],
        "الذكاءالاصطناعي": ["الذكاء الاصطناعي", "التقنية", "البرمجة"],
        "الكمبيوتر": ["الكمبيوتر", "الحاسوب", "علوم الحاسوب", "تقنية المعلومات", "البرمجة"],
        "كمبيوتر": ["الكمبيوتر", "الحاسوب", "علوم الحاسوب", "تقنية المعلومات", "البرمجة"],
        "الحاسوب": ["الكمبيوتر", "الحاسوب", "علوم الحاسوب", "تقنية المعلومات", "البرمجة"],
        "الحاسب": ["الكمبيوتر", "الحاسوب", "علوم الحاسوب", "تقنية المعلومات", "البرمجة"],
        "الشبكات": ["الشبكات", "تقنية المعلومات", "الأمن السيبراني"],
        "تطويرالتطبيقات": ["البرمجة", "تقنية المعلومات", "علوم الحاسوب"],
    }
    related_terms = list(related) + list(subjects)
    normalized_related = [normalize(value) for value in related_terms]
    matched = []
    for choice in selected:
        # Split common custom phrases (e.g. "القيادة والانضباط") into their ideas.
        atoms = [part.strip() for part in re.split(r"[،,;/+]|(?<=\S)و(?=ال)|\s+و\s*", choice) if part.strip()]
        for atom in atoms:
            atom_norm = normalize(atom)
            wanted = expansions.get(atom_norm, [atom])
            normalized_wanted = [normalize(value) for value in wanted]
            if any(
                wanted_term in related_term or related_term in wanted_term
                for wanted_term in normalized_wanted
                for related_term in normalized_related
                if wanted_term and related_term
            ):
                matched.append(choice)
                break
    return sorted(set(matched))


def grade_weight(program_name, subject):
    """Give each entered grade a weight that reflects the program's core study area."""
    name = program_name.replace(" ", "")
    subject = SUBJECT_ALIASES.get(subject, subject)
    health = any(term in name for term in ("الطب", "التمريض", "الصيدلة", "الأسنان", "المختبراتالطبية", "الأشعة", "التغذية", "البيطري"))
    engineering = any(term in name for term in ("هندسة", "الهندسي", "الجيوماتكس", "الطيران", "الميكانيكية"))
    computing = any(term in name for term in ("الحاسوب", "المعلومات", "السيبراني", "البيانات", "البرمجيات", "الذكاءالاصطناعي"))
    if health:
        return {"الأحياء": 1.5, "الكيمياء": 1.3, "الفيزياء": 0.7, "الرياضيات": 0.6,
                "مهارات اللغة الإنجليزية": 0.7, "اللغة الإنجليزية": 0.7}.get(subject, 1.0)
    if engineering:
        weights = {"الرياضيات": 1.5, "الفيزياء": 1.4, "الكيمياء": 0.8, "تقنية المعلومات": 0.7,
                   "الأحياء": 0.25, "مهارات اللغة الإنجليزية": 0.6, "اللغة الإنجليزية": 0.6}
        if any(term in name for term in ("الكيميائية", "النفط", "الغاز")):
            weights["الكيمياء"] = 1.25
        return weights.get(subject, 1.0)
    if computing:
        return {"تقنية المعلومات": 1.5, "الرياضيات": 1.2, "مهارات اللغة الإنجليزية": 0.8,
                "اللغة الإنجليزية": 0.8}.get(subject, 1.0)
    if any(term in name for term in ("الأحياء", "الحيوية", "البيئية", "الزراعة", "الحيوان")):
        return {"الأحياء": 1.5, "الكيمياء": 1.2, "العلوم البيئية": 1.2, "الرياضيات": 0.6}.get(subject, 1.0)
    return 1.0


def rank_academic_programs(average, selected_subjects, interests, subject_grades, math_choice, math_grade, academic_preference):
    """Use one deterministic grade + elective + interest score for both results and Gemini."""
    selected = {SUBJECT_ALIASES.get(subject, subject) for subject in selected_subjects}
    ranked, unmet_official = [], []
    for name, data in PROGRAMS.items():
        related_subjects = [SUBJECT_ALIASES.get(subject, subject) for subject in data["مواد"]]
        matching_subjects = sorted(selected & set(related_subjects))
        matching_interests = matching_interest_terms(interests, data["اهتمامات"], related_subjects)
        grade_pairs = []
        for subject in data["مواد"]:
            grade_key = SUBJECT_ALIASES.get(subject, subject)
            if grade_key == "الرياضيات":
                if math_grade is not None:
                    grade_pairs.append((subject, math_grade))
            else:
                actual_key = next((key for key in subject_grades if SUBJECT_ALIASES.get(key, key) == grade_key), None)
                if actual_key:
                    grade_pairs.append((subject, subject_grades[actual_key]))
        weights = [grade_weight(name, subject) for subject, _ in grade_pairs]
        grade_match = (sum(grade * weight for (_, grade), weight in zip(grade_pairs, weights)) / sum(weights)) if weights else 50
        total_weight = sum(grade_weight(name, subject) for subject in data["مواد"])
        grade_coverage = (sum(weights) / total_weight) if total_weight else 0
        elective_match = len(matching_subjects) / max(1, len(selected)) if selected else 0.5
        interest_match = len(matching_interests) / max(1, len(interests)) if interests else 0.5
        science_program = any(subject in related_subjects for subject in ("الأحياء", "الكيمياء", "الفيزياء", "الرياضيات"))
        literary_program = any(term in name for term in ("القانون", "التربية", "الإعلام", "الترجمة", "اللغات", "العلاقات الدولية", "التاريخ", "السياحة"))
        preference_match = 100 if (academic_preference == "علمي" and science_program) or (academic_preference == "أدبي" and literary_program) else 50
        # Missing grades are neutral and lower confidence; they are never silently treated as 80%.
        evidence_grade = 50 + (grade_match - 50) * grade_coverage
        score = round(evidence_grade * 0.65 + interest_match * 100 * 0.15
                      + elective_match * 100 * 0.10 + average * 0.05 + preference_match * 0.05)
        # Explicit computing interests should reliably bring computing degrees into view,
        # even when the student has many other interests selected at the same time.
        normalized_name = name.replace(" ", "")
        computing_program = any(term in normalized_name for term in (
            "الحاسوب", "المعلومات", "السيبراني", "البيانات", "البرمجيات", "الذكاءالاصطناعي", "نظمالمعلومات"
        ))
        computing_interest_words = (
            "التقنية", "الكمبيوتر", "الحاسوب", "علومالحاسوب", "تقنيةالمعلومات", "البرمجة",
            "الذكاءالاصطناعي", "الأمنالسيبراني", "الروبوتات", "الشبكات", "تطويرالتطبيقات",
        )
        has_computing_interest = any(
            any(word in choice.replace(" ", "") for word in computing_interest_words)
            for choice in interests
        )
        if computing_program and has_computing_interest:
            score += 18
        # Interest matching can return several synonyms for one selected interest.
        # Keep the displayed percentage within Streamlit's accepted 0–100 range.
        score = max(0, min(100, score))
        reasons = []
        if matching_subjects:
            reasons.append("موادك الاختيارية المرتبطة: " + "، ".join(matching_subjects))
        if grade_pairs:
            reasons.append("درجات المواد الأساسية: " + "، ".join(f"{subject} {grade}%" for subject, grade in grade_pairs))
        missing = [subject for subject in data["مواد"] if not any(SUBJECT_ALIASES.get(key, key) == SUBJECT_ALIASES.get(subject, subject) for key, _ in grade_pairs)]
        if missing:
            reasons.append("درجات لم تدخلها بعد: " + "، ".join(missing))
        if matching_interests:
            reasons.append("ميول متوافقة: " + "، ".join(matching_interests))
        if preference_match == 100:
            reasons.append("يناسب اختيارك للمسار " + academic_preference)
        if grade_pairs and min(grade for _, grade in grade_pairs) < 60:
            low_subject, low_grade = min(grade_pairs, key=lambda pair: pair[1])
            reasons.append(f"انخفض التوافق بسبب {low_subject} ({low_grade}%). هذا ليس حد قبول رسميًا.")
        if data.get("متطلبات الدليل"):
            reasons.append("من دليل الطالب 2026/2027: " + data["متطلبات الدليل"])
        if data.get("حدود رسمية"):
            shortfalls = official_requirement_gaps(data, average, subject_grades, math_choice, math_grade)
            if shortfalls:
                unmet_official.append((name, shortfalls, data["متطلبات الدليل"]))
                continue
            reasons.append("الدرجات تحقق الحدود الدنيا المذكورة في الدليل؛ القبول غير مضمون ويعتمد على المفاضلة والمقاعد.")
        ranked.append((score, name, "؛ ".join(reasons) or "توافق عام؛ أضف ميولًا أو درجات أكثر لزيادة دقة الترتيب."))
    return sorted(ranked, reverse=True), unmet_official


def official_requirement_gaps(data, average, subject_grades, math_choice, math_grade):
    """Return missing or unmet documented minimums; do not treat tie-breaks as admission gates."""
    requirements = data.get("حدود رسمية")
    if not requirements:
        return []
    gaps = []
    if average < requirements["معدل"]:
        gaps.append(f"المعدل العام {average}% أقل من {requirements['معدل']}%")
    for subject, minimum in requirements["مواد"].items():
        grade_subject = SUBJECT_ALIASES.get(subject, subject)
        if grade_subject not in subject_grades:
            gaps.append(f"لم تُدخل درجة {subject}")
        elif subject_grades[grade_subject] < minimum:
            gaps.append(f"{subject} {subject_grades[grade_subject]}% (المطلوب {minimum}%)")
    advanced_math_minimum = requirements.get("رياضيات متقدمة")
    if advanced_math_minimum:
        if math_choice != "الرياضيات المتقدمة":
            gaps.append("يشترط اختيار الرياضيات المتقدمة")
        elif math_grade is None:
            gaps.append("لم تُدخل درجة الرياضيات المتقدمة")
        elif math_grade < advanced_math_minimum:
            gaps.append(f"الرياضيات المتقدمة {math_grade}% (المطلوب {advanced_math_minimum}%)")
    alternatives = requirements["بديل"]
    alternative_met = not alternatives or any(
        (subject == "الرياضيات المتقدمة" and math_choice == subject and math_grade is not None and math_grade >= minimum)
        or (subject != "الرياضيات المتقدمة" and subject in subject_grades and subject_grades[subject] >= minimum)
        for subject, minimum in alternatives
    )
    if alternatives and not alternative_met:
        gaps.append("لم تتحقق درجة الحد الأدنى في الفيزياء أو الرياضيات المتقدمة")
    return gaps


TECHNICAL_SPECIALTIES = {
    "تقنية المعلومات (BTEC)": {
        "وصف": "تخصص تقني تطبيقي، وتختلف وحداته ومجالاته التفصيلية حسب المدرسة والبرنامج.",
        "اهتمامات": ["التقنية", "البرمجة", "حل المشكلات", "التصميم"],
    },
    "ريادة الأعمال (BTEC)": {
        "وصف": "يركز على أفكار المشاريع والعمل التجاري ومهارات المبادرة.",
        "اهتمامات": ["الأعمال", "القيادة", "التواصل", "الأرقام", "الاقتصاد"],
    },
    "السفر والسياحة (BTEC)": {
        "وصف": "يرتبط بالسياحة وخدمة الزوار وتنظيم الخبرات والأنشطة السياحية.",
        "اهتمامات": ["التواصل", "القيادة", "مساعدة الناس", "اللغات", "السفر والسياحة"],
    },
    "هندسة التصنيع الميكانيكية": {
        "وصف": "التصنيع الميكانيكي ومهارات العمل على المعدات والعمليات الصناعية.",
        "اهتمامات": ["التقنية", "حل المشكلات", "التصميم", "البحث"],
    },
    "الصيانة الهندسية": {
        "وصف": "فحص المعدات والأنظمة الهندسية وصيانتها.",
        "اهتمامات": ["التقنية", "حل المشكلات", "البحث"],
    },
    "صيانة المنشآت الصلبة": {
        "وصف": "أعمال صيانة المنشآت والبنية الأساسية.",
        "اهتمامات": ["التقنية", "حل المشكلات", "التصميم"],
    },
    "اللحام وتشكيل المعادن": {
        "وصف": "تشكيل المعادن واللحام باستخدام مهارات وأدوات عملية.",
        "اهتمامات": ["التصميم", "التقنية", "حل المشكلات"],
    },
    "عمليات الرفع والتنزيل": {
        "وصف": "تشغيل ومتابعة عمليات ومعدات الرفع والتنزيل مع الاهتمام بإجراءات السلامة.",
        "اهتمامات": ["التقنية", "حل المشكلات", "القيادة"],
    },
    "الصحة والسلامة المهنية": {
        "وصف": "التعرّف على السلامة في بيئات العمل والوقاية من المخاطر المهنية.",
        "اهتمامات": ["الصحة", "مساعدة الناس", "البحث", "حل المشكلات"],
    },
}

st.markdown('''<div class="hero"><div class="hero-kicker">خطوتك الأولى لاختيار مستقبلك</div>
<h1>🎓 تخصصي</h1><p>اكتشف مسارك، قارن التخصصات، وخذ فكرة أوضح عن الخيارات المناسبة لك.</p></div>''', unsafe_allow_html=True)
st.write("")
feature_columns = st.columns(3)
feature_cards = [
    ("🧭", "اختر مسارك", "أكاديمي أو مهني وتقني، واستكشف الخيارات المناسبة لكل مسار."),
    ("📊", "أدخل درجاتك", "المعدل ودرجات المواد تساعد على ترتيب الاقتراحات بشكل أوضح."),
    ("✨", "اكتشف الأنسب", "شاهد أفضل 20 اقتراحًا، أو اطلب من Gemini ترتيبها حسب اهتماماتك."),
]
for column, (icon, title, description) in zip(feature_columns, feature_cards):
    with column:
        st.markdown(
            f'<div class="feature-card"><strong>{icon} {title}</strong><span>{description}</span></div>',
            unsafe_allow_html=True,
        )
st.write("")

# Gemini API key is read from Streamlit Secrets on the hosted app.
with st.popover("💬", help="اضغط هنا لفتح مساعد التخصص الذكي"):
    st.markdown('<div class="assistant-badge">💬</div>', unsafe_allow_html=True)
    st.subheader("مساعد التخصص الذكي")
    st.caption("اسأل عن التخصصات أو المواد أو المسارات الدراسية. يساعدك Gemini على فهم الخيارات ومقارنتها، والاختيار النهائي لك.")
    try:
        saved_api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        saved_api_key = ""
    api_key = saved_api_key
    if not api_key:
        st.warning("أضف المفتاح مرة واحدة من Manage app ← Settings ← Secrets باسم GEMINI_API_KEY.")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for role, message in st.session_state.chat[-4:]:
        with st.chat_message(role):
            st.write(message)
    with st.form("assistant_form", clear_on_submit=True):
        question = st.text_input("اكتب سؤالك", placeholder="مثال: وش يناسبني إذا أحب التقنية؟")
        ask = st.form_submit_button("إرسال", use_container_width=True)
    if ask and question.strip():
        q = question.strip()
        try:
            from google import genai
            from google.genai import types
            if not api_key:
                answer = "لم يُضف مفتاح Gemini بعد. احفظه في Streamlit Secrets باسم GEMINI_API_KEY."
            else:
                client = genai.Client(api_key=api_key)
                prior = st.session_state.chat[-4:]
                transcript = "\n".join(
                    ("الطالب" if role == "user" else "المساعد") + ": " + message
                    for role, message in prior
                )
                transcript += "\nالطالب: " + q
                prompt = (
                    "أنت مرشد أكاديمي لطالب في سلطنة عُمان. أجب بالعربية السهلة وباختصار في 2–4 جمل. "
                    "ساعده على التفكير في التخصصات ولا تدّعِ شروط قبول محدثة أو ضمان القبول؛ ذكّره بدليل القبول عند الحاجة.\n\n" + transcript
                )
                def answer_chunks():
                    yield from client.models.generate_content_stream(
                        model="gemini-3.5-flash-lite",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=300,
                            thinking_config=types.ThinkingConfig(thinking_level="minimal"),
                        ),
                    )
                with st.chat_message("assistant"):
                    answer = st.write_stream(chunk.text for chunk in answer_chunks() if chunk.text)
                answer = (answer or "").strip() or "لم يصلني رد. جرّب صياغة السؤال مرة أخرى."
        except ImportError:
            answer = "مكتبة Gemini غير مثبتة. أعد تشغيل البرنامج بعد تحديث requirements.txt."
        except Exception as error:
            answer = "تعذر الاتصال بـ Gemini. تأكد من المفتاح والإنترنت وحدود الاستخدام في Google AI Studio. التفاصيل: " + str(error)[:300]
        st.session_state.chat.extend([("user", q), ("assistant", answer)])
        st.rerun()

st.subheader("ابدأ باختيار مسارك الدراسي")
study_path = st.radio("المسار", ["أكاديمي", "مهني وتقني"], horizontal=True)
st.caption("أدخل المعدل العام ودرجات المواد التي اخترتها؛ يستخدمها الموقع لترتيب الاقتراحات، وليس لتأكيد القبول الجامعي.")
math_choice = "غير محددة"
academic_preference = "علمي"
average = 80
strong_subjects = []
interests = []
selected_vocational = []
subject_grades = {}

if study_path == "أكاديمي":
    academic_preference = st.radio("ميولك الأكاديمية", ["علمي", "أدبي"], horizontal=True, key="academic_preference")
    st.caption("هذا الميل يساعد في التوجيه فقط، وليس شرط قبول. اختر 3 مواد اختيارية بينها مادة علوم واحدة على الأقل. اترك خانة الدرجة فارغة إذا لم تعرفها؛ لن يفترض الموقع أنها 80%. اللغات الأجنبية قد لا تتوفر في كل المدارس.")
    math_choice = st.radio("الرياضيات", ["الرياضيات المتقدمة", "الرياضيات الأساسية"], horizontal=True)
    average = st.number_input("معدلك العام (%)", min_value=0, max_value=100, value=80, step=1, key="academic_average")
    math_grade = st.number_input("درجة " + math_choice + " (%)", min_value=0, max_value=100, value=None, step=1, key="academic_math_grade_v2", placeholder="أدخل درجتك")
    strong_subjects = st.multiselect("اختر 3 مواد اختيارية", ELECTIVE_SUBJECTS, max_selections=3, placeholder="اختر المواد التي تدرسها")
    grade_subject_options = list(dict.fromkeys(SUBJECT_ALIASES.get(subject, subject) for subject in strong_subjects))
    grade_subject_options = [subject for subject in grade_subject_options if subject != "الرياضيات"]
    if math_grade is not None:
        subject_grades["الرياضيات"] = math_grade
    if grade_subject_options:
        st.markdown("**درجات المواد التي اخترتها (%)**")
        for subject in grade_subject_options:
            subject_grades[subject] = st.number_input(
                "درجة " + subject + " (%)", min_value=0, max_value=100, value=None, step=1, placeholder="أدخل درجتك",
                key="academic_grade_v2_" + subject,
            )
            if subject_grades[subject] is None:
                subject_grades.pop(subject)
    extra_grade_options = list(dict.fromkeys(
        SUBJECT_ALIASES.get(subject, subject)
        for subject in GRADE_SUBJECTS
        if SUBJECT_ALIASES.get(subject, subject) not in subject_grades
    ))
    extra_grade_subjects = st.multiselect(
        "أضف درجات مواد أخرى (اختياري؛ تفيد في ترتيب بقية التخصصات)",
        extra_grade_options,
        placeholder="اختر أي مادة تعرف درجتها",
        key="academic_extra_grade_subjects",
    )
    for subject in extra_grade_subjects:
        subject_grades[subject] = st.number_input(
            "درجة " + subject + " (%)", min_value=0, max_value=100, value=None, step=1, placeholder="أدخل درجتك",
            key="academic_extra_grade_v2_" + subject,
        )
        if subject_grades[subject] is None:
            subject_grades.pop(subject)
    interests = st.multiselect("المجالات التي تهمك", INTERESTS, placeholder="اختر مجالًا أو أكثر")
    custom_interest = st.text_input("أضف مجالًا غير موجود (اختياري)", key="academic_custom_interest", placeholder="مثال: تصميم الألعاب")
    if custom_interest.strip() and custom_interest.strip() not in interests:
        interests.append(custom_interest.strip())
    st.caption("المجال الذي تكتبه يُرسل إلى Gemini عند استخدام ترتيب الذكاء الاصطناعي.")
    submitted = st.button("اعرض التخصصات المناسبة", type="primary", use_container_width=True)
else:
    st.caption("يضم المسار تخصصات في تقنية المعلومات وريادة الأعمال والسفر والسياحة، والهندسة والصناعة. التخصصات المتاحة تختلف حسب المدرسة والمحافظة.")
    average = st.number_input("معدلك العام (%)", min_value=0, max_value=100, value=80, step=1, key="vocational_average")
    selected_vocational = st.multiselect(
        "التخصصات التي تريد المفاضلة بينها (اتركها فارغة لعرضها كلها)",
        list(TECHNICAL_SPECIALTIES),
        placeholder="اختر تخصصات، أو اتركه فارغًا لعرض الكل",
    )
    vocational_subjects = st.multiselect("اختر المواد التي عندك درجاتها", GRADE_SUBJECTS, placeholder="اختر المواد")
    if vocational_subjects:
        st.markdown("**درجات المواد المختارة (%)**")
        for subject in vocational_subjects:
            subject_grades[subject] = st.number_input(
                "درجة " + subject + " (%)", min_value=0, max_value=100, value=None, step=1,
                key="vocational_grade_v2_" + subject, placeholder="أدخل درجتك",
            )
            if subject_grades[subject] is None:
                subject_grades.pop(subject)
    interests = st.multiselect("المهارات والمجالات التي تهمك", INTERESTS, placeholder="اختر ما يناسبك")
    custom_interest = st.text_input("أضف مجالًا غير موجود (اختياري)", key="vocational_custom_interest", placeholder="مثال: صيانة الطائرات")
    if custom_interest.strip() and custom_interest.strip() not in interests:
        interests.append(custom_interest.strip())
    st.caption("المجال الذي تكتبه يُرسل إلى Gemini عند استخدام ترتيب الذكاء الاصطناعي.")
    submitted = st.button("رتّب التخصصات المهنية المناسبة", type="primary", use_container_width=True)

academic_rankings, academic_unmet = [], []
if study_path == "أكاديمي" and len(strong_subjects) == 3 and set(strong_subjects) & set(SCIENCE_SUBJECTS):
    academic_rankings, academic_unmet = rank_academic_programs(
        average, strong_subjects, interests, subject_grades, math_choice, math_grade, academic_preference
    )

st.markdown("### ترتيب أذكى بالذكاء الاصطناعي")
st.caption("يرتب Gemini التخصصات حسب معدلك ودرجات المواد واهتماماتك. قد تنفد الحصة المجانية إذا استخدمه زوار كثيرون.")
ai_rank_requested = st.button("رتّب الاقتراحات بالذكاء الاصطناعي", use_container_width=True)
if ai_rank_requested:
    st.session_state.pop("ai_rank_result", None)
    if not api_key:
        st.session_state["ai_rank_result"] = "أضف مفتاح Gemini في Streamlit Secrets أولًا."
    elif study_path == "أكاديمي" and len(strong_subjects) != 3:
        st.session_state["ai_rank_result"] = "اختر ثلاث مواد اختيارية أولًا، وبينها مادة علمية واحدة على الأقل."
    elif study_path == "أكاديمي" and not (set(strong_subjects) & set(SCIENCE_SUBJECTS)):
        st.session_state["ai_rank_result"] = "اختر مادة علمية واحدة على الأقل: أحياء أو كيمياء أو فيزياء أو علوم بيئية."
    else:
        try:
            from google import genai
            from google.genai import types

            grades_summary = "، ".join(
                f"{subject}: {grade}%" for subject, grade in subject_grades.items()
            ) or "لم يدخل درجات مواد"
            if study_path == "أكاديمي":
                catalog = "\n".join(
                    f"{rank}. {name} — توافق الموقع {score}% — سبب الترتيب: {reason}"
                    for rank, (score, name, reason) in enumerate(academic_rankings[:20], start=1)
                )
                profile = (
                    f"المسار الأكاديمي، الميل الذي يفضله الطالب {academic_preference}، المعدل {average}%، نوع الرياضيات {math_choice}، "
                    f"المواد المختارة {', '.join(strong_subjects)}، الدرجات: {grades_summary}، "
                    f"الاهتمامات: {', '.join(interests) or 'لم يحدد'}"
                )
                count_instruction = "حافظ على الترتيب والأرقام كما هي تمامًا؛ لا تعِد ترتيب التخصصات ولا تضف أو تحذف أي تخصص. اشرح سبب كل خيار باختصار."
            else:
                candidate_names = selected_vocational or list(TECHNICAL_SPECIALTIES)
                catalog = "\n".join(
                    f"- {name}: {TECHNICAL_SPECIALTIES[name]['وصف']} المواد المرتبطة: "
                    f"{', '.join(VOCATIONAL_RELEVANT_SUBJECTS[name])}; مجالات: "
                    f"{', '.join(TECHNICAL_SPECIALTIES[name]['اهتمامات'])}"
                    for name in candidate_names
                )
                profile = (
                    f"المسار المهني والتقني، المعدل {average}%، الدرجات: {grades_summary}، "
                    f"الاهتمامات: {', '.join(interests) or 'لم يحدد'}"
                )
                count_instruction = "رتّب كل التخصصات المتاحة في القائمة، ولا تضف تخصصات أخرى."

            prompt = (
                "أنت مرشد دراسي لطالب في سلطنة عُمان. استخدم قائمة التخصصات المحددة فقط، "
                "ولا تخترع أسماء أو شروط قبول. المواد المدرجة بجانب التخصصات هي ارتباطات إرشادية عامة وليست شروط قبول رسمية، "
                "كما أن الميل العلمي أو الأدبي مجرد تفضيل وليس قيدًا على الأهلية. الموقع حسب التوافق من درجات المواد والمواد الاختيارية والميول؛ "
                "أبقِ الترتيب المحسوب في القائمة كما هو ولا تغيّره بناءً على رأيك. لا ترفع أي تخصص بسبب الاهتمام وحده. "
                "إذا لم تُدخل درجة مادة مرتبطة، اذكر أن البيانات غير كافية بدل افتراض درجة مرتفعة. لا تخلط بين الملاءمة الإرشادية واستيفاء شروط دليل الطالب، "
                "ولا تدّعِ أن الطالب مؤهل أو غير مؤهل إلا إذا كانت شروط البرنامج الرسمية موجودة صراحة في البيانات. "
                + count_instruction + "\n"
                f"بيانات الطالب: {profile}\nالتخصصات المسموح بها:\n{catalog}\n"
                "أجب بالعربية الواضحة، واكتب لكل تخصص سببًا قصيرًا مرتبطًا ببيانات الطالب. "
                "لا تضمن القبول، واختم بالتنبيه إلى مراجعة شروط القبول الرسمية."
            )
            client = genai.Client(api_key=api_key)
            with st.spinner("الذكاء الاصطناعي يرتب التخصصات..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=1400,
                        thinking_config=types.ThinkingConfig(thinking_level="low"),
                    ),
                )
            st.session_state["ai_rank_result"] = (response.text or "ما وصلني ترتيب. حاول مرة أخرى.").strip()
        except ImportError:
            st.session_state["ai_rank_result"] = "مكتبة Gemini غير مثبتة. ثبّت المكتبات من requirements.txt ثم شغّل البرنامج من جديد."
        except Exception as error:
            st.session_state["ai_rank_result"] = "تعذر الاتصال بـ Gemini. راجع المفتاح والإنترنت وحدود الاستخدام في Google AI Studio. التفاصيل: " + str(error)[:300]
if st.session_state.get("ai_rank_result"):
    st.markdown(st.session_state["ai_rank_result"])

st.subheader("رتّب تخصصات من صورة")
uploaded_image = st.file_uploader(
    "ارفع صورة واضحة لقائمة التخصصات المتاحة لك",
    type=["png", "jpg", "jpeg"],
    help="استخدم صورة لقائمة التخصصات فقط، ولا ترفع بيانات شخصية أو صورًا حساسة.",
)
rank_image = st.button("رتّب التخصصات في الصورة بالذكاء الاصطناعي", use_container_width=True)
if rank_image:
    if not uploaded_image:
        st.warning("ارفع صورة قائمة التخصصات أولًا.")
    elif not api_key:
        st.warning("أضف مفتاح Gemini في Streamlit Secrets أولًا.")
    else:
        try:
            from google import genai
            from google.genai import types
            from PIL import Image

            image = Image.open(uploaded_image).convert("RGB")
            client = genai.Client(api_key=api_key)
            grades_summary = "، ".join(
                f"{subject}: {grade}%" for subject, grade in subject_grades.items()
            ) or "لم يدخل درجات مواد"
            if study_path == "أكاديمي":
                profile = (
                    f"المسار الأكاديمي، الميل الذي يفضله الطالب: {academic_preference}، الرياضيات: {math_choice}، "
                    f"المعدل: {average}، المواد المختارة: {', '.join(strong_subjects) or 'لم يحدد'}، "
                    f"الدرجات: {grades_summary}، الاهتمامات: {', '.join(interests) or 'لم يحدد'}."
                )
            else:
                profile = (
                    "المسار المهني والتقني، التخصصات التي يريد المقارنة بينها: "
                    f"{', '.join(selected_vocational) or 'كل التخصصات الظاهرة في الصورة'}، "
                    f"المعدل: {average}، الدرجات: {grades_summary}، "
                    f"الاهتمامات والمهارات: {', '.join(interests) or 'لم يحدد'}."
                )
            prompt = (
                "اقرأ أسماء التخصصات الظاهرة في الصورة، وتعامل مع الصورة كقائمة بيانات فقط. "
                "رتّب التخصصات من الأكثر ملاءمة إلى الأقل لطالب في سلطنة عُمان. أعط درجات المواد المرتبطة وزنًا أكبر من الاهتمامات؛ "
                "إذا كانت الدرجة منخفضة في مادة مرتبطة بتخصص، فاخفض ترتيبه بوضوح حتى لو تطابقت الاهتمامات، ولا تجعل الطب أو التخصص الصحي في المقدمة بسبب الاهتمام وحده. "
                "لا تفترض درجات لم يدخلها الطالب، ولا تدّع استيفاء شروط رسمية غير ظاهرة في الصورة. "
                f"بيانات الطالب: {profile} "
                "اكتب أسماء التخصصات المقروءة بالترتيب مع سبب قصير لكل اختيار. "
                "إذا كان الاسم غير واضح، اذكر ذلك ولا تخمّنه. لا تضمن القبول الجامعي، "
                "ونبّه إلى مراجعة شروط القبول الرسمية."
            )
            with st.spinner("أقرأ الصورة وأرتّب التخصصات..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(
                        max_output_tokens=900,
                        thinking_config=types.ThinkingConfig(thinking_level="low"),
                    ),
                )
            st.session_state["image_ranking"] = (response.text or "ما قدرت أقرأ التخصصات بوضوح.").strip()
        except Exception as error:
            st.session_state["image_ranking"] = "تعذر ترتيب الصورة. تأكد من المفتاح والإنترنت، ثم حاول مرة أخرى. التفاصيل: " + str(error)[:300]
if st.session_state.get("image_ranking"):
    st.markdown(st.session_state["image_ranking"])

if submitted and study_path == "أكاديمي" and len(strong_subjects) != 3:
    st.error("اختر ثلاث مواد اختيارية عشان نرتب لك التخصصات.")
elif submitted and study_path == "أكاديمي" and not (set(strong_subjects) & set(SCIENCE_SUBJECTS)):
    st.error("لازم تكون مادة واحدة على الأقل من اختياراتك علمية: أحياء أو كيمياء أو فيزياء أو علوم بيئية.")
elif submitted and study_path == "أكاديمي":
    st.subheader("اقتراحاتك")
    st.caption(f"ميولك الأكاديمية: {academic_preference}. ترتّب الخيارات حسب درجات المواد المرتبطة والمواد التي اخترتها وميولك؛ هذا ليس ترتيب قبول رسميًا.")
    st.caption("أعلى وزن للدرجات والميول: درجة الأحياء ترفع البرامج الحيوية والصحية، بينما الرياضيات والفيزياء ترفع الهندسة. المواد التي لم تدخل درجتها لا تُحسب كأنها مرتفعة.")
    for rank, (score, name, reason) in enumerate(academic_rankings[:20], start=1):
        with st.container(border=True):
            st.markdown(
                f'<div style="display:flex;align-items:baseline;gap:.65rem;flex-wrap:wrap;direction:rtl">'
                f'<span style="font-size:1.35rem;font-weight:700">{rank}. {name}</span>'
                f'<a href="{STUDENT_GUIDE_URL}" target="_blank" rel="noopener noreferrer" '
                'style="font-size:.76rem;color:#82cfff;text-decoration:none">'
                'دليل الطالب الرسمي ↗</a></div>',
                unsafe_allow_html=True,
            )
            st.progress(score, text=f"التوافق المبدئي: {score}%")
            st.write(reason)
    if academic_unmet:
        with st.expander("برامج لم تتحقق شروطها الرسمية أو لا تكفي البيانات للتحقق"):
            for name, shortfalls, requirement in academic_unmet:
                st.markdown(f"**{name}**")
                st.caption(requirement)
                st.write("؛ ".join(shortfalls))
elif submitted and study_path == "مهني وتقني":
    options = selected_vocational or list(TECHNICAL_SPECIALTIES)
    ranked = []
    for name in options:
        data = TECHNICAL_SPECIALTIES[name]
        matches = matching_interest_terms(interests, data["اهتمامات"], VOCATIONAL_RELEVANT_SUBJECTS[name])
        interest_score = 100 * len(matches) / max(1, len(set(interests))) if interests else 50
        relevant_subjects = VOCATIONAL_RELEVANT_SUBJECTS[name]
        relevant_grades = [subject_grades[subject] for subject in relevant_subjects if subject in subject_grades]
        grade_coverage = len(relevant_grades) / max(1, len(relevant_subjects))
        grade_score = sum(relevant_grades) / len(relevant_grades) if relevant_grades else 50
        evidence_grade = 50 + (grade_score - 50) * grade_coverage
        score = round(evidence_grade * 0.65 + interest_score * 0.20 + grade_coverage * 10 + average * 0.05)
        score = max(0, min(100, score))
        ranked.append((score, name, data["وصف"], matches, relevant_subjects, relevant_grades))

    st.subheader("التخصصات المهنية والتقنية المناسبة")
    st.caption("هذه اقتراحات أولية. اسأل مدرستك عن التخصصات المتاحة في محافظتك؛ فهي لا تُطرح في كل المدارس.")
    for rank, (score, name, description, matches, relevant_subjects, relevant_grades) in enumerate(sorted(ranked, reverse=True), start=1):
        with st.container(border=True):
            details_url = VOCATIONAL_GUIDE_URLS.get(name, "https://home.moe.gov.om/images/library/file/Book916206.pdf")
            st.markdown(
                f'<div style="display:flex;align-items:baseline;gap:.65rem;flex-wrap:wrap;direction:rtl">'
                f'<span style="font-size:1.35rem;font-weight:700">{rank}. {name}</span>'
                f'<a href="{details_url}" target="_blank" rel="noopener noreferrer" '
                'style="font-size:.76rem;color:#82cfff;text-decoration:none">'
                'تفاصيل التخصص ↗</a></div>',
                unsafe_allow_html=True,
            )
            st.progress(score, text=f"التوافق مع اهتماماتك: {score}%")
            st.write(description)
            st.caption("المواد التي تؤثر في الملاءمة: " + "، ".join(relevant_subjects))
            if matches:
                st.caption("اهتمامات متوافقة: " + "، ".join(matches))
            st.caption(f"أُدخلت درجات {len(relevant_grades)} من {len(relevant_subjects)} مواد مرتبطة؛ أدخل البقية لرفع دقة المقارنة.")

st.divider()
with st.expander("ℹ️ كيف تستفيد من النتائج؟"):
    st.markdown(
        "- أدخل المعدل والدرجات المتوفرة عندك، واختر المواد والاهتمامات الأقرب لك.\n"
        "- النسبة والترتيب حساب إرشادي من الموقع وليسا نسبة قبول أو حدًا رسميًا. المواد المرتبطة بالتخصصات أمثلة لمساعدتك على الاستكشاف فقط.\n"
        "- دليل الطالب للعام 2026/2027 يعرض البرامج وشروط كل برنامج، وقد تختلف الشروط بين المؤسسات وتتحدث عبر ملاحق؛ اعتمد دائمًا أحدث نسخة.\n"
        "- اسأل مدرستك عن المواد والمسارات المتاحة في محافظتك."
    )
    st.markdown("[افتح دليل الطالب للقبول الجامعي 2026/2027 (PDF)](https://heac.gov.om/uploads/15fb0d0c-dacf-4e0e-a4fb-19470ce4d852.pdf)  ·  [ضوابط اختيار المواد 2026/2027 – وزارة التعليم](https://home.moe.gov.om/ar/topics/1/show/13053)")
st.caption("تخصصي • أداة إرشادية أولية للطالب العُماني")


