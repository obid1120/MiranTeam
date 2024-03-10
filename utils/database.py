import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_user(self, username, password):
        users = self.cursor.execute("SELECT fname, username, password, rule FROM staff WHERE username=? and password=?",
                                    (username, password))

        return users.fetchone()

    # work with admins panel

    def get_admin_list(self):
        admins = self.cursor.execute("SELECT count(*), id, fname, lname, shift, contact, tg_username from staff")
        return admins.fetchone()

    def get_admin_list_all(self):
        admins = self.cursor.execute(
            "SELECT id, fname, lname, shift, contact, tg_username, rule, username, password from staff"
        )
        return admins.fetchall()

    def add_admin(self, fname, lname, username, password, rule, tg_username, contact, shift, user_id=None):
        if user_id is None:
            self.cursor.execute(
                f"INSERT INTO staff (fname, lname, username, password, rule, "
                f"tg_username, contact, shift) values (?,?,?,?,?,?,?,?)",
                (fname, lname, username, password, rule, tg_username, contact, shift)
            )
        else:
            self.cursor.execute(
                f'UPDATE staff '
                f'set fname=?, lname=?, username=?, password=?, rule=?, tg_username=?, contact=?, shift=?'
                f'where id=?', (fname, lname, username, password, rule, tg_username, contact, shift, user_id)
            )
        self.conn.commit()

    def remove_admin(self, admin_id):
        self.cursor.execute(
            "DELETE FROM staff where id=?", (admin_id, )
        )
        self.conn.commit()

    # ----------------------------------------------------
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

    def set_miran_info_desc(self, video, description):
        self.cursor.execute(
            "Insert into miran_info_desc (video, description) values (?, ?)",
            (video, description)
        )
        self.conn.commit()

    def get_miran_info_desc(self):
        info = self.cursor.execute(
            "select video, description from miran_info_desc order by id DESC LIMIT 1"
        )
        return info.fetchone()
