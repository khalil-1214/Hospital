import streamlit as st
import pandas as pd
from datetime import date
from database import (
    init_db, db_empty,
    add_doctor, get_doctors, delete_doctor,
    add_patient, get_patients, delete_patient,
    add_appointment, get_appointments, get_patient_appointments,
    update_appointment_status, delete_appointment,
    add_report, get_reports, get_patient_reports,
)

# پہلی بار ڈیٹا بیس بنے
init_db()

st.set_page_config(page_title="ہسپتال پورٹل", page_icon="🏥", layout="wide")

# ------- اگر ڈیٹا بیس خالی ہو تو خود seed چلے -------
if db_empty():
    import seed
    seed.seed()

# ================= سائیڈ بار =================
st.sidebar.title("🏥 ہسپتال پورٹل")

role = st.sidebar.radio("لاگ ان بطور", ["مریض", "ایڈمن"])

doctors_df = pd.DataFrame(get_doctors())
patients_df = pd.DataFrame(get_patients())
appointments_df = pd.DataFrame(get_appointments())
reports_df = pd.DataFrame(get_reports())

st.sidebar.markdown(f"""
---
- ڈاکٹرز: **{len(doctors_df)}**
- مریض: **{len(patients_df)}**
- اپائنٹمنٹس: **{len(appointments_df)}**
- رپورٹس: **{len(reports_df)}**
""")

# =====================================================
# ==================  مریض سیکشن  =====================
# =====================================================
if role == "مریض":
    st.sidebar.subheader("مریض لاگ ان")
    patient_name = st.sidebar.selectbox(
        "اپنا نام منتخب کریں",
        [""] + (list(patients_df["name"]) if not patients_df.empty else [])
    )

    menu = st.sidebar.radio("مینو", [
        "ڈاکٹرز دیکھیں",
        "اپائنٹمنٹ بک کریں",
        "میری اپائنٹمنٹس",
        "میری رپورٹس",
        "کنسلٹیشن فیس",
    ])

    if not patient_name:
        st.warning("براہ کرم سائیڈ بار سے اپنا نام منتخب کریں۔")
        st.stop()

    st.title(f"خوش آمدید، {patient_name}")

    if menu == "ڈاکٹرز دیکھیں":
        st.subheader(f"کل ڈاکٹرز: {len(doctors_df)}")
        st.dataframe(doctors_df, use_container_width=True)

    elif menu == "اپائنٹمنٹ بک کریں":
        st.subheader("نئی اپائنٹمنٹ")
        if doctors_df.empty:
            st.warning("کوئی ڈاکٹر موجود نہیں۔")
        else:
            doctor_name = st.selectbox("ڈاکٹر منتخب کریں", doctors_df["name"])
            doc = doctors_df[doctors_df["name"] == doctor_name].iloc[0]
            st.info(f"دستیابی: {doc['available']} | فیس: {doc['fee']} روپے")

            d = st.date_input("تاریخ", value=date.today())
            t = st.time_input("وقت")

            if st.button("بک کریں"):
                add_appointment(patient_name, int(doc["id"]), str(d), str(t))
                st.success(f"✅ اپائنٹمنٹ محفوظ ہو گئی: {doctor_name}، {d}، {t}")
                st.rerun()

    elif menu == "میری اپائنٹمنٹس":
        st.subheader("میری اپائنٹمنٹس")
        mine = get_patient_appointments(patient_name)
        if not mine:
            st.info("کوئی اپائنٹمنٹ نہیں ملی۔")
        else:
            df = pd.DataFrame(mine)
            df = df.merge(doctors_df[["id", "name"]], left_on="doctor_id",
                          right_on="id", suffixes=("", "_doc"))
            df = df.rename(columns={"name": "doctor_name"})
            st.dataframe(df[["date", "time", "doctor_name", "status"]],
                         use_container_width=True)

    elif menu == "میری رپورٹس":
        st.subheader("میری طبی رپورٹس")
        mine = get_patient_reports(patient_name)
        if not mine:
            st.info("کوئی رپورٹ نہیں ملی۔")
        else:
            st.dataframe(pd.DataFrame(mine), use_container_width=True)

    elif menu == "کنسلٹیشن فیس":
        st.subheader("ڈاکٹرز کی کنسلٹیشن فیس")
        st.dataframe(doctors_df[["name", "specialty", "fee"]],
                     use_container_width=True)

# =====================================================
# ==================  ایڈمن سیکشن  ====================
# =====================================================
else:
    st.sidebar.subheader("ایڈمن لاگ ان")
    password = st.sidebar.text_input("پاس ورڈ", type="password")

    if password != "admin123":
        st.warning("پاس ورڈ درست نہیں۔ (ڈیمو پاس ورڈ: admin123)")
        st.stop()

    st.title("🛠️ ایڈمن پینل")

    tab1, tab2, tab3, tab4 = st.tabs([
        "ڈاکٹرز", "مریض", "اپائنٹمنٹس", "رپورٹس"
    ])

    # -------- ڈاکٹرز ٹیب --------
    with tab1:
        st.subheader("نئے ڈاکٹر کا اضافہ")
        with st.form("add_doctor_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("نام")
            specialty = c2.text_input("خاصیت")
            education = c1.text_input("تعلیم")
            experience = c2.number_input("تجربہ (سال)", 0, 60, 1)
            fee = c1.number_input("فیس (روپے)", 0, 100000, 1000)
            available = c2.text_input("دستیابی", "پیر تا جمعہ، 10-2")

            if st.form_submit_button("شامل کریں"):
                if name.strip():
                    add_doctor(name, specialty, education, int(experience),
                               int(fee), available)
                    st.success("✅ ڈاکٹر شامل ہو گیا")
                    st.rerun()
                else:
                    st.error("نام لازمی ہے")

        st.divider()
        st.subheader(f"موجودہ ڈاکٹرز: {len(doctors_df)}")
        st.dataframe(doctors_df, use_container_width=True)

        if not doctors_df.empty:
            del_id = st.selectbox("حذف کرنے کے لیے ڈاکٹر",
                                  doctors_df["id"], key="del_doc")
            if st.button("ڈاکٹر حذف کریں", key="del_doc_btn"):
                delete_doctor(int(del_id))
                st.success("ڈاکٹر حذف ہو گیا")
                st.rerun()

    # -------- مریض ٹیب --------
    with tab2:
        st.subheader("نیا مریض")
        with st.form("add_patient_form"):
            c1, c2 = st.columns(2)
            pname = c1.text_input("نام")
            page_ = c2.number_input("عمر", 0, 120, 25)
            pgender = c1.selectbox("جنس", ["مرد", "عورت"])
            pphone = c2.text_input("فون", "0300-0000000")

            if st.form_submit_button("شامل کریں"):
                if pname.strip():
                    add_patient(pname, int(page_), pgender, pphone, "1234")
                    st.success("✅ مریض شامل ہو گیا")
                    st.rerun()
                else:
                    st.error("نام لازمی ہے")

        st.divider()
        st.subheader(f"موجودہ مریض: {len(patients_df)}")
        st.dataframe(patients_df, use_container_width=True)

        if not patients_df.empty:
            del_pid = st.selectbox("حذف کرنے کے لیے مریض",
                                   patients_df["id"], key="del_pat")
            if st.button("مریض حذف کریں", key="del_pat_btn"):
                delete_patient(int(del_pid))
                st.success("مریض حذف ہو گیا")
                st.rerun()

    # -------- اپائنٹمنٹس ٹیب --------
    with tab3:
        st.subheader("اپائنٹمنٹس کا انتظام")

        if appointments_df.empty:
            st.info("کوئی اپائنٹمنٹ نہیں")
        else:
            # ڈاکٹر کا نام شامل کریں
            merged = appointments_df.merge(
                doctors_df[["id", "name"]],
                left_on="doctor_id", right_on="id",
                suffixes=("", "_doc")
            ).rename(columns={"name": "doctor_name"})

            st.dataframe(
                merged[["id", "patient", "doctor_name", "date", "time", "status"]],
                use_container_width=True
            )

            st.divider()
            c1, c2, c3 = st.columns(3)
            appt_id = c1.selectbox("اپائنٹمنٹ ID", appointments_df["id"])
            new_status = c2.selectbox(
                "نیا اسٹیٹس",
                ["تصدیق شدہ", "زیرِ التوا", "مکمل", "منسوخ"]
            )
            if c3.button("اسٹیٹس اپ ڈیٹ"):
                update_appointment_status(int(appt_id), new_status)
                st.success("اسٹیٹس تبدیل ہو گیا")
                st.rerun()

            if st.button("اپائنٹمنٹ حذف کریں"):
                delete_appointment(int(appt_id))
                st.success("اپائنٹمنٹ حذف ہو گئی")
                st.rerun()

        st.divider()
        st.subheader("نئی اپائنٹمنٹ (ایڈمن کی طرف سے)")
        with st.form("admin_appt_form"):
            c1, c2 = st.columns(2)
            if not patients_df.empty and not doctors_df.empty:
                ap = c1.selectbox("مریض", patients_df["name"])
                ad = c2.selectbox("ڈاکٹر", doctors_df["name"])
                adate = c1.date_input("تاریخ", value=date.today())
                atime = c2.time_input("وقت")
                astatus = st.selectbox(
                    "اسٹیٹس",
                    ["تصدیق شدہ", "زیرِ التوا", "مکمل", "منسوخ"]
                )
                if st.form_submit_button("شامل کریں"):
                    doc_id = int(doctors_df[doctors_df["name"] == ad].iloc[0]["id"])
                    add_appointment(ap, doc_id, str(adate), str(atime), astatus)
                    st.success("✅ اپائنٹمنٹ شامل ہو گئی")
                    st.rerun()
            else:
                st.info("پہلے مریض اور ڈاکٹر شامل کریں")

    # -------- رپورٹس ٹیب --------
    with tab4:
        st.subheader("نئی رپورٹ")
        with st.form("add_report_form"):
            if not patients_df.empty and not doctors_df.empty:
                c1, c2 = st.columns(2)
                rp = c1.selectbox("مریض", patients_df["name"], key="rep_p")
                rd = c2.selectbox("ڈاکٹر", doctors_df["name"], key="rep_d")
                rdate = c1.date_input("تاریخ", value=date.today(), key="rep_dt")
                diagnosis = c2.text_input("تشخیص")
                prescription = st.text_area("نسخہ")

                if st.form_submit_button("شامل کریں"):
                    doc_id = int(doctors_df[doctors_df["name"] == rd].iloc[0]["id"])
                    add_report(rp, doc_id, str(rdate), diagnosis, prescription)
                    st.success("✅ رپورٹ شامل ہو گئی")
                    st.rerun()
            else:
                st.info("پہلے مریض اور ڈاکٹر شامل کریں")

        st.divider()
        st.subheader(f"تمام رپورٹس: {len(reports_df)}")
        if not reports_df.empty:
            st.dataframe(reports_df, use_container_width=True)
