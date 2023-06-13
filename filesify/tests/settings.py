DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = (
    "filesify",
    "filesify.tests",
)

SECRET_KEY = "e$vz=-@a(6h_$a1#z6rbe0ixtqcwuyncq)e#s*wx)4_1n2laht"
