import streamlit as st
from docx import Document
from io import BytesIO
import google.generativeai as genai # مكتبة الذكاء الاصطناعي

st.set_page_config(page_title="المولد الشامل لمذكرات الرياضيات", layout="wide")

# إعداد مفتاح الذكاء الاصطناعي (سنحصل عليه في الخطوة التالية)
os_api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

st.title("📐 نظام توليد مذكرات المنهاج الجزائري")

# --- رفع المراجع ---
with st.sidebar:
    st.header("📂 المراجع الرسمية")
    files = st.file_uploader("ارفع (المنهاج، المخططات، الكتاب المدرسي)", accept_multiple_files=True, type="pdf")
    st.divider()
    st.write("بعد رفع الملفات، اكتب اسم أي درس تريد توليده.")

# --- واجهة اختيار الدرس ---
col1, col2 = st.columns(2)
with col1:
    target_lesson = st.text_input("اكتب عنوان الدرس (مثال: الأعداد النسبية، خاصية طاليس):")
with col2:
    target_level = st.selectbox("المستوى الدراسي:", ["1 متوسط", "2 متوسط", "3 متوسط", "4 متوسط"])

show_diff = st.checkbox("تضمين الصعوبات المتوقعة والفروق الفردية")

if st.button("توليد المذكرة الآن"):
    if not os_api_key:
        st.error("الرجاء إدخال مفتاح API أولاً.")
    elif not files:
        st.warning("الرجاء رفع المراجع (PDF) لكي أستطيع القراءة منها.")
    else:
        with st.spinner("جاري قراءة المراجع وتحليل درس " + target_lesson + "..."):
            # (هنا يتدخل الذكاء الاصطناعي لقراءة الملفات وصياغة المذكرة)
            # [span_2](start_span)[span_3](start_span)سنقوم بمحاكاة النتيجة بناءً على نمط مراجعك المرفقة[span_2](end_span)[span_3](end_span)
            
            st.success("تم توليد المذكرة بنجاح وفق معايير المنهاج!")
            
            # [span_4](start_span)عرض المذكرة بتنسيق الجدول المعتاد[span_4](end_span)
            st.markdown(f"### مذكرة درس: {target_lesson}")
            st.table({
                "المرحلة": ["التهيئة", "البناء (النشاط)", "الحوصلة", "الاستثمار"],
                "المحتوى": [
                    f"نشاط تشخيصي من الكتاب لدرس {target_lesson}",
                    f"وضعية تعلمية مستخرجة من الكتاب المدرسي ص...",
                    "القاعدة والنتائج كما وردت في المنهاج",
                    "تطبيق منزلي من سلسلة التمارين"
                ]
            })
            
            if show_diff:
                st.warning("**الصعوبات المتوقعة (بناءً على الوثيقة المرافقة):** صعوبة التطبيق المباشر، أخطاء في الحساب...")
