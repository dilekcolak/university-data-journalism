import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src.data_loader import load_analysis_dataset
from src.analysis import (
    filter_dataset,
    get_top_departments_by_score,
    get_most_demanded_departments,
    get_most_competitive_departments,
    get_city_summary,
    get_yearly_score_trend,
    get_department_trend,
    get_fastest_rising_departments,
    compare_universities,
)
from src.visualization import (
    plot_top_departments_by_score,
    plot_most_demanded_departments,
    plot_most_competitive_departments,
    plot_city_preferences,
    plot_yearly_score_trend,
    plot_department_trend,
    plot_fastest_rising_departments,
    plot_university_comparison,
)
from src.ai_commentary import (
    generate_top_departments_commentary,
    generate_demand_commentary,
    generate_competitive_commentary,
    generate_trend_commentary,
    generate_rising_departments_commentary,
    generate_city_commentary,
    generate_university_comparison_commentary,
)

st.set_page_config(
    page_title="University Data Journalism",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Yapay Zeka Destekli Üniversite Veri Analizi Platformu")
st.markdown("Türkiye üniversite yerleştirme verileri üzerinde etkileşimli analizler")


@st.cache_data
def get_data():
    return load_analysis_dataset()


df = get_data()

st.sidebar.header("Filtreler")

selected_years = st.sidebar.multiselect(
    "Yıl seç",
    options=sorted(df["year"].dropna().unique().tolist()),
    default=sorted(df["year"].dropna().unique().tolist()),
)

selected_cities = st.sidebar.multiselect(
    "Şehir seç",
    options=sorted(df["city"].dropna().unique().tolist()),
)

selected_uni_types = st.sidebar.multiselect(
    "Üniversite türü seç",
    options=sorted(df["university_type"].dropna().unique().tolist()),
)

selected_departments = st.sidebar.multiselect(
    "Bölüm seç",
    options=sorted(df["department_name"].dropna().unique().tolist()),
)

selected_score_types = st.sidebar.multiselect(
    "Puan türü seç",
    options=sorted(df["score_type"].dropna().unique().tolist()),
)

analysis_option = st.sidebar.selectbox(
    "Analiz seç",
    [
        "En Yüksek Puanlı Bölümler",
        "En Çok Tercih Edilen Bölümler",
        "En Rekabetçi Bölümler",
        "Şehir Bazlı Analiz",
        "Yıllık Puan Trendi",
        "Seçili Bölüm Trendleri",
        "En Hızlı Yükselen Bölümler",
        "Üniversite Karşılaştırma",
    ],
)

filtered_df = filter_dataset(
    df,
    years=selected_years,
    cities=selected_cities,
    university_types=selected_uni_types,
    departments=selected_departments,
    score_types=selected_score_types,
)

filters_dict = {
    "years": selected_years,
    "cities": selected_cities,
    "university_types": selected_uni_types,
    "departments": selected_departments,
    "score_types": selected_score_types,
}

st.subheader("Filtrelenmiş Veri Özeti")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Kayıt Sayısı", f"{len(filtered_df):,}")
col2.metric("Üniversite Sayısı", filtered_df["university_name"].nunique())
col3.metric("Bölüm Sayısı", filtered_df["department_name"].nunique())
col4.metric("Şehir Sayısı", filtered_df["city"].nunique())

st.markdown("---")

if filtered_df.empty:
    st.warning("Seçilen filtrelere uygun veri bulunamadı. Lütfen filtreleri genişlet.")
    st.stop()

result_df = None
fig = None
commentary = ""

if analysis_option == "En Yüksek Puanlı Bölümler":
    result_df = get_top_departments_by_score(filtered_df)
    fig = plot_top_departments_by_score(result_df)
    commentary = generate_top_departments_commentary(result_df, filters=filters_dict)

elif analysis_option == "En Çok Tercih Edilen Bölümler":
    result_df = get_most_demanded_departments(filtered_df)
    fig = plot_most_demanded_departments(result_df)
    commentary = generate_demand_commentary(result_df, filters=filters_dict)

elif analysis_option == "En Rekabetçi Bölümler":
    result_df = get_most_competitive_departments(filtered_df)
    fig = plot_most_competitive_departments(result_df)
    commentary = generate_competitive_commentary(result_df, filters=filters_dict)

elif analysis_option == "Şehir Bazlı Analiz":
    result_df = get_city_summary(filtered_df)
    fig = plot_city_preferences(result_df)
    commentary = generate_city_commentary(result_df, filters=filters_dict)

elif analysis_option == "Yıllık Puan Trendi":
    result_df = get_yearly_score_trend(filtered_df)
    fig = plot_yearly_score_trend(result_df)
    commentary = generate_trend_commentary(result_df, filters=filters_dict)

elif analysis_option == "Seçili Bölüm Trendleri":
    default_depts = ["Bilgisayar Mühendisliği", "Tıp", "Hukuk", "Psikoloji"]
    available_departments = sorted(filtered_df["department_name"].dropna().unique().tolist())

    trend_departments = st.multiselect(
        "Trend için bölüm seç",
        options=available_departments,
        default=[d for d in default_depts if d in available_departments],
    )

    if not trend_departments:
        st.warning("Lütfen en az bir bölüm seç.")
        st.stop()

    result_df = get_department_trend(filtered_df, trend_departments)
    fig = plot_department_trend(result_df)
    commentary = (
        "Seçilen bölümlerin yıllara göre ortalama taban puan değişimi gösterilmektedir. "
        "Bu görünüm, bölümler arasındaki uzun dönemli eğilim farklarını karşılaştırmak için uygundur."
    )

elif analysis_option == "En Hızlı Yükselen Bölümler":
    years_sorted = sorted(filtered_df["year"].dropna().unique().tolist())

    if len(years_sorted) < 2:
        st.warning("Bu analiz için en az iki farklı yıl bulunmalıdır.")
        st.stop()

    start_year = st.selectbox("Başlangıç yılı", options=years_sorted, index=0)
    end_year = st.selectbox("Bitiş yılı", options=years_sorted, index=len(years_sorted) - 1)

    if start_year >= end_year:
        st.warning("Bitiş yılı başlangıç yılından büyük olmalıdır.")
        st.stop()

    result_df = get_fastest_rising_departments(filtered_df, start_year, end_year)
    fig = plot_fastest_rising_departments(result_df)
    commentary = generate_rising_departments_commentary(
        result_df,
        start_year,
        end_year,
        filters=filters_dict,
    )

elif analysis_option == "Üniversite Karşılaştırma":
    universities = sorted(filtered_df["university_name"].dropna().unique().tolist())

    if len(universities) < 2:
        st.warning("Karşılaştırma için en az iki üniversite bulunmalıdır.")
        st.stop()

    uni_1 = st.selectbox("1. Üniversite", options=universities, index=0)
    uni_2 = st.selectbox("2. Üniversite", options=universities, index=1)

    department_options = sorted(filtered_df["department_name"].dropna().unique().tolist())
    department = st.selectbox(
        "İsteğe bağlı bölüm filtresi",
        options=["Tümü"] + department_options,
    )
    department = None if department == "Tümü" else department

    result_df = compare_universities(filtered_df, uni_1, uni_2, department=department)
    fig = plot_university_comparison(result_df)
    commentary = generate_university_comparison_commentary(result_df, filters=filters_dict)

if result_df is None or result_df.empty:
    st.warning("Bu analiz için gösterilecek sonuç bulunamadı.")
    st.stop()

st.plotly_chart(fig, use_container_width=True)

st.subheader("Tablo")
st.dataframe(result_df, use_container_width=True)

st.subheader("AI Yorum")
st.info(commentary)