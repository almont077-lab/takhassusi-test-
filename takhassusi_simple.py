import streamlit as st

st.set_page_config(page_title="تخصصي", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Cairo',sans-serif;}
.stApp {direction:rtl; text-align:right;}
h1,h2,h3,p,label {text-align:right;}
[data-testid="stSidebar"] {direction:rtl; text-align:right;}
.assistant-badge {width:48px;height:48px;border-radius:50%;background:#176b5d;color:white;
 display:flex;align-items:center;justify-content:center;font-size:25px;margin:4px 0 10px auto;}
.hero {padding:1.2rem 1.5rem;border-radius:16px;background:linear-gradient(120deg,#123b36,#176b5d);color:white;}
</style>
""", unsafe_allow_html=True)

PROGRAMS = {
    "الطب والعلوم الصحية": {"مواد": ["الأحياء", "الكيمياء"], "اهتمامات": ["الصحة", "مساعدة الناس", "البحث"]},
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
    "العلوم البيئية": {"مواد": ["الأحياء", "الكيمياء", "الرياضيات"], "اهتمامات": ["البيئة", "البحث", "حل المشكلات"]},
}
SUBJECTS = ["الرياضيات", "اللغة الإنجليزية", "الأحياء", "الكيمياء", "الفيزياء", "تقنية المعلومات", "اللغة العربية", "التاريخ والجغرافيا"]
INTERESTS = ["الصحة", "مساعدة الناس", "البحث", "التقنية", "البرمجة", "التصميم", "حل المشكلات", "الأعمال", "الأرقام", "الاقتصاد", "القيادة", "التواصل", "القانون", "القراءة والكتابة", "التعليم", "الإعلام", "الكتابة", "البيئة"]

st.markdown('<div class="hero"><h1>🎓 تخصصي</h1><p>اكتشف تخصصات تناسب درجاتك واهتماماتك بخطوات بسيطة.</p></div>', unsafe_allow_html=True)
st.write("")

# AI assistant in the left sidebar. The API key is entered as a password and kept in this session only.
with st.sidebar:
    st.markdown('<div class="assistant-badge">💬</div>', unsafe_allow_html=True)
    st.subheader("مساعد التخصص الذكي")
    st.caption("اسأل عن التخصصات الجامعية. محادثتك تُرسل إلى OpenAI عند الضغط على إرسال.")
    api_key = st.text_input("مفتاح OpenAI API", type="password", key="openai_key", help="أدخل مفتاحك هنا؛ لا تكتبه في المحادثة ولا تشاركه مع أحد.")
    st.markdown("[إنشاء مفتاح API](https://platform.openai.com/api-keys)")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for role, message in st.session_state.chat[-6:]:
        with st.chat_message(role):
            st.write(message)
    with st.form("assistant_form", clear_on_submit=True):
        question = st.text_input("اكتب سؤالك", placeholder="مثال: وش يناسبني إذا أحب التقنية؟")
        ask = st.form_submit_button("إرسال", use_container_width=True)
    if ask and question.strip():
        q = question.strip()
        if not api_key:
            answer = "أدخل مفتاح OpenAI API أعلاه أولًا. إنشاء المفتاح واستخدام API قد يتطلب إعداد الفوترة بشكل منفصل عن اشتراك ChatGPT."
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                prior = st.session_state.chat[-8:]
                transcript = "\n".join(
                    ("الطالب" if role == "user" else "المساعد") + ": " + message
                    for role, message in prior
                )
                transcript += "\nالطالب: " + q
                response = client.responses.create(
                    model="gpt-6-astra",
                    instructions=(
                        "أنت مرشد أكاديمي لطالب في سلطنة عمان. أجب بالعربية السهلة وباختصار. "
                        "ساعده على التفكير في التخصصات ولا تدّع معرفة شروط قبول محدثة أو ضمان القبول؛ "
                        "ذكّره بالتحقق من دليل القبول الرسمي عند الحاجة."
                    ),
                    input=transcript,
                )
                answer = response.output_text.strip() or "لم يصلني رد. جرّب صياغة السؤال مرة أخرى."
            except ImportError:
                answer = "مكتبة OpenAI غير مثبتة. أغلق نافذة تشغيل البرنامج مؤقتًا وثبّتها بالأمر: py -m pip install openai، ثم شغّل البرنامج من جديد."
            except Exception:
                answer = "تعذر الاتصال. تأكد من صحة مفتاح API والإنترنت وإعداد الفوترة، ثم حاول مرة أخرى."
        st.session_state.chat.extend([("user", q), ("assistant", answer)])
        st.rerun()
    st.caption("استخدمه محليًا على جهازك، ولا تشارك مفتاح API أو صورة تظهره.")
with st.form("recommendation_form"):
    st.subheader("بيانات بسيطة")
    average = st.number_input("معدلك العام (%)", min_value=0, max_value=100, value=80, step=1)
    strong_subjects = st.multiselect("المواد التي تحبها أو تتميز فيها", SUBJECTS)
    interests = st.multiselect("المجالات التي تهمك", INTERESTS)
    submitted = st.form_submit_button("اعرض التخصصات المناسبة", type="primary", use_container_width=True)

if submitted:
    results = []
    for name, data in PROGRAMS.items():
        subject_match = len(set(strong_subjects) & set(data["مواد"])) / max(1, len(data["مواد"]))
        interest_match = len(set(interests) & set(data["اهتمامات"])) / max(1, len(data["اهتمامات"]))
        score = round(average * 0.5 + subject_match * 25 + interest_match * 25)
        reasons = []
        matching_subjects = sorted(set(strong_subjects) & set(data["مواد"]))
        matching_interests = sorted(set(interests) & set(data["اهتمامات"]))
        if matching_subjects:
            reasons.append("مواد تناسبك: " + "، ".join(matching_subjects))
        if matching_interests:
            reasons.append("اهتمامات مشتركة: " + "، ".join(matching_interests))
        if not reasons:
            reasons.append("اقتراح عام بناءً على معدلك؛ أضف موادك واهتماماتك لتحسين الترتيب")
        results.append((score, name, "؛ ".join(reasons)))

    st.subheader("اقتراحاتك")
    st.caption("هذه اقتراحات مبدئية وليست توقعًا للقبول. تأكد من شروط القبول الرسمية في سلطنة عُمان.")
    for rank, (score, name, reason) in enumerate(sorted(results, reverse=True)[:5], start=1):
        with st.container(border=True):
            st.markdown(f"### {rank}. {name}")
            st.progress(score, text=f"التوافق المبدئي: {score}%")
            st.write(reason)

st.divider()
st.caption("تخصصي — أداة إرشادية أولية. النتائج لا تضمن القبول الجامعي.")


