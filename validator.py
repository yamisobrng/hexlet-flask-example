def validate(user):
    print('Validate: ', user)
    name = user.get('name', '')
    email = user.get('email', '')
    errors = {}
    if len(name.strip()) < 4:
        errors['name'] = 'Nickname must be grater then 4 characters'
    return errors