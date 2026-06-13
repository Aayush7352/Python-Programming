"""
SQLAlchemy ORM demonstration.

Requires: pip install sqlalchemy
"""
import sys


def main():
    """SQLAlchemy ORM demo."""
    try:
        from sqlalchemy import (
            create_engine, Column, Integer, String, Float,
            ForeignKey, DateTime, func, select
        )
        from sqlalchemy.orm import declarative_base, relationship, Session
        from datetime import datetime
    except ImportError:
        print("SQLAlchemy is not installed.")
        print("Install with: pip install sqlalchemy")
        sys.exit(1)

    Base = declarative_base()

    # Define models
    class Department(Base):
        __tablename__ = "departments"

        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False, unique=True)
        location = Column(String(200))
        employees = relationship("Employee", back_populates="department")

        def __repr__(self):
            return f"Department({self.name})"

    class Employee(Base):
        __tablename__ = "employees"

        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        email = Column(String(200), unique=True)
        salary = Column(Float)
        hire_date = Column(DateTime, default=datetime.now)
        department_id = Column(Integer, ForeignKey("departments.id"))
        department = relationship("Department", back_populates="employees")

        def __repr__(self):
            return f"Employee({self.name}, ${self.salary:.2f})"

    print("=== SQLAlchemy ORM ===")

    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Create departments
        eng = Department(name="Engineering", location="Building A")
        mkt = Department(name="Marketing", location="Building B")
        hr = Department(name="HR", location="Building A")
        session.add_all([eng, mkt, hr])
        session.commit()
        print("\n  Departments created")

        # Create employees
        employees = [
            Employee(name="Alice Smith", email="alice@company.com",
                     salary=85000, department=eng),
            Employee(name="Bob Jones", email="bob@company.com",
                     salary=72000, department=mkt),
            Employee(name="Charlie Brown", email="charlie@company.com",
                     salary=92000, department=eng),
            Employee(name="Diana Ross", email="diana@company.com",
                     salary=65000, department=hr),
            Employee(name="Eve Wilson", email="eve@company.com",
                     salary=78000, department=mkt),
        ]
        session.add_all(employees)
        session.commit()
        print(f"  Created {len(employees)} employees")

        # Query: all employees
        print("\n=== All Employees ===")
        for emp in session.query(Employee).order_by(Employee.salary.desc()).all():
            print(f"  {emp.name}: ${emp.salary:.2f} ({emp.department.name})")

        # Query with filter
        print("\n=== Engineering Department ===")
        for emp in session.query(Employee).join(Department).filter(
            Department.name == "Engineering"
        ).all():
            print(f"  {emp.name}: ${emp.salary:.2f}")

        # Aggregation
        print("\n=== Department Stats ===")
        stats = (
            session.query(
                Department.name,
                func.count(Employee.id).label("count"),
                func.avg(Employee.salary).label("avg_salary"),
            )
            .join(Employee, Department.id == Employee.department_id)
            .group_by(Department.name)
            .all()
        )
        for dept_name, count, avg_salary in stats:
            print(f"  {dept_name}: {count} employees, Avg: ${avg_salary:.2f}")

        # Update
        print("\n=== Update ===")
        emp = session.query(Employee).filter_by(name="Alice Smith").first()
        emp.salary = 90000
        session.commit()
        print(f"  Updated Alice's salary to ${emp.salary:.2f}")

        # Relationship navigation
        print("\n=== Department Employees (via relationship) ===")
        for dept in session.query(Department).all():
            print(f"  {dept.name}: {[e.name for e in dept.employees]}")

        # Raw SQL query
        print("\n=== Raw SQL ===")
        result = session.execute(
            select(Employee.name, Employee.salary).where(Employee.salary > 75000)
        )
        for name, salary in result:
            print(f"  {name}: ${salary:.2f}")

    print("\n  Cleanup complete")


if __name__ == "__main__":
    main()
