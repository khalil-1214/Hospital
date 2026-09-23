import streamlit as st
import pandas as pd
import random
from datetime import date

st.set_page_config(page_title="ہسپتال پورٹل", page_icon="🏥", layout="wide")

# ---------------- ڈیٹا (Session State) ----------------
if "init" not in st.session_state:
    random.seed(42)

    doctors_list = [
        {"id": 1, "name": "ڈاکٹر احمد خان", "specialty": "کارڈیالوجی", "education": "MBBS, FCPS", "experience": 12, "fee": 2000, "available": "پیر تا جمعہ، 10-2"},
        {"id": 2, "name": "ڈاکٹر فاطمہ بی بی", "specialty": "امراضِ نسواں", "education": "MBBS, FCPS", "experience": 8, "fee": 1500, "available": "پیر تا ہفتہ، 4-8"},
        {"id": 3, "name": "ڈاکٹر بلال احمد", "specialty": "بچوں کے امراض", "education": "MBBS, DCH", "experience": 10, "fee": 1200, "available": "منگل تا اتوار، 9-1"},
        {"id": 4, "name": "ڈاکٹر عائشہ صدیقی", "specialty": "جلدی امراض", "education": "MBBS, MD", "experience": 6, "fee": 1800, "available": "پیر، بدھ، جمعہ، 3-7"},
        {"id": 5, "name": "ڈاکٹر حسن رضا", "specialty": "ہڈیوں کے امراض", "education": "MBBS, FCPS", "experience": 14, "fee": 2500, "available": "پیر تا جمعرات، 11-3"},
        {"id": 6, "name": "ڈاکٹر مریم نواز", "specialty": "آنکھوں کے امراض", "education": "MBBS, FCPS", "experience": 9, "fee": 1600, "available": "پیر تا ہفتہ، 9-1"},
        {"id": 7, "name": "ڈاکٹر عمر فاروق", "specialty": "دماغ و اعصاب", "education": "MBBS, FCPS", "experience": 15, "fee": 3000, "available": "منگل، جمعرات، ہفتہ، 2-6"},
        {"id": 8, "name": "ڈاکٹر ثنا اللہ", "specialty": "دانتوں کے امراض", "education": "BDS, FCPS", "experience": 7, "fee": 1500, "available": "پیر تا جمعہ، 10-4"},
        {"id": 9, "name": "ڈاکٹر کامران اکمل", "specialty": "نفسیاتی امراض", "education": "MBBS, FCPS", "experience": 11, "fee": 2200, "available": "پیر، بدھ، جمعہ، 4-8"},
        {"id": 10, "name": "ڈاکٹر نادیہ اقبال", "specialty": "ذیابیطس", "education": "MBBS, MRCP", "experience": 13, "fee": 2000, "available": "پیر تا ہفتہ، 10-2"},
        {"id": 11, "name": "ڈاکٹر طارق جمیل", "specialty": "گردوں کے امراض", "education": "MBBS, FCPS", "experience": 16, "fee": 2800, "available": "منگل تا جمعرات، 11-3"},
        {"id": 12, "name": "ڈاکٹر رابعہ خان", "specialty": "جلد و خوبصورتی", "education": "MBBS, MD", "experience": 5, "fee": 2500, "available": "پیر تا جمعہ، 3-7"},
        {"id": 13, "name": "ڈاکٹر سلمان یوسف", "specialty": "پھیپھڑوں کے امراض", "education": "MBBS, FCPS", "experience": 12, "fee": 2100, "available": "پیر تا ہفتہ، 9-1"},
        {"id": 14, "name": "ڈاکٹر عثمان غنی", "specialty": "کان، ناک، گلا", "education": "MBBS, FCPS", "experience": 9, "fee": 1700, "available": "منگل تا اتوار، 4-8"},
        {"id": 15, "name": "ڈاکٹر حمیرا اسلم", "specialty": "امراضِ اطفال", "education": "MBBS, DCH", "experience": 8, "fee": 1300, "available": "پیر تا جمعہ، 10-2"},
        {"id": 16, "name": "ڈاکٹر عدنان شاہ", "specialty": "سرجری", "education": "MBBS, FRCS", "experience": 18, "fee": 3500, "available": "پیر، بدھ، جمعہ، 11-3"},
        {"id": 17, "name": "ڈاکٹر زینب فاطمہ", "specialty": "امراضِ قلب", "education": "MBBS, FCPS", "experience": 10, "fee": 2300, "available": "منگل تا ہفتہ، 9-1"},
        {"id": 18, "name": "ڈاکٹر فیصل محمود", "specialty": "ہومیوپیتھی", "education": "BHMS", "experience": 6, "fee": 1000, "available": "پیر تا جمعہ، 10-4"},
        {"id": 19, "name": "ڈاکٹر انور علی", "specialty": "بخار و انفیکشن", "education": "MBBS", "experience": 4, "fee": 900, "available": "روزانہ، 9-1"},
        {"id": 20, "name": "ڈاکٹر صائمہ رشید", "specialty": "خون کے امراض", "education": "MBBS, FCPS", "experience": 11, "fee": 2200, "available": "پیر تا ہفتہ، 2-6"},
        {"id": 21, "name": "ڈاکٹر نوید انجم", "specialty": "معدے کے امراض", "education": "MBBS, FCPS", "experience": 13, "fee": 2000, "available": "منگل تا جمعرات، 10-2"},
        {"id": 22, "name": "ڈاکٹر سعدیہ ملک", "specialty": "امراضِ چشم", "education": "MBBS, FCPS", "experience": 7, "fee": 1600, "available": "پیر تا جمعہ، 3-7"},
        {"id": 23, "name": "ڈاکٹر وہاب احمد", "specialty": "کینسر (آنکولوجی)", "education": "MBBS, FCPS", "experience": 17, "fee": 4000, "available": "پیر، بدھ، جمعہ، 10-2"},
        {"id": 24, "name": "ڈاکٹر رفعت جبین", "specialty": "بچوں کی سرجری", "education": "MBBS, FRCS", "experience": 14, "fee": 3000, "available": "منگل تا ہفتہ، 9-1"},
        {"id": 25, "name": "ڈاکٹر شہزاد قریشی", "specialty": "فزیوتھراپی", "education": "DPT", "experience": 5, "fee": 1200, "available": "پیر تا ہفتہ، 11-5"},
    ]

    names = ["علی رضا", "سارہ خان", "احمد نواز", "فاطمہ بی بی", "بلال احمد", "عائشہ صدیقی", "حسن رضا", "مریم نواز", "عمر فاروق", "ثنا اللہ", "کامران اکمل", "نادیہ اقبال", "طارق جمیل", "رابعہ خان", "سلمان یوسف", "عثمان غنی", "حمیرا اسلم", "عدنان شاہ", "زینب فاطمہ", "فیصل محمود", "انور علی", "صائمہ رشید", "نوید انجم", "سعدیہ ملک", "وہاب احمد", "نور فاطمہ", "عبداللہ خان", "خدیجہ بی بی", "یوسف رضا", "زہرہ بتول", "محمد اسلم", "آمنہ صدیقی", "اکرم شہزاد", "شبنم نواز", "ریحان خان", "ثوبیہ انور", "عمران ملک", "رانیہ احمد", "قاسم علی", "نجمہ پروین"]
    
    patients_list = [{"id": i+1, "name": names[i], "age": random.randint(18, 70), "gender": random.choice(["مرد", "عورت"]), "phone": f"03{random.randint(0,4)}{random.randint(0,9)}-{random.randint(1000000,9999999)}"} for i in range(len(names))]

    appts_list = []
    for i in range(60):
        appts_list.append({"id": i+1, "patient": random.choice(names), "doctor_id": random.randint(1, 25), "date": f"2026-09-{random.randint(1,30):02d}", "time": f"{random.randint(9,17):02d}:{random.choice(['00','15','30','45'])}", "status": random.choice(["تصدیق شدہ", "زیرِ التوا", "مکمل", "منسوخ"])})

    st.session_state.doctors = pd.DataFrame(doctors_list)
    st.session_state.patients = pd.DataFrame(patients_list)
    st.session_state.appointments = pd.DataFrame(appts_list)
    st.session_state.init = True

doctors_df = st.session_state.doctors
patients_df = st.session_state.patients
appointments_df = st.session_state.appointments

# ---------------- سائیڈ بار ----------------
st.sidebar.title("🏥 ہسپتال پورٹل")
st.sidebar.markdown(f"ڈاکٹرز: **{len(doctors_df)}** | مریض: **{len(patients_df)}** | اپائنٹمنٹس: **{len(appointments_df)}**")

role = st.sidebar.radio("لاگ ان بطور", ["مریض", "ایڈمن"])

# ---------------- مریض سیکشن ----------------
if role == "مریض":
    patient_name = st.sidebar.selectbox("اپنا نام منتخب کریں", [""] + list(patients_df["name"]))
    menu = st.sidebar.radio("مینو", ["ڈاکٹرز دیکھیں", "اپائنٹمنٹ بک کریں", "میری اپائنٹمنٹس", "کنسلٹیشن فیس"])

    if not patient_name:
        st.warning("براہ کرم سائیڈ بار سے اپنا نام منتخب کریں۔")
        st.stop()

    st.title(f"خوش آمدید، {patient_name}")

    if menu == "ڈاکٹرز دیکھیں":
        st.subheader(f"کل ڈاکٹرز: {len(doctors_df)}")
        st.dataframe(doctors_df, use_container_width=True)

    elif menu == "اپائنٹمنٹ بک کریں":
        st.subheader("نئی اپائنٹمنٹ")
        doctor_name = st.selectbox("ڈاکٹر منتخب کریں", doctors_df["name"])
        doc = doctors_df[doctors_df["name"] == doctor_name].iloc[0]
        st.info(f"دستیابی: {doc['available']} | فیس: {doc['fee']} روپے")
        d = st.date_input("تاریخ", value=date.today())
        t = st.time_input("وقت")
        if st.button("بک کریں"):
            new_appt = {"id": len(appointments_df)+1, "patient": patient_name, "doctor_id": int(doc["id"]), "date": str(d), "time": str(t), "status": "زیرِ التوا"}
            st.session_state.appointments = pd.concat([appointments_df, pd.DataFrame([new_appt])], ignore_index=True)
            st.success(f"✅ اپائنٹمنٹ محفوظ ہو گئی: {doctor_name}، {d}")
            st.rerun()

    elif menu == "میری اپائنٹمنٹس":
        st.subheader("میری اپائنٹمنٹس")
        mine = appointments_df[appointments_df["patient"] == patient_name]
        if mine.empty:
            st.info("کوئی اپائنٹمنٹ نہیں ملی۔")
        else:
            merged = mine.merge(doctors_df[["id", "name"]], left_on="doctor_id", right_on="id", suffixes=("", "_doc"))
            st.dataframe(merged[["date", "time", "name", "status"]], use_container_width=True)

    elif menu == "کنسلٹیشن فیس":
        st.subheader("ڈاکٹرز کی فیس")
        st.dataframe(doctors_df[["name", "specialty", "fee"]], use_container_width=True)

# ---------------- ایڈمن سیکشن ----------------
else:
    password = st.sidebar.text_input("پاس ورڈ", type="password")
    if password != "admin123":
        st.warning("پاس ورڈ درست نہیں۔ (ڈیمو پاس ورڈ: admin123)")
        st.stop()

    st.title("🛠️ ایڈمن پینل")
    tab1, tab2, tab3 = st.tabs(["ڈاکٹرز", "مریض", "اپائنٹمنٹس"])

    with tab1:
        st.subheader("نیا ڈاکٹر شامل کریں")
        with st.form("add_doc"):
            c1, c2 = st.columns(2)
            name = c1.text_input("نام")
            specialty = c2.text_input("خاصیت")
            education = c1.text_input("تعلیم")
            experience = c2.number_input("تجربہ", 0, 60, 1)
            fee = c1.number_input("فیس", 0, 100000, 1000)
            available = c2.text_input("دستیابی", "پیر تا جمعہ، 10-2")
            if st.form_submit_button("شامل کریں"):
                if name.strip():
                    new_id = len(doctors_df) + 1
                    new_doc = {"id": new_id, "name": name, "specialty": specialty, "education": education, "experience": int(experience), "fee": int(fee), "available": available}
                    st.session_state.doctors = pd.concat([doctors_df, pd.DataFrame([new_doc])], ignore_index=True)
                    st.success("✅ ڈاکٹر شامل ہو گیا")
                    st.rerun()
        st.divider()
        st.dataframe(doctors_df, use_container_width=True)

    with tab2:
        st.subheader("نیا مریض شامل کریں")
        with st.form("add_pat"):
            c1, c2 = st.columns(2)
            pname = c1.text_input("نام")
            page_ = c2.number_input("عمر", 0, 120, 25)
            pgender = c1.selectbox("جنس", ["مرد", "عورت"])
            pphone = c2.text_input("فون", "0300-0000000")
            if st.form_submit_button("شامل کریں"):
                if pname.strip():
                    new_id = len(patients_df) + 1
                    new_pat = {"id": new_id, "name": pname, "age": int(page_), "gender": pgender, "phone": pphone}
                    st.session_state.patients = pd.concat([patients_df, pd.DataFrame([new_pat])], ignore_index=True)
                    st.success("✅ مریض شامل ہو گیا")
                    st.rerun()
        st.divider()
        st.dataframe(patients_df, use_container_width=True)

    with tab3:
        st.subheader("اپائنٹمنٹس کا انتظام")
        merged = appointments_df.merge(doctors_df[["id", "name"]], left_on="doctor_id", right_on="id", suffixes=("", "_doc"))
        st.dataframe(merged[["id", "patient", "name", "date", "time", "status"]], use_container_width=True)
        st.divider()
        c1, c2, c3 = st.columns(3)
        appt_id = c1.selectbox("اپائنٹمنٹ ID", appointments_df["id"])
        new_status = c2.selectbox("نیا اسٹیٹس", ["تصدیق شدہ", "زیرِ التوا", "مکمل", "منسوخ"])
        if c3.button("اپ ڈیٹ"):
            st.session_state.appointments.loc[st.session_state.appointments["id"] == appt_id, "status"] = new_status
            st.success("اسٹیٹس تبدیل ہو گیا")
            st.rerun()
