<h1>FLEXI BOOK 🗒️</h1>
FlexiBook is a Command Line Interface (CLI) slot booking system developed with Python and PostgreSQL using psycopg2. It allows users to seamlessly book slots for various services (e.g., restaurants, hotels) while providing admins with tools to manage services, vendors, and slot availability.</br>

<h2>💡 Features</h2>
<h3>User Features</h3>
✺ Register & Login with security question for password reset </br>
✺ Book a slot for available services/vendors  </br>
✺ View booking history  </br>
✺ Manage user settings (Change username, password, clear booking history)  </br>
✺ Secure authentication with password hashing  </br>
<h3>Admin Features</h3>
✺ Admin login functionality  </br>
✺ Add new services dynamically (e.g., Restaurants, Hotels, Spa, etc.)  </br>
✺ Add vendors (e.g., specific restaurants or hotels under services)  </br>
✺ Add slots with time, price, and availability status  </br>
✺ Manage the database directly from the CLI  </br>

<h2>🛠️ Tech Stack</h2>
✺ Python 3.10+ </br>
✺ PostgreSQL </br>
✺ psycopg2 </br>
✺ bcrypt (for secure password handling) </br>

<h2>🚀 How to Run</h2>
1. Clone this repository:

```bash
https://github.com/nilavans/flexi-book.git
cd flexi-book
```
2. Install the required dependencies:

```bash
pip install -r requirement.txt
```
3. Configure your PostgreSQL settings in <b> database.ini </b>

4. Run the application:

```bash
python main.py
```

<h2>🧩 Future Enhancements</h2>
<h4>🎮 Voucher Feature (Gamification):</h4>
Allow users to play a mini-game inside the CLI (e.g., number guessing, spin wheel, etc.). On winning, they will earn vouchers/discounts that can be applied to future bookings.
