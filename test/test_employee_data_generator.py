import unittest
import pandas as pd
import numpy as np
from employee_data_generator import (
    EmployeeDataGenerator,
    US_STATE_CITIES,
    DEPARTMENT_JOB_TITLES,
)
from datetime import datetime, timedelta
from scipy.stats import cauchy, norm


class TestEmployeeDataGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a generator instance before each test."""
        self.row_count = 100
        self.generator = EmployeeDataGenerator(self.row_count)
        # Define expected columns based on generate_data output
        self.expected_columns = [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "department",
            "job_title",
            "hire_date",
            "days_service",
            "base_salary",
            "bonus_percentage",
            "status",
            "birth_date",
            "address",
            "city",
            "state",
            "zip_code",
            "country",
            "gender",
            "education",
            "performance_score",
            "last_review_date",
            "employee_level",
            "vacation_days",
            "sick_days",
            "work_location",
            "shift",
            "emergency_contact",
            "ssn",
            "bank_account",
        ]

    def test_init(self):
        """Test initialization of EmployeeDataGenerator."""
        self.assertEqual(self.generator.row_count, self.row_count)
        self.assertEqual(self.generator.departments, list(DEPARTMENT_JOB_TITLES.keys()))
        self.assertEqual(self.generator.states, list(US_STATE_CITIES.keys()))

    def test_generate_employee_id(self):
        """Test employee_id generation for uniqueness and format."""
        employee_ids = self.generator.generate_employee_id()
        self.assertEqual(len(employee_ids), self.row_count)
        self.assertEqual(len(set(employee_ids)), self.row_count)  # Check uniqueness
        for emp_id in employee_ids:
            self.assertTrue(emp_id.startswith("EMP"))
            self.assertTrue(len(emp_id) == 9)  # EMP + 6 digits
            self.assertTrue(emp_id[3:].isdigit())

    def test_generate_base_salary(self):
        """Test base_salary generation with Cauchy distribution."""
        education_levels = ["High School", "Professional", "Master", "PhD"]
        salaries = self.generator.generate_base_salary(education_levels)
        self.assertEqual(len(salaries), len(education_levels))
        for salary, edu in zip(salaries, education_levels):
            self.assertTrue(30000 <= salary <= 200000)  # Check clipping
            self.assertIsInstance(salary, float)
            self.assertEqual(round(salary, 2), salary)  # Check rounding

    def test_generate_state_city(self):
        """Test state and city generation with normal distribution for states."""
        states, cities = self.generator.generate_state_city()
        self.assertEqual(len(states), self.row_count)
        self.assertEqual(len(cities), self.row_count)
        for state, city in zip(states, cities):
            self.assertIn(state, US_STATE_CITIES)
            self.assertIn(city, US_STATE_CITIES[state])
        # Check if states follow a rough normal distribution
        state_counts = pd.Series(states).value_counts()
        self.assertTrue(len(state_counts) > 1)  # Ensure multiple states are selected

    def test_generate_data_columns(self):
        """Test that generate_data produces a DataFrame with all expected columns."""
        df = self.generator.generate_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(set(df.columns), set(self.expected_columns))
        self.assertEqual(len(df), self.row_count)

    def test_generate_data_types(self):
        """Test data types of generated columns."""
        df = self.generator.generate_data()
        self.assertTrue(all(df["base_salary"].apply(lambda x: isinstance(x, float))))
        self.assertTrue(
            all(df["bonus_percentage"].apply(lambda x: isinstance(x, float)))
        )
        self.assertTrue(
            all(df["performance_score"].apply(lambda x: isinstance(x, float)))
        )
        self.assertTrue(all(df["days_service"].apply(lambda x: isinstance(x, int))))
        self.assertTrue(all(df["vacation_days"].apply(lambda x: isinstance(x, int))))
        self.assertTrue(all(df["sick_days"].apply(lambda x: isinstance(x, int))))

    def test_generate_data_values(self):
        """Test that generated values are within expected ranges and categories."""
        df = self.generator.generate_data()
        # Categorical columns
        self.assertTrue(all(df["gender"].isin(["M", "F", "Other"])))
        self.assertTrue(
            all(df["education"].isin(["High School", "Professional", "Master", "PhD"]))
        )
        self.assertTrue(all(df["status"].isin(["Active", "Inactive", "Leave"])))
        self.assertTrue(all(df["work_location"].isin(["Office", "Remote", "Hybrid"])))
        self.assertTrue(all(df["shift"].isin(["Day", "Night", "Flexible"])))
        self.assertTrue(all(df["country"] == "USA"))
        self.assertTrue(all(df["department"].isin(DEPARTMENT_JOB_TITLES.keys())))
        self.assertTrue(all(df["state"].isin(US_STATE_CITIES.keys())))
        # Numeric columns
        self.assertTrue(
            all((df["base_salary"] >= 30000) & (df["base_salary"] <= 200000))
        )
        self.assertTrue(
            all((df["bonus_percentage"] >= 0) & (df["bonus_percentage"] <= 15))
        )
        self.assertTrue(
            all((df["performance_score"] >= 0) & (df["performance_score"] <= 100))
        )
        self.assertTrue(all(df["vacation_days"] >= 0))
        self.assertTrue(all(df["sick_days"] >= 0))
        self.assertTrue(all(df["days_service"] >= 0))

    def test_employee_level_logic(self):
        """Test employee_level assignment based on days_service."""
        df = self.generator.generate_data()
        for days, level in zip(df["days_service"], df["employee_level"]):
            if days < 365:
                self.assertEqual(level, "Entry")
            elif 365 <= days <= 730:
                self.assertEqual(level, "Mid")
            else:
                self.assertEqual(level, "Senior")

    def test_last_review_date_logic(self):
        """Test that last_review_date is after hire_date and within expected range."""
        df = self.generator.generate_data()
        one_year_ago = datetime.now().date() - timedelta(days=365)
        for hire, review in zip(df["hire_date"], df["last_review_date"]):
            hire_date = (
                hire.date() if isinstance(hire, (datetime, pd.Timestamp)) else hire
            )
            review_date = (
                review.date()
                if isinstance(review, (datetime, pd.Timestamp))
                else review
            )
            self.assertGreaterEqual(review_date, hire_date)
            if hire_date <= one_year_ago:
                self.assertLessEqual(review_date, one_year_ago)
            else:
                self.assertLessEqual(review_date, datetime.now().date())

    def test_job_title_department_consistency(self):
        """Test that job titles correspond to their departments."""
        df = self.generator.generate_data()
        for dept, title in zip(df["department"], df["job_title"]):
            self.assertIn(title, DEPARTMENT_JOB_TITLES[dept])

    def test_email_format(self):
        """Test that emails are correctly formatted."""
        df = self.generator.generate_data()
        for email, first, last in zip(df["email"], df["first_name"], df["last_name"]):
            expected_email = f"{first.lower()}.{last.lower()}@company.com"
            self.assertEqual(email, expected_email)

    def test_distribution_properties(self):
        """Test statistical properties of generated distributions."""
        df = self.generator.generate_data()
        # Performance score: normal distribution ~ N(75, 10)
        perf_mean = df["performance_score"].mean()
        perf_std = df["performance_score"].std()
        self.assertAlmostEqual(perf_mean, 75, delta=5)
        self.assertAlmostEqual(perf_std, 10, delta=3)
        # Bonus percentage: normal distribution ~ N(5, 2)
        bonus_mean = df["bonus_percentage"].mean()
        bonus_std = df["bonus_percentage"].std()
        self.assertAlmostEqual(bonus_mean, 5, delta=1)
        self.assertAlmostEqual(bonus_std, 2, delta=1)
        # Vacation days: Poisson ~ lambda=15
        vacation_lambda = df["vacation_days"].mean()
        self.assertAlmostEqual(vacation_lambda, 15, delta=3)
        # Sick days: Poisson ~ lambda=5
        sick_lambda = df["sick_days"].mean()
        self.assertAlmostEqual(sick_lambda, 5, delta=2)

    def test_edge_case_small_row_count(self):
        """Test data generation with a small row count."""
        small_generator = EmployeeDataGenerator(1)
        df = small_generator.generate_data()
        self.assertEqual(len(df), 1)
        self.assertEqual(set(df.columns), set(self.expected_columns))

    def test_generate_and_save_data(self):
        """Test the generate_and_save_data function."""
        from employee_data_generator import generate_and_save_data
        import os

        output_file = "test_employee_data.csv"
        generate_and_save_data(10, output_file)
        self.assertTrue(os.path.exists(output_file))
        df = pd.read_csv(output_file)
        self.assertEqual(len(df), 10)
        self.assertEqual(set(df.columns), set(self.expected_columns))
        os.remove(output_file)  # Clean up


if __name__ == "__main__":
    unittest.main()
