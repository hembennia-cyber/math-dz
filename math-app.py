import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# إعداد واجهة الموقع
st.set_page_config(page_title="المساعد البيداغوجي الذكي", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")
    uploaded_files = st.file_uploader("ارفع المراجع (منهاج، كتاب، وثيقة مرافقة):", type="pdf", accept_multiple_files=True)
    st.info("ملاحظة: سيقوم الذكاء الاصطناعي بتحليل هذه الملفات لتوليد محتوى دقيق.")

st.title("🎓 نظام توليد المذكرات والأنشطة الذكي")
st.write("اكتب عنوان الدرس وسيقوم النظام بتحليل مراجعك لتوليد محتوى بيداغوجي متكامل.")

# مدخلات المستخدم
col1, col2 = st.columns(2)
with col1:
    lesson_title = st.text_input("عنوان الدرس (مثلاً: خاصية طاليس):")
with col2:
    level = st.selectbox("المستوى الدراسي:", ["1 متوسط", "2 متوسط", "3 متوسط", "4 متوسط"])

mode = st.radio("ماذا تريد أن تولد؟", 
                ["مذكرة درس كاملة (حسب المنهاج)", 
                 "أنشطة ووضعيات جديدة (ذكاء اصطناعي)", 
                 "سلسلة تمارين متدرجة (فروق فردية)"])

if st.button("إبدأ المعالجة الذكية ✨"):
    if not api_key or not uploaded_files:
        st.error("الرجاء إدخال المفتاح ورفع الملفات أولاً.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # استخراج النص من الملفات المرفوعة (تحليل المراجع)
            all_text = ""
            with st.spinner("جاري قراءة وتحليل المراجع..."):
                for uploaded_file in uploaded_files:
                    pdf_reader = PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        all_text += page.extract_text()[:1000] # نأخذ عينات من كل ملف للسرعة
            
            # بناء الأمر (Prompt) بناءً على الاختيار
            if "مذكرة" in mode:
                prompt = f"بناءً على هذا الجزء من المنهاج والمراجع: {all_text[:2000]}... صمم مذكرة بيداغوجية جزائرية لدرس {lesson_title} لسنوات {level}. تشمل: مؤشرات الكفاءة، العقبات المتوقعة، والوضعية التعليمية."
            elif "أنشطة" in mode:
                prompt = f"بناءً على مراجع الرياضيات التالية: {all_text[:2000]}... ولد نشاطاً تعليمياً جديداً ومبتكراً لدرس {lesson_title} يختلف عن الكتاب المدرسي ويكون مستوحى من الواقع الجزائري."
            else:
                prompt = f"من خلال تحليل درس {lesson_title}، أنشئ 3 تمارين متدرجة: تمرين بسيط (تطبيق مباشر)، تمرين متوسط (إدماج)، وتمرين معمق (للمتفوقين). مع ذكر الصعوبات التي قد تواجه المتعثرين."

            # توليد المحتوى
            with st.spinner("الذكاء الاصطناعي يحلل ويولد المحتوى الآن..."):
                response = model.generate_content(prompt)
                st.success("تم التوليد بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
