from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_csv(filename: str, low_memory: bool = False) -> pd.DataFrame:
    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
    return pd.read_csv(file_path, low_memory=low_memory)


def load_main_dataset() -> pd.DataFrame:
    return load_csv("01_university_admissions_turkey_2019_2024.csv")


def load_net_stats() -> pd.DataFrame:
    return load_csv("department_avg_net_stats.csv")


def load_lessons() -> pd.DataFrame:
    return load_csv("lessons.csv")


def load_master_dataset() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "master_university_dataset.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            "master_university_dataset.csv bulunamadı. "
            "Önce prepare_master_dataset fonksiyonunu çalıştır."
        )
    return pd.read_csv(file_path)


def load_analysis_dataset() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "analysis_dataset.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            "analysis_dataset.csv bulunamadı. "
            "Önce create_analysis_dataset fonksiyonunu çalıştır."
        )
    return pd.read_csv(file_path)