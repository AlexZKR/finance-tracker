CURRENCY_CHOICES = (
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("GBP", "British Pound"),
    ("JPY", "Japanese Yen"),
    ("BYN", "Belarusian Rouble"),
)

COLOR_CHOICES = [
    ("#4CAF50", "Green"),  # Success, positive growth
    ("#F44336", "Red"),  # Loss, negative growth
    ("#FFC107", "Amber"),  # Warning, attention needed
    ("#2196F3", "Blue"),  # Information, general category
    ("#FF9800", "Orange"),  # Expenses, outgoing money
    ("#9C27B0", "Purple"),  # Investments, portfolio-related
    ("#3F51B5", "Indigo"),  # Assets, long-term categories
    ("#009688", "Teal"),  # Accounts, bank-related
    ("#8BC34A", "Light Green"),  # Growth, positive change
    ("#795548", "Brown"),  # Loans, liabilities
    ("#607D8B", "Blue Grey"),  # Neutral, miscellaneous
    ("#E91E63", "Pink"),  # Custom, user-defined
    ("#00BCD4", "Cyan"),  # Cash Flow, liquidity
    ("#673AB7", "Deep Purple"),  # Revenue, incoming funds
    ("#F57C00", "Dark Orange"),  # Depreciation, asset loss
]
TRANSACTION_TYPES = [
    ("IN", "Income"),
    ("EX", "Expense"),
    ("TR", "Transfer"),
]

BUDGET_TYPES = [
    ("M", "Monthly"),
    ("C", "Category"),
    ("A", "Account"),
]

CATEGORY_CHOICES = [
    ("salary", "Salary"),
    ("freelance", "Freelance"),
    ("investment_income", "Investment Income"),
    ("gift", "Gift"),
    ("savings", "Savings"),
    ("rent", "Rent"),
    ("utilities", "Utilities"),
    ("groceries", "Groceries"),
    ("transportation", "Transportation"),
    ("entertainment", "Entertainment"),
    ("healthcare", "Healthcare"),
    ("education", "Education"),
    ("debt_repayment", "Debt Repayment"),
    ("insurance", "Insurance"),
    ("travel", "Travel"),
    ("charity", "Charity"),
    ("taxes", "Taxes"),
    ("subscriptions", "Subscriptions"),
    ("miscellaneous", "Miscellaneous"),
]
