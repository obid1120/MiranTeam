import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_user(self, username, password):
        users = self.cursor.execute("SELECT fname, username, password, rule FROM staff WHERE username=? and password=?",
                                    (username, password))

        return users.fetchone()

    def get_admin_list(self):
        admins = self.cursor.execute("SELECT fname, lname, contact, tg_username from staff")
        return admins.fetchall()

    def get_updates(self):
        updates = self.cursor.execute("SELECT update_id, company_name, truck_unit, driver, issue FROM updates")
        return updates.fetchall()

    def set_updates(self, company, truck, driver, issue):
        self.cursor.execute(
            f"INSERT INTO updates (company_name, truck_unit, driver, issue)"
                f"VALUES (?, ?, ?, ?)", (company, truck, driver, issue)
        )
        self.conn.commit()

    def delete_updates(self, update_id):
        print(update_id, type(update_id))
        try:
            self.cursor.execute(
                "DELETE FROM updates WHERE update_id=?",
                (int(update_id),)
            )
            self.conn.commit()
            return True
        except:
            return False

    def update_miran_info(self, title, description, image):
        self.cursor.execute(
            "INSERT INTO miran_info (title, image, miran_desc) VALUES (?, ?, ?)",
            (title, image, description)
        )
        self.conn.commit()

    def get_miran_info(self):
        last_info = self.cursor.execute(
            "SELECT title, image, miran_desc FROM miran_info ORDER BY id DESC LIMIT 1"
        )
        return last_info.fetchone()
