from owner import Owner
from tkinter import messagebox
import pandas as pd

class OwnerController:
    def __init__(self):
        self.owners = []
        self.owner_columns = ["id",
                        "owner_name",
                        "license",
                        "type",
                        "draft_date",
                        "release_date",
                        "pay_from_date",
                        "pay_until_date",
                        "payment_amount",
                        "sapak"]


    def generate_owners(self, df, id_lists):
        for id in df["id"].unique():
            owner_id_lists = []
            try:
                for id_list in id_lists:
                    list_df = id_list.get_df()
                    merge = pd.merge(df[df["id"] == id], list_df, on="id", how='inner')
                    if not merge.empty:
                        owner_id_lists.append(id_list)
            except Exception as e:
                messagebox.showerror("Error", f"generate_owners {e}")

            df_owner = df
            df_owner = df_owner[df_owner["id"] == id]
            df_owner = df_owner[self.owner_columns]
            if not df_owner.empty:
                self.owners.append(Owner(df_owner, owner_id_lists))


    def get_messages(self, owner):
        return owner.get_message()


    def get_owners(self):
        return self.owners
