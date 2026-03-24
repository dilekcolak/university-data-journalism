import plotly.express as px


def plot_top_departments_by_score(df):
    fig = px.bar(
        df,
        x="final_score",
        y="department_name",
        orientation="h",
        title="En Yüksek Ortalama Taban Puanlı Bölümler",
        labels={
            "final_score": "Ortalama Taban Puan",
            "department_name": "Bölüm",
        },
        text="final_score",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def plot_most_demanded_departments(df):
    fig = px.bar(
        df,
        x="total_preferences",
        y="department_name",
        orientation="h",
        title="En Çok Tercih Edilen Bölümler",
        labels={
            "total_preferences": "Toplam Tercih",
            "department_name": "Bölüm",
        },
        text="total_preferences",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def plot_most_competitive_departments(df):
    fig = px.bar(
        df,
        x="demand_per_quota",
        y="department_name",
        orientation="h",
        title="En Rekabetçi Bölümler",
        labels={
            "demand_per_quota": "Talep / Kontenjan",
            "department_name": "Bölüm",
        },
        text="demand_per_quota",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def plot_city_preferences(df):
    top_df = df.sort_values("total_preferences", ascending=False).head(15)
    fig = px.bar(
        top_df,
        x="city",
        y="total_preferences",
        title="En Çok Tercih Edilen Şehirler",
        text="total_preferences",
        labels={
            "city": "Şehir",
            "total_preferences": "Toplam Tercih",
        },
    )
    return fig


def plot_yearly_score_trend(df):
    fig = px.line(
        df,
        x="year",
        y="avg_final_score",
        markers=True,
        title="Yıllara Göre Ortalama Taban Puan Değişimi",
        labels={
            "year": "Yıl",
            "avg_final_score": "Ortalama Taban Puan",
        },
    )
    return fig


def plot_department_trend(df):
    fig = px.line(
        df,
        x="year",
        y="avg_final_score",
        color="department_name",
        markers=True,
        title="Seçili Bölümlerin Yıllara Göre Taban Puan Trendi",
        labels={
            "year": "Yıl",
            "avg_final_score": "Ortalama Taban Puan",
            "department_name": "Bölüm",
        },
    )
    return fig


def plot_fastest_rising_departments(df):
    fig = px.bar(
        df,
        x="score_change",
        y="department_name",
        orientation="h",
        title="En Hızlı Yükselen Bölümler",
        labels={
            "score_change": "Puan Artışı",
            "department_name": "Bölüm",
        },
        text="score_change",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def plot_university_comparison(df):
    fig = px.bar(
        df,
        x="university_name",
        y="avg_final_score",
        barmode="group",
        title="Üniversite Karşılaştırması",
        labels={
            "university_name": "Üniversite",
            "avg_final_score": "Ortalama Taban Puan",
        },
        text="avg_final_score",
    )
    return fig