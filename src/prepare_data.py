import pandas as pd

# Загрузка
df = pd.read_csv("../data/raw/train.csv", parse_dates=["date"])

# Фильтрация (чтобы не обучать модель на 900k строк сразу)
# Возьмём один магазин и 10 товаров
df = df[(df["store"] == 1) & (df["item"].isin(range(1, 11)))].copy()

# Агрегация до месячного уровня
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby("month")["sales"].sum().reset_index()
monthly["date"] = monthly["month"].dt.to_timestamp()
monthly["product"] = "Store_1_Top10"  # условная "продуктовая группа"
monthly["demand_tons"] = monthly["sales"]  # переименуем для совместимости

# Оставляем нужные колонки и сохраняем в едином формате
monthly = monthly[["date", "product", "demand_tons"]]
monthly.to_csv("../data/raw/demand_real.csv", index=False)
print(monthly.head())