from datetime import datetime, timedelta, timezone

from src.auth.models import User, UserRole
from src.auth.utils import get_password_hash
from src.chatbot.models import Query, QueryStatus
from src.db.database import SessionLocal, apply_schema_updates


CUSTOMER_PASSWORD = "pass1234"
COMPANY_PASSWORD = "company123"
OPERATOR_PASSWORD = "operator123"


CUSTOMERS = [
    ("Aarav Sharma", "aarav.sharma01@gmail.com"),
    ("Isha Verma", "isha.verma02@gmail.com"),
    ("Rohan Mehta", "rohan.mehta03@gmail.com"),
    ("Neha Singh", "neha.singh04@gmail.com"),
    ("Kunal Jain", "kunal.jain05@gmail.com"),
    ("Priya Nair", "priya.nair06@gmail.com"),
    ("Arjun Rao", "arjun.rao07@gmail.com"),
    ("Sana Khan", "sana.khan08@gmail.com"),
    ("Vikram Das", "vikram.das09@gmail.com"),
    ("Meera Iyer", "meera.iyer10@gmail.com"),
]

COMPANIES = [
    ("Navient Solutions, Inc.", "navient.ops@gmail.com"),
    ("Wells Fargo & Company", "wellsfargo.ops@gmail.com"),
    ("Capital One", "capitalone.ops@gmail.com"),
    ("JPMorgan Chase & Co.", "jpmorgan.ops@gmail.com"),
    ("Amex", "amex.ops@gmail.com"),
]

OPERATORS = [
    ("Loans Desk", "operator.loans@gmail.com", "Loans"),
    ("Card Desk", "operator.cards@gmail.com", "Credit Card"),
    ("Payments Desk", "operator.payments@gmail.com", "Payments"),
]

QUERY_FIXTURES = [
    ("CA", "Navient Solutions, Inc.", "Mortgage EMI was debited twice this month.", "Loans", QueryStatus.PENDING),
    ("NY", "Wells Fargo & Company", "My student loan repayment portal is down.", "Loans", QueryStatus.SOLVED),
    ("TX", "Capital One", "Credit card annual fee charged despite waiver confirmation.", "Credit Card", QueryStatus.PENDING),
    ("FL", "JPMorgan Chase & Co.", "Wrong late fee shown in my credit card statement.", "Credit Card", QueryStatus.CLOSED),
    ("IL", "Amex", "Credit report still shows closed account as active.", "Credit Reporting", QueryStatus.PENDING),
    ("GA", "Navient Solutions, Inc.", "Debt collector is calling outside legal hours.", "Debt Collection", QueryStatus.SOLVED),
    ("NC", "Wells Fargo & Company", "Bank account was frozen without prior notice.", "Banking", QueryStatus.PENDING),
    ("AZ", "Capital One", "Money transfer marked complete but beneficiary did not receive.", "Payments", QueryStatus.PENDING),
    ("PA", "JPMorgan Chase & Co.", "Prepaid card balance is not updating after top-up.", "Payments", QueryStatus.SOLVED),
    ("VA", "Amex", "Payday loan interest rate looks incorrect.", "Payday", QueryStatus.CLOSED),
    ("OH", "Navient Solutions, Inc.", "Need support for unusual financial service dispute.", "Other", QueryStatus.PENDING),
    ("MI", "Wells Fargo & Company", "Mortgage account still reflects old address details.", "Loans", QueryStatus.PENDING),
    ("NJ", "Capital One", "My consumer loan foreclosure amount is inaccurate.", "Loans", QueryStatus.SOLVED),
    ("WA", "JPMorgan Chase & Co.", "Credit reporting agency ignored dispute evidence.", "Credit Reporting", QueryStatus.PENDING),
    ("MA", "Amex", "Debt collection team threatened legal action unfairly.", "Debt Collection", QueryStatus.CLOSED),
    ("CO", "Navient Solutions, Inc.", "Bank service charge applied without notification.", "Banking", QueryStatus.PENDING),
    ("MD", "Wells Fargo & Company", "International money transfer failed repeatedly.", "Payments", QueryStatus.SOLVED),
    ("MN", "Capital One", "Prepaid travel card blocked during transaction.", "Payments", QueryStatus.PENDING),
    ("OR", "JPMorgan Chase & Co.", "Student loan interest capitalization looks wrong.", "Loans", QueryStatus.PENDING),
    ("SC", "Amex", "Credit card cashback not credited for eligible spend.", "Credit Card", QueryStatus.SOLVED),
]


def get_or_create_user(db, email: str, **kwargs) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.add(user)
        db.flush()
        return user

    user = User(email=email, **kwargs)
    db.add(user)
    db.flush()
    return user


def main() -> None:
    apply_schema_updates()
    db = SessionLocal()
    try:
        customers = []
        for name, email in CUSTOMERS:
            customer = get_or_create_user(
                db,
                email=email,
                hashed_password=get_password_hash(CUSTOMER_PASSWORD),
                role=UserRole.customer,
                name=name,
            )
            customers.append(customer)

        company_users = []
        for company_name, email in COMPANIES:
            company_user = get_or_create_user(
                db,
                email=email,
                hashed_password=get_password_hash(COMPANY_PASSWORD),
                role=UserRole.company,
                name=f"{company_name} Team",
                company_name=company_name,
            )
            company_users.append(company_user)

        for name, email, department in OPERATORS:
            get_or_create_user(
                db,
                email=email,
                hashed_password=get_password_hash(OPERATOR_PASSWORD),
                role=UserRole.operator,
                name=name,
                department=department,
            )

        customer_ids = [customer.id for customer in customers]
        db.query(Query).filter(Query.customer_id.in_(customer_ids)).delete(
            synchronize_session=False
        )

        for idx, fixture in enumerate(QUERY_FIXTURES):
            state, company, query_text, department, status = fixture
            customer = customers[idx % len(customers)]
            created_at = datetime.now(timezone.utc) - timedelta(hours=idx * 3)
            company_response = None
            if status in {QueryStatus.SOLVED, QueryStatus.CLOSED}:
                company_response = (
                    "Issue resolved and confirmation shared with customer."
                    if status == QueryStatus.SOLVED
                    else "Request rejected due to insufficient supporting details."
                )

            db.add(
                Query(
                    customer_id=customer.id,
                    state=state,
                    company=company,
                    query_text=query_text,
                    company_response=company_response,
                    department=department,
                    status=status,
                    created_at=created_at,
                )
            )

        db.commit()

        print("Seed complete.")
        print("\nCustomer credentials:")
        for name, email in CUSTOMERS:
            print(f"- {name}: {email} / {CUSTOMER_PASSWORD}")

        print("\nCompany credentials:")
        for company_name, email in COMPANIES:
            print(f"- {company_name}: {email} / {COMPANY_PASSWORD}")

        print("\nOperator credentials:")
        for name, email, department in OPERATORS:
            print(f"- {name} ({department}): {email} / {OPERATOR_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
