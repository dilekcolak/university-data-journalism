import pandas as pd


def filter_dataset(
    df: pd.DataFrame,
    years=None,
    cities=None,
    university_types=None,
    departments=None,
    score_types=None,
):
    filtered = df.copy()

    if years:
        filtered = filtered[filtered["year"].isin(years)]
    if cities:
        filtered = filtered[filtered["city"].isin(cities)]
    if university_types:
        filtered = filtered[filtered["university_type"].isin(university_types)]
    if departments:
        filtered = filtered[filtered["department_name"].isin(departments)]
    if score_types:
        filtered = filtered[filtered["score_type"].isin(score_types)]

    return filtered


def get_top_departments_by_score(df: pd.DataFrame, min_count: int = 10, top_n: int = 20):
    result = (
        df.groupby("department_name")
        .agg(
            final_score=("final_score", "mean"),
            record_count=("department_name", "size"),
        )
        .query("record_count >= @min_count")
        .sort_values("final_score", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return result


def get_most_demanded_departments(df: pd.DataFrame, min_count: int = 10, top_n: int = 20):
    result = (
        df.groupby("department_name")
        .agg(
            total_preferences=("total_preferences", "sum"),
            record_count=("department_name", "size"),
        )
        .query("record_count >= @min_count")
        .sort_values("total_preferences", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return result


def get_most_competitive_departments(df: pd.DataFrame, min_count: int = 10, top_n: int = 20):
    result = (
        df.groupby("department_name")
        .agg(
            demand_per_quota=("demand_per_quota", "mean"),
            record_count=("department_name", "size"),
        )
        .query("record_count >= @min_count")
        .sort_values("demand_per_quota", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return result


def get_city_summary(df: pd.DataFrame):
    result = (
        df.groupby("city", as_index=False)
        .agg(
            university_count=("university_name", "nunique"),
            department_count=("department_name", "nunique"),
            total_preferences=("total_preferences", "sum"),
            avg_final_score=("final_score", "mean"),
            total_enrolled=("total_enrolled", "sum"),
        )
        .sort_values("total_preferences", ascending=False)
    )
    return result


def get_yearly_score_trend(df: pd.DataFrame):
    result = (
        df.groupby("year", as_index=False)
        .agg(avg_final_score=("final_score", "mean"))
        .sort_values("year")
    )
    return result


def get_department_trend(df: pd.DataFrame, departments: list[str]):
    result = (
        df[df["department_name"].isin(departments)]
        .groupby(["year", "department_name"], as_index=False)
        .agg(avg_final_score=("final_score", "mean"))
        .sort_values(["department_name", "year"])
    )
    return result


def get_fastest_rising_departments(
    df: pd.DataFrame,
    start_year: int,
    end_year: int,
    min_count_per_period: int = 3,
    top_n: int = 20,
):
    period_df = df[df["year"].isin([start_year, end_year])].copy()

    summary = (
        period_df.groupby(["department_name", "year"], as_index=False)
        .agg(
            avg_final_score=("final_score", "mean"),
            record_count=("department_name", "size"),
        )
    )

    summary = summary[summary["record_count"] >= min_count_per_period]

    pivot = summary.pivot(
        index="department_name",
        columns="year",
        values="avg_final_score",
    ).reset_index()

    if start_year not in pivot.columns or end_year not in pivot.columns:
        return pd.DataFrame(columns=["department_name", "start_score", "end_score", "score_change"])

    pivot = pivot.dropna(subset=[start_year, end_year]).copy()
    pivot["start_score"] = pivot[start_year]
    pivot["end_score"] = pivot[end_year]
    pivot["score_change"] = pivot["end_score"] - pivot["start_score"]

    result = (
        pivot[["department_name", "start_score", "end_score", "score_change"]]
        .sort_values("score_change", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def compare_universities(df: pd.DataFrame, university_1: str, university_2: str, department: str | None = None):
    compare_df = df[df["university_name"].isin([university_1, university_2])].copy()

    if department:
        compare_df = compare_df[compare_df["department_name"] == department]

    result = (
        compare_df.groupby("university_name", as_index=False)
        .agg(
            avg_final_score=("final_score", "mean"),
            total_preferences=("total_preferences", "sum"),
            avg_occupancy_rate=("occupancy_rate", "mean"),
            total_enrolled=("total_enrolled", "sum"),
            female_ratio=("female_ratio", "mean"),
        )
    )
    return result