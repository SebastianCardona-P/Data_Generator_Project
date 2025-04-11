import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, cauchy, poisson
import numpy as np

# Load the data
df = pd.read_csv("employee_data.csv")

# General plotting configuration
sns.set_palette("Set2")  # Seaborn color palette

# 1. Base Salary Distributions by Education Level
education_levels = ["High School", "Professional", "Master", "PhD"]

# Individual plots for each education level
for edu in education_levels:
    plt.figure(figsize=(12, 6))
    subset = df[df["education"] == edu]
    if len(subset) > 0:  # Ensure there is data
        sns.histplot(subset["base_salary"], kde=True, stat="density", label=f"Base Salary ({edu})")
        # Fit a Cauchy distribution (as per employee_data_generator.py)
        loc_cauchy = subset["base_salary"].median()
        scale_cauchy = (subset["base_salary"].quantile(0.75) - subset["base_salary"].quantile(0.25)) / 2
        x_cauchy = np.linspace(30000, 200000, 100)
        p_cauchy = cauchy.pdf(x_cauchy, loc=loc_cauchy, scale=scale_cauchy)
        plt.plot(
            x_cauchy,
            p_cauchy,
            "r-",
            lw=2,
            label=f"Cauchy (loc={loc_cauchy:.2f}, scale={scale_cauchy:.2f})",
        )
    plt.title(f"Distribución de Base Salary ({edu})")
    plt.xlabel("Base Salary")
    plt.ylabel("Density")
    plt.legend()
    plt.show()

# Combined plot for all education levels
plt.figure(figsize=(12, 6))
for edu in education_levels:
    subset = df[df["education"] == edu]
    if len(subset) > 0:
        sns.histplot(
            subset["base_salary"],
            kde=True,
            stat="density",
            label=f"Base Salary ({edu})",
            element="step",
            alpha=0.3,
        )
plt.title("Distribución de Base Salary (Todos los Niveles de Educación)")
plt.xlabel("Base Salary")
plt.ylabel("Density")
plt.legend()
plt.show()

# 2. Pie Charts for Categorical Columns
categorical_columns = [
    "gender",
    "education",
    "employee_level",
    "status",
    "work_location",
    "shift",
]

for column in categorical_columns:
    plt.figure(figsize=(12, 10))
    data_counts = df[column].value_counts()
    # Limit to top 10 categories if more than 10
    if len(data_counts) > 10:
        data_counts = data_counts[:10]
        title = f"Distribución de {column.capitalize()} (Top 10)"
    else:
        title = f"Distribución de {column.capitalize()}"
    plt.pie(
        data_counts,
        labels=data_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": 10},
    )
    plt.title(title)
    plt.axis("equal")  # Ensure circular pie chart
    plt.show()

# 3. Performance Score Distribution
plt.figure(figsize=(12, 6))
sns.histplot(
    df["performance_score"], kde=True, stat="density", label="Performance Score"
)
# Fit a normal distribution
mean_ps = df["performance_score"].mean()
std_ps = df["performance_score"].std()
x = np.linspace(0, 100, 100)
p_ps = norm.pdf(x, mean_ps, std_ps)
plt.plot(
    x,
    p_ps,
    "r-",
    lw=2,
    label=f"Normal (μ={mean_ps:.2f}, σ={std_ps:.2f})",
)
plt.title("Distribución de Performance Score (Normal)")
plt.xlabel("Performance Score")
plt.ylabel("Density")
plt.legend()
plt.show()

# 4. Bonus Percentage Distribution
plt.figure(figsize=(12, 6))
sns.histplot(
    df["bonus_percentage"], kde=True, stat="density", label="Bonus Percentage"
)
# Fit a normal distribution
mean_bp = df["bonus_percentage"].mean()
std_bp = df["bonus_percentage"].std()
x = np.linspace(0, 15, 100)
p_bp = norm.pdf(x, mean_bp, std_bp)
plt.plot(
    x,
    p_bp,
    "r-",
    lw=2,
    label=f"Normal (μ={mean_bp:.2f}, σ={std_bp:.2f})",
)
plt.title("Distribución de Bonus Percentage (Normal)")
plt.xlabel("Bonus Percentage")
plt.ylabel("Density")
plt.legend()
plt.show()

# 5. Vacation Days Distribution
plt.figure(figsize=(12, 6))
sns.histplot(
    df["vacation_days"],
    kde=False,
    stat="density",
    label="Vacation Days",
    discrete=True,
)
# Fit a Poisson distribution
lambda_vd = df["vacation_days"].mean()
x_vd = np.arange(0, df["vacation_days"].max() + 1)
p_vd = poisson.pmf(x_vd, lambda_vd)
plt.plot(
    x_vd,
    p_vd,
    "r-",
    lw=2,
    label=f"Poisson (λ={lambda_vd:.2f})",
)
plt.title("Distribución de Vacation Days (Poisson)")
plt.xlabel("Vacation Days")
plt.ylabel("Density")
plt.legend()
plt.show()

# 6. Sick Days Distribution
plt.figure(figsize=(12, 6))
sns.histplot(
    df["sick_days"],
    kde=False,
    stat="density",
    label="Sick Days",
    discrete=True,
)
# Fit a Poisson distribution
lambda_sd = df["sick_days"].mean()
x_sd = np.arange(0, df["sick_days"].max() + 1)
p_sd = poisson.pmf(x_sd, lambda_sd)
plt.plot(
    x_sd,
    p_sd,
    "r-",
    lw=2,
    label=f"Poisson (λ={lambda_sd:.2f})",
)
plt.title("Distribución de Sick Days (Poisson)")
plt.xlabel("Sick Days")
plt.ylabel("Density")
plt.legend()
plt.show()