# employee_data_generator.py
import sys
import pandas as pd
import numpy as np
from faker import Faker
from scipy.stats import cauchy, norm
from datetime import datetime, timedelta

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
    def __init__(self, row_count):
        self.row_count = row_count
        self.departments = list(DEPARTMENT_JOB_TITLES.keys())
        self.states = list(US_STATE_CITIES.keys())

    def generate_employee_id(self):
        """Generate unique employee IDs"""
        return [
            f"EMP{fake.unique.random_number(digits=6, fix_len=True)}"
            for _ in range(self.row_count)
        ]

    def generate_base_salary(self, education_levels):
        """Generate salaries with Cauchy distribution based on education"""
        salaries = []
        for edu in education_levels:
            if edu == "High School":
                loc, scale = 45000, 10000
            elif edu == "Professional":
                loc, scale = 60000, 12000
            elif edu == "Master":
                loc, scale = 80000, 15000
            else:  # PhD
                loc, scale = 100000, 20000
            salary = cauchy.rvs(loc=loc, scale=scale, size=1)[0]
            salaries.append(np.clip(salary, 30000, 200000))
        return [round(salary, 2) for salary in salaries]  # Round to 2 decimals

    def generate_state_city(self):

        num_states = len(self.states)
        mean = (num_states - 1) / 2
        std_dev = num_states / 4
        indices = np.arange(num_states)
        weights = norm.pdf(indices, loc=mean, scale=std_dev)
        weights /= weights.sum()
        states = np.random.choice(self.states, size=self.row_count, p=weights)
        cities = [np.random.choice(US_STATE_CITIES[state]) for state in states]
        return states, cities

    def generate_data(self):
        """Generate complete employee dataset"""
        # genders with a "cake" distribution
        genders = np.random.choice(["M", "F", "Other"], self.row_count, p=[0.45, 0.45, 0.1])
        first_names = []
        last_names = [fake.last_name() for _ in range(self.row_count)]
        for gender in genders:
            if gender == "M":
                first_names.append(fake.first_name_male())
            elif gender == "F":
                first_names.append(fake.first_name_female())
            else:
                first_names.append(fake.first_name())

        emails = [
            f"{first.lower()}.{last.lower()}@company.com"
            for first, last in zip(first_names, last_names)
        ]

        education_levels = np.random.choice(
            ["High School", "Professional", "Master", "PhD"],
            self.row_count,
            p=[0.2, 0.5, 0.25, 0.05],
        )

        employee_ids = self.generate_employee_id()
        base_salaries = self.generate_base_salary(education_levels)
        departments = np.random.choice(self.departments, size=self.row_count)
        job_titles = [
            np.random.choice(DEPARTMENT_JOB_TITLES[dept]) for dept in departments
        ]
        hire_dates = [
            fake.date_between(start_date="-5y", end_date="today")
            for _ in range(self.row_count)
        ]

        # Generate last_review_date: after hire_date, before one year ago
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

        days_service = [(datetime.now().date() - date).days for date in hire_dates]

        # Generate employee_level based on days_service
        employee_levels = []
        for days in days_service:
            if days < 365:  # Less than 1 year
                employee_levels.append("Entry")
            elif 365 <= days <= 730:  # 1 to 2 years
                employee_levels.append("Mid")
            else:  # More than 2 years
                employee_levels.append("Senior")

        states, cities = self.generate_state_city()
        addresses = [fake.street_address() for _ in range(self.row_count)]
        zip_codes = [fake.zipcode() for _ in range(self.row_count)]

        # Generate performance_score with 2 decimal places
        performance_scores = np.random.normal(75, 10, self.row_count).clip(0, 100)
        performance_scores = [round(score, 2) for score in performance_scores]

        # Generate bonus_percentage with 2 decimal places
        bonus_percentages = np.random.normal(5, 2, self.row_count).clip(0, 15)
        bonus_percentages = [round(bonus, 2) for bonus in bonus_percentages]

        data = {
            "employee_id": employee_ids,
            "first_name": first_names,
            "last_name": last_names,
            "email": emails,
            "phone_number": [fake.phone_number() for _ in range(self.row_count)],
            "department": departments,
            "job_title": job_titles,
            "hire_date": hire_dates,
            "days_service": days_service,
            "base_salary": base_salaries,
            "bonus_percentage": bonus_percentages,
            "status": np.random.choice(
                ["Active", "Inactive", "Leave"], self.row_count, p=[0.85, 0.10, 0.05]
            ),
            "birth_date": [
                fake.date_of_birth(minimum_age=18, maximum_age=65)
                for _ in range(self.row_count)
            ],
            "address": addresses,
            "city": cities,
            "state": states,
            "zip_code": zip_codes,
            "country": ["USA" for _ in range(self.row_count)],
            "gender": genders,
            "education": education_levels,
            "performance_score": performance_scores,
            "last_review_date": last_review_dates,
            "employee_level": employee_levels,  # Now based on days_service
            "vacation_days": np.random.poisson(15, self.row_count),
            "sick_days": np.random.poisson(5, self.row_count),
            "work_location": np.random.choice(
                ["Office", "Remote", "Hybrid"], self.row_count, p=[0.5, 0.3, 0.2]
            ),
            "shift": np.random.choice(
                ["Day", "Night", "Flexible"], self.row_count, p=[0.6, 0.3, 0.1]
            ),
            "emergency_contact": [fake.phone_number() for _ in range(self.row_count)],
            "ssn": [fake.ssn() for _ in range(self.row_count)],
            "bank_account": [fake.bban() for _ in range(self.row_count)],
        }

        return pd.DataFrame(data)


def generate_and_save_data(row_count, output_file="employee_data.csv"):
    """Generate data and save to CSV"""
    generator = EmployeeDataGenerator(row_count)
    df = generator.generate_data()
    df.to_csv(output_file, index=False)
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
