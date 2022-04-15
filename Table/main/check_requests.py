import pandas as pd


def check_request(table, name, status):
    table = table.values()
    table = pd.DataFrame(table).to_dict(orient="list")

    if "name" not in table:
        return True

    else:
        if name not in table["name"]:
            return True

        else:
            if status != table["status"][len(table["name"]) - table["name"][::-1].index(name) - 1]:
                return True

    return False
