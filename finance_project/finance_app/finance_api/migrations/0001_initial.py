# Generated by Django 5.1.2 on 2024-10-30 09:28

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("USD", "US Dollar"),
                            ("EUR", "Euro"),
                            ("GBP", "British Pound"),
                            ("JPY", "Japanese Yen"),
                            ("BYN", "Belarusian Rouble"),
                        ],
                        default="BYN",
                        max_length=3,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "display_color",
                    models.CharField(
                        choices=[
                            ("#4CAF50", "Green"),
                            ("#F44336", "Red"),
                            ("#FFC107", "Amber"),
                            ("#2196F3", "Blue"),
                            ("#FF9800", "Orange"),
                            ("#9C27B0", "Purple"),
                            ("#3F51B5", "Indigo"),
                            ("#009688", "Teal"),
                            ("#8BC34A", "Light Green"),
                            ("#795548", "Brown"),
                            ("#607D8B", "Blue Grey"),
                            ("#E91E63", "Pink"),
                            ("#00BCD4", "Cyan"),
                            ("#673AB7", "Deep Purple"),
                            ("#F57C00", "Dark Orange"),
                        ],
                        default="#4CAF50",
                        max_length=7,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
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
                    ),
                ),
                (
                    "display_color",
                    models.CharField(
                        choices=[
                            ("#4CAF50", "Green"),
                            ("#F44336", "Red"),
                            ("#FFC107", "Amber"),
                            ("#2196F3", "Blue"),
                            ("#FF9800", "Orange"),
                            ("#9C27B0", "Purple"),
                            ("#3F51B5", "Indigo"),
                            ("#009688", "Teal"),
                            ("#8BC34A", "Light Green"),
                            ("#795548", "Brown"),
                            ("#607D8B", "Blue Grey"),
                            ("#E91E63", "Pink"),
                            ("#00BCD4", "Cyan"),
                            ("#673AB7", "Deep Purple"),
                            ("#F57C00", "Dark Orange"),
                        ],
                        default="#4CAF50",
                        max_length=7,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "budget_type",
                    models.CharField(
                        choices=[("M", "Monthly"), ("C", "Category"), ("A", "Account")]
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField()),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance_api.account",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance_api.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("IN", "Income"),
                            ("EX", "Expense"),
                            ("TR", "Transfer"),
                        ],
                        default="EX",
                        max_length=2,
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("description", models.TextField(max_length=200)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance_api.account",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        default="null_category",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="finance_api.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
