# employee_data_generator.py
import sys
import pandas as pd
import numpy as np
from faker import Faker
from scipy.stats import lognorm
from datetime import datetime, timedelta
import os

fake = Faker("en_US")  # US locale for consistent data

# Dictionary mapping states to cities
US_STATE_CITIES = {
    "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
    "NY": ["New York", "Buffalo", "Rochester", "Albany"],
    "TX": ["Houston", "Austin", "Dallas", "San Antonio"],
    "FL": ["Miami", "Orlando", "Tampa", "Jacksonville"],
    "IL": ["Chicago", "Springfield", "Peoria", "Rockford"],
    "WA": ["Seattle", "Spokane", "Tacoma"],
    "PA": ["Philadelphia", "Pittsburgh", "Allentown"],
    "MA": ["Boston", "Worcester", "Springfield"],
    "OH": ["Columbus", "Cleveland", "Cincinnati"],
    "GA": ["Atlanta", "Savannah", "Augusta"],
}

# Dictionary mapping departments to relevant job titles
DEPARTMENT_JOB_TITLES = {
    "IT": [
        "Systems Administrator",
        "Network Engineer",
        "Software Developer",
        "IT Support Specialist",
        "Database Administrator",
    ],
    "HHRR": [
        "HR Manager",
        "Recruitment Specialist",
        "Payroll Coordinator",
        "Training Coordinator",
        "Employee Relations Specialist",
    ],
    "Finance": [
        "Financial Analyst",
        "Accountant",
        "Budget Manager",
        "Tax Specialist",
        "Accounts Payable Clerk",
    ],
    "Sales": [
        "Sales Representative",
        "Account Manager",
        "Business Development Manager",
        "Sales Coordinator",
        "Regional Sales Director",
    ],
    "Marketing": [
        "Marketing Manager",
        "Content Strategist",
        "Digital Marketing Specialist",
        "Brand Manager",
        "Market Research Analyst",
    ],
    "Operations": [
        "Operations Manager",
        "Supply Chain Coordinator",
        "Logistics Specialist",
        "Production Supervisor",
        "Operations Analyst",
    ],
    "Support": [
        "Customer Support Representative",
        "Technical Support Specialist",
        "Help Desk Technician",
        "Service Desk Analyst",
    ],
    "Legal": [
        "Corporate Lawyer",
        "Compliance Officer",
        "Legal Assistant",
        "Contract Specialist",
        "Paralegal",
    ],
    "Logistics": [
        "Logistics Manager",
        "Warehouse Supervisor",
        "Transportation Coordinator",
        "Inventory Control Specialist",
    ],
    "R&D": [
        "Research Scientist",
        "Product Development Engineer",
        "Innovation Manager",
        "R&D Technician",
    ],
    "Procurement": [
        "Procurement Manager",
        "Purchasing Agent",
        "Supply Chain Analyst",
        "Vendor Manager",
    ],
    "Quality": [
        "Quality Assurance Manager",
        "Quality Control Inspector",
        "Production Assistant",
        "Process Improvement Specialist",
    ],
    "Security": [
        "Security Manager",
        "Cybersecurity Analyst",
        "Physical Security Specialist",
        "Safety Coordinator",
    ],
    "Training": [
        "Training Manager",
        "Instructional Designer",
        "Corporate Trainer",
        "Learning and Development Specialist",
    ],
    "Customer Service": [
        "Customer Service Representative",
        "Client Relations Manager",
        "Call Center Supervisor",
        "Customer Success Manager",
    ],
    "Engineering": [
        "Systems Engineer",
        "Industrial Engineer",
        "Mechanical Engineer",
        "Electrical Engineer",
        "Civil Engineer",
    ],
    "Design": [
        "Graphic Designer",
        "UX/UI Designer",
        "Industrial Designer",
        "Creative Director",
    ],
    "Development": [
        "Software Engineer",
        "Web Developer",
        "Mobile App Developer",
        "DevOps Engineer",
    ],
    "Research": [
        "Research Analyst",
        "Data Scientist",
        "Market Researcher",
        "Academic Researcher",
    ],
}

class EmployeeDataGenerator:
    def __init__(self, row_count, start_id=1):
        self.row_count = row_count
        self.departments = list(DEPARTMENT_JOB_TITLES.keys())
        self.states = list(US_STATE_CITIES.keys())
        self.start_id = start_id  # Starting ID for this chunk

    def generate_employee_id(self):
        """Generate employee IDs incrementally starting from start_id"""
        end_id = self.start_id + self.row_count
        unique_numbers = range(self.start_id, end_id)
        self.start_id = end_id  # Update start_id for the next chunk
        return [f"EMP{num:012d}" for num in unique_numbers]

    def generate_base_salary(self, education_levels):
        """Generate salaries with Log-Normal distribution based on education"""
        salaries = []
        for edu in education_levels:
            if edu == "High School":
                s, scale = 0.3, 45000
            elif edu == "Professional":
                s, scale = 0.3, 60000
            elif edu == "Master":
                s, scale = 0.3, 80000
            else:  # PhD
                s, scale = 0.3, 100000
            salary = lognorm.rvs(s, scale=scale, size=1)[0]
            salaries.append(np.clip(salary, 30000, 200000))
        return [round(salary, 2) for salary in salaries]

    def generate_state_city(self):
        """Generate states and cities with uniform distribution"""
        states = np.random.choice(self.states, size=self.row_count)
        cities = [np.random.choice(US_STATE_CITIES[state]) for state in states]
        return states, cities

    def generate_data(self):
        # Genders with specified probabilities
        genders = np.random.choice(
            ["M", "F", "Other"], self.row_count, p=[0.45, 0.45, 0.1]
        )
        first_names = np.array(
            [
                (
                    fake.first_name_male()
                    if g == "M"
                    else fake.first_name_female() if g == "F" else fake.first_name()
                )
                for g in genders
            ]
        )
        last_names = np.array([fake.last_name() for _ in range(self.row_count)])
        emails = np.array(
            [
                f"{first.lower()}.{last.lower()}@company.com"
                for first, last in zip(first_names, last_names)
            ]
        )

        education_levels = np.random.choice(
            ["High School", "Professional", "Master", "PhD"],
            self.row_count,
            p=[0.2, 0.5, 0.25, 0.05],
        )

        employee_ids = self.generate_employee_id()
        base_salaries = self.generate_base_salary(education_levels)
        departments = np.random.choice(self.departments, size=self.row_count)
        job_titles = np.array(
            [np.random.choice(DEPARTMENT_JOB_TITLES[dept]) for dept in departments]
        )
        hire_dates = np.array(
            [
                fake.date_between(start_date="-5y", end_date="today")
                for _ in range(self.row_count)
            ]
        )

        one_year_ago = datetime.now().date() - timedelta(days=365)
        last_review_dates = []
        for hire_date in hire_dates:
            if isinstance(hire_date, datetime):
                hire_date = hire_date.date()
            if hire_date > one_year_ago:
                review_date = fake.date_between(start_date=hire_date, end_date="today")
            else:
                review_date = fake.date_between(
                    start_date=hire_date, end_date=one_year_ago
                )
            last_review_dates.append(review_date)
        last_review_dates = np.array(last_review_dates)

        days_service = np.array(
            [(datetime.now().date() - date).days for date in hire_dates]
        )

        employee_levels = []
        for days in days_service:
            if days < 365:
                employee_levels.append("Entry")
            elif 365 <= days <= 730:
                employee_levels.append("Mid")
            else:
                employee_levels.append("Senior")
        employee_levels = np.array(employee_levels)

        states, cities = self.generate_state_city()
        addresses = np.array([fake.street_address() for _ in range(self.row_count)])
        zip_codes = np.array([fake.zipcode() for _ in range(self.row_count)])

        performance_scores = np.random.normal(75, 10, self.row_count).clip(0, 100)
        performance_scores = np.round(performance_scores, 2)

        bonus_percentages = np.random.normal(5, 2, self.row_count).clip(0, 15)
        bonus_percentages = np.round(bonus_percentages, 2)

        data = {
            "employee_id": employee_ids,
            "first_name": first_names,
            "last_name": last_names,
            "email": emails,
            "phone_number": np.array(
                [fake.phone_number() for _ in range(self.row_count)]
            ),
            "department": departments,
            "job_title": job_titles,
            "hire_date": hire_dates,
            "days_service": days_service,
            "base_salary": base_salaries,
            "bonus_percentage": bonus_percentages,
            "status": np.random.choice(
                ["Active", "Inactive", "Leave"], self.row_count, p=[0.85, 0.10, 0.05]
            ),
            "birth_date": np.array(
                [
                    fake.date_of_birth(minimum_age=18, maximum_age=65)
                    for _ in range(self.row_count)
                ]
            ),
            "address": addresses,
            "city": cities,
            "state": states,
            "zip_code": zip_codes,
            "country": np.array(["USA" for _ in range(self.row_count)]),
            "gender": genders,
            "education": education_levels,
            "performance_score": performance_scores,
            "last_review_date": last_review_dates,
            "employee_level": employee_levels,
            "vacation_days": np.random.poisson(15, self.row_count),
            "sick_days": np.random.poisson(5, self.row_count),
            "work_location": np.random.choice(
                ["Office", "Remote", "Hybrid"], self.row_count, p=[0.5, 0.3, 0.2]
            ),
            "shift": np.random.choice(
                ["Day", "Night", "Flexible"], self.row_count, p=[0.6, 0.3, 0.1]
            ),
            "emergency_contact": np.array(
                [fake.phone_number() for _ in range(self.row_count)]
            ),
            "ssn": np.array([fake.ssn() for _ in range(self.row_count)]),
            "bank_account": np.array([fake.bban() for _ in range(self.row_count)]),
        }

        return pd.DataFrame(data)


def generate_and_save_data(
    row_count, output_file="employee_data.csv", chunk_size=500000
):
    """Generate data in chunks and save to CSV incrementally to manage memory"""
    # Calculate number of chunks
    num_chunks = (row_count + chunk_size - 1) // chunk_size  # Ceiling division
    first_chunk = True
    current_id = 1  # Starting ID for incremental generation

    for i in range(num_chunks):
        # Calculate the number of rows for this chunk
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, row_count)
        current_chunk_size = end_idx - start_idx

        print(f"Generating chunk {i + 1}/{num_chunks} ({current_chunk_size} rows)...")

        # Generate data for this chunk, passing the current_id as start_id
        generator = EmployeeDataGenerator(current_chunk_size, start_id=current_id)
        df_chunk = generator.generate_data()

        # Update the current_id for the next chunk
        current_id += current_chunk_size

        # Write to CSV: append mode for subsequent chunks, write mode for the first
        mode = "w" if first_chunk else "a"
        header = first_chunk
        df_chunk.to_csv(output_file, mode=mode, header=header, index=False)
        first_chunk = False

        del df_chunk
        import gc

        gc.collect()

    print(f"Generated {row_count} rows and saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python employee_data_generator.py <row_count>")
        sys.exit(1)

    try:
        row_count = int(sys.argv[1])
        if row_count <= 0:
            raise ValueError("Row count must be positive")
        generate_and_save_data(row_count)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
