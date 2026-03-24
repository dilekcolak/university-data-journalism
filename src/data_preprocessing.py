from pathlib import Path
import numpy as np
import pandas as pd

from src.data_loader import (
    load_main_dataset,
    load_net_stats,
    load_lessons,
    load_master_dataset,
)

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def prepare_master_dataset(save: bool = True) -> pd.DataFrame:
    main = load_main_dataset()
    net = load_net_stats()
    lessons = load_lessons()

    net = net.merge(lessons, on="lesson_id", how="left")

    net_pivot = (
        net.pivot_table(
            index=["program_code", "year"],
            columns="lesson_name",
            values="average_net",
            aggfunc="mean",
        )
        .reset_index()
    )

    net_pivot.columns.name = None

    master = main.merge(
        net_pivot,
        on=["program_code", "year"],
        how="left",
    )

    if save:
        output_path = PROCESSED_DIR / "master_university_dataset.csv"
        master.to_csv(output_path, index=False)
        print(f"Kaydedildi: {output_path}")

    return master


def create_analysis_dataset(save: bool = True) -> pd.DataFrame:
    df = load_master_dataset()

    keep_cols = [
        "year",
        "university_name",
        "city",
        "university_type",
        "department_name",
        "faculty_name",
        "score_type",
        "scholarship_type",
        "is_undergraduate",
        "total_quota",
        "total_enrolled",
        "male",
        "female",
        "final_score_012",
        "final_rank_012",
        "final_score_018",
        "final_rank_018",
        "initial_placement_rate",
        "total_preferences",
        "demand_per_quota",
        "avg_preference_rank",
        "placed_count",
        "TYT Türkçe",
        "TYT Temel Matematik",
        "TYT Sosyal Bilimler",
        "TYT Fen Bilimleri",
        "AYT Matematik",
        "AYT Fizik",
        "AYT Kimya",
        "AYT Biyoloji",
    ]

    existing_cols = [col for col in keep_cols if col in df.columns]
    analysis_df = df[existing_cols].copy()

    if "final_score_018" in analysis_df.columns or "final_score_012" in analysis_df.columns:
        analysis_df["final_score"] = analysis_df.get("final_score_018").combine_first(
            analysis_df.get("final_score_012")
        )

    if "final_rank_018" in analysis_df.columns or "final_rank_012" in analysis_df.columns:
        analysis_df["final_rank"] = analysis_df.get("final_rank_018").combine_first(
            analysis_df.get("final_rank_012")
        )

    total_gender = analysis_df["male"].fillna(0) + analysis_df["female"].fillna(0)

    analysis_df["female_ratio"] = np.where(
        total_gender > 0,
        analysis_df["female"].fillna(0) / total_gender,
        np.nan,
    )

    analysis_df["male_ratio"] = np.where(
        total_gender > 0,
        analysis_df["male"].fillna(0) / total_gender,
        np.nan,
    )

    analysis_df["occupancy_rate"] = np.where(
        analysis_df["total_quota"].fillna(0) > 0,
        analysis_df["total_enrolled"].fillna(0) / analysis_df["total_quota"],
        np.nan,
    )

    analysis_df["score_change_label"] = pd.cut(
        analysis_df["final_score"],
        bins=[0, 250, 350, 450, 600],
        labels=["Düşük", "Orta", "Yüksek", "Çok Yüksek"],
        include_lowest=True,
    )

    if save:
        output_path = PROCESSED_DIR / "analysis_dataset.csv"
        analysis_df.to_csv(output_path, index=False)
        print(f"Kaydedildi: {output_path}")

    return analysis_df


if __name__ == "__main__":
    prepare_master_dataset(save=True)
    create_analysis_dataset(save=True)