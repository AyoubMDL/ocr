def get_role_names(description_list):
    """Takes a list of descriptions and returns a corresponding list of roles."""

    role_names = []
    for desc in description_list:
        split_desc = desc.split('-')
        num_parts = len(split_desc)
        if num_parts == 1:
            role_name = 'Not Available'
        else:
            role_name = split_desc[1]
        role_names.append(role_name)

    return role_names


def get_company_names(description_list):
    return [description_list[i].split("-")[0] for i in range(len(description_list))]


def get_first_last_names(names_list):
    first_names = [names_list[i].split(" ")[0] for i in range(len(names_list))]
    last_names = [names_list[i].split(" ")[1] for i in range(len(names_list))]

    return first_names, last_names
