import pandas as pd


def _format_number(value, decimals: int = 2) -> str:
    if pd.isna(value):
        return "bilinmiyor"
    if isinstance(value, (int, float)):
        return f"{value:,.{decimals}f}"
    return str(value)


def _build_filter_context(filters=None) -> str:
    if not filters:
        return ""

    context_parts = []

    score_types = filters.get("score_types")
    years = filters.get("years")
    cities = filters.get("cities")
    university_types = filters.get("university_types")
    departments = filters.get("departments")

    if score_types:
        context_parts.append(f"{', '.join(score_types)} puan türünde")

    if years:
        context_parts.append(f"{min(years)}-{max(years)} yılları arasında")

    if cities:
        if len(cities) == 1:
            context_parts.append(f"{cities[0]} özelinde")
        else:
            context_parts.append(f"{len(cities)} şehir filtresi altında")

    if university_types:
        if len(university_types) == 1:
            context_parts.append(f"{university_types[0]} üniversitelerinde")
        else:
            context_parts.append(f"{', '.join(university_types)} üniversite tiplerinde")

    if departments:
        if len(departments) == 1:
            context_parts.append(f"{departments[0]} bölümü odağında")
        else:
            context_parts.append(f"{len(departments)} bölüm filtresiyle")

    context_text = " ".join(context_parts).strip()
    if context_text:
        context_text += " yapılan analizde "

    return context_text


def generate_top_departments_commentary(df: pd.DataFrame, filters=None) -> str:
    if df.empty:
        return "Seçilen filtrelere göre yorum üretilemedi."

    top_name = df.iloc[0]["department_name"]
    top_score = df.iloc[0]["final_score"]
    bottom_name = df.iloc[-1]["department_name"]
    bottom_score = df.iloc[-1]["final_score"]

    context_text = _build_filter_context(filters)

    return (
        f"{context_text}en yüksek ortalama taban puana sahip bölüm {top_name} "
        f"({_format_number(top_score)}) olarak öne çıkıyor. Listenin alt kısmındaki "
        f"{bottom_name} ({_format_number(bottom_score)}) ile arasında dikkat çekici bir fark bulunuyor. "
        f"Bu görünüm, üst sıralardaki bölümlerin daha seçici ve rekabetçi bir profile sahip olduğunu düşündürüyor."
    )


def generate_demand_commentary(df: pd.DataFrame, filters=None) -> str:
    if df.empty:
        return "Seçilen filtrelere göre yorum üretilemedi."

    top_name = df.iloc[0]["department_name"]
    top_pref = df.iloc[0]["total_preferences"]
    context_text = _build_filter_context(filters)

    return (
        f"{context_text}toplam tercih sayısına göre {top_name} bölümü öne çıkıyor "
        f"({_format_number(top_pref, 0)} tercih). Bu tablo, bazı bölümlerin yalnızca yüksek puanlı değil, "
        f"aynı zamanda geniş aday kitlesi tarafından yoğun ilgi gören alanlar olduğunu gösteriyor."
    )

def generate_competitive_commentary(df, filters=None):
    if df.empty:
        return "Rekabet analizi için yeterli veri bulunamadı."

    top_name = df.iloc[0]["department_name"]
    top_ratio = df.iloc[0]["demand_per_quota"]

    context_parts = []

    if filters:
        if filters.get("score_types"):
            context_parts.append(f"{', '.join(filters['score_types'])} puan türünde")
        if filters.get("years"):
            context_parts.append(f"{min(filters['years'])}-{max(filters['years'])} yılları arasında")

    context_text = " ".join(context_parts)
    if context_text:
        context_text += " yapılan analizde "

    return (
        f"{context_text}talep/kontenjan oranı en yüksek bölüm {top_name} "
        f"({top_ratio:.2f}) olarak öne çıkıyor. "
        f"Bu durum, bu bölümün kontenjanına göre oldukça yoğun talep gördüğünü "
        f"ve rekabet düzeyinin yüksek olduğunu gösteriyor."
    )



def generate_trend_commentary(df: pd.DataFrame, filters=None) -> str:
    if df.empty or len(df) < 2:
        return "Trend yorumu için yeterli veri yok."

    df = df.sort_values("year").reset_index(drop=True)

    first_year = df.iloc[0]["year"]
    last_year = df.iloc[-1]["year"]
    first_score = df.iloc[0]["avg_final_score"]
    last_score = df.iloc[-1]["avg_final_score"]
    diff = last_score - first_score

    if diff > 0:
        direction = "arttığı"
    elif diff < 0:
        direction = "azaldığı"
    else:
        direction = "büyük ölçüde sabit kaldığı"

    context_text = _build_filter_context(filters)

    return (
        f"{context_text}{first_year} ile {last_year} yılları arasında ortalama taban puanın "
        f"{direction} görülüyor. Toplam değişim {_format_number(diff)} puan düzeyinde. "
        f"Bu eğilim; aday ilgisi, kontenjan politikaları ve ilgili alanın popülerliğindeki değişimlerle ilişkili olabilir."
    )


def generate_rising_departments_commentary(
    df: pd.DataFrame,
    start_year: int,
    end_year: int,
    filters=None,
) -> str:
    if df.empty:
        return "Yükselen bölümler analizi için yeterli veri bulunamadı."

    top_name = df.iloc[0]["department_name"]
    start_score = df.iloc[0]["start_score"]
    end_score = df.iloc[0]["end_score"]
    change = df.iloc[0]["score_change"]
    context_text = _build_filter_context(filters)

    return (
        f"{context_text}{start_year}-{end_year} döneminde en dikkat çekici yükseliş {top_name} bölümünde görülüyor. "
        f"Ortalama taban puan {_format_number(start_score)} seviyesinden {_format_number(end_score)} seviyesine çıkmış "
        f"ve toplamda {_format_number(change)} puanlık artış kaydedilmiştir. Bu sonuç, ilgili alana yönelik ilginin son yıllarda güçlendiğini düşündürebilir."
    )


def generate_city_commentary(df: pd.DataFrame, filters=None) -> str:
    if df.empty:
        return "Şehir analizi için yeterli veri yok."

    top_city = df.iloc[0]["city"]
    top_pref = df.iloc[0]["total_preferences"]
    context_text = _build_filter_context(filters)

    return (
        f"{context_text}şehir bazında toplam tercihler incelendiğinde {top_city} öne çıkıyor "
        f"({_format_number(top_pref, 0)} tercih). Bu görünüm, büyük ve eğitim çeşitliliği yüksek şehirlerin "
        f"adaylar tarafından daha fazla tercih edildiğini düşündürüyor."
    )


def generate_university_comparison_commentary(df: pd.DataFrame, filters=None) -> str:
    if df.empty or len(df) < 2:
        return "Karşılaştırma için yeterli veri yok."

    sorted_df = df.sort_values("avg_final_score", ascending=False).reset_index(drop=True)
    winner = sorted_df.iloc[0]
    loser = sorted_df.iloc[1]
    context_text = _build_filter_context(filters)

    return (
        f"{context_text}karşılaştırmada {winner['university_name']}, ortalama taban puan açısından "
        f"{loser['university_name']} üniversitesinin önünde görünüyor "
        f"({_format_number(winner['avg_final_score'])} vs {_format_number(loser['avg_final_score'])}). "
        f"Bunun yanında tercih sayısı, doluluk oranı ve yerleşen öğrenci sayısı gibi göstergeler birlikte değerlendirildiğinde daha bütüncül bir yorum yapılabilir."
    )