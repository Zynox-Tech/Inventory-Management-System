# Unique Modern Inventory Management System

A highly modern, dark-themed desktop application built using Python and Tkinter for robust product tracking, category structure, supplier coordination, and checkout/billing execution.

This application has been modernized and is developed by **Zynox Tech**.

---

## Developed by: Zynox Tech

* **Website:** [https://zynoxtech.site](https://zynoxtech.site)
* **Email:** [hello@zynoxtech.site](mailto:hello@zynoxtech.site)
* **Location:** Abbottabad, Pakistan

### About Zynox Tech
Zynox Tech is a software development company focused on building modern digital solutions including web applications, mobile applications, enterprise software, AI solutions, and custom software products.

We help startups, businesses, and organizations transform their ideas into scalable, reliable, and user-friendly technology solutions.

For software development services, reach out to us at:
* **Website:** [https://zynoxtech.site](https://zynoxtech.site)
* **Email:** [hello@zynoxtech.site](mailto:hello@zynoxtech.site)

---

## Key Enhancements (Modernized UI/UX)

1. **Sleek Modern Dark Theme:** Uses an elegant slate-900 `#0F172A` and slate-800 `#1E293B` layout to prevent eye strain and align with premium modern web aesthetics.
2. **Flat Flat Design Components:** Standard Tkinter buttons, entries, text fields, and scrollbars are styled flat, removing the legacy 90s-style ridge/groove borders.
3. **Interactive Micro-Animations:** Clean buttons feature interactive hover events that smooth-transition background colors upon mouse hover.
4. **Custom Styled Grids:** Grid components (`ttk.Treeview`) and dropdowns (`ttk.Combobox`) have custom dark-styled headers and alternating highlight colors.
5. **Path Resolution System:** Incorporates a smart relative and absolute path resolution framework so that file assets (images, receipts) load correctly regardless of how the script is executed.

---

## File Overview

1. **`dashboard.py`** - The primary control panel of the application. Lists totals for Employees, Suppliers, Categories, Products, and Sales. Includes a dynamic left navigation bar.
2. **`employee.py`** - Collects and tracks complete employee database entries with built-in search and record filtering.
3. **`supplier.py`** - Manages suppliers, records invoice details, and descriptions.
4. **`product.py`** - Tracks product availability, quantity, pricing, status, and binds items to corresponding categories and suppliers.
5. **`category.py`** - Manages categories (e.g. mapping "iPhone" to the category "Phones").
6. **`sales.py`** - Displays and retrieves historical customer checkout receipts and generated text invoices.
7. **`create_db.py`** - Database initialization script that builds the SQLite tables.
8. **`billing.py`** - Checkout cashier portal featuring customer data entries, a sleek calculator utility, shopping cart list, and instant bill generation.

---

## Getting Started

### Pre-Requisites

Make sure you have Python installed, then run:
```bash
pip install pillow
```
*(SQLite3, OS, Time, and Tempfile modules are included out-of-the-box in standard Python environments).*

### Installation and Usage

1. **Initialize the database:**
   Run `create_db.py` to create `ims.db` and the database structure:
   ```bash
   python create_db.py
   ```
2. **Run the Dashboard Application:**
   ```bash
   python dashboard.py
   ```
3. **Run the Cashier Billing Portal:**
   To access the checkout and generate receipts:
   ```bash
   python billing.py
   ```