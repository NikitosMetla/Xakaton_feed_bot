import json


class Admin:
    def __init__(self, admin_id: str | int | None = ""):
        self.admin_id = str(admin_id)
        with open("db/admin/admins_data.json", "r", encoding="utf-8") as admins:
            self.admins = json.load(admins)

    async def is_admin(self):
        if self.admin_id in self.admins.get("admins"):
            return True
        else:
            return False

    async def get_admins(self):
        return self.admins.get("admins")

    async def add_admin(self):
        self.admins["admins"].append(self.admin_id)
        self.save_data()

    async def delete_admin(self):
        self.admins["admins"].remove(self.admin_id)
        self.save_data()

    def save_data(self):
        with open("db/admin/admins_data.json", "w", encoding="utf-8") as admins:
            json.dump(self.admins, admins, indent=2)